from dateutil.parser import parse
from mountaineer import RenderBase, ControllerBase, sideeffect
from mountaineer.database import DatabaseDependencies

from fastapi import Depends
from sqlalchemy import DateTime
from sqlalchemy.ext.asyncio import AsyncSession

from everest import models
from everest.controllers.app.layout import AdminDependencies
from everest.core.tables import AdminTable, ALL_TABLES
from everest.core.types import AdminTableItem, AdminTableRow


class ItemCreate(RenderBase):
    table: AdminTable


class ItemCreateController(ControllerBase):
    url = "/table/{table_id}/create"
    view_path = "/app/table/create/page.tsx"

    async def render(
            self,
            session: AsyncSession = Depends(DatabaseDependencies.get_db_session),
            table: AdminTable = Depends(AdminDependencies.require_table),
    ) -> ItemCreate:
        return ItemCreate(
            table=table,
        )

    @sideeffect
    async def create(self, create: AdminTableRow,
                     session: AsyncSession = Depends(DatabaseDependencies.get_db_session),
                     table: AdminTable = Depends(AdminDependencies.require_table),
                     ) -> None:
        model = getattr(models, table.name)
        for key, value in create.data.items():
            column_type = model.__table__.columns[key].type
            if isinstance(column_type, DateTime):
                create.data[key] = parse(value)
        new_item = model(**create.data)
        session.add(new_item)
        await session.commit()
