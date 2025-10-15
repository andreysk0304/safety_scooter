from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database_manager import session_maker, get_db_session

from app.handlers.components.hash_component import HashComponent
from app.handlers.components.responses_component import ResponsesComponent
from app.handlers.models.login import Login

from sqlalchemy import text


router = APIRouter(tags=["Authorization"])


@router.post("/login")
async def login_func(data: Login, request: Request, session: AsyncSession = Depends(get_db_session)):

    user = await session.execute(
        text('''SELECT id, password FROM users WHERE phone_number = :phone'''),
        {'phone': data.phone_number}
    )

    user = user.fetchone()

    if user == None:
        return ResponsesComponent.response(request=request, status_code=400, json={'detail': 'Профиль с таким номером телефона не существует.'})

    clean_hash: str = user[1][2:-1]

    print(clean_hash)

    if not await HashComponent.check_password(password=data.password, password_hash=clean_hash):
       return ResponsesComponent.response_403(request=request)

    access_token = await session.execute(
        text('''SELECT access_token FROM access_tokens WHERE user_id = :user_id'''),
        {'user_id': user[0]}
    )

    access_token = access_token.fetchone()

    return ResponsesComponent.response(request=request, json={'detail': 'Вход произведён успешно!', 'access_token': access_token[0]})