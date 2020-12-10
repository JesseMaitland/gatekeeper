import yaml
from typing import Dict, List


class Model:

    def __init__(self, name: str) -> None:
        self._name = name

    @classmethod
    def from_yaml(cls, loader, node) -> 'Model':
        values = loader.construct_mapping(node, deep=True)
        return cls(**values)

    @classmethod
    def from_sql_result(cls, name: str) -> 'Model':
        raise NotImplementedError

    @property
    def name(self) -> str:
        return self._name

    @property
    def file_name(self) -> str:
        return f"{self._name}.sql"


class Group(Model):
    yaml_tag = '!Group'
    allowed_kinds = ['full', 'limited_read', 'limited_write']

    def __init__(self, name: str, schema: str, access: str, kind: str, names: List[str] = None) -> None:
        super(Group, self).__init__(name)
        self._schema = schema
        self._access = access
        self._kind = kind
        self._names = names or []
        self._validate_kind()
        self._validate_construction()

    def _validate_kind(self) -> None:
        if self.kind and self.kind not in self.allowed_kinds:
            raise ValueError(f"{self.kind} is not allowed, must specify any of {self.allowed_kinds}")

    def _validate_construction(self) -> None:
        if 'limited' in self._kind and not self._names:
            raise ValueError(f"{self._kind} was specified. A list of names for group {self.name} must be provided.")

    @classmethod
    def from_sql_result(cls, name: str) -> 'Model':
        return cls(name, "", "", "")

    @property
    def schema(self) -> str:
        return self._schema

    @property
    def access(self) -> str:
        return self._access

    @property
    def kind(self) -> str:
        return self._kind

    @property
    def names(self) -> List[str]:
        return self._names


class Role(Model):
    yaml_tag = '!Role'

    def __init__(self, name: str, group_names: List[str]) -> None:
        super(Role, self).__init__(name)
        self._group_names = group_names
        self._groups = []

    @property
    def groups(self) -> List[Group]:
        return self._groups

    @property
    def group_names(self) -> List[str]:
        return self._group_names

    def add_group(self, group: Group) -> None:
        self._groups.append(group)


class User(Model):
    yaml_tag = '!User'

    def __init__(self, name: str, role_names: List[str], is_admin: bool = False) -> None:
        super(User, self).__init__(name)
        self._is_admin = is_admin
        self._role_names = role_names or []
        self._roles = []

    @classmethod
    def from_sql_result(cls, name: str) -> 'User':
        return cls(name, role_names=[], is_admin=False)

    @property
    def is_admin(self) -> bool:
        return self._is_admin

    @property
    def role_names(self) -> List[str]:
        return self._role_names

    @property
    def roles(self) -> List[Role]:
        return self._roles

    @property
    def groups(self) -> List[Group]:
        return [group for role in self._roles for group in role.groups]

    def add_role(self, role: Role) -> None:
        self._roles.append(role)


class GateKeeper:

    def __init__(self, users: List[User], roles: List[Role], groups: List[Group] = None) -> None:

        # map roles
        for role in roles:
            for user in users:
                if role.name in user.role_names:
                    user.add_role(role)

        # map groups
        for group in groups:
            for role in roles:
                if group.name in role.group_names:
                    role.add_group(group)

        self._items = {
            'users': users,
            'roles': roles,
            'groups': groups
        }

    @staticmethod
    def register_yaml_constructors() -> None:
        yaml.SafeLoader.add_constructor('!User', User.from_yaml)
        yaml.SafeLoader.add_constructor('!Role', Role.from_yaml)
        yaml.SafeLoader.add_constructor('!Group', Group.from_yaml)

    def __getitem__(self, key) -> Dict:
        return self._items[key]

    @property
    def render_keys(self) -> List[str]:
        return ['users', 'groups']

    @property
    def users(self) -> Dict[str, User]:
        return self._items['users']

    @property
    def roles(self) -> Dict[str, Role]:
        return self._items['roles']

    @property
    def groups(self) -> Dict[str, Group]:
        return self._items['groups']

    def get_names(self, kind: str) -> List[str]:
        return [i.name for i in self._items[kind]]


class Schema(Model):

    def __init__(self, name: str) -> None:
        super(Schema, self).__init__(name)

    @classmethod
    def from_sql_result(cls, name: str) -> 'Model':
        return cls(name)


class Table(Model):

    def __init__(self, schema: str, name: str) -> None:
        super(Table, self).__init__(name)
        self._schema = schema

    @classmethod
    def from_sql_result(cls, schema: str, name: str) -> 'Model':
        return cls(schema, name)

    @property
    def schema(self) -> str:
        return self._schema

    @property
    def name(self) -> str:
        return self._name

    @property
    def qualified_name(self) -> str:
        return f"{self._schema}.{self._name}"
