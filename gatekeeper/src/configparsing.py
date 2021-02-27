import yaml
from gatekeeper.src.paths import CONFIGS_DIR, CONFIG_FILE_NAMES
from gatekeeper.src.models import GateKeeper


def create_gatekeeper() -> GateKeeper:
    GateKeeper.register_yaml_constructors()
    return GateKeeper(
        **{filename.split('.')[0]: list(yaml.safe_load_all(CONFIGS_DIR.joinpath(filename).open())) for filename in CONFIG_FILE_NAMES}
    )
