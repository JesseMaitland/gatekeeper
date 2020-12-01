import os
import psycopg2
from psycopg2.extensions import connection
from configparser import ConfigParser
from dotenv import load_dotenv
from jinja2 import PackageLoader, Environment

from gatekeeper.project.config import GATEKEEPER_CONFIG_PATH


def get_jinja_environment() -> Environment:
    loader = PackageLoader(package_name='gatekeeper', package_path='templates')
    return Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)


class GateKeeperEnvironment:

    def __init__(self):
        self.config = ConfigParser()
        self.config.read(GATEKEEPER_CONFIG_PATH.open())

        try:
            load_dotenv(self.config['env']['file'])
        except KeyError:
            load_dotenv()

    def get_redshift_connection(self) -> connection:
        connection_string = self.config['redshift']['connection']
        connection_string = os.getenv(connection_string, connection_string)
        return psycopg2.connect(connection_string)


