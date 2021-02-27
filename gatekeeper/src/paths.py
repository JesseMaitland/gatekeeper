from pathlib import Path

# Path to the cli environment config file
GATEKEEPER_CONFIG_PATH = Path.cwd().absolute() / '.gatekeeper'

# project root. this is where all of the gatekeeper output lives
PROJECT_ROOT = Path.cwd().absolute() / "redshift" / "gatekeeper"

# mapping of project directories to be referenced by name
CONFIGS_DIR = PROJECT_ROOT / 'configs'
RENDERED_DIR = PROJECT_ROOT / 'rendered'
COMMIT_DIR = PROJECT_ROOT / 'commits'

CONFIG_FILE_NAMES = ['users.yml', 'groups.yml']

RENDERED_DIR_NAMES = ['users', 'groups']
