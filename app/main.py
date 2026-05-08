from fastapi import FastAPI

from app.routers.upload import router as upload_router

app = FastAPI()

app.include_router(upload_router)