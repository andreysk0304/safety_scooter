from sqlalchemy import select
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database_manager import get_db_session
from app.database.table_models import Applications
from app.handlers.components.authorization_component import AuthorizationComponent
from app.handlers.components.responses_component import ResponsesComponent

router = APIRouter()

STATUSES = {"for consideration": "На рассмотрение", "canceled": "Отклонена"}

@router.get("/applications")
async def get_user_applications(request: Request, session: AsyncSession = Depends(get_db_session), user: dict = Depends(AuthorizationComponent.get_user_id)):
    user_id = user.get("user_id", "")

    if not user_id:
        return ResponsesComponent.response_401(request=request)

    stmt = select(Applications).where(Applications.user_id == user_id, Applications.is_delete == False)
    result = await session.execute(stmt)
    applications = result.scalars().all()

    data = [
        {
            "id": app.id,
            "status": STATUSES.get(app.status, "что то не тоо ю_ю"),
            "key": app.key,
            "record_time": app.record_time.isoformat() if app.record_time else None,
            "last_change": app.last_change.isoformat() if app.last_change else None,
        }
        for app in applications
    ]

    return ResponsesComponent.response(request=request, json={"applications": data})
