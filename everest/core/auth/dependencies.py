from typing import Type, TypeVar

from fastapi import Depends, Request
from mountaineer.dependencies import CoreDependencies
from mountaineer.database import DatabaseDependencies
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from everest.core.auth.config import AuthConfig
from everest.core.auth.exceptions import UnauthorizedError
from everest.models import User

T = TypeVar("T", bound=User)


class AuthDependencies:
    @staticmethod
    def lookup_user(user_model: Type[T]):
        async def internal(
            request: Request,
            auth_config: AuthConfig = Depends(
                CoreDependencies.get_config_with_type(AuthConfig)
            ),
            db: AsyncSession = Depends(DatabaseDependencies.get_db_session),
        ) -> T | None:
            """
            Peek the user from the request, if it exists
            """
            try:
                token = request.cookies.get(auth_config.SESSION_COOKIE_NAME, None)
                if not token:
                    return None

                payload = jwt.decode(
                    token,
                    auth_config.API_SECRET_KEY,
                    algorithms=[auth_config.API_KEY_ALGORITHM],
                )

                user_id = payload.get("user_id")
                if user_id is None:
                    return None

                return await db.get(user_model, user_id)
            except ExpiredSignatureError:
                return None
            except JWTError:
                return None

        return internal

    @staticmethod
    def require_valid_user(
        user_model: Type[T],
    ):
        def internal(
            peeked_user: T | None = Depends(AuthDependencies.lookup_user(user_model)),
        ) -> T:
            if peeked_user is None:
                raise UnauthorizedError()

            return peeked_user

        return internal

    @staticmethod
    def require_admin(
        user_model: Type[T],
    ):
        def internal(
            user: T = Depends(AuthDependencies.require_valid_user(user_model)),
        ) -> T:
            if not user.is_admin:
                raise UnauthorizedError()

            return user

        return internal

    @staticmethod
    def access_token_cookie_key():
        return "access_key"