import shutil
from pathlib import Path
from argparse import Namespace
from gatekeeper.src.environment import get_jinja_environment, gatekeeper_env
from gatekeeper.src.database import fetch_and_map_query_result
from gatekeeper.src.configparsing import create_gatekeeper
from gatekeeper.src.paths import RENDERED_DIR
from gatekeeper.src.helpers import (
    format_template_name,
    format_render_key
)


def clear_tree(path: Path) -> None:
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass


@gatekeeper_env()
def render(cmd: Namespace) -> None:

    print("rendering configs to .sql files")

    # get a jinja env for template rendering
    jinja = get_jinja_environment()

    # gatekeeper object used to parse config files
    gate_keeper = create_gatekeeper()

    # first render the users
    user_path = RENDERED_DIR / 'users'
    clear_tree(user_path)
    user_path.mkdir(parents=True, exist_ok=True)
    user_template = jinja.get_template('user.sql')

    for user in gate_keeper.users():
        file = user_path / user.file_name
        file.touch(exist_ok=True)
        file.write_text(user_template.render(**{'user': user}))



    # query redshift for all available schemas. These will be used for templating groups
    schemas = fetch_and_map_query_result('REDSHIFT', 'schemas')
    tables = fetch_and_map_query_result('REDSHIFT', 'tables')

    # here we render the groups
    group_path = RENDERED_DIR / 'groups'
    clear_tree(group_path)
    group_path.mkdir(parents=True, exist_ok=True)
    user_template = jinja.get_template('group.sql')

    for group in gate_keeper.groups():
        pass
