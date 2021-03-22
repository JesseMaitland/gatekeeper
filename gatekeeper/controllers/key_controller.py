import boto3
import botocore
from datetime import datetime
from cryptography.fernet import Fernet
from transitions import Machine
from gatekeeper.src.db import RedshiftClient
from gatekeeper.src.db.models import Secrets
from gatekeeper.src.configparsing import GateKeeperConfig
from gatekeeper.src.secrets import put_ssm_parameter, get_fernet_from_ssm


class KeyController:
    states = [
        'not_created',
        'new',
        'applied',
        'deleted'
    ]

    def __init__(self, config: GateKeeperConfig):
        self.config = config
        self.ssm = boto3.client('ssm')
        self.redshift_client = RedshiftClient(config.redshift_connection)
        self.key_state = Secrets(name='secret_key', state='not_created')
        self.key_value = None

        self.state_machine = Machine(
            model=self,
            states=self.states,
            initial='not_created'
        )

        self.state_machine.add_transition(
            trigger='generate_key',
            source='*',
            dest='new',
            before='_set_new_key_value',
            after=['_set_key_state',
                   '_push_key_to_ssm',
                   '_save_key_state_to_redshift']
        )

        self.state_machine.add_transition(
            trigger='delete_key_from_ssm',
            source='*',
            dest='deleted',
            before='_delete_from_ssm',
            after=['_set_key_state',
                   '_save_key_state_to_redshift']
        )

        self.state_machine.add_transition(
            trigger='apply_key',
            source='new',
            dest='applied',
            after=['_set_key_state',
                   '_save_key_state_to_redshift']
        )

    def set_key_state_from_redshift(self) -> None:
        key_state = Secrets.get_fernet_key_state(self.redshift_client.get_session())

        if key_state:
            self.key_state = key_state

        self.state_machine.set_state(self.key_state.state)

    def _save_key_state_to_redshift(self) -> None:
        self.key_state.updated_at = datetime.now()
        Secrets.save_key_state(self.key_state, self.redshift_client.get_session())

    def _set_new_key_value(self) -> None:
        self.key_value = Fernet.generate_key().decode()

    def fetch_key_from_ssm(self) -> None:
        return get_fernet_from_ssm(ssm_name=self.config.fernet_key_ssm,
                                   ssm=self.ssm)

    def _push_key_to_ssm(self) -> None:
        put_ssm_parameter(
            ssm_name=self.config.fernet_key_ssm,
            value=self.key_value,
            ssm=self.ssm
        )

    def _delete_from_ssm(self) -> None:
        try:
            self.ssm.delete_parameter(Name=self.config.fernet_key_ssm)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] != 'ParameterNotFound':
                raise

    def _set_status_to_deleted(self) -> None:
        self.key_state.state = 'deleted'
        self.save_key_state_to_redshift()

    def _set_key_state(self) -> None:
        self.key_state.state = self.state
