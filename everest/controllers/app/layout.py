from fastapi import Depends, Request
from mountaineer import APIException, LayoutControllerBase, RenderBase
from sqlalchemy import Row
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel
from mountaineer.database import DatabaseDependencies

import everest.models.auth
from everest import models
from everest.core.auth.dependencies import AuthDependencies
from everest.core.tables import AdminTable, ALL_TABLES
from everest.core.types import AdminTableItem
from everest.models.auth import UserPublic


class NotFoundException(APIException):
    status_code = 404
    detail = "Detail item not found"


class AdminLayout(RenderBase):
    user: UserPublic | None = None
    item: AdminTableItem | None = None
    table: AdminTable | None = None
    tables: dict[str, AdminTable]
    table_id: str | None = None
    item_id: str | None = None
    sidebar_open: bool = True

    @property
    def model(self) -> SQLModel | None:
        from everest import models
        return self.table and getattr(models, self.table.table_schema.name) or None

    @property
    def db_item(self) -> Row | None:
        return getattr(self, '_db_item', None)


class AdminLayoutController(LayoutControllerBase):
    view_path = "/app/layout.tsx"

    async def render(self,
                     request: Request,
                     session: AsyncSession = Depends(DatabaseDependencies.get_db_session),
                     user=Depends(AuthDependencies.require_admin(everest.models.auth.User)),
                     table_id: str | None = None,
                     item_id: str | None = None,
                     ) -> AdminLayout:
        from everest.models.auth import UserPublic
        profile = user and user.dict() or None
        if profile:
            profile = UserPublic(id=str(profile.pop('id', '')), **profile)
        tables = ALL_TABLES()
        table = table_id and tables.get(table_id) or None
        model = table and getattr(models, table.table_schema.name)
        item = model and item_id and await table.get_row_by_id(session, item_id) or None
        layout = AdminLayout(tables=tables,
                             user=profile,
                             table_id=table_id,
                             item_id=item_id,
                             table=table,
                             item=item and dict(item) or None,
                             sidebar_open=request.cookies.get('sidebarOpen', 'true') == 'true',
                             )
        setattr(layout, '_db_item', item)
        return layout


class AdminDependencies:
    @staticmethod
    def get_table(table_id: str | None = None):
        if not table_id:
            return None
        tables = ALL_TABLES()
        return tables.get(table_id)

    @staticmethod
    def require_table(table_id: str | None = None):
        table = AdminDependencies.get_table(table_id)
        if not table:
            raise NotFoundException
        return table

    @staticmethod
    async def get_row(table_id: str | None = None, item_id: str | None = None,
                      session: AsyncSession = Depends(DatabaseDependencies.get_db_session)):
        table = AdminDependencies.get_table(table_id)
        if not table or not item_id:
            return None
        try:
            return await table.get_row_by_id(session, item_id)
        except NoResultFound:
            return None

    @staticmethod
    async def get_item(table_id: str | None = None, item_id: str | None = None,
                       session: AsyncSession = Depends(DatabaseDependencies.get_db_session)):
        row = await AdminDependencies.get_row(table_id, item_id, session)
        return row and dict(row) or None

    @staticmethod
    async def require_item(table_id: str | None = None, item_id: str | None = None,
                           session: AsyncSession = Depends(DatabaseDependencies.get_db_session)):
        item = await AdminDependencies.get_item(table_id, item_id, session)
        if not item:
            raise NotFoundException
        return item

    @staticmethod
    async def require_table_view(table_id: str | None = None,
                                 view: str = "default",
                                 session: AsyncSession = Depends(DatabaseDependencies.get_db_session)):
        table = AdminDependencies.get_table(table_id)
        if not table:
            raise NotFoundException
        view = await table.get_view(session, view) or table.get_view(session, "default")
        if not view:
            raise NotFoundException
        return view
