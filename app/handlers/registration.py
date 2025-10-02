import datetime

from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from app.database.database_manager import session_maker
from app.database.table_models import Users, AccessTokens
from app.handlers.components.hash_component import HashComponent
from app.handlers.components.tokens_component import generate_access_token
from app.handlers.models.registration_model import Registration

from sqlalchemy import text


router = APIRouter(tags=["Authorization"])


async def check_validation(data: Registration) -> dict | None:
    phone_number = data.phone_number
    password = data.password

    msg = ''

    if password == '':
        msg += 'password is empty. '

    if phone_number == '':
        msg += 'phone_number is empty. '

    if msg != '':
        return {'detail': msg}

    else:
        return None



@router.post("/registration")
async def registration_func(data: Registration, request: Request):

    async with session_maker() as session:

        validator = await check_validation(data)

        if validator != None:
            return JSONResponse(content=validator, headers={
                "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
                "Access-Control-Allow-Credentials": "true",
                "Vary": "Origin"
            }, status_code=400)


        user = await session.execute(
            text('''SELECT id FROM users WHERE phone_number = :phone'''),
            {'phone': data.phone_number}
        )

        user = user.fetchone()

        if user != None:
            return JSONResponse(content={'detail': 'Аккаунт с таким номером телефона уже существует.'}, headers={
                "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
                "Access-Control-Allow-Credentials": "true",
                "Vary": "Origin"
            }, status_code=409)

        user = Users(
            phone_number = data.phone_number,
            password = await HashComponent.hash_password(password=data.password),
            created_at = datetime.datetime.now()
        )

        session.add(
            user
        )

        await session.commit()

        access_token = await generate_access_token()

        session.add(
            AccessTokens(
                user_id = user.id,
                access_token = access_token,
                created_at = datetime.datetime.now()
            )
        )

        await session.commit()

        return  JSONResponse(content={'datail': 'Аккаунт успешно создан', 'access_token': access_token}, headers={
            "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
            "Access-Control-Allow-Credentials": "true",
            "Vary": "Origin"
        })

