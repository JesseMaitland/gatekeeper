from argparse import Namespace
from gatekeeper.project.environment import get_jinja_environment, gatekeeper_env
from gatekeeper.project.file_manager import generate_status, STAGING_FILE_PATH
from gatekeeper.project.database import fetch_and_map_query_result
from gatekeeper.project.helpers import format_template_name


@gatekeeper_env()
def stage(cmd: Namespace) -> None:
    """
    TODO: break this up into smaller functions in its own module as they may also be needed in the audit commands
    """
    print("staging rendered files")
    # kill whatever is in the staging file and re-write it
    change_result = generate_status()
    jinja = get_jinja_environment()

    change_result.print_status()

    with STAGING_FILE_PATH.open(mode='w') as staging_file:

        # creating new things is easy, just add whatever is in the file.
        # however groups must be created and assigned permissions before users.
        for to_add in change_result['to_add']['groups']:
            staging_file.write(to_add.read_text())
            staging_file.write('\n\n')

        for to_add in change_result['to_add']['users']:
            staging_file.write(to_add.read_text())
            staging_file.write('\n\n')

        # only do this if we have things to remove
        if [v for v in change_result['to_remove'].values()]:

            # since we will drop the user, just get a list of all schemas and groups from redshift
            # and we will remove all access rights to everything.
            schemas = fetch_and_map_query_result('REDSHIFT', 'schemas')
            groups = fetch_and_map_query_result('REDSHIFT', 'groups')

            # dropping things means we need to revoke all rights and group membership
            for kind in change_result['to_remove'].keys():

                # TODO: remove this once proper templates exist
                try:
                    template = jinja.get_template(f"drop_{format_template_name(kind)}")
                except Exception:
                    continue

                for entry in change_result['to_remove'][kind]:
                    content = template.render(**{kind: entry, 'groups': groups, 'schemas': schemas})
                    staging_file.write(content)
                    staging_file.write('\n\n')
