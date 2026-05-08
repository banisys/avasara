import os
import secrets

from fastapi import UploadFile

UPLOAD_DIR = "uploads"

ALLOWED_EXTENSIONS = ["mp3", "wav"]


def generate_file_token():
    return secrets.token_hex(32)


async def save_uploaded_file(file: UploadFile):
    extension = file.filename.split(".")[-1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise Exception("Invalid file format")

    file_token = generate_file_token()

    filename = f"{file_token}.{extension}"

    file_path = os.path.join(UPLOAD_DIR, filename)

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    return {
        "file_token": file_token,
        "extension": extension,
        "original_name": file.filename
    }