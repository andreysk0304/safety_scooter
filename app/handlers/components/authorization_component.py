import datetime

from app.database.database_manager import session_maker

from sqlalchemy import text

from fastapi import HTTPException, status, Request

from app.handlers.components.responses_component import ResponsesComponent


class AuthorizationComponent:

    @staticmethod
    async def get_user_id(request: Request) -> dict | None:

        access_token = request.headers.get("Authorization", "")

        if access_token == "":
            ResponsesComponent.response_401_error()

        async with session_maker() as session:

            user_with_token = await session.execute(
                text('''SELECT user_id, created_at FROM access_tokens WHERE access_token = :access_token'''),
                {'access_token': access_token}
            )

            user_with_token = user_with_token.fetchone()

            if user_with_token is None:
                ResponsesComponent.response_401_error()

            if user_with_token[1] - datetime.datetime.now() > datetime.timedelta(days=7):
                ResponsesComponent.response_401_error()

            return {'user_id': user_with_token[0]}