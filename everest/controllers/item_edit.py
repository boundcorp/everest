from datetime import datetime

from dateutil.parser import parse
from mountaineer import RenderBase, ControllerBase, sideeffect
from mountaineer.database import DatabaseDependencies

from fastapi import Depends
from sqlalchemy import DateTime
from sqlalchemy.ext.asyncio import AsyncSession

from everest.core.layout import LayoutContext
from everest.core.types import AdminTableItem, AdminTableRow


class ItemEdit(RenderBase):
    id: str
    layout: LayoutContext
    item: AdminTableItem


class ItemEditController(ControllerBase):
    url = "/table/{table_id}/{item_id}/edit"
    view_path = "/app/table/edit/page.tsx"

    async def render(
            self,
            session: AsyncSession = Depends(DatabaseDependencies.get_db_session),
            layout: LayoutContext = Depends(LayoutContext.get_layout),
    ) -> ItemEdit:
        return ItemEdit(
            id=layout.item_id,
            layout=layout,
            item=layout.item,
        )

    @sideeffect
    async def partial_update(self, update: AdminTableRow,
                             session: AsyncSession = Depends(DatabaseDependencies.get_db_session),
                             layout: LayoutContext = Depends(LayoutContext.get_item_layout)
                             ) -> None:
        for key, value in update.data.items():
            column_type = layout.model.__table__.columns[key].type
            if isinstance(column_type, DateTime):
                value = parse(value)
            setattr(layout.db_item, key, value)
        session.add(layout.db_item)
        await session.commit()
