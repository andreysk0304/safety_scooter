from sqlalchemy import select
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database_manager import get_db_session
from app.database.table_models import Applications, Verdicts
from app.handlers.components.authorization_component import AuthorizationComponent
from app.handlers.components.responses_component import ResponsesComponent

router = APIRouter()

STATUSES = {"pending": "Проверяется", "canceled": "Отклонена", 'processing': 'Проверяется', 'completed': 'Нарушение обнаружено', 'no_violations': 'Нарушение не обнаружено', 'failed': 'Нуждается в ручной проверке'}
VERDICTS = {"multiple_people_on_scooter": "Езда на самокате вдвоём", "riding_on_zebra_crossing": "Езда по пешеходному переходу"}

@router.get("/applications")
async def get_user_applications(request: Request, session: AsyncSession = Depends(get_db_session), user: dict = Depends(AuthorizationComponent.get_user_id)):
    user_id = user.get("user_id", "")

    if user_id is None:
        return ResponsesComponent.response_401(request=request)

    stmt = (
        select(Applications, Verdicts)
        .join(Verdicts, Verdicts.application_id == Applications.id, isouter=True)
        .where(
            Applications.user_id == user_id,
            Applications.is_delete == False
        )
        .order_by(Applications.id)
    )

    rows = (await session.execute(stmt)).all()

    apps_dict = {}

    for app, verdict in rows:
        if app.id not in apps_dict:
            apps_dict[app.id] = {
                "id": app.id,
                "status": STATUSES.get(app.status, "Неизвестный статус"),
                "key": app.key,
                "record_time": app.record_time.isoformat() if app.record_time else None,
                "last_change": app.last_change.isoformat() if app.last_change else None,
                "verdicts": []
            }

        if verdict:
            apps_dict[app.id]["verdicts"].append({
                "id": verdict.id,
                "type": VERDICTS.get(verdict.type, verdict.type),
                "scooter_type": verdict.scooter_type,
                "object_id": verdict.object_id,
                "timestamp": verdict.timestamp,
                "coordinates": verdict.coordinates,
                "created_at": verdict.created_at.isoformat() if verdict.created_at else None,
            })

    apps_list = list(apps_dict.values())

    return ResponsesComponent.response(
        request=request,
        json={"applications": apps_list}
    )
