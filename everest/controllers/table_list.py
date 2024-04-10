from mountaineer import RenderBase, ControllerBase
from mountaineer.database import DatabaseDependencies

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from everest import models
from everest.core.exceptions import NotFoundException
from everest.core.layout import LayoutContext
from everest.core.tables import ALL_TABLES
from everest.core.types import GenericTableRowItem


class TableListRender(RenderBase):
    id: str
    layout: LayoutContext
    items: list[GenericTableRowItem] = []


class TableListController(ControllerBase):
    url = "/table/{table_id}/"
    view_path = "/app/table/list/page.tsx"

    def __init__(self):
        super().__init__()

    async def render(
            self,
            table_id: str,
            session: AsyncSession = Depends(DatabaseDependencies.get_db_session)
    ) -> TableListRender:
        layout = LayoutContext(tables=ALL_TABLES())
        table = layout.tables.get(table_id)
        model = getattr(models, table.table_schema.name, None)
        if not model:
            raise NotFoundException()
        items = await session.execute(select(model).order_by(*table.table_schema.default_sort_order))
        items = [dict(row) for row in items.scalars().all()]

        return TableListRender(
            id=table_id,
            layout=layout,
            items=items
        )
