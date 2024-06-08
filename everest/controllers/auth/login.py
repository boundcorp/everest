import json

from jose import jwt
from mountaineer import ControllerBase, Metadata, RenderBase, sideeffect, APIException
from mountaineer.database import DatabaseDependencies
from mountaineer.dependencies import CoreDependencies

from fastapi import Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from everest.core.auth.dependencies import AuthDependencies
from everest.core.auth.config import AuthConfig
from everest.models import User
from everest.models.auth import verify_password


class LoginRender(RenderBase):
    pass


class FormError(APIException):
    status_code = 400
    detail = "An error occurred while processing the form"
    field_errors: dict[str, str] | None = None


class LoginController(ControllerBase):
    url = "/login"
    view_path = "/auth/login/page.tsx"

    async def render(
            self,
            user=Depends(AuthDependencies.lookup_user(User)),
    ) -> LoginRender:
        if user:
            raise HTTPException(status_code=302, headers={"Location": "/"})
        return LoginRender(
            metadata=Metadata(title="Login"),
        )

    @sideeffect(exception_models=[FormError])
    async def login(self, username: str, password: str, response: Response,
                    db: AsyncSession = Depends(DatabaseDependencies.get_db_session),
                    ) -> None:

        if not username or not password:
            raise FormError(status_code=400, detail="Invalid username or password")

        lookup = await db.execute(select(User).where(User.username == username))
        user = lookup.scalars().first()

        if not lookup or not user or not verify_password(password, user.hashed_password):
            raise FormError(status_code=400, detail="Invalid username or password")

        print(f"User: {user}")

        payload = {"user_id": str(user.id)}

        response.headers['update-session-cookie'] = json.dumps(payload)
