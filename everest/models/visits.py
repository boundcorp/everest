from datetime import datetime

from mountaineer.database.sqlmodel import SQLModel, Field
from uuid import uuid4, UUID
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, Column

from everest.models.mixins import TimeStampMixin


class Session(SQLModel, table=True):
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            default=datetime.utcnow,
            nullable=False,
        )
    )

    updated_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
        )
    )
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID | None = Field(foreign_key="user.id", nullable=True)


class Visit(SQLModel, table=True):
    created_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            default=datetime.utcnow,
            nullable=False,
        )
    )

    updated_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
        )
    )
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    session_id: UUID | None = Field(foreign_key="session.id")
    user_id: UUID | None = Field(foreign_key="user.id", nullable=True)
    ip: str
    page: str
    method: str
