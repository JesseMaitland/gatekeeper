from pathlib import Path

# Path to the cli environment config file
GATEKEEPER_CONFIG_PATH = Path.cwd().absolute() / 'gatekeeper.yml'

# project root. this is where all of the gatekeeper output lives
PROJECT_ROOT = Path.cwd().absolute() / "redshift" / "gatekeeper"

# mapping of project directories to be referenced by name
CONFIG_DIR = PROJECT_ROOT / 'config'
CONFIG_FILE = CONFIG_DIR / 'permissions.yml'

# directories to store planned sql files
PLANNED_DIR = PROJECT_ROOT / 'planned'
INDEX_DIR = PROJECT_ROOT / "index"
PLANNED_USERS_DIR = PLANNED_DIR / 'users'
PLANNED_GROUPS_DIR = PLANNED_DIR / 'groups'

USER_INDEX_FILE = INDEX_DIR / "users.json"
GROUP_INDEX_FILE = INDEX_DIR / "groups.json"
PASSWORD_INDEX_FILE = INDEX_DIR / 'passwords.json'

# permissions template file
PERMISSIONS_TEMPLATE = Path(__file__).absolute().parent.parent / 'templates/configs/permissions_template.yml'
GATEKEEPER_CONFIG_TEMPLATE = Path(__file__).absolute().parent.parent / 'templates/configs/gatekeeper_template.yml'

# secrets path
GATEKEEPER_SECRETS_PATH = PROJECT_ROOT / "gatekeeper_secrets.json"
