import shutil
from argparse import Namespace
from gatekeeper.project.gatekeeper_config import (
    PROJECT_CONFIG_FILE_PATHS,
    PROJECT_DIRECTORY_PATHS
)
from gatekeeper.project.project_config import ConfigMapping
from gatekeeper.project.environment import get_jinja_environment


def render(cmd: Namespace) -> None:
    # TODO: variable naming in render command is horrible
    # TODO: add try / catch logic to allow for nice error messages

    # get the parsed and mapped yaml configs from the project
    config_mapping = ConfigMapping.from_config_paths(config_paths=PROJECT_CONFIG_FILE_PATHS)

    # get jinja to render our sql templates
    jinja = get_jinja_environment()

    for obj_type, objs in config_mapping.to_render().items():

        template = jinja.get_template(f"{obj_type}.sql")

        render_path = PROJECT_DIRECTORY_PATHS['rendered'] / obj_type

        # Clear out the path before we render the objects.
        # Insures that the rendered files always reflect the config
        shutil.rmtree(render_path)

        for obj_name, config_value in objs.items():
            rendered_file_path = render_path / f"{obj_name}.sql"
            content = template.render(**{obj_type.rstrip('s'): config_value})
            rendered_file_path.parent.mkdir(exist_ok=True, parents=True)
            rendered_file_path.write_text(content)
