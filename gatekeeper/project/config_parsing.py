import yaml
from gatekeeper.project.file_manager import get_config_path
from gatekeeper.project.models import GateKeeper


def create_gatekeeper() -> GateKeeper:
    GateKeeper.register_yaml_constructors()
    return GateKeeper(
        users=list(yaml.safe_load_all(get_config_path('users').open())),
        roles=list(yaml.safe_load_all(get_config_path('roles').open())),
        groups=list(yaml.safe_load_all(get_config_path('groups').open()))
    )
