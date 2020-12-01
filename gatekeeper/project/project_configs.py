import yaml
from typing import List, Dict
from pathlib import Path


class Group(yaml.YAMLObject):

    yaml_tag = "!Group"

    def __init__(self, name: str, schemas: List[str], permissions: List[str]) -> None:
        self.name = name
        self.schemas = schemas
        self.permissions = permissions


class Role(yaml.YAMLObject):

    yaml_tag = "!Role"

    def __init__(self, name: str, groups: List[str]) -> None:
        self.name = name
        self.groups = groups
        self._groups = {}

    def set_groups(self, groups: Dict[str, Group]) -> None:
        self._groups = {}
        for group_name, group in groups.items():
            if group_name in self.groups:
                self._groups[group_name] = group

    def get_groups(self) -> Dict[str, Group]:
        return self._groups


class User(yaml.YAMLObject):

    yaml_tag = '!User'

    def __init__(self, name: str, roles: List[str], is_admin: bool = False, owns_schemas: List[str] = None) -> None:
        self.name = name
        self.roles = roles
        self._roles = {}
        self.is_admin = is_admin
        self.owns_schemas = owns_schemas or []

    def set_roles(self, roles: Dict[str, Role]) -> None:
        self._roles = {}
        for role_name, role in roles.items():
            if role_name in self.roles:
                self._roles[role_name] = role

    def get_roles(self) -> Dict[str, Role]:
        return self._roles

    @property
    def groups(self) -> List[Group]:
        groups = []
        for role in self._roles.values():
            for group in role.get_groups().values():
                groups.append(group)
        return list(set(groups))

    @property
    def owned_schemas(self) -> List[str]:
        return self.owns_schemas


class ConfigMapping:

    def __init__(self, users: Dict[str, User], roles: Dict[str, Role], groups: Dict[str, Group]) -> None:

        for role in roles.values():
            role.set_groups(groups)

        for user in users.values():
            user.set_roles(roles)

        self.objects = {
            'users': users,
            'roles': roles,
            'groups': groups
        }

    def to_render(self) -> Dict:
        return {key: value for key, value in self.objects.items() if key in ['users', 'groups']}

    @classmethod
    def from_config_paths(cls, config_paths: Dict[str, Path]) -> 'ConfigMapping':
        config = {}
        for config_name, config_path in config_paths.items():
            c = yaml.load_all(config_path.open(), Loader=yaml.FullLoader)
            config[config_name] = {i.name: i for i in c}
        return cls(**config)
