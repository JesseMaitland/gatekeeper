from typing import Dict, List


class Model:
    pass


class Group(Model):

    # TODO: actually create the group implementation
    def __init__(self, **kwargs) -> None:
        self.kwargs = kwargs


class Role(Model):

    def __init__(self, name: str, groups: Dict[str, Group]) -> None:
        self._name = name
        self._groups = groups

    @property
    def name(self) -> str:
        return self._name

    @property
    def groups(self) -> Dict[str, Group]:
        return self._groups


class User(Model):

    def __init__(self, name: str, is_admin: bool = False, roles: Dict[str, Role] = None) -> None:
        self._name = name
        self._is_admin = is_admin
        self._roles = roles or {}

    @property
    def name(self) -> str:
        return self._name

    @property
    def is_admin(self) -> bool:
        return self._is_admin

    @property
    def roles(self) -> Dict[str, Role]:
        return self._roles


class GateKeeper:

    def __init__(self, users: Dict[str, User], roles: Dict[str, Role], groups: Dict[str, Group]) -> None:
        self._users = users
        self._roles = roles
        self._groups = groups

    @property
    def users(self) -> Dict[str, User]:
        return self._users

    @property
    def roles(self) -> Dict[str, Role]:
        return self._roles

    @property
    def groups(self) -> Dict[str, Group]:
        return self._groups

    def get_users(self, *names) -> Dict[str, User]:
        return {name: self._users[name] for name in names if name in self._users.keys()}

    def get_roles(self, *roles) -> Dict[str, Role]:
        return {role: self._roles[role] for role in roles if role in self._roles.keys()}

    def get_groups(self, *groups) -> Dict[str, Group]:
        return {group: self._groups[group] for group in groups if group in self._groups.keys()}

    def get_associated_user(self, name: str) -> Dict:
        user = self._users[name]
        roles = [self._roles[role] for role in user.roles if role in self._roles.keys()]
        groups = [self.groups[group] for role in roles for group in role.groups if group in self._groups.keys()]
        return {
            'user': user,
            'roles': roles,
            'groups': groups
        }


class Table:

    def __init__(self, schema: str, name: str) -> None:
        self._schema = schema
        self._name = name

    @property
    def schema(self) -> str:
        return self._schema

    @property
    def name(self) -> str:
        return self._name

    @property
    def qualified_name(self) -> str:
        return f"{self._schema}.{self._name}"
