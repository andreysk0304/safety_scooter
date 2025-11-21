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

    current_pos = file.file.tell()
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(current_pos)

    if size > MAX_FILE_SIZE:
        return ResponsesComponent.response(request=request, status_code=413, json={"detail": "Файл слишком большой (макс 1 ГБ)"})

    key: str = await S3Client.upload_video(file=file)

    if key == 'null':
        return ResponsesComponent.response_503(request=request)

    try:
        if not gps or len(gps) == 0:
            return ResponsesComponent.response(request=request, status_code=400, json={"detail": "GPS координаты не предоставлены"})
        
        gps_str = gps[-1] if isinstance(gps[-1], str) else str(gps[-1])
        gps_clean = gps_str.strip().replace('"', '').replace('[', '').replace(']', '')
        gps_parts = [part.strip() for part in gps_clean.split(',')]
        
        if len(gps_parts) < 2:
            return ResponsesComponent.response(request=request, status_code=400, json={"detail": "Неверный формат GPS координат"})
        
        gps_longitude = gps_parts[0]
        gps_width = gps_parts[1]

        float(gps_longitude)
        float(gps_width)

    except (ValueError, IndexError, AttributeError) as e:
        return ResponsesComponent.response(request=request, status_code=400, json={"detail": f"Неверный формат GPS координат: {str(e)}"})

    session.add(
        Applications(
            user_id = user_id,
            key = key,
            status = 'pending',
            gps_longitude = gps_longitude,
            gps_width = gps_width,
            record_time = datetime.datetime.fromtimestamp(time),
            is_delete = False,
            created_at = datetime.datetime.now(),
            last_change = datetime.datetime.now()
        )
    )

    await session.commit()

    return ResponsesComponent.response(request=request, json={'detail': 'Заявка успешно создана!'})