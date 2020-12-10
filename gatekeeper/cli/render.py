import shutil
from argparse import Namespace
from gatekeeper.project.environment import get_jinja_environment
from gatekeeper.project.config_parsing import create_gatekeeper
from gatekeeper.project.helpers import (
    format_template_name,
    format_render_key
)
from gatekeeper.project.file_manager import (
    get_project_path
)


def render(cmd: Namespace) -> None:
    print("rendering configs to .sql files")
    jinja = get_jinja_environment()
    gate_keeper = create_gatekeeper()

    for key in gate_keeper.render_keys:
        template = jinja.get_template(format_template_name(key))
        path = get_project_path('rendered') / key

        try:
            shutil.rmtree(path)
        except FileNotFoundError:
            pass

        for item in gate_keeper[key]:
            content = template.render(**{format_render_key(key): item})
            write_path = path / item.file_name
            write_path.parent.mkdir(exist_ok=True)
            write_path.touch(exist_ok=True)
            write_path.write_text(content)
