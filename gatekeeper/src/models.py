import yaml
from typing import Dict, List
from gatekeeper.src.exceptions import ConfigurationError


"""
fetch config
-- query for tables, only when resource requires

"""


class Model:

    def __init__(self, name: str) -> None:
        self.name = name

    @classmethod
    def from_yaml(cls, loader, node) -> 'Model':
        values = loader.construct_mapping(node, deep=True)
        return cls(**values)

    @classmethod
    def from_sql_result(cls, name: str) -> 'Model':
        raise NotImplementedError

    @property
    def file_name(self) -> str:
        return f"{self.name}.sql"


class Schema(Model):

    def __init__(self, name: str) -> None:
        super(Schema, self).__init__(name)

    def __eq__(self, other):
        return self.name == other

    @classmethod
    def from_sql_result(cls, name: str) -> 'Model':
        return cls(name)


class Table(Model):

    def __init__(self, schema: str, name: str) -> None:
        super(Table, self).__init__(name)
        self.schema = schema

    def __eq__(self, other):
        return (self.schema == other.schema) and (self.name == other.name)

    @classmethod
    def from_sql_result(cls, schema: str, name: str) -> 'Model':
        return cls(schema, name)

    @property
    def qualified_name(self) -> str:
        return f"{self.schema}.{self.name}"


class Resource(Model):
    yaml_tag = "!Resource"

    def __init__(self, name: str,
                 schema: str,
                 tables: List[str] = None,
                 views: List[str] = None,
                 functions: List[str] = None,
                 procedures: List[str] = None,
                 filters: List[str] = None) -> None:

        super(Resource, self).__init__(name)
        self.schema = Schema(schema)
        self.tables = [Table(schema, t) for t in tables] or []

        self.views = views or []
        self.functions = functions or []
        self.procedures = procedures or []
        self.filters = filters or []

    def table_access(self) -> List[str]:
        if self.tables[0] == 'all':
            return [f"ON ALL TABLES IN SCHEMA {self.schema}"]
        return [f"ON {self.schema}.{t}" for t in self.tables]

    @classmethod
    def from_sql_result(cls, name: str) -> 'Model':
        pass


class Group(Model):
    yaml_tag = '!Group'

    def __init__(self, name: str, kind: str, creator: bool, super_group: bool = False, resources: List[Resource] = None,
                 database: str = None) -> None:
        super(Group, self).__init__(name)
        self.kind = kind
        self.creator = creator
        self.resources = resources or []
        self.super_group = super_group
        self.database = database or ''

        # make sure that the config is set up correctly
        self.validate_kind(kind)
        self.validate_creator(creator)
        self.validate_super_group(super_group)
        self.validate_database(database)
        self.validate_config()

    @classmethod
    def from_sql_result(cls, name: str) -> 'Model':
        pass

    @staticmethod
    def validate_kind(kind: str) -> None:
        allowed_kinds = ['reader', 'writer', 'reader_writer', 'full_access']
        if kind not in allowed_kinds:
            raise ConfigurationError(f"{kind} is not a valid config. allowed kinds are {allowed_kinds}")

    @staticmethod
    def validate_creator(creator: bool) -> None:
        # TODO: implement validate_creator
        pass

    @staticmethod
    def validate_super_group(super_group: bool) -> None:
        # TODO: implement validate_super_group
        pass

    @staticmethod
    def validate_database(database: str) -> None:
        # TODO: implement validate_database
        pass

    def schemas(self) -> List[str]:
        return [r.schema for r in self.resources]

    def tables(self) -> Dict[str, List[str]]:
        return {r.schema: t for r in self.resources for t in r.tables}

    def access(self) -> str:
        if self.kind == 'reader':
            return "SELECT"

        if self.kind == 'writer':
            return "INSERT UPDATE DELETE"

        if self.kind == 'reader_writer':
            return "SELECT INSERT UPDATE DELETE"

        if self.kind == 'full_access':
            return "ALL PRIVILEGES"

    def validate_config(self) -> None:
        # TODO: finish config validation
        if self.super_group and self.resources:
            raise ConfigurationError(
                f"group {self.name} must either be a super group, or have resources assigned, but not both")

        if self.creator and not self.database:
            raise ConfigurationError(
                f"group {self.name} has creator privileges, therefore the parameter 'database' must be provided.")


class User(Model):
    yaml_tag = '!User'

    def __init__(self, name: str, membership: List[str], superuser: bool = False) -> None:
        super(User, self).__init__(name)
        self.superuser = superuser
        self.membership = membership or []
        self.groups = []

    @classmethod
    def from_sql_result(cls, name: str) -> 'User':
        return cls(name, membership=[], superuser=False)

    def add_group(self, group: Group) -> None:
        self.groups.append(group)


class GateKeeper:

    def __init__(self, users: List[User], groups: List[Group] = None) -> None:

        # map roles
        for group in groups:
            for user in users:
                if group.name in user.membership:
                    user.add_group(group)

        self.groups = groups
        self.users = users

        self.validate_group_assignment()

    def __getitem__(self, item):
        allowed = ['users', 'groups']

        if item not in allowed:
            raise KeyError(f"{item} not allowed, only groups and users are subscriptable.")

        return self.__dict__[f"_{item}"]

    def validate_group_assignment(self):
        user_groups = list(set([m for u in self._users for m in u.membership]))
        diff = ', '.join(list(set(user_groups).difference(self.group_names())))
        if diff:
            raise ConfigurationError(f"{diff} is not configured in the group.yml config.")

    @staticmethod
    def register_yaml_constructors() -> None:
        yaml.SafeLoader.add_constructor('!User', User.from_yaml)
        yaml.SafeLoader.add_constructor('!Resource', Resource.from_yaml)
        yaml.SafeLoader.add_constructor('!Group', Group.from_yaml)

    def group_names(self) -> List[str]:
        return [g.name for g in self.groups]

    def user_names(self) -> List[str]:
        return [u.name for u in self.users]


