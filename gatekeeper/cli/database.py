from argparse import Namespace
from gatekeeper.environment import load_cli_env
from gatekeeper.src.configparsing import GateKeeperConfig
from gatekeeper.src.db import RedshiftClient


class DatabaseCommand:

    @load_cli_env
    def __init__(self, config: GateKeeperConfig):
        self.config = config
        self.redshift_client = RedshiftClient(config.redshift_connection)

    def __call__(self, cmd: Namespace) -> None:
        action = getattr(self, cmd.action)
        action()

    def init(self) -> None:
        # create the required tables in redshift
        print("Creating schema gatekeeper")
        self.redshift_client.create_schema()
        print("Creating gatekeeper tables")
        self.redshift_client.create_tables()

    def drop(self):
        self.redshift_client.drop_tables()
