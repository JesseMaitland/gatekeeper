from typing import Dict


class Model:
    pass


class Group(Model):

    #TODO: actually create the group implementation
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
