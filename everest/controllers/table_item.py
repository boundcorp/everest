from datetime import datetime
from uuid import UUID

from mountaineer import RenderBase, ControllerBase, APIException, sideeffect
from mountaineer.database import DatabaseDependencies

from fastapi import Depends
from sqlalchemy import select, String, cast, Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel

from everest import models
from everest.core.auth.dependencies import AuthDependencies
from everest.core.layout import LayoutContext
from everest.core.tables import ALL_TABLES
from everest.core.types import AdminTableItem, AdminTableRow


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

    @sideeffect
    async def partial_update(self, update: AdminTableRow,
                             session: AsyncSession = Depends(DatabaseDependencies.get_db_session),
                             layout: LayoutContext = Depends(LayoutContext.get_layout)
                             ) -> None:
        if not layout.item:
            raise NotFoundException
        existing = await session.execute(select(layout.table.table_model).where(layout.table.table_model.id == layout.item_id))
        existing = existing.scalars().one()
        for key, value in update.data.items():
            setattr(existing, key, value)
        session.add(existing)
        await session.commit()
