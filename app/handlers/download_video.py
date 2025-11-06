from fastapi import APIRouter

from fastapi import APIRouter, UploadFile, File, Request, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.database_manager import get_db_session
from app.database.table_models import Applications
from app.handlers.components.authorization_component import AuthorizationComponent
from app.handlers.components.responses_component import ResponsesComponent
from app.utils.s3_client import S3Client

router = APIRouter(tags=["Video"])


@router.get("/download/{application_id}")
async def download_video_func(request: Request, application_id: int, session: AsyncSession = Depends(get_db_session), user: dict = Depends(AuthorizationComponent.get_user_id)):
    user_id = user.get("user_id", "")

    if not user_id:
        return ResponsesComponent.response_401(request=request)

    stmt = select(Applications).where(
        Applications.id == application_id,
        Applications.user_id == user_id
    )
    result = await session.execute(stmt)

    application = result.scalar_one_or_none()

    if not application:
        return ResponsesComponent.response(
            request=request,
            status_code=404,
            json={"detail": "Видео не найдено или нет доступа"}
        )

    url = S3Client.generate_presigned_url(key=application.key, expires_in=600)

    if not url:
        return ResponsesComponent.response_503(request=request)

    return ResponsesComponent.response(
        request=request,
        json={"download_url": url}
    )