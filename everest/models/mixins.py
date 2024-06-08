from datetime import datetime
from typing import Optional

from mountaineer.database import Field
from pydantic import BaseModel
from sqlalchemy import Column, DateTime


class TimeStampMixin(object):
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
