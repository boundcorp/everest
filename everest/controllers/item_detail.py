from datetime import datetime
from uuid import UUID

from mountaineer import RenderBase, ControllerBase, APIException
from mountaineer.database import DatabaseDependencies

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from everest.core.layout import LayoutContext
from everest.core.types import AdminTableItem


class NotFoundException(APIException):
    status_code = 404
    detail = "Detail item not found"


AnyType = None | bool | str | int | datetime | UUID


class TableItemRender(RenderBase):
    id: str
    layout: LayoutContext
    item: AdminTableItem


class TableItemController(ControllerBase):
    url = "/table/{table_id}/{item_id}"
    view_path = "/app/table/item/page.tsx"

    async def render(
            self,
            session: AsyncSession = Depends(DatabaseDependencies.get_db_session),
            layout: LayoutContext = Depends(LayoutContext.get_layout),
    ) -> TableItemRender:
        return TableItemRender(
            id=layout.item_id,
            layout=layout,
            item=layout.item,
        )