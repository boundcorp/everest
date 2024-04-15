from typing import List

from pydantic import BaseModel
from sqlalchemy import Row, select, cast, String
from sqlalchemy.ext.asyncio import AsyncSession

from everest import models
from everest.core.utils import to_snake_case


class PropertySchema(BaseModel):
    type: str | None = None
    anyOf: list[dict[str, str]] | None = None
    title: str | None = None
    default: str | int | None = None


class TableSchema(BaseModel):
    id: str
    name: str
    properties: dict[str, PropertySchema]
    required: list[str]
    title: str
    type: str

    @property
    def view_columns(self):
        return self.properties.keys()

    @property
    def default_view_columns(self):
        return [p for p in self.view_columns if p != "id" and not p.startswith("_")]

    @property
    def model(self):
        return getattr(models, self.name)

    @property
    def default_sort_order(self):
        return [self.model.id.desc(), ]


class TableViewColumnDefinition(BaseModel):
    source: str
    title: str | None = None
    hidden: bool = False


class TableView(BaseModel):
    columns: list[str | TableViewColumnDefinition] | None = None


class AdminTable(BaseModel):
    table_schema: TableSchema
    views: List[TableView] = []

    @classmethod
    def from_model(cls, model: type) -> "AdminTable":
        js_schema = model.model_json_schema()
        schema = TableSchema(
            properties=js_schema["properties"],
            required=js_schema.get('required', []),
            title=js_schema["title"],
            type=js_schema["type"],
            id=to_snake_case(model.__name__),
            name=model.__name__,
        )
        return cls(
            table_schema=schema,
            views=[TableView(columns=schema.default_view_columns)]
        )

    @property
    def table_model(self):
        return getattr(models, self.table_schema.name)

    async def get_row_by_id(self, session: AsyncSession, item_id: str) -> Row:
        result = await session.execute(select(self.table_model).where(cast(self.table_model.id, String) == item_id))
        return result.scalars().one()


def ALL_TABLES():
    return {model.table_schema.id: model for model in
            [AdminTable.from_model(cls) for cls in models.__dict__.values() if hasattr(cls, "model_json_schema")]}
