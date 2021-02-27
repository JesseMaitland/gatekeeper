from argparse import Namespace
from configparser import ConfigParser
from gatekeeper.src.environment import gatekeeper_env
from gatekeeper.src.database import fetch_and_map_query_result


@gatekeeper_env(provide_config=True)
def query(cmd: Namespace, config: ConfigParser) -> None:

    conn = config['redshift']['connection']
    result = fetch_and_map_query_result(conn, cmd.query)

    print(result)
