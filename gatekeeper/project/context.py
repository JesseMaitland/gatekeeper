import os
import shutil
import yaml
import psycopg2
from hashlib import sha1
from psycopg2.extensions import connection
from pathlib import Path
from typing import Dict, List, Tuple
from configparser import ConfigParser
from dotenv import load_dotenv
from jinja2 import PackageLoader, Environment
from .ymlobj import User, Role, Group


class GateKeeper:

    def __init__(self, users: Dict[str, User], roles: Dict[str, Role], groups: Dict[str, Group]) -> None:

        for role in roles.values():
            role.set_groups(groups)

        for user in users.values():
            user.set_roles(roles)

        self.access_configs = {
            'users': users,
            'roles': roles,
            'groups': groups
        }

    def get_user(self, name: str) -> User:
        return self.access_configs['users'][name]

    def get_users(self) -> List[User]:
        return list(self.access_configs['users'].values())


class GateKeeperProject:

    gatekeeper_config_file = Path.cwd().absolute() / '.gatekeeper'

    def __init__(self):

        self.root = Path.cwd().absolute() / "redshift" / "gatekeeper"

        self.dirs = {
            'configs': self.root / 'configs',
            'rendered': self.root / 'rendered',
            'object_store': self.root / '.gk1',
            'objects': self.root / '.gk1' / 'objects'
        }

        self.config_files = {
            'groups': self.dirs['configs'] / 'groups.yml',
            'users': self.dirs['configs'] / 'users.yml',
            'roles': self.dirs['configs'] / 'roles.yml'
        }

    def init(self):
        self.root.mkdir(exist_ok=True, parents=True)
        self.gatekeeper_config_file.touch(exist_ok=True)

        for v in self.dirs.values():
            v.mkdir(exist_ok=True, parents=True)

        for v in self.config_files.values():
            v.touch(exist_ok=True)

    def clean_dir(self, dir_name: str) -> None:
        d = self.dirs[dir_name]
        shutil.rmtree(d)
        d.mkdir(exist_ok=True, parents=True)

    def get_gatekeeper(self) -> GateKeeper:
        config = {}
        for config_name, config_path in self.config_files.items():
            c = yaml.load_all(config_path.open(), Loader=yaml.FullLoader)
            config[config_name] = {i.name: i for i in c}
        return GateKeeper(**config)

    def hash_file(self, file: os.DirEntry) -> str:
        with open(file.path) as data:
            obj_type = 'file'
            sha_hash = sha1(data.read()).digest()

    def hash_files(self) -> str:
        object_dir = self.dirs.get('objects')
        with os.scandir(self.dirs.get('rendered')) as it:

            for entry in it:


    def update_head(self, oid: str) -> None:
        pass


class GateKeeperEnvironment:

    def __init__(self):
        self.config = ConfigParser()
        self.config.read(GateKeeperProject.gatekeeper_config_file)

        try:
            load_dotenv(self.config['env']['file'])
        except KeyError:
            load_dotenv()

    @staticmethod
    def get_jinja_env() -> Environment:
        loader = PackageLoader(package_name='gatekeeper', package_path='templates')
        return Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)

    def redshift_connection(self) -> connection:
        connection_string = self.config['redshift']['connection']
        connection_string = os.getenv(connection_string, connection_string)
        return psycopg2.connect(connection_string)

    def execute_query(self, query: str, params: List = None, fetch: bool = True) -> Tuple:
        with self.redshift_connection() as conn:
            with conn.cursor() as cursor:
                result = None

                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                if fetch:
                    result = cursor.fetchall()

                conn.commit()
                return result
