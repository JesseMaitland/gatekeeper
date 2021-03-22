from argparse import Namespace
from gatekeeper.environment import get_jinja_environment, load_cli_env
from gatekeeper.src.configparsing import GateKeeper, GateKeeperConfig
from gatekeeper.src.db import RedshiftClient
from gatekeeper.src.db.models import UserData
from gatekeeper.src.index import hash_file
from gatekeeper.src.paths import (
    CONFIG_FILE,
    PLANNED_USERS_DIR
)


class UsersCommand:

    @load_cli_env
    def __init__(self, config: GateKeeperConfig):
        self.config = config
        self.redshift_client = RedshiftClient(config.redshift_connection)

    def __call__(self, cmd: Namespace) -> None:
        action = getattr(self, cmd.kind)
        action()

    def new(self, cmd: Namespace) -> None:
        # set up a gatekeeper
        gatekeeper = GateKeeper.from_configs(CONFIG_FILE)

        # get the jinja template for the users
        template = get_jinja_environment().get_template('user.sql')

        # make a collection of User state
        user_states = []

        # figure out what we are doing for each user
        for user in gatekeeper.users.values():
            # render the user file, and hash what we have created.
            user_sql_file_content = template.render(user=user)
            user_sql_file_content_md5_hash = hash_file(user_sql_file_content)

            user_state = ObjectState(
                name=user.name,
                kind='user',
                hash_value=user_sql_file_content_md5_hash,
                current_state='new',
                next_state='create'
            )
            user_states.append(user_state)
            # save the user file
            file_path = PLANNED_USERS_DIR / user.file_name
            file_path.touch(exist_ok=True)
            file_path.write_text(user_sql_file_content)

            session = self.redshift_client.get_session()
            ObjectState.save_users(user_state, session)
