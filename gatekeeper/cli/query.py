from argparse import Namespace
from gatekeeper.project.database.executor import execute_query
from gatekeeper.project.database.queries import get_query
from gatekeeper.project.database.mapper import map_results
from gatekeeper.project.environment import load_gatekeeper_env, get_gatekeeper_config
from gatekeeper.project.database import fetch_and_map_query_result


def query(cmd: Namespace) -> None:
    config = get_gatekeeper_config()
    load_gatekeeper_env(config)

    conn = config['redshift']['connection']
    result = fetch_and_map_query_result(conn, cmd.query)

    print(result)
