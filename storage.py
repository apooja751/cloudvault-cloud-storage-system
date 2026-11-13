
import os
from io import BytesIO

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()


def get_supabase_client():
    url = os.getenv("SUPABASE_URL")
    secret_key = os.getenv("SUPABASE_SECRET_KEY")

    if not url or not secret_key:
        raise RuntimeError("Supabase credentials are missing.")

    return create_client(url, secret_key)


def get_bucket_name():
    bucket_name = os.getenv("SUPABASE_BUCKET_NAME")

    if not bucket_name:
        raise RuntimeError("Supabase bucket name is missing.")

    return bucket_name


def upload_file(file, filename, category="Documents"):
    client = get_supabase_client()

    allowed_categories = ["Documents", "Images", "Others"]

    if category not in allowed_categories:
        raise ValueError("Invalid file category")

    file_content = file.read()
    storage_path = f"{category}/{filename}"

    client.storage.from_(get_bucket_name()).upload(
        path=storage_path,
        file=file_content,
        file_options={
            "content-type": file.content_type or "application/octet-stream",
            "upsert": "false"
        }
    )

    return True


def list_files():
    client = get_supabase_client()
    bucket = client.storage.from_(get_bucket_name())

    categories = ["Documents", "Images", "Others"]
    all_files = []

    # Include older files stored in the bucket root
    root_objects = bucket.list()

    for item in root_objects:
        if item.get("name") and item.get("metadata"):
            all_files.append({
                "Key": item["name"],
                "Size": (item.get("metadata") or {}).get("size", 0),
                "Category": "Uncategorized"
            })

    # List files inside category folders
    for category in categories:
        objects = bucket.list(category)

        for item in objects:
            if item.get("name") and item.get("metadata"):
                all_files.append({
                    "Key": f"{category}/{item['name']}",
                    "Size": (item.get("metadata") or {}).get("size", 0),
                    "Category": category
                })

    return all_files


def delete_file(filename):
    client = get_supabase_client()

    client.storage.from_(get_bucket_name()).remove([filename])

    return True


def download_file(filename):
    client = get_supabase_client()

    file_content = client.storage.from_(get_bucket_name()).download(filename)

    return {
        "Body": BytesIO(file_content)
    }