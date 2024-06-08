from typing import Optional, List, Any

import sqlalchemy
from mountaineer import RenderBase, ControllerBase
from mountaineer.database import DatabaseDependencies

from fastapi import Depends, Query
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from everest.controllers.app.layout import AdminDependencies
from everest.core.tables import AdminTable, TableView
from everest.core.types import AdminTableItem


class TablePagination(BaseModel):
    page: int
    page_size: int
    total_items: int


class TableListRender(RenderBase):
    table: AdminTable
    current_view: str
    items: list[AdminTableItem] = []
    pagination: TablePagination


async def paginate_table(
        session: AsyncSession,
        table: AdminTable,
        page: int = Query(1, alias="page", ge=1),
        cursor: Optional[Any] = Query(None, alias="cursor"),
        page_size: int = Query(10, alias="pageSize", ge=1, le=100),
        sort_by: Optional[List[str]] = Query(None, alias="sortBy"),
        sort_order: Optional[List[str]] = Query(None, alias="sortOrder")
):
    # Calculate the offset for pagination
    offset = (page - 1) * page_size

    # Handle custom sorting
    if sort_by and sort_order:
        order_by_clauses = []
        for field, order in zip(sort_by, sort_order):
            column = getattr(table.db_model, field)
            if order.lower() == "desc":
                column = column.desc()
            order_by_clauses.append(column)
    else:
        order_by_clauses = table.table_schema.default_sort_order

    primary_key_column = table.db_model.__table__.primary_key.columns.values()[0]
    if cursor:
        # Add primary key to order by clauses if not already included
        if primary_key_column not in order_by_clauses:
            order_by_clauses.append(primary_key_column)

        # If cursor is provided, add a filter to start after the cursor
        query = select(table.db_model).filter(primary_key_column > cursor).order_by(*order_by_clauses).limit(
            page_size)
    elif page:
        # Execute the query with pagination and sorting
        query = select(table.db_model).order_by(*order_by_clauses).offset(offset).limit(page_size)
    result = await session.execute(query)
    items = [dict(row) for row in result.scalars().all()]

    if items:
        next_cursor = items[-1][primary_key_column.name]
    else:
        next_cursor = None

    total_items_query = select(func.count()).select_from(table.db_model)
    total_items_result = await session.execute(total_items_query)
    total_items = total_items_result.scalar_one()

    return TableListRender(
        table=table,
        current_view="default",
        items=items,
        pagination=TablePagination(page=page, page_size=page_size, total_items=total_items, next_cursor=next_cursor)
    )


class TableListController(ControllerBase):
    url = "/table/{table_id}/"
    view_path = "/app/table/list/page.tsx"

    def __init__(self):
        super().__init__()

    async def render(
            self,
            table: AdminTable = Depends(AdminDependencies.require_table),
            session: AsyncSession = Depends(DatabaseDependencies.get_db_session),
            page: int = Query(1, alias="page", ge=1),
            cursor: Optional[Any] = Query(None, alias="cursor"),
            page_size: int = Query(10, alias="pageSize", ge=1, le=100),
            sort_by: Optional[List[str]] = Query(None, alias="sortBy"),
            sort_order: Optional[List[str]] = Query(None, alias="sortOrder"),
            view: TableView = Depends(AdminDependencies.require_table_view),
    ) -> TableListRender:

        return await paginate_table(session, table, page=page, cursor=cursor, page_size=page_size, sort_by=sort_by,
                                    sort_order=sort_order)
