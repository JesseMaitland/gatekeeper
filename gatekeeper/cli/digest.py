from argparse import Namespace
from gatekeeper.project.file_manager import populate_object_store


def digest(cmd: Namespace) -> None:
    populate_object_store(rebuild=True)
