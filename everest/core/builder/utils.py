import os
from pathlib import Path


def ensure_package_path(package, base_path=None):
    base_path = Path(base_path or "./")
    nested = package.split('.')[:-1]
    for idx, child in enumerate(nested):
        path = Path('/'.join(nested[:idx + 1]))
        os.makedirs(base_path / path, exist_ok=True)
        init = base_path / path / '__init__.py'
        if not os.path.exists(init):
            with open(init, 'w+') as fh:
                fh.write("")

    return base_path / '/'.join(nested)


def indent(lines, n=1):
    return [
        str(('    ' * n) + line) for line in lines
    ]
