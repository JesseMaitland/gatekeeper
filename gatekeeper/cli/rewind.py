from argparse import Namespace
from gatekeeper.project.file_manager import rewind_head


def rewind(cmd: Namespace) -> None:
    rewind_head()
