from typing import List, Tuple, Type
from gatekeeper.project.models import (
    Model, User, Table
)


def map_results(columns: List[str], results: List[Tuple], type_: str) -> List[Type[Model]]:
    model = globals()[type_]
    return [model(**dict(zip(columns, result))) for result in results]
