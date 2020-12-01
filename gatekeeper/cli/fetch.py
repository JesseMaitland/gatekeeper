from argparse import Namespace
from gatekeeper.project.file_manager import fetch_from_object_store, fetch_from_rendered


def fetch(cmd: Namespace):
    obj = fetch_from_rendered(cmd.name, cmd.type_)
    print(obj.read_text())
