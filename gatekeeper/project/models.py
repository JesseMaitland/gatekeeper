from typing import Dict, List


class Model:

    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def file_name(self) -> str:
        return f"{self._name}.sql"


class Group(Model):

    # TODO: actually create the group implementation
    def __init__(self, name: str, **kwargs) -> None:
        super(Group, self).__init__(name)


class Role(Model):

    def __init__(self, name: str, groups: List[str]) -> None:
        super(Role, self).__init__(name)
        self._group_keys = groups
        self._groups = []

    @property
    def groups(self) -> List[Group]:
        return self._groups

    def set_groups(self, groups: Dict[str, Group]) -> None:
        self._groups = [value for key, value in groups.items() if key in self._group_keys]


class User(Model):

    def __init__(self, name: str, is_admin: bool = False, roles: List[str] = None) -> None:
        super(User, self).__init__(name)
        self._is_admin = is_admin
        self._role_keys = roles or []
        self._roles = []

    @property
    def is_admin(self) -> bool:
        return self._is_admin

    @property
    def roles(self) -> List[Role]:
        return self._roles

    @property
    def groups(self) -> List[Group]:
        return [group for role in self._roles for group in role.groups]

    def set_roles(self, roles: Dict[str, Role]) -> None:
        self._roles = [value for key, value in roles.items() if key in self._role_keys]


class GateKeeper:

    def __init__(self, users: Dict[str, User], roles: Dict[str, Role], groups: Dict[str, Group]) -> None:

        for role in roles.values():
            role.set_groups(groups)

        for user in users.values():
            user.set_roles(roles)

        self._items = {
            'users': users,
            'roles': roles,
            'groups': groups
        }

    def __getitem__(self, key) -> Dict:
        return self._items[key]

    @property
    def users(self) -> Dict[str, User]:
        return self._items['users']

    @property
    def roles(self) -> Dict[str, Role]:
        return self._items['roles']

    @property
    def groups(self) -> Dict[str, Group]:
        return self._items['groups']

    @property
    def render_keys(self) -> List[str]:
        return ['users', 'groups']

    def get_users(self, *names) -> Dict[str, User]:
        return {name: self._items['users'][name] for name in names if name in self._items['users'].keys()}

    def get_roles(self, *roles) -> Dict[str, Role]:
        return {role: self._items['roles'] for role in roles if role in self._items['roles'].keys()}

    def get_groups(self, *groups) -> Dict[str, Group]:
        return {group: self._items['groups'][group] for group in groups if group in self._items['groups'].keys()}

    def get_associated_user(self, name: str) -> Dict:
        user = self._items['users'][name]
        roles = [self._items['roles'][role] for role in user.roles if role in self._items['roles'].keys()]
        groups = [self._items['groups'][group] for role in roles for group in role.groups if group in self._items['groups'].keys()]
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
