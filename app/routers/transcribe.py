import os

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    BackgroundTasks
)

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.file import File
from app.services.transcribe_service import transcribe_audio

router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def process_transcription(file_id: int):

    db = SessionLocal()

    try:

        file_record = db.query(File).filter(
            File.id == file_id
        ).first()

        if not file_record:
            return

        filename = (
            f"{file_record.file_token}."
            f"{file_record.extension}"
        )

        try:

            file_record.status = "processing"
            db.commit()

            text = transcribe_audio(filename)

            file_record.text = text
            file_record.status = "finished"

            db.commit()

        except Exception:

            file_record.status = "failed"
            db.commit()

    finally:
        db.close()


@router.post("/transcribe/{file_token}")
def transcribe(
    file_token: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    file_record = db.query(File).filter(
        File.file_token == file_token
    ).first()

    if not file_record:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    if file_record.status == "processing":
        return {
            "status": False,
            "message": "File is already processing"
        }

    file_record.status = "pending"
    db.commit()

    background_tasks.add_task(
        process_transcription,
        file_record.id
    )

    return {
        "status": True,
        "message": "Transcription started",
        "file_token": file_token
    }