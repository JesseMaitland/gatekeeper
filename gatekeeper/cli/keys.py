import boto3
import botocore
from argparse import Namespace
from cryptography.fernet import Fernet
from gatekeeper.environment import load_cli_env
from gatekeeper.src.configparsing import GateKeeperConfig
from gatekeeper.src.secrets import get_fernet, put_ssm_parameter
from gatekeeper.src.db.models import Secrets
from gatekeeper.src.db import RedshiftClient


def yes_no_input(msg: str) -> str:
    while True:
        selection = input(f"{msg} [y/n] -> ").lower()

        if selection in ['y', 'n']:
            return selection
        else:
            print("selection invalid")


class KeyCommand:

    @load_cli_env
    def __init__(self, config: GateKeeperConfig):
        self.config = config
        self.ssm = boto3.client('ssm')
        self.redshift_client = RedshiftClient(config.redshift_connection)

    def __call__(self, cmd: Namespace) -> None:
        action = getattr(self, cmd.action)
        action()

    def generate(self) -> None:
        secret_key = None

        try:
            secret_key = get_fernet(self.config.fernet_key_ssm, self.ssm)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] != 'ParameterNotFound':
                raise

        # Either no exception was raised, or we got a ParameterNotFound. Either way,
        # we will propose to make a new key.
        finally:

            if secret_key:
                msg = 'An existing key was found in aws ssm. Would you like to overwrite it?'
            else:
                msg = 'No key found in aws ssm. Would you like to create one?'

            option = yes_no_input(msg)

            if option == 'n':
                return
            else:
                self._generate_and_save_fernet_key_to_ssm()
                self._update_key_state_in_redshift()

    def _generate_and_save_fernet_key_to_ssm(self) -> None:

        fernet = Fernet.generate_key()
        put_ssm_parameter(ssm_name=self.config.fernet_key_ssm,
                          value=fernet.decode(),
                          ssm=self.ssm)

        print("A new fernet secret key was generated and saved in ssm")

    def _update_key_state_in_redshift(self) -> None:
        print("Saving secret state to redshift")
        session = self.redshift_client.get_session()
        key_state = Secrets.get_fernet_key_state(session)

        if not key_state:
            key_state = Secrets(name='secret_key')

        # any time we run this command, the state is always new
        key_state.state = 'new'

        session.add(key_state)
        session.commit()

        print("Secret state saved to redshift.\n"
              "All passwords for configured users must be rotated.\n"
              "Use the 'gatekeeper password rotate' command")
