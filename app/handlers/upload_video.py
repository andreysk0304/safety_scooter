from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database_manager import get_db_session
from app.handlers.components.authorization_component import AuthorizationComponent
from app.handlers.components.responses_component import ResponsesComponent

router = APIRouter(tags=["Video"])


@router.post("/upload")
async def upload_video_func(request: Request, file: UploadFile = File(...), session: AsyncSession = Depends(get_db_session), user: dict = Depends(AuthorizationComponent.get_user_id)):



    if not file.filename.lower().endswith(".mp4"):
        raise ResponsesComponent.response(request=request, status_code=400, json={"detail": "Только MP4 файлы разрешены"))

    file_key = f"{uuid4()}_{file.filename}"

    s3.upload_fileobj(file.file, BUCKET, file_key, ExtraArgs={"ContentType": "video/mp4"})

    url = s3.generate_presigned_url("get_object", Params={"Bucket": BUCKET, "Key": key}, ExpiresIn=3600)

    session.add(
        Applications(
            user_id
        )
    )


    return ResponsesComponent.response(request=request, )