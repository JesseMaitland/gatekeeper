from argparse import Namespace
from gatekeeper.project.config_parsing import parse_project_configs


def cat(cmd: Namespace) -> None:
    gk = parse_project_configs()
    print(gk.get_associated_user('jesse'))
