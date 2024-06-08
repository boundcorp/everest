import os
from pathlib import Path
from typing import AnyStr

from pydantic import BaseModel

from everest.core.builder.utils import ensure_package_path, indent


class ClassBuilder(BaseModel):
    package: str
    name: str
    path: str
    base_classes: list[str]
    imports: dict[str, list[str]]
    typing_imports: dict[str, list[str]]
    partials: list[str]

    def save_to_disk(self):
        os.makedirs(self.path, exist_ok=True)
        with open(Path(self.path) / f'{self.name}.py', 'wb+') as fh:
            fh.writelines([(s + "\n").encode('utf-8') for s in self.class_template()])

    def register_import(self, i, typing=False):
        if '.' in i:
            parts = i.split('.')
            from_package, name = '.'.join(parts[:-1]), parts[-1]
        else:
            from_package, name = '.', i
        if not from_package:
            from_package = "."
        if from_package == "." and name in ["str", "int", "float", "bool", "Any"]:
            return name
        if typing:
            if from_package not in self.typing_imports:
                self.typing_imports[from_package] = []
            self.typing_imports[from_package] += [name]
        else:
            if from_package not in self.imports:
                self.imports[from_package] = []

            self.imports[from_package] += [name]
        return name

    def register_partial(self, p):
        name = p.split('.')[-1]
        parent = '.'.join(p.split('.')[:-1])
        ensure_package_path(parent)
        self.partials.append(name)

    def class_params(self):
        return [self.register_import(base) for base in self.base_classes]

    def class_template(self) -> list[AnyStr]:
        body = indent(self.class_body_lines() or ["pass"])
        typing_imports = [
            f"from {package} import {', '.join(set(names))}" for package, names in self.typing_imports.items()
        ]
        if typing_imports:
            self.register_import("typing.TYPE_CHECKING")
            typing_imports = [
                "if TYPE_CHECKING:",
                *indent(typing_imports),
            ]

        imports = [
            f"from {package} import {', '.join(set(names))}" for package, names in self.imports.items()
        ]
        return [
            *imports,
            *typing_imports,
            "", "",
            f"class {self.name}({', '.join(self.class_params())}):",
            *body,
            "",
        ]

    def class_body_lines(self):
        return ["pass"]
