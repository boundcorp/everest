from mountaineer import RenderBase, ControllerBase
from mountaineer.database import DatabaseDependencies

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from everest import models
from everest.core.exceptions import NotFoundException
from everest.core.layout import LayoutContext
from everest.core.tables import ALL_TABLES
from everest.core.types import AdminTableItem


class TableListRender(RenderBase):
    id: str
    layout: LayoutContext
    items: list[AdminTableItem] = []


class TableListController(ControllerBase):
    url = "/table/{table_id}/"
    view_path = "/app/table/list/page.tsx"

    def __init__(self):
        super().__init__()

    async def render(
            self,
            table_id: str,
            session: AsyncSession = Depends(DatabaseDependencies.get_db_session),
            layout: LayoutContext = Depends(LayoutContext.get_layout),
    ) -> TableListRender:
        items = await session.execute(select(layout.table.table_model).order_by(*layout.table.table_schema.default_sort_order))
        items = [dict(row) for row in items.scalars().all()]

        return TableListRender(
            id=table_id,
            layout=layout,
            items=items
        )
