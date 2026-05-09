from fastapi import FastAPI

from app.routers.upload import router as upload_router
from app.routers.transcribe import router as transcribe_router
from app.routers.file import router as file_router

app = FastAPI()

app.include_router(upload_router)
app.include_router(transcribe_router)
app.include_router(file_router)