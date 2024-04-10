import os
from pathlib import Path
from typing import AnyStr

from pydantic import BaseModel

from everest.core.builder.utils import ensure_package_path, indent

TABLE_PATH = 'everest/models/managed/'

class FieldBuilder(BaseModel):
    name: str
    type: str
    default_factory: str | None

class TableBuilder(BaseModel):
    package: str
    name: str
    path: str
    base_classes: list[str]
    imports: dict[str, list[str]]
    partials: list[str]
    primary_key: str
    field_names: list[str]
    field_options: dict[str, FieldBuilder]

    @classmethod
    def create(cls, package, name=None, base_path=None, base_classes=None):
        pkey = 'id'
        return cls(
            package=package,
            name=name or package.split('.')[-1],
            path=str(ensure_package_path(package, base_path or TABLE_PATH)),
            base_classes=base_classes or ['object'],
            imports={},
            partials=[],
            primary_key=pkey,
            field_names=[pkey],
            field_options={pkey: FieldBuilder(name=pkey, type='uuid.UUID', default_factory='uuid.uuid4')}
        )

    def save_to_disk(self):
        os.makedirs(self.path, exist_ok=True)
        with open(Path(self.path) / f'{self.name}.py', 'wb+') as fh:
            fh.writelines([(s + "\n").encode('utf-8') for s in self.class_template()])

    def register_import(self, i):
        if '.' in i:
            parts = i.split('.')
            from_package, name = '.'.join(parts[:-1]), parts[-1]
        else:
            from_package, name = '.', i
        if from_package not in self.imports:
            self.imports[from_package] = []

        self.imports[from_package] += [name]
        return name

    def register_partial(self, p):
        name = p.split('.')[-1]
        parent = '.'.join(p.split('.')[:-1])
        ensure_package_path(parent)
        self.partials.append(name)

    def class_template(self) -> list[AnyStr]:
        body = indent(self.class_body_lines() or ["pass"])
        base_classes = ', '.join(self.register_import(base) for base in self.base_classes)
        imports = [
            f"from {package} import {', '.join(set(names))}" for package, names in self.imports.items()
        ]
        return [
            *imports,
            "",
            "",
            f"class {self.name}({base_classes}, table=True):", *body,
            "",
        ]

    def class_body_lines(self):
        return [
            *self.class_field_lines()
        ]

    def class_field_lines(self):
        return [
            self.field_line(field) for field in self.field_names
        ]

    def field_line(self, field):
        options = self.field_options[field]
        self.register_import('mountaineer.database.sqlmodel.Field')
        _type = self.register_import(options.type)
        args = []
        if options.default_factory:
            args.append(f'default_factory={self.register_import(options.default_factory)}')
        if field == self.primary_key:
            args.append('primary_key=True')

        return f"{field}: {_type} = Field({', '.join(args)})"
