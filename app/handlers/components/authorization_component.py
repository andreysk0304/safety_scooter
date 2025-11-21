import datetime

from app.database.database_manager import session_maker

from sqlalchemy import text

from fastapi import HTTPException, status, Request

from app.handlers.components.responses_component import ResponsesComponent


class AuthorizationComponent:

    @staticmethod
    async def get_user_id(request: Request) -> dict | None:
        auth_header = request.headers.get("Authorization", "")
        
        # Проверка формата токена (Bearer <token>)
        if not auth_header.startswith("Bearer "):
            ResponsesComponent.response_401_error()
        
        access_token = auth_header.replace("Bearer ", "").strip()

        if not access_token:
            ResponsesComponent.response_401_error()

        async with session_maker() as session:

            user_with_token = await session.execute(
                text('''SELECT user_id, created_at FROM access_tokens WHERE access_token = :access_token'''),
                {'access_token': access_token}
            )

            user_with_token = user_with_token.fetchone()

            if user_with_token is None:
                ResponsesComponent.response_401_error()

            token_age = datetime.datetime.now() - user_with_token[1]
            
            if token_age > datetime.timedelta(days=7):
                ResponsesComponent.response_401_error()

            return {'user_id': user_with_token[0]}