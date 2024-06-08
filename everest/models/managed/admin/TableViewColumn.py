from mountaineer.database.sqlmodel import SQLModel, Field
from uuid import uuid4, UUID


class TableViewColumn(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    column: str = Field()
    table_id: UUID = Field(foreign_key="tableview.id", index=True)

