
import os
import uuid
from io import BytesIO

from flask import (
    Flask, render_template, request,
    jsonify, send_file
)
from werkzeug.utils import secure_filename

from storage import (
    upload_file,
    list_files,
    delete_file,
    download_file
)

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = {
    "pdf", "doc", "docx", "txt",
    "jpg", "jpeg", "png"
}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "message": "Cloud File Storage API is running"
    })


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if not file or not file.filename:
        return jsonify({"error": "Please select a file"}), 400

    safe_name = secure_filename(file.filename)

    if not safe_name or not allowed_file(safe_name):
        return jsonify({"error": "File type not allowed"}), 400

    unique_name = f"{uuid.uuid4().hex}_{safe_name}"

    try:
        upload_file(file, unique_name)
        return jsonify({
            "message": "File uploaded successfully",
            "filename": unique_name
        }), 201
    except Exception:
        app.logger.exception("File upload failed")
        return jsonify({"error": "File upload failed"}), 500


@app.route("/files", methods=["GET"])
def files():
    try:
        objects = list_files()

        result = [
            {
                "filename": item["Key"],
                "size": item["Size"]
            }
            for item in objects
        ]

        return jsonify(result)
    except Exception:
        app.logger.exception("Could not list files")
        return jsonify({"error": "Could not retrieve files"}), 500


@app.route("/download/<path:filename>", methods=["GET"])
def download(filename):
    try:
        response = download_file(filename)

        return send_file(
            BytesIO(response["Body"].read()),
            as_attachment=True,
            download_name=filename.split("_", 1)[-1]
        )
    except Exception:
        app.logger.exception("File download failed")
        return jsonify({"error": "File download failed"}), 404


@app.route("/delete/<path:filename>", methods=["DELETE"])
def delete(filename):
    try:
        delete_file(filename)
        return jsonify({"message": "File deleted successfully"})
    except Exception:
        app.logger.exception("File deletion failed")
        return jsonify({"error": "File deletion failed"}), 500


if __name__ == "__main__":
    app.run(debug=True)
