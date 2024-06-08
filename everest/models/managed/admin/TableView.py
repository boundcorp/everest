from mountaineer.database.sqlmodel import SQLModel, Field
from uuid import uuid4, UUID
from sqlmodel import Relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .TableViewColumn import TableViewColumn


class TableView(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    table: str = Field()
    stub: str = Field()
    description: str = Field()

