
import os
import uuid
import hmac
from io import BytesIO
from functools import wraps

from flask import (
    Flask, render_template, request,
    jsonify, send_file, redirect,
    url_for, session
)
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from storage import (
    upload_file,
    list_files,
    delete_file,
    download_file
)

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("APP_SECRET_KEY")

if not app.secret_key:
    raise RuntimeError("APP_SECRET_KEY is missing from environment variables.")

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = os.getenv("FLASK_ENV") == "production"

ALLOWED_EXTENSIONS = {
    "pdf", "doc", "docx", "txt",
    "jpg", "jpeg", "png"
}

ALLOWED_CATEGORIES = ["Documents", "Images", "Others"]


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def valid_storage_path(filename):
    """Allow legacy root files or files inside approved category folders."""
    if not filename:
        return False

    parts = filename.split("/")

    if len(parts) == 1:
        return secure_filename(parts[0]) == parts[0] and bool(parts[0])

    if len(parts) == 2:
        category, stored_name = parts

        return (
            category in ALLOWED_CATEGORIES
            and bool(stored_name)
            and secure_filename(stored_name) == stored_name
        )

    return False


def login_required(api=False):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if not session.get("logged_in"):
                if api:
                    return jsonify({"error": "Please log in"}), 401

                return redirect(url_for("login"))

            return function(*args, **kwargs)

        return wrapper
    return decorator


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        return redirect(url_for("home"))

    if request.method == "POST":
        username = os.getenv("APP_USERNAME")
        password = os.getenv("APP_PASSWORD")

        if not username or not password:
            return render_template(
                "login.html",
                error="Login credentials are not configured."
            ), 500

        entered_username = request.form.get("username", "")
        entered_password = request.form.get("password", "")

        valid_username = hmac.compare_digest(
            entered_username, username
        )
        valid_password = hmac.compare_digest(
            entered_password, password
        )

        if valid_username and valid_password:
            session.clear()
            session["logged_in"] = True
            return redirect(url_for("home"))

        return render_template(
            "login.html",
            error="Invalid username or password."
        ), 401

    return render_template("login.html")


@app.route("/logout")
@login_required()
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required()
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "message": "CloudVault is running"
    })


@app.route("/upload", methods=["POST"])
@login_required(api=True)
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if not file or not file.filename:
        return jsonify({"error": "Please select a file"}), 400

    safe_name = secure_filename(file.filename)

    if not safe_name or not allowed_file(safe_name):
        return jsonify({"error": "File type not allowed"}), 400

    category = request.form.get("category", "Documents")

    if category not in ALLOWED_CATEGORIES:
        return jsonify({"error": "Invalid category"}), 400

    unique_name = f"{uuid.uuid4().hex}_{safe_name}"
    storage_path = f"{category}/{unique_name}"

    try:
        upload_file(file, unique_name, category)

        return jsonify({
            "message": "File uploaded successfully",
            "filename": storage_path,
            "category": category
        }), 201

    except Exception:
        app.logger.exception("File upload failed")
        return jsonify({"error": "File upload failed"}), 500


@app.route("/files", methods=["GET"])
@login_required(api=True)
def files():
    try:
        objects = list_files()

        result = [
            {
                "filename": item["Key"],
                "size": item["Size"],
                "category": item.get("Category", "Uncategorized")
            }
            for item in objects
        ]

        return jsonify(result)

    except Exception:
        app.logger.exception("Could not list files")
        return jsonify({"error": "Could not retrieve files"}), 500


@app.route("/download/<path:filename>", methods=["GET"])
@login_required(api=True)
def download(filename):
    if not valid_storage_path(filename):
        return jsonify({"error": "Invalid filename"}), 400

    try:
        response = download_file(filename)

        stored_name = filename.split("/")[-1]
        original_name = stored_name.split("_", 1)[-1]

        return send_file(
            BytesIO(response["Body"].read()),
            as_attachment=True,
            download_name=original_name
        )

    except Exception:
        app.logger.exception("File download failed")
        return jsonify({"error": "File download failed"}), 404


@app.route("/delete/<path:filename>", methods=["DELETE"])
@login_required(api=True)
def delete(filename):
    if not valid_storage_path(filename):
        return jsonify({"error": "Invalid filename"}), 400

    try:
        delete_file(filename)

        return jsonify({
            "message": "File deleted successfully"
        })

    except Exception:
        app.logger.exception("File deletion failed")
        return jsonify({"error": "File deletion failed"}), 500


@app.errorhandler(413)
def file_too_large(error):
    return jsonify({
        "error": "File size exceeds the 10 MB limit."
    }), 413


if __name__ == "__main__":
    app.run(debug=False)
