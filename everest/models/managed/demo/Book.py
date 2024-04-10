from mountaineer.database.sqlmodel import Field, SQLModel
from uuid import UUID, uuid4


class Book(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

