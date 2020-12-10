from argparse import Namespace
from gatekeeper.project.environment import gatekeeper_env
from gatekeeper.project.config_parsing import create_gatekeeper
from gatekeeper.project.database.queries import get_query
from gatekeeper.project.database.executor import execute_query
from gatekeeper.project.database.mapper import map_results
from gatekeeper.project.helpers import format_model_name
from gatekeeper.project.audits import Audit


@gatekeeper_env()
def audit(cmd: Namespace) -> None:

    # a gatekeeper will be used for the audit
    gatekeeper = create_gatekeeper()

    # run query against db to get the object we are doing the audit on
    query = get_query(cmd.kind)
    results = map_results(*execute_query('REDSHIFT', query), format_model_name(cmd.kind))

    audit_result = Audit.perform(gatekeeper.get_names(cmd.kind), [r.name for r in results])

    audit_result.print_table()
