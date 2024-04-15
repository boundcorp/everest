from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

AnyType = None | bool | str | int | datetime | UUID
AdminTableItem = dict[str, AnyType]


class AdminTableRow(BaseModel):
    row_id: str
    table_id: str
    data: AdminTableItem
