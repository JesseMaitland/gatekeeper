import shutil
import yaml
from pathlib import Path
from typing import Dict, List
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
        return self.access['users'][name]

    def get_users(self) -> List[User]:
        return list(self.access['users'].values())


class GateKeeperProject:

    gatekeeper_config_file = Path.cwd().absolute() / '.gatekeeper'

    def __init__(self):

        self.root = Path.cwd().absolute() / "redshift" / "gatekeeper"

        self.dirs = {
            'configs': self.root / 'configs',
            'rendered': self.root / 'rendered'
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


class GateKeeperEnvironment:

    def __init__(self):
        self.config = ConfigParser()
        self.config.read(GateKeeperProject.gatekeeper_config_file.open())

        try:
            load_dotenv(self.config['env']['file'])
        except KeyError:
            load_dotenv()

    @staticmethod
    def get_jinja_env() -> Environment:
        loader = PackageLoader(package_name='gatekeeper', package_path='templates')
        return Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
