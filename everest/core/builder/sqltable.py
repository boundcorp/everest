from pydantic import BaseModel
from sqlmodel import SQLModel

from everest.core.builder.classbuilder import ClassBuilder
from everest.core.builder.utils import ensure_package_path

TABLE_PATH = 'everest/models/managed/'


class FieldBuilder(BaseModel):
    name: str
    type: str
    or_none: bool = False
    foreign_key: str | None = None
    primary_key: bool = False
    default_factory: str | None = None
    index: bool | None = False

class Relationship(BaseModel):
    name: str
    table: "SQLModelTableBuilder"
    reverse_name: str
    is_reverse: bool = False


class SQLModelTableBuilder(ClassBuilder):
    primary_key: str
    field_names: list[str]
    field_options: dict[str, FieldBuilder]
    relationships: dict[str, Relationship]

    @classmethod
    def create_single(cls, package, name=None, base_path=None, base_classes=None, pkey='id'):
        table = cls(
            package=package,
            name=name or package.split('.')[-1],
            path=str(ensure_package_path(package, base_path or TABLE_PATH)),
            base_classes=base_classes or ['object'],
            imports={},
            typing_imports={},
            partials=[],
            primary_key=pkey,
            field_names=[pkey],
            field_options={
                pkey: FieldBuilder(name=pkey, type='uuid.UUID', default_factory='uuid.uuid4', primary_key=True)},
            relationships={},
        )
        for base in base_classes:
            table.register_import(base)

        return table

    @property
    def primary_key_field(self):
        return self.field_options[self.primary_key]

    def add_field(self, name, type, default_factory=None, foreign_key=None, primary_key=False, index=False):
        self.field_names.append(name)
        self.field_options[name] = FieldBuilder(name=name, type=type, default_factory=default_factory, foreign_key=foreign_key, primary_key=primary_key, index=index)
        return self

    def add_relation(self, name, table, reverse_name, is_reverse=False):
        self.relationships[name] = Relationship(name=name, table=table, reverse_name=reverse_name, is_reverse=is_reverse)

    def add_foreign_key(self, name: str, table: "SQLModelTableBuilder", reverse_name: str):
        self.add_field(name + "_id", table.primary_key_field.type, foreign_key="%s.%s" %(table.name.lower(), table.primary_key), index=True)
        self.add_relation(name, table, reverse_name)
        table.add_relation(reverse_name, self, name)


    def class_params(self):
        return super().class_params() + ["table=True"]

    def class_body_lines(self):
        return [
            *self.class_field_lines(),
            *self.class_relationship_lines(),
        ]

    def class_field_lines(self):
        return [
            self.field_line(field) for field in self.field_names
        ]

    def class_relationship_lines(self):
        return [
            self.relationship_line(rel) for rel in self.relationships.values()
        ]

    def relationship_line(self, rel):
        if rel.table.package != self.package:
            self.register_import("." + rel.table.name, typing=True)
        self.register_import('sqlmodel.Relationship')

        if rel.is_reverse:
            return f"{rel.name}: List[\"{rel.table.name}\"] = Relationship(back_populates='{rel.reverse_name}')"

        return f"{rel.name}: \"{rel.table.name}\" = Relationship(back_populates='{rel.reverse_name}')"


    def field_line(self, field):
        options = self.field_options[field]
        self.register_import('mountaineer.database.sqlmodel.Field')
        _type = self.register_import(options.type)
        args = []
        if options.default_factory:
            args.append(f'default_factory={self.register_import(options.default_factory)}')
        if options.primary_key:
            args.append('primary_key=True')
        if options.foreign_key:
            args.append(f'foreign_key="{options.foreign_key}"')
        if options.index:
            args.append('index=True')

        return f"{field}: {_type} = Field({', '.join(args)})"
