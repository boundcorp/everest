from mountaineer import RenderBase, ControllerBase
from mountaineer.database import DatabaseDependencies

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from everest.controllers.layout import AdminDependencies
from everest.core.tables import AdminTable
from everest.core.types import AdminTableItem


class TableListRender(RenderBase):
    table: AdminTable
    items: list[AdminTableItem] = []


class TableListController(ControllerBase):
    url = "/table/{table_id}/"
    view_path = "/app/table/list/page.tsx"

    def __init__(self):
        super().__init__()

    async def render(
            self,
            table: AdminTable = Depends(AdminDependencies.require_table),
            session: AsyncSession = Depends(DatabaseDependencies.get_db_session),
    ) -> TableListRender:
        items = await session.execute(select(table.db_model).order_by(*table.table_schema.default_sort_order))
        items = [dict(row) for row in items.scalars().all()]

        return TableListRender(
            table=table,
            items=items
        )
