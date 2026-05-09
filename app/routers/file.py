from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.file import File

router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/files/{file_token}")
def get_file(
    file_token: str,
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

    return {
        "file_token": file_record.file_token,
        "status": file_record.status,
        "text": file_record.text
    }