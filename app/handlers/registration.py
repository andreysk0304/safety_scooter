import datetime

from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database_manager import session_maker, get_db_session
from app.database.table_models import Users, AccessTokens

from app.handlers.components.hash_component import HashComponent
from app.handlers.components.responses_component import ResponsesComponent
from app.handlers.components.tokens_component import generate_access_token
from app.handlers.models.registration_model import Registration

from sqlalchemy import text


router = APIRouter(tags=["Authorization"])



@router.post("/registration")
async def registration_func(data: Registration, request: Request, session: AsyncSession = Depends(get_db_session)):
    user = await session.execute(
        text('''SELECT id FROM users WHERE phone_number = :phone'''),
        {'phone': data.phone_number}
    )

    user = user.fetchone()

    if user != None:
        return ResponsesComponent.response_409(request=request)

    new_user = Users(
        phone_number = data.phone_number,
        password = await HashComponent.hash_password(password=data.password),
        created_at = datetime.datetime.now()
    )

    session.add(
        new_user
    )

    await session.commit()
    await session.refresh(new_user)

    access_token = await generate_access_token()

    session.add(
        AccessTokens(
            user_id = new_user.id,
            access_token = access_token,
            created_at = datetime.datetime.now()
        )
    )

    await session.commit()

    return  ResponsesComponent.response(request=request, json={'detail': 'Аккаунт успешно создан', 'access_token': access_token})