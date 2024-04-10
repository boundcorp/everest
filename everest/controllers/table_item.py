from datetime import datetime
from uuid import UUID

from mountaineer import RenderBase, ControllerBase, APIException
from mountaineer.database import DatabaseDependencies

from fastapi import Depends
from sqlalchemy import select, String, cast
from sqlalchemy.ext.asyncio import AsyncSession

from everest import models
from everest.core.auth.dependencies import AuthDependencies
from everest.core.layout import LayoutContext
from everest.core.tables import ALL_TABLES
from everest.core.types import GenericTableRowItem


class NotFoundException(APIException):
    status_code = 404
    detail = "Detail item not found"


AnyType = None | bool | str | int | datetime | UUID


class TableItemRender(RenderBase):
    id: str
    layout: LayoutContext
    item: GenericTableRowItem


class TableItemController(ControllerBase):
    url = "/table/{table_id}/{item_id}"
    view_path = "/app/table/item/page.tsx"

    async def render(
            self,
            table_id: str,
            item_id: str,
            session: AsyncSession = Depends(DatabaseDependencies.get_db_session),
            user=Depends(AuthDependencies.require_valid_user(models.User))
    ) -> TableItemRender:
        print("Current user", user)
        layout = LayoutContext(tables=ALL_TABLES())
        table = layout.tables.get(table_id)
        model = getattr(models, table.table_schema.name, None)
        if not model:
            raise NotFoundException()
        item = await session.execute(select(model).where(cast(model.id, String) == item_id))

        return TableItemRender(
            id=table_id,
            layout=layout,
            item=dict(item.scalars().one())
        )
