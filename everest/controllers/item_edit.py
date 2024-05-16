from dateutil.parser import parse
from mountaineer import RenderBase, ControllerBase, sideeffect
from mountaineer.database import DatabaseDependencies

from fastapi import Depends
from sqlalchemy import DateTime
from sqlalchemy.ext.asyncio import AsyncSession

from everest.controllers.layout import AdminDependencies
from everest.core.tables import AdminTable
from everest.core.types import AdminTableItem, AdminTableRow


class ItemEdit(RenderBase):
    item: AdminTableItem
    table: AdminTable


class ItemEditController(ControllerBase):
    url = "/table/{table_id}/{item_id}/edit"
    view_path = "/app/table/edit/page.tsx"

    async def render(
            self,
            session: AsyncSession = Depends(DatabaseDependencies.get_db_session),
            item: AdminTableItem = Depends(AdminDependencies.require_item),
            table: AdminTable = Depends(AdminDependencies.require_table),
    ) -> ItemEdit:
        return ItemEdit(
            item=item,
            table=table,
        )

    #@sideeffect
    #async def partial_update(self, update: AdminTableRow,
                             #session: AsyncSession = Depends(DatabaseDependencies.get_db_session),
                             #) -> None:
        #layout = update.layout
        #for key, value in update.data.items():
            #column_type = layout.model.__table__.columns[key].type
            #if isinstance(column_type, DateTime):
                #value = parse(value)
            #setattr(layout.db_item, key, value)
        #session.add(layout.db_item)
        #await session.commit()
