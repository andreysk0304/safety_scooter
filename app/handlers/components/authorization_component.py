import datetime

from app.database.database_manager import session_maker

from sqlalchemy import text

from fastapi import HTTPException, status


class AuthorizationComponent:

    @staticmethod
    async def get_user_id() -> dict | None:
        async with session_maker() as session:

            user_with_token = await session.execute(
                text('''SELECT user_id, created_at FROM access_tokens WHERE access_token = :access_token'''),
                {'access_token': access_token}
            )

            user_with_token = user_with_token.fetchone()

            if user_with_token == None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Не верный токен авторизации."
                )

            if user_with_token[1] - datetime.datetime.now() > datetime.timedelta(days=7):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Не верный токен авторизации."
                )

            return {'user_id': user_with_token[0]}