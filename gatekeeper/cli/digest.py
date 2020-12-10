from argparse import Namespace
from gatekeeper.project.file_manager import populate_object_store


def digest(cmd: Namespace) -> None:
    print("populating gatekeeper object store.")
    populate_object_store(rebuild=True)
