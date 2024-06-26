from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

import bcrypt
from mountaineer.database import Field, SQLModel
from pydantic import BaseModel
from sqlalchemy import Column, DateTime

from everest.models.mixins import TimeStampMixin


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password=plain_password.encode(), hashed_password=hashed_password.encode()
    )


class UserBase(BaseModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str
    email: str | None = None
    is_verified: bool = False
    is_staff: bool = False
    is_superuser: bool = False
    last_login: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            nullable=True,
        )
    )


class UserPublic(UserBase):
    id: str


class User(SQLModel, UserBase, TimeStampMixin, table=True):
    hashed_password: str | None = None

    @classmethod
    def create_superuser(cls, email: str, password: str):
        return cls(
            username=email,
            email=email,
            hashed_password=hash_password(password),
            is_superuser=True,
            is_staff=True,
            is_verified=True,
            last_login=datetime.utcnow(),
        )
