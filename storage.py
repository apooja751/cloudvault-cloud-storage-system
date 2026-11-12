
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


def upload_file(file, filename):
    client = get_supabase_client()

    file_content = file.read()

    client.storage.from_(get_bucket_name()).upload(
        path=filename,
        file=file_content,
        file_options={
            "content-type": file.content_type or "application/octet-stream",
            "upsert": "false"
        }
    )

    return True


def list_files():
    client = get_supabase_client()

    objects = client.storage.from_(get_bucket_name()).list()

    return [
        {
            "Key": item["name"],
            "Size": (item.get("metadata") or {}).get("size", 0)
        }
        for item in objects
        if item.get("name")
    ]


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
