import datetime

from app.database.database_manager import session_maker

from sqlalchemy import select

from fastapi import Request

from app.database.table_models import AccessTokens
from app.handlers.components.responses_component import ResponsesComponent


class AuthorizationComponent:

    @staticmethod
    async def get_user_id(request: Request) -> dict | None:
        auth_header = request.headers.get("Authorization", "")

        access_token = auth_header.replace("Bearer ", "").strip()

        if not access_token:
            ResponsesComponent.response_401_error()

        async with session_maker() as session:
            user_with_token = await session.execute(select(AccessTokens).where(AccessTokens.access_token == access_token))
            user_with_token = user_with_token.scalars().first()

            if user_with_token is None:
                ResponsesComponent.response_401_error()

            token_age = datetime.datetime.now() - user_with_token[1]
            
            if token_age > datetime.timedelta(days=7):
                ResponsesComponent.response_401_error()

            return {'user_id': user_with_token[0]}