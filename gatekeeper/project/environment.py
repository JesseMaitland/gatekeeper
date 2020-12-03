import os
import psycopg2
from psycopg2.extensions import connection
from configparser import ConfigParser
from dotenv import load_dotenv
from jinja2 import PackageLoader, Environment

from gatekeeper.project.file_manager import GATEKEEPER_CONFIG_PATH


def get_jinja_environment() -> Environment:
    loader = PackageLoader(package_name='gatekeeper', package_path='templates')
    return Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)


def get_gatekeeper_config() -> ConfigParser:
    config = ConfigParser()
    config.read(GATEKEEPER_CONFIG_PATH)
    return config


def load_gatekeeper_env(config: ConfigParser = None) -> None:
    if not config:
        config = get_gatekeeper_config()
    try:
        load_dotenv(config['env']['file'])
    except KeyError:
        load_dotenv()


def get_redshift_connection() -> connection:
    config = get_gatekeeper_config()
    var_name = config['redshift']['connection']
    connection_string = os.getenv(var_name)
    return psycopg2.connect(connection_string)




