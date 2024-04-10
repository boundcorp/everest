from pydantic import BaseModel

from everest.core.tables import AdminTable


class LayoutContext(BaseModel):
    tables: dict[str, AdminTable]
