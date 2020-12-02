
class Model:
    pass


class User(Model):

    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name


class Table(Model):

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
