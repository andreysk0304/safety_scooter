import logging

from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database.database_manager import get_db_session
from app.database.table_models import Users, Applications, Verdicts

from app.handlers.components.authorization_component import AuthorizationComponent
from app.handlers.components.responses_component import ResponsesComponent

router = APIRouter(tags=["Profile"])

logger = logging.getLogger(__name__)


@router.get("/profile")
async def get_profile(request: Request, session: AsyncSession = Depends(get_db_session), user: dict = Depends(AuthorizationComponent.get_user_id)):
    try:
        user_id = user.get("user_id", "")

        if user_id is None:
            return ResponsesComponent.response_401(request=request)

        user_stmt = select(Users).where(Users.id == user_id)
        user_result = await session.execute(user_stmt)
        user_data = user_result.scalar_one_or_none()

        if not user_data:
            return ResponsesComponent.response(
                request=request,
                status_code=404,
                json={'detail': 'Пользователь не найден'}
            )

        total_applications_stmt = select(func.count(Applications.id)).where(
            Applications.user_id == user_id,
            Applications.is_delete == False
        )

        total_applications_result = await session.execute(total_applications_stmt)
        total_applications = total_applications_result.scalar() or 0

        violations_applications_stmt = (
            select(func.count(func.distinct(Applications.id)))
            .join(Verdicts, Verdicts.application_id == Applications.id)
            .where(
                Applications.user_id == user_id,
                Applications.is_delete == False
            )
        )
        violations_applications_result = await session.execute(violations_applications_stmt)
        violations_count = violations_applications_result.scalar() or 0

        return ResponsesComponent.response(
            request=request,
            json={
                'phone_number': user_data.phone_number,
                'balance': float(user_data.balance),
                'total_applications': total_applications,
                'violations_found': violations_count
            }
        )

    except Exception as e:
        logger.error(f'Profile error: {e}', exc_info=True)

        return ResponsesComponent.response(
            request=request,
            status_code=500,
            json={'detail': 'Внутренняя ошибка сервера при получении профиля'}
        )
