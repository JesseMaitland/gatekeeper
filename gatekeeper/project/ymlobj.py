import yaml
from typing import List, Dict


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

    def __init__(self, name: str, password: str, roles: List[str], is_system_user: bool = False, owns_schemas: List[str] = None) -> None:
        self.name = name
        self.password = password
        self.roles = roles
        self._roles = {}
        self.is_system_user = is_system_user
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
