from fastapi import Depends
from mountaineer import APIException, LayoutControllerBase, RenderBase
from pydantic import BaseModel
from sqlalchemy import Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel
from mountaineer.database import DatabaseDependencies

import everest.models.auth
from everest import models
from everest.core.auth.dependencies import AuthDependencies
from everest.core.tables import AdminTable, ALL_TABLES
from everest.core.types import AdminTableItem
from everest.models.auth import UserPublic


class NotFoundException(APIException):
    status_code = 404
    detail = "Detail item not found"


class AuthLayout(RenderBase):
    user: UserPublic | None = None


class AuthLayoutController(LayoutControllerBase):
    view_path = "/auth/layout.tsx"

    async def render(self,
                     user=Depends(AuthDependencies.lookup_user(everest.models.auth.User)),
                     ) -> AuthLayout:
        profile = user and user.dict() or None
        if profile:
            profile = UserPublic(id=str(profile.pop('id', '')), **profile)
        return AuthLayout(user=profile)