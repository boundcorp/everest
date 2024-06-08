from mountaineer import RenderBase, ControllerBase
from mountaineer.database import DatabaseDependencies

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from everest.controllers.app.layout import AdminDependencies
from everest.core.tables import AdminTable
from everest.core.types import AdminTableItem


class TableItemRender(RenderBase):
    item: AdminTableItem
    table: AdminTable


class TableItemController(ControllerBase):
    url = "/table/{table_id}/{item_id}"
    view_path = "/app/table/item/page.tsx"

    async def render(
            self,
            table: AdminTable = Depends(AdminDependencies.require_table),
            item: AdminTableItem = Depends(AdminDependencies.require_item),
            session: AsyncSession = Depends(DatabaseDependencies.get_db_session),
    ) -> TableItemRender:
        return TableItemRender(
            table=table,
            item=item,
        )
