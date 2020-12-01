from argparse import Namespace
from gatekeeper.project.file_manager import generate_status


def stage(cmd: Namespace) -> None:
    result = generate_status()
    print(result)
