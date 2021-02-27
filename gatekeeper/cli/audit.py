from argparse import Namespace
from gatekeeper.src.environment import gatekeeper_env
from gatekeeper.src.configparsing import create_gatekeeper
from gatekeeper.src.database.queries import SqlManager
from gatekeeper.src.database.executor import execute_query
from gatekeeper.src.database.mapper import map_results
from gatekeeper.src.helpers import format_model_name
from gatekeeper.src.audits import Audit


@gatekeeper_env()
def audit(cmd: Namespace) -> None:

    # a gatekeeper will be used for the audit
    gatekeeper = create_gatekeeper()

    # get a query manager
    sql_manager = SqlManager()

    # run query against db to get the object we are doing the audit on
    query = sql_manager.get_query(cmd.kind)
    results = map_results(*execute_query('REDSHIFT', query), format_model_name(cmd.kind))

    audit_result = Audit.perform(gatekeeper.get_names(cmd.kind), [r.name for r in results])
    audit_result.print_table()
