from argparse import Namespace
from gatekeeper.src.configparsing import create_gatekeeper


def cat(cmd: Namespace) -> None:
    gate_keeper = create_gatekeeper()
    for user in gate_keeper.users:
        for group in user.groups:
            print(user.name, group.name)
