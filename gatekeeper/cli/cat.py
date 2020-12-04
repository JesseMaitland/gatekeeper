from argparse import Namespace
from gatekeeper.project.config_parsing import parse_project_configs


def cat(cmd: Namespace) -> None:
    gk = parse_project_configs()
    user = gk['users']['jesse']

    for role in user.roles:
        print(role.name)
        for group in role.groups:
            print(group.name)
