import shutil
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from jinja2 import PackageLoader, Environment

from .ymlobj import User, Role, Group


class GateKeeper:

    def __init__(self, users: Dict[str, User], roles: Dict[str, Role], groups: Dict[str, Group]) -> None:

        for role in roles.values():
            role.set_groups(groups)

        for user in users.values():
            user.set_roles(roles)

        self.items = {
            'users': users,
            'roles': roles,
            'groups': groups
        }

    def get_user(self, name: str) -> User:
        return self.items['users'][name]

    def get_users(self) -> List[User]:
        return list(self.items['users'].values())


class ProjectContext:

    def __init__(self):

        root = Path.cwd().absolute() / "gate-keeper"
        configs = root / "configs"
        ddl = root / "ddl"
        migrations = root / "migrations"
        users = ddl / "users"
        groups = ddl / "groups"

        self.dirs = {
            'root': root,
            'configs': configs,
            'ddl': ddl,
            'users': users,
            'groups': groups,
            'migrations': migrations
        }

        self.config_files = {
            'groups': configs / 'groups.yml',
            'users': configs / 'users.yml',
            'roles': configs / 'roles.yml'
        }

    def init(self):

        for v in self.dirs.values():
            v.mkdir(exist_ok=True, parents=True)

        for v in self.config_files.values():
            v.touch(exist_ok=True)

    def clean_dir(self, dir_name: str) -> None:
        d = self.dirs[dir_name]
        shutil.rmtree(d)
        d.mkdir(exist_ok=True, parents=True)

    @staticmethod
    def get_jinja_env() -> Environment:
        loader = PackageLoader(package_name='gatekeeper', package_path='templates')
        return Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)

    def get_config(self) -> GateKeeper:
        config = {}
        for config_name, config_path in self.config_files.items():
            c = yaml.load_all(config_path.open(), Loader=yaml.FullLoader)
            config[config_name] = {i.name: i for i in c}
        return GateKeeper(**config)

    @staticmethod
    def get_permission_diff_file_name() -> str:
        return f"perm-{str(int(datetime.now().timestamp()))}.sql"


def provide_project_context(func):
    def wrapper(*args, **kwargs):
        pc = ProjectContext()
        return func(pc=pc, *args, **kwargs)
    return wrapper
