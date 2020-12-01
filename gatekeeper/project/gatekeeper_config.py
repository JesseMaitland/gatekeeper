from pathlib import Path

GATEKEEPER_CONFIG_PATH = Path.cwd().absolute() / '.gatekeeper'

PROJECT_ROOT = Path.cwd().absolute() / "redshift" / "gatekeeper"

OBJECT_STORE_ROOT = PROJECT_ROOT / '.gk'


PROJECT_DIRECTORY_PATHS = {
    'configs': PROJECT_ROOT / 'configs',
    'rendered': PROJECT_ROOT / 'rendered'
}


PROJECT_CONFIG_FILE_PATHS = {
    'groups': PROJECT_DIRECTORY_PATHS['configs'] / 'groups.yml',
    'users': PROJECT_DIRECTORY_PATHS['configs'] / 'users.yml',
    'roles': PROJECT_DIRECTORY_PATHS['configs'] / 'roles.yml'
}


OBJECT_STORE_PATHS = {
    'users': OBJECT_STORE_ROOT / 'users',
    'groups': OBJECT_STORE_ROOT / 'groups'
}
