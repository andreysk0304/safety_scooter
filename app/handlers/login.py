import logging

from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database_manager import get_db_session
from app.database.table_models import Users, AccessTokens

from app.handlers.components.hash_component import HashComponent
from app.handlers.components.responses_component import ResponsesComponent
from app.handlers.models.login import Login

from sqlalchemy import select

router = APIRouter(tags=["Authorization"])

logger = logging.getLogger(__name__)


@router.post("/login")
async def login_func(data: Login, request: Request, session: AsyncSession = Depends(get_db_session)):
    try:
        user = await session.execute(select(Users).where(Users.phone_number == data.phone_number))
        user = user.scalars().first()

        if not user:
            return ResponsesComponent.response(request=request, status_code=400, json={'detail': 'Профиль с таким номером телефона не существует.'})

        stored_hash: str = user.password

        if not stored_hash:
            return ResponsesComponent.response(request=request, status_code=500, json={'detail': 'Ошибка базы данных'})

        if not await HashComponent.check_password(password=data.password, password_hash=stored_hash):
           return ResponsesComponent.response_403(request=request)

        access_token = await session.execute(select(AccessTokens).where(AccessTokens.user_id == user.id))
        access_token = access_token.scalars().first()

        if not access_token:
            return ResponsesComponent.response(request=request, status_code=500, json={'detail': 'Ошибка получения токена доступа'})

        return ResponsesComponent.response(request=request, json={'detail': 'Вход произведён успешно!', 'access_token': access_token.access_token})
    
    except Exception as e:
        logger.error(f'Login error: {e}', exc_info=True)

        return ResponsesComponent.response(
            request=request, 
            status_code=500, 
            json={'detail': 'Внутренняя ошибка сервера при входе'}
        )