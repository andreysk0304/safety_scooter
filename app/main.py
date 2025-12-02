import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.database.table_models import create_db
from app.utils.tags import openapi_tags

from app.handlers import registration, login, upload_video, download_video, applications, profile

app = FastAPI(openapi_tags=openapi_tags)


app.include_router(registration.router, prefix="")
app.include_router(login.router, prefix="")
app.include_router(applications.router, prefix="")
app.include_router(profile.router, prefix="")
app.include_router(upload_video.router, prefix="/video")
app.include_router(download_video.router, prefix="/video")

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",") if os.getenv("ALLOWED_ORIGINS") else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():

    await create_db()