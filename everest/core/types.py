from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

AnyType = None | bool | str | int | datetime | UUID
AdminTableItem = dict[str, AnyType]


class AdminTableRow(BaseModel):
    data: AdminTableItem
