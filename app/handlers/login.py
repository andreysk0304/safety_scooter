import datetime

from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from app.database.database_manager import session_maker
from app.database.table_models import Users, AccessTokens
from app.handlers.components.hash_component import HashComponent
from app.handlers.components.tokens_component import generate_access_token
from app.handlers.models.login import Login

from sqlalchemy import text


router = APIRouter(tags=["Authorization"])


async def check_validation(data: Login) -> dict | None:
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



@router.post("/login")
async def login_func(data: Login, request: Request):

    async with session_maker() as session:

        validator = await check_validation(data)

        if validator != None:
            return JSONResponse(content=validator, headers={
                "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
                "Access-Control-Allow-Credentials": "true",
                "Vary": "Origin"
            }, status_code=400)


        user = await session.execute(
            text('''SELECT id, password FROM users WHERE phone_number = :phone'''),
            {'phone': data.phone_number}
        )

        user = user.fetchone()

        if user != None:
            return JSONResponse(content={'detail': 'Аккаунт с таким номером телефона уже существует.'}, headers={
                "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
                "Access-Control-Allow-Credentials": "true",
                "Vary": "Origin"
            }, status_code=409)

        if HashComponent.check_password(password=data.password, password_hash=user[1]):
            access_token = await generate_access_token()

            session.add(
                AccessTokens(
                    user_id = user.id,
                    access_token = access_token,
                    created_at = datetime.datetime.now()
                )
            )

            await session.commit()

            return JSONResponse(content={'detail': 'Аккаунт успешно создан', 'access_token': access_token}, headers={
                "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
                "Access-Control-Allow-Credentials": "true",
                "Vary": "Origin"
            })

        else:

            return JSONResponse(content={'detail': 'Не удалось войти в аккаунт'}, headers={
                "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
                "Access-Control-Allow-Credentials": "true",
                "Vary": "Origin"
            }, status_code=403)
