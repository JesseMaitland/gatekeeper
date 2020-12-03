from argparse import Namespace
from gatekeeper.project.config_parsing import parse_project_configs


def cat(cmd: Namespace) -> None:
    parse_project_configs()
