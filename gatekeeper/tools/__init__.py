from itertools import groupby
from typing import Dict
from redscope.schema_introspection.db_objects import DbCatalog
from redscope.schema_introspection.db_objects.ownership import Ownership


def group_ownership(dbc: DbCatalog) -> Dict[str, Ownership]:
    # TODO: refactor this into dbCatalog
    ownership = dbc.ownership
    ownership.sort(key=lambda x: x.owner)

    groups = {}
    for key, group in groupby(ownership, lambda x: x.owner):
        g = list(group)
        g.sort(key=lambda x: x.db_obj_type)
        groups[key] = {}
        for k, v in groupby(g, lambda x: x.db_obj_type):
            groups[key][k] = list(v)

    return groups
