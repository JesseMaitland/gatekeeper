import yaml
from hashlib import md5
from typing import List, Union
from pathlib import Path
from gatekeeper.src.exceptions import ConfigurationError


class YamlModel(yaml.YAMLObject):

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def from_yaml(cls, loader, node) -> 'YamlModel':
        values = loader.construct_mapping(node, deep=True)
        return cls(**values)


class GateKeeperConfig(YamlModel):
    yaml_tag = '!GateKeeperConfig'

    def __init__(self, env: str, redshift_connection: str, ssm_path: str) -> None:
        super(GateKeeperConfig, self).__init__()
        self.env = env
        self.redshift_connection = redshift_connection
        self.ssm_path = ssm_path

    @property
    def fernet_key_ssm(self) -> str:
        return f"{self.ssm_path}/SECRET_KEY"


class UserConfig(YamlModel):
    yaml_tag = '!User'

    def __init__(self,
                 name: str,
                 create_db: bool,
                 create_user: bool,
                 sys_log_access: str,
                 connection_limit: Union[str, int],
                 valid_until: str = None) -> None:
        super(User, self).__init__()
        self.name = name
        self.create_db = create_db
        self.create_user = create_user
        self.sys_log_access = sys_log_access
        self.connection_limit = connection_limit
        self.valid_until = valid_until

        self._validate_fields()

    @property
    def file_name(self) -> str:
        return f"{self.name}.sql"

    def _validate_fields(self) -> None:

        if not isinstance(self.connection_limit, str) and not isinstance(self.connection_limit, int):
            raise ConfigurationError(
                f"connection_limit must be string or int, got {type(self.connection_limit)}")

        if isinstance(self.connection_limit, str) and self.connection_limit != 'unlimited':
            raise ConfigurationError(
                f"connection_limit must be either set to 'unlimited' or an integer, got {type(self.connection_limit)}")

        allowed_sys_log = ['restricted', 'unrestricted']
        if self.sys_log_access not in allowed_sys_log:
            raise ConfigurationError(
                f"Valid values for 'sys_log_access' are {allowed_sys_log}, got {self.sys_log_access}")

        if not isinstance(self.create_db, bool):
            raise ConfigurationError(
                f"create_db must be a boolean value, got {type(self.create_db)}")

        if not isinstance(self.create_user, bool):
            raise ConfigurationError(f"create_user must be a boolean value, got {type(self.create_user)}")


def register_constructors() -> None:
    yaml.SafeLoader.add_constructor('!User', UserConfig.from_yaml)
    yaml.SafeLoader.add_constructor('!GateKeeperConfig', GateKeeperConfig.from_yaml)


def parse_config(path: Path) -> Union[List[UserConfig], GateKeeperConfig]:
    register_constructors()
    configs = list(yaml.safe_load_all(path.open()))

    if len(configs) > 1:
        return configs
    else:
        return configs[0]


class GateKeeper:

    def __init__(self, entries: List[UserConfig]) -> None:
        self.users = {u.name: u for u in entries if isinstance(u, UserConfig)}

    @classmethod
    def from_configs(cls, path: Path) -> 'GateKeeper':
        return cls(entries=parse_config(path))
