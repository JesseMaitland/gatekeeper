from hashlib import sha1
from pathlib import Path
from typing import Generator
from gatekeeper.project.gatekeeper_config import (
    OBJECT_STORE_PATHS,
    PROJECT_DIRECTORY_PATHS
)


def hash_file(path: Path) -> str:
    digest = sha1(path.read_text().encode()).hexdigest()
    return f"{digest}-{path.name}"


def save_file_hash(path: Path, file_hash: str, type_: str) -> None:
    root = OBJECT_STORE_PATHS[type_] / file_hash
    root.touch(exist_ok=True)
    root.write_text(path.read_text())


def clear_object_store() -> None:
    for path in OBJECT_STORE_PATHS.values():
        for p in path.iterdir():
            if p.is_file():
                p.unlink(missing_ok=True)


def get_rendered_paths(type_: str) -> Generator[Path, None, None]:
    path = PROJECT_DIRECTORY_PATHS['rendered'] / type_
    for p in path.iterdir():
        if p.is_file():
            yield p


def populate_object_store(rebuild: bool = False) -> None:

    if rebuild:
        clear_object_store()

    types = ['users', 'groups']

    for type_ in types:
        for path in get_rendered_paths(type_):
            file_hash = hash_file(path)
            save_file_hash(path, file_hash, type_)
