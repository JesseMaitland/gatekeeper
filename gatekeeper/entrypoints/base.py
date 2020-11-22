from rambo import SingleActionEntryPoint, MultiActionEntryPoint

from gatekeeper.project.context import GateKeeperEnvironment, GateKeeperProject


class BaseGateKeeperEntry:

    def __init__(self):
        self.project = GateKeeperProject()
        self.environment = GateKeeperEnvironment()


class GateKeeperSingleActionEntryPoint(BaseGateKeeperEntry, SingleActionEntryPoint):

    def __init__(self):
        super(GateKeeperSingleActionEntryPoint, self).__init__()

    def action(self) -> None:
        raise NotImplementedError


class GateKeeperMultiActionEntryPoint(BaseGateKeeperEntry, MultiActionEntryPoint):

    def __init__(self):
        super(GateKeeperMultiActionEntryPoint, self).__init__()
