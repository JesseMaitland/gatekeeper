from shutil import copy
from argparse import Namespace
from gatekeeper.src.paths import (
    PROJECT_ROOT,
    GATEKEEPER_CONFIG_PATH,
    CONFIG_DIR,
    PLANNED_DIR,
    CONFIG_FILE,
    PERMISSIONS_TEMPLATE,
    GATEKEEPER_CONFIG_TEMPLATE,
    PLANNED_GROUPS_DIR,
    PLANNED_USERS_DIR,
    INDEX_DIR,
    USER_INDEX_FILE,
    GROUP_INDEX_FILE
)


class ProjectCommand:

    def __call__(self, cmd: Namespace) -> None:
        action = getattr(self, cmd.action)
        action()

    @staticmethod
    def init() -> None:
        """
        Initializes gatekeeper project directories and config files. This command must be run at least once to start a
        gatekeeper project, but can be run again at any time to rebuild the project directories. Running this command
        is *NOT* destructive to the existing project.

        Command:
            ``gatekeeper init``
        """
        for directory in PROJECT_ROOT, CONFIG_DIR, PLANNED_DIR, PLANNED_GROUPS_DIR, PLANNED_USERS_DIR, INDEX_DIR:
            directory.mkdir(parents=True, exist_ok=True)

        for file in USER_INDEX_FILE, GROUP_INDEX_FILE:
            file.touch(exist_ok=True)

        if GATEKEEPER_CONFIG_PATH.exists():
            print("A a gatekeeper.yml file already exists and will not be overwritten")
        else:
            print("Creating a new gatekeeper.yml config file in the project root")
            copy(GATEKEEPER_CONFIG_TEMPLATE, GATEKEEPER_CONFIG_PATH)

        # copy the template to the permissions file
        if CONFIG_FILE.exists():
            print("A permissions.yml file already exists and will not be overwritten.")
        else:
            print("A new permissions.yml file has been created.")
            copy(PERMISSIONS_TEMPLATE, CONFIG_FILE)
