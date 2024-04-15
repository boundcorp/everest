from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel
from mountaineer.database import DatabaseDependencies

from everest import models
from everest.core.auth.dependencies import AuthDependencies
from everest.core.tables import AdminTable, ALL_TABLES
from everest.core.types import AdminTableItem, AdminTableRow
from everest.models.detail import UserPublic


class LayoutContext(BaseModel):
    user: UserPublic | None
    table: AdminTable | None
    table_id: str | None
    item: AdminTableItem | None
    item_id: str | None
    tables: dict[str, AdminTable]

    @property
    def model(self) -> SQLModel | None:
        from everest import models
        return self.table and getattr(models, self.table.table_schema.name) or None

    @staticmethod
    async def get_layout(
            table_id: str | None = None,
            item_id: str | None = None,
            session: AsyncSession = Depends(DatabaseDependencies.get_db_session),
            user=Depends(AuthDependencies.lookup_user(models.User))
    ) -> ("LayoutContext", SQLModel | None):
        from everest.models.detail import UserPublic
        profile = user and user.dict() or None
        if profile:
            profile = UserPublic(id=str(profile.pop('id', '')), **profile)
        tables = ALL_TABLES()
        table = table_id and tables.get(table_id) or None
        model = table and getattr(models, table.table_schema.name)
        item = model and item_id and await table.get_row_by_id(session, item_id) or None

        return LayoutContext(tables=tables,
                             user=profile,
                             table_id=table_id,
                             item_id=item_id,
                             table=table,
                             item=item and dict(item) or None)
