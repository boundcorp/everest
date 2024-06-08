from typing import List

import sqlalchemy
from pydantic import BaseModel
from sqlalchemy import Row, select, cast, String
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from everest import models
from everest.core.utils import to_snake_case
from enum import Enum

from everest.models.tasks import ModelChoices


class PropertyChoice(BaseModel):
    value: str
    label: str
    color: str | None = None


class PropertySchema(BaseModel):
    type: str | None = None
    field_type: str | None = None
    format: str | None = None
    anyOf: list[dict[str, str]] | None = None
    title: str | None = None
    default: str | int | None = None
    choices: list[PropertyChoice] | None = None

    @classmethod
    def from_model(cls, name: str, data: dict, model: BaseModel):
        # If the schema has an anyOf, we want to use the first type as the type
        if data.get("anyOf") and not data.get("type"):
            data["type"] = data["anyOf"][0]["type"]
            if not data.get("format"):
                data["format"] = data["anyOf"][0].get("format")

        # If the type is a date-time, we want to convert it to a datetime
        if data.get("type") == "string" and data.get("format") == "date-time":
            data["type"] = "datetime"

        field_info = model.model_fields.get(name)

        if field_info and isinstance(field_info.annotation, type):
            if issubclass(field_info.annotation, str) and issubclass(field_info.annotation, Enum):
                data["type"] = "string"
                data["field_type"] = "enum"
                data["choices"] = [
                    PropertyChoice(value=e.value, label=getattr(e, 'label', e.name), color=getattr(e, 'color', None))
                    for e in field_info.annotation.__members__.values()]
        return cls.parse_obj(data)


class TableSchema(BaseModel):
    id: str
    name: str
    properties: dict[str, PropertySchema]
    required: list[str]
    package: str
    app_label: str
    title: str
    type: str

    @property
    def view_columns(self):
        return self.properties.keys()

    @property
    def default_view_columns(self):
        return [p for p in self.view_columns if not p.startswith("_")]

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
    columns: list[str]


def get_app_label(model: BaseModel):
    app_label = package = model.__module__
    if hasattr(model, "app_label"):
        app_label = model.app_label
    else:
        if package.endswith(".models"):
            app_label = package[:-7]
        if "models." in app_label:
            app_label = app_label.split("models.")[1]
        app_label = ".".join(app_label.split(".")[-2:])
    return package, app_label


class AdminTable(BaseModel):
    name: str
    table_schema: TableSchema
    views: List[TableView] = []

    @classmethod
    def from_model(cls, model: BaseModel) -> "AdminTable":
        js_schema = model.model_json_schema()
        package, app_label = get_app_label(model)
        properties = {
            k: PropertySchema.from_model(k, v, model) for k, v in js_schema["properties"].items()
        }
        schema = TableSchema(
            properties=properties,
            required=js_schema.get('required', []),
            title=js_schema["title"],
            type=js_schema["type"],
            id=to_snake_case(model.__name__),
            package=package,
            app_label=app_label,
            name=model.__name__,
        )
        return cls(
            name=model.__name__,
            table_schema=schema,
            views=[TableView(columns=schema.default_view_columns)]
        )

    @property
    def db_model(self):
        return getattr(models, self.table_schema.name)

    async def get_row_by_id(self, session: AsyncSession, item_id: str) -> Row:
        result = await session.execute(select(self.db_model).where(cast(self.db_model.id, String) == item_id))
        return result.scalars().one()

    async def get_view(self, session: AsyncSession, stub: str = "default") -> TableView:
        from everest.models.managed.admin import TableView
        existing = await session.execute(
            select(TableView).filter(TableView.table == self.name, TableView.stub == stub))
        try:
            return existing.scalars().one()
        except sqlalchemy.exc.NoResultFound:
            if stub == "default":
                view = TableView(table=self.name, stub="default", description="Default view")
                session.add(view)
                await session.commit()
                return view


def ALL_TABLES():
    return {model.table_schema.id: model for model in
            [AdminTable.from_model(cls) for cls in models.__dict__.values() if hasattr(cls, "model_json_schema")]}
