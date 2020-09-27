from typing import Dict, List
from rsterm import EntryPoint
from jinja2 import Environment
from gatekeeper.project import provide_project_context, ProjectContext


class NewProject(EntryPoint):

    @provide_project_context
    def run(self, pc: ProjectContext) -> None:
        pc.init()


