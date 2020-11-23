from gatekeeper.entrypoints.base import GateKeeperSingleActionEntryPoint


class Query(GateKeeperSingleActionEntryPoint):

    discover = True

    def action(self) -> None:
        pass
