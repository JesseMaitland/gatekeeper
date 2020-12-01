from hashlib import sha1
from pathlib import Path
from typing import Generator, Dict
from gatekeeper.project.gatekeeper_config import (
    STAGING_FILE_PATH,
    OBJECT_STORE_PATHS,
    PROJECT_DIRECTORY_PATHS
)

TYPES = ['users', 'groups']


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
                p.unlink()


def get_rendered_paths(type_: str) -> Generator[Path, None, None]:
    path = PROJECT_DIRECTORY_PATHS['rendered'] / type_
    for p in path.iterdir():
        if p.is_file():
            yield p


def get_object_store_paths(type_: str) -> Generator[Path, None, None]:
    path = OBJECT_STORE_PATHS[type_]
    for p in path.iterdir():
        if p.is_file():
            yield p


def fetch_from_object_store(name: str, type_: str) -> Path:
    path = OBJECT_STORE_PATHS[type_]
    for p in path.iterdir():
        if p.is_file():
            if p.name.split('-')[-1] == name:
                return p
    else:
        raise FileNotFoundError(f"no object with type {type_} and name {name} exists in the object store")


def fetch_from_rendered(name: str, type_: str):
    path = PROJECT_DIRECTORY_PATHS['rendered'] / type_
    for p in path.iterdir():
        if p.is_file():
            if p.name == name:
                return p
    else:
        raise FileNotFoundError(f"no rendered file found with type {type_} and name {name} in the rendered store")


#########################################################
#               HIGHER LEVEL FUNCTIONS                  #
#########################################################


def populate_object_store(rebuild: bool = False) -> None:
    if rebuild:
        clear_object_store()

    for type_ in TYPES:
        for path in get_rendered_paths(type_):
            file_hash = hash_file(path)
            save_file_hash(path, file_hash, type_)


def generate_status() -> dict:

    status = {
        'to_add': [],
        'to_remove': [],
        'to_update': []
    }

    for type_ in TYPES:
        for path in get_rendered_paths(type_):

            try:
                stored_path = fetch_from_object_store(path.name, type_)

            except FileNotFoundError:
                status['to_add'].append(path)

            else:
                file_hash = hash_file(path)
                if file_hash != stored_path.name:
                    status['to_update'].append(path)

        for path in get_object_store_paths(type_):

            try:
                _ = fetch_from_rendered(path.name.split('-')[-1], type_)

            except FileNotFoundError:
                status['to_remove'].append(path)

    return status
