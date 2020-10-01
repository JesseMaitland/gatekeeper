from rsterm import EntryPoint
from gatekeeper.project import provide_project_context, ProjectContext


class NewProject(EntryPoint):

    @provide_project_context
    def run(self, pc: ProjectContext) -> None:
        pc.init()


