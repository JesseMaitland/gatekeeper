from typing import Callable
from dotenv import load_dotenv
from jinja2 import PackageLoader, Environment
from gatekeeper.src.paths import GATEKEEPER_CONFIG_PATH
from gatekeeper.src.configparsing import parse_config


def load_cli_env(func: Callable):
    def wrapper(*args, **kwargs):

        try:
            config = parse_config(GATEKEEPER_CONFIG_PATH)
            load_dotenv(config.env, override=True)
        except FileNotFoundError:
            config = None
            print("gatekeeper.yml not found in root directory.")

        return func(config=config, *args, **kwargs)

    return wrapper


def get_jinja_environment() -> Environment:
    loader = PackageLoader(package_name='gatekeeper', package_path='templates')
    return Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)
