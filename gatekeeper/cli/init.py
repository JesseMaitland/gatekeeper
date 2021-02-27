from argparse import Namespace
from gatekeeper.src.paths import (
    PROJECT_ROOT,
    GATEKEEPER_CONFIG_PATH,
    CONFIGS_DIR,
    COMMIT_DIR,
    CONFIG_FILE_NAMES,
    RENDERED_DIR_NAMES,
    RENDERED_DIR
)


def init(cmd: Namespace) -> None:
    """

    Initializes gatekeeper project directories and config files. This command must be run at least once to start a
    gatekeeper project, but can be run again at any time to rebuild the project directories. Running this command
    is *NOT* destructive to the existing project.

    Command:
        ``gatekeeper init``
    """
    for directory in [PROJECT_ROOT, RENDERED_DIR, CONFIGS_DIR, COMMIT_DIR]:
        directory.mkdir(parents=True, exist_ok=True)

    GATEKEEPER_CONFIG_PATH.touch(exist_ok=True)

    for file in CONFIG_FILE_NAMES:
        CONFIGS_DIR.joinpath(file).touch(exist_ok=True)

    for directory in RENDERED_DIR_NAMES:
        RENDERED_DIR.joinpath(directory).mkdir(exist_ok=True)
