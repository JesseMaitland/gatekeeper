from pathlib import Path

PROJECT_ROOT = Path.cwd().absolute() / "redshift" / "gatekeeper"

GATEKEEPER_CONFIG_PATH = Path.cwd().absolute() / '.gatekeeper'

PROJECT_DIRECTORY_PATHS = {
    'configs': PROJECT_ROOT / 'configs',
    'rendered': PROJECT_ROOT / 'rendered'
}

PROJECT_CONFIG_FILE_PATHS = {
    'groups': PROJECT_DIRECTORY_PATHS['configs'] / 'groups.yml',
    'users': PROJECT_DIRECTORY_PATHS['configs'] / 'users.yml',
    'roles': PROJECT_DIRECTORY_PATHS['configs'] / 'roles.yml'
}
