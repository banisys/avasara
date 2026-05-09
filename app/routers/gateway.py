from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends,
    BackgroundTasks,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.file import File as FileModel

from app.services.file_service import save_uploaded_file
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

        file_record = db.query(FileModel).filter(
            FileModel.id == file_id
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


@router.post("/api/ocr/getway")
async def gateway(
    background_tasks: BackgroundTasks,
    command: str = Form(...),
    filetoken: str = Form(None),
    filehandle: UploadFile = File(None),
    db: Session = Depends(get_db)
):

    command = command.lower()

    #
    # ADD FILE
    #
    if command == "addfile":

        if not filehandle:
            raise HTTPException(
                status_code=400,
                detail="filehandle is required"
            )

        uploaded = await save_uploaded_file(filehandle)

        new_file = FileModel(
            file_token=uploaded["file_token"],
            original_name=uploaded["original_name"],
            extension=uploaded["extension"],
            status="pending"
        )

        db.add(new_file)
        db.commit()

        return {
            "Status": "Done",
            "FileToken": uploaded["file_token"]
        }

    #
    # CONVERT
    #
    elif command == "convert":

        if not filetoken:
            raise HTTPException(
                status_code=400,
                detail="filetoken is required"
            )

        file_record = db.query(FileModel).filter(
            FileModel.file_token == filetoken
        ).first()

        if not file_record:
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )

        if file_record.status == "processing":
            return {
                "Status": "AlreadyProcessing"
            }

        background_tasks.add_task(
            process_transcription,
            file_record.id
        )

        return {
            "Status": "ConvertStarted"
        }

    #
    # CHECK CONVERT
    #
    elif command == "checkconvert":

        if not filetoken:
            raise HTTPException(
                status_code=400,
                detail="filetoken is required"
            )

        file_record = db.query(FileModel).filter(
            FileModel.file_token == filetoken
        ).first()

        if not file_record:
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )

        return {
            "Status": file_record.status,
            "Output": file_record.text or ""
        }

    #
    # INVALID COMMAND
    #
    else:

        raise HTTPException(
            status_code=400,
            detail="Invalid command"
        )