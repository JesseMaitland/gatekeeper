from gatekeeper.entrypoints.base import GateKeeperSingleActionEntryPoint


class Init(GateKeeperSingleActionEntryPoint):

    discover = True
    description = " -- run this command to initialize a gatekeeper project --"

    def action(self) -> None:
        self.project.init()
