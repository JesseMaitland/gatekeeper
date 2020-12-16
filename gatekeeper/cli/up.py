from argparse import Namespace
from gatekeeper.project.database.executor import execute_statement
from gatekeeper.project.environment import gatekeeper_env
from gatekeeper.project.file_manager import (
    read_index,
    fetch_commit,
    move_commit_to_executed,
    parse_commit,
    clear_staged,
    reset_head,
    reset_index
)

@gatekeeper_env()
def up(cmd: Namespace) -> None:

    for entry in read_index():
        commit = fetch_commit(entry)
        query = parse_commit(commit)
        if cmd.print:
            print(query)
            exit()
        else:
            execute_statement('REDSHIFT', query)
            move_commit_to_executed(entry)

    clear_staged()
    reset_index()
    reset_head()
