import datetime

from fastapi import APIRouter, UploadFile, File, Request, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database_manager import get_db_session
from app.database.table_models import Applications
from app.handlers.components.authorization_component import AuthorizationComponent
from app.handlers.components.responses_component import ResponsesComponent
from app.utils.s3_client import S3Client


router = APIRouter(tags=["Video"])


MAX_FILE_SIZE = 1 * 1024 * 1024 * 1024


@router.post("/upload")
async def upload_video_func(request: Request, gps: list[str] = Form(...), time: int = Form(...), file: UploadFile = File(...), session: AsyncSession = Depends(get_db_session), user: dict = Depends(AuthorizationComponent.get_user_id)):

    user_id = user.get("user_id", "")

    if user_id == "":
        return ResponsesComponent.response_401(request=request)

    if not file.filename.lower().endswith(".mp4"):
        return ResponsesComponent.response(request=request, status_code=400, json={"detail": "Только MP4 файлы разрешены"})

    size = file.file.seek(0, 2)

    if size > MAX_FILE_SIZE:
        return ResponsesComponent.response(request=request, status_code=413, json={"detail": "Файл слишком большой (макс 1 ГБ)"})

    key: str = S3Client.upload_video(file=file)

    if key == 'null':
        return ResponsesComponent.response_503(request=request)

    session.add(
        Applications(
            user_id = user_id,
            key = key,
            status = 'pending',
            gps_longitude = gps[-1].split(',')[0].replace('"', '').replace('[', ''),
            gps_width = gps[-1].split(',')[1].replace('"', '').replace('[', ''),
            record_time = datetime.datetime.fromtimestamp(time),
            is_delete = False,
            created_at = datetime.datetime.now(),
            last_change = datetime.datetime.now()
        )
    )

    await session.commit()

    return ResponsesComponent.response(request=request, json={'detail': 'Заявка успешно создана!'})