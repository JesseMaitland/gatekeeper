from argparse import Namespace
from gatekeeper.project.file_manager import (
    GATEKEEPER_CONFIG_PATH,
    PROJECT_DIRECTORY_PATHS,
    PROJECT_CONFIG_FILE_PATHS,
    OBJECT_STORE_PATHS
)


def init(cmd: Namespace) -> None:
    """
    Create all necessary project paths and files to make the gatekeeper work
    Args:
        cmd: Must be taken by an entrypoint

    Returns: None

    """

    GATEKEEPER_CONFIG_PATH.touch(exist_ok=True)

    for dir_path in PROJECT_DIRECTORY_PATHS.values():
        dir_path.mkdir(exist_ok=True, parents=True)

    for dir_path in OBJECT_STORE_PATHS.values():
        dir_path.mkdir(exist_ok=True, parents=True)

    for config_file in PROJECT_CONFIG_FILE_PATHS.values():
        config_file.parent.mkdir(exist_ok=True, parents=True)
        config_file.touch(exist_ok=True)
