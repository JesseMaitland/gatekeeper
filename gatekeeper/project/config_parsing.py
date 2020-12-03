import yaml
from gatekeeper.project.helpers import format_model_name
from gatekeeper.project.file_manager import get_config_path
from gatekeeper.project.models import (
    User, Group, Role, GateKeeper
)


def parse_project_configs():

    types = ['groups', 'users', 'roles']
    parsed = {}

    for type_ in types:
        config = yaml.safe_load(get_config_path(type_).open())[type_]
        model = globals()[format_model_name(type_)]
        parsed[type_] = {key: model(name=key, **values) for key, values in config.items()}

    return GateKeeper(**parsed)
