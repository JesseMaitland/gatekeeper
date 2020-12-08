from argparse import Namespace
from gatekeeper.project.config_parsing import create_gatekeeper


def cat(cmd: Namespace) -> None:
    gate_keeper = create_gatekeeper()
    for user in gate_keeper.users:
        for group in user.groups:
            print(user.name, group.name)
