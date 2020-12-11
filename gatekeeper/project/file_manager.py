from hashlib import sha1
from pathlib import Path
from datetime import datetime
from typing import Generator, Dict, List

MESSAGE_TOKEN = '>>>>MESSAGE<<<<'
TIMESTAMP_TOKEN = '>>>>TIMESTAMP<<<<'

# Path to the cli environment config file
GATEKEEPER_CONFIG_PATH = Path.cwd().absolute() / '.gatekeeper'

# project root. this is where all of the gatekeeper output lives
PROJECT_ROOT = Path.cwd().absolute() / "redshift" / "gatekeeper"

# this file is rebuilt each time the stage command is run
STAGING_FILE_PATH = PROJECT_ROOT / 'staged.sql'

# root for the object store, where the state of the project is stored
OBJECT_STORE_ROOT = PROJECT_ROOT / '.gk'

# HEAD file path
HEAD_FILE_PATH = OBJECT_STORE_ROOT / 'HEAD.txt'

# index file path
INDEX_FILE_PATH = OBJECT_STORE_ROOT / 'INDEX.txt'

# history file
HISTORY_FILE_PATH = OBJECT_STORE_ROOT / 'HISTORY.txt'

# paths to be object store allow reference by name
OBJECT_STORE_PATHS = {
    'users': OBJECT_STORE_ROOT / 'users',
    'groups': OBJECT_STORE_ROOT / 'groups'
}

# mapping of project directories to be referenced by name
PROJECT_DIRECTORY_PATHS = {
    'configs': PROJECT_ROOT / 'configs',
    'rendered': PROJECT_ROOT / 'rendered',
    'commits': PROJECT_ROOT / 'commits'
}

# mapping of all the yaml config files used by gatekeeper to render sql templates
PROJECT_CONFIG_FILE_PATHS = {
    'groups': PROJECT_DIRECTORY_PATHS['configs'] / 'groups.yml',
    'users': PROJECT_DIRECTORY_PATHS['configs'] / 'users.yml',
    'roles': PROJECT_DIRECTORY_PATHS['configs'] / 'roles.yml'
}

# allowable types used by rendering functions
TYPES = ['users', 'groups']


def hash_file(path: Path, file_name: str = None) -> str:
    digest = sha1(path.read_text().encode()).hexdigest()

    if file_name:
        return f"{digest}-{file_name}"
    else:
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


def write_head_file(file_hash: str) -> None:
    HEAD_FILE_PATH.write_text(file_hash)


def read_head_file() -> str:
    return HEAD_FILE_PATH.read_text()


def rewind_head() -> str:
    index = INDEX_FILE_PATH.read_text().split()
    last_entry = index.pop(-1).split(' : ')[0]
    write_head_file(last_entry)
    INDEX_FILE_PATH.write_text('\n'.join(index))


def write_commit(content_path: Path, message: str) -> None:
    content_hash = hash_file(content_path, 'commit') + f" : {datetime.now().isoformat()}"
    commit = PROJECT_DIRECTORY_PATHS['commits'] / content_hash

    with commit.open(mode='w+') as file:
        file.write(message)
        file.write(f'\n\n{MESSAGE_TOKEN}')
        file.write('\n\n')
        file.write(content_path.read_text())


def update_index(file_hash: str) -> None:
    with INDEX_FILE_PATH.open(mode='a') as index:
        index.write(file_hash)
        index.write('\n')


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


def get_config_path(name: str) -> Path:
    return PROJECT_CONFIG_FILE_PATHS[name]


def get_project_path(name: str) -> Path:
    return PROJECT_DIRECTORY_PATHS[name]


#  TODO: refactor these into their own module
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


class StateStatus:

    def __init__(self, to_add: Dict[str, List], to_remove: Dict[str, List], to_update: Dict[str, List]) -> None:
        self._items = {
            'to_add': to_add,
            'to_remove': to_remove,
            'to_update': to_update
        }

    def __getitem__(self, item) -> Dict[str, List]:
        return self._items[item]

    @property
    def add(self) -> bool:
        return True if [v for v in self._items['to_add'].values()] else False

    @property
    def remove(self) -> bool:
        return True if [v for v in self._items['to_remove'].values()] else False

    @property
    def update(self) -> bool:
        return True if [v for v in self._items['to_update'].values()] else False

    def print_status(self):
        for key, value in self._items.items():
            print(f"{key} : {value}")


def generate_status() -> StateStatus:
    status = {
        'to_add': {'users': [], 'groups': [], 'ownership': []},
        'to_remove': {'users': [], 'groups': [], 'ownership': []},
        'to_update': {'users': [], 'groups': [], 'ownership': []}
    }

    for type_ in TYPES:
        for path in get_rendered_paths(type_):

            try:
                stored_path = fetch_from_object_store(path.name, type_)

            except FileNotFoundError:
                status['to_add'][type_].append(path)

            else:
                file_hash = hash_file(path)
                if file_hash != stored_path.name:
                    status['to_update'][type_].append(path)

        for path in get_object_store_paths(type_):

            try:
                _ = fetch_from_rendered(path.name.split('-')[-1], type_)

            except FileNotFoundError:
                status['to_remove'][type_].append(path.name.split('-')[-1].split('.')[0])

    return StateStatus(**status)
