from datetime import datetime
from uuid import UUID

AnyType = None | bool | str | int | datetime | UUID

GenericTableRowItem = dict[str, AnyType]
