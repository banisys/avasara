from fastapi import FastAPI

from app.routers.gateway import router as gateway_router

app = FastAPI()

app.include_router(gateway_router)