from argparse import Namespace
from transitions import MachineError
from gatekeeper.controllers.key_controller import KeyController
from gatekeeper.environment import load_cli_env
from gatekeeper.src.configparsing import GateKeeperConfig


def yes_no_input(msg: str) -> str:
    while True:
        selection = input(f"{msg} [y/n] -> ").lower()

        if selection in ['y', 'n']:
            return selection
        else:
            print("selection invalid")


class KeyCommands:

    @load_cli_env
    def __init__(self, config: GateKeeperConfig):
        self.config = config
        self.controller = KeyController(self.config)
        self.controller.set_key_state_from_redshift()

    def __call__(self, cmd: Namespace) -> None:
        action = getattr(self, cmd.action)
        action()

    def generate(self) -> None:

        # if we have no key we need to generate a new one
        try:
            self.controller.generate_key()
        except MachineError:
            print("An error was encountered when generating a new fernet key.")
        else:
            print("A new fernet key has been created and saved in the ssm parameter store. "
                  "Passwords can now be generated using the gatekeeper cli.")

    def status(self) -> None:

        if self.controller.state == 'not_created':
            print("A fernet key has not yet been created. Please run the 'gatekeeper key generate' command. ")
            exit()

        if self.controller.state == 'new':
            print(f"A new fernet key was created on {self.controller.key_state.updated_at}. "
                  f"This key has not yet been applied, but can be by using the gatekeeper cli")
            exit()

        if self.controller.state == 'active':
            print(f"The fernet key is currently active and was created at {self.controller.key_state.updated_at} ")

        if self.controller.state == 'deleted':
            print(f"The fernet key was deleted from ssm at {self.controller.key_state.updated_at}. "
                  "Create a new one using the 'gatekeeper key generate' command")

    def delete(self) -> None:
        self.controller.delete_key_from_ssm()
