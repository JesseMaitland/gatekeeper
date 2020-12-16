from argparse import Namespace
from gatekeeper.project.file_manager import (
    clear_object_store,
    clear_commits,
    clear_staged,
    reset_index,
    reset_head,
)


def purge(cmd: Namespace) -> None:
    clear_object_store()
    clear_commits()
    reset_index()
    reset_head()
    clear_staged()

