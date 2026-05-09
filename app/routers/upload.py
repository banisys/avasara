from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.file import File as FileModel
from app.services.file_service import save_uploaded_file

router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/upload")
async def upload_audio(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    uploaded = await save_uploaded_file(file)

    new_file = FileModel(
        file_token=uploaded["file_token"],
        original_name=uploaded["original_name"],
        extension=uploaded["extension"]
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {
        "status": True,
        "file_token": uploaded["file_token"]
    }
