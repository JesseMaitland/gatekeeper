from typing import List, Any
from gatekeeper.project.helpers import format_model_name
from .executor import execute_query, execute_statement
from .mapper import map_results
from .queries import get_query


def fetch_and_map_query_result(connection_name: str, query_name: str) -> List[Any]:
    return map_results(
        *execute_query(
            connection_name,
            get_query(query_name)
        ),
        format_model_name(query_name)
    )
