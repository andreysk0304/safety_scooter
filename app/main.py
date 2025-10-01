import asyncio

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.database.table_models import create_db
from app.utils.tags import openapi_tags

from app.handlers import registration


app = FastAPI(openapi_tags=openapi_tags)


app.include_router(registration.router)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.on_event("startup")
async def on_startup():

    await create_db()