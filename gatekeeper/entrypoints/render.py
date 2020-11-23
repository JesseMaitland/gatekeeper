# # standard lib
# from typing import Dict
# from itertools import groupby
# from datetime import datetime
#
# # 3rd party deps
# from rsterm import EntryPoint
# from redscope.api import introspect_redshift
#
# # project deps
# from gatekeeper.project import ProjectContext
# from gatekeeper.tools import group_ownership
#
#
# class CreateDdl(EntryPoint):
#
#     config_choices = ['users', 'groups', 'all']
#
#     entry_point_args = {
#         ('--config', '-c'): {
#             'help': "the name of the config you would like to build. default is all",
#             'choices': config_choices,
#             'default': 'all'
#         }
#     }
#
#     def __init__(self, config_path) -> None:
#         self.pc = ProjectContext()
#         self.je = self.pc.get_jinja_env()
#         self.co = self.pc.get_config()
#         super(CreateDdl, self).__init__(config_path=config_path)
#
#         db_connection = self.rsterm.get_db_connection('redscope')
#         self.dbc = introspect_redshift(db_connection, verbose=True)
#         db_connection.close()
#
#     def run(self) -> None:
#
#         if self.cmd_args.config == 'all':
#             for config_choice in self.config_choices:
#                 self.create(config_choice)
#             self.create_ownership()
#         else:
#             self.create(self.cmd_args.config)
#
#
#     def create(self, name: str) -> None:
#
#         # exclude these options
#         if name == 'all':
#             return
#
#         print(f"generating sql for {name}......")
#         self.pc.clean_dir(name)
#         p_dir = self.pc.dirs[name]
#         template = self.je.get_template(f"{name}.sql")
#         dt = datetime.now().replace(microsecond=0)
#
#         for key, value in self.co.items[name].items():
#             content = template.render(**{name: value, 'dt': dt})
#             fp = p_dir / f"{value.name}.sql"
#             fp.touch()
#             fp.write_text(content)
#
#     def create_ownership(self):
#         """
#         to implement ownership assignment
#
#         get all users from config
#         get all objects in schema from introspection
#
#         assign introspection objects to users for a schema
#
#         check that all schemas have been assigned
#             if not, print warning
#
#         """
#         ownership = {}
#         gatekeeper_users = self.co.get_users()
#         ownership_dir = self.pc.dirs['ownership']
#         self.pc.clean_dir('ownership')
#         dt = datetime.now().replace(microsecond=0)
#
#         for gatekeeper_user in gatekeeper_users:
#             ownership[gatekeeper_user.name] = {}
#
#             for owned_schema in gatekeeper_user.owned_schemas:
#                 try:
#                     db_objects = self.dbc.get_objects_by_schema(owned_schema)
#                     ownership[gatekeeper_user.name]['owns'] = db_objects
#                 except KeyError:
#                     print(f"the schema {owned_schema} assigned to user {gatekeeper_user.name} "
#                           f"does not exist and will be skipped.")
#
#         for user_name, db_objects in ownership.items():
#             template = self.je.get_template('ownership.sql')
#             content = template.render(**{'user':user_name, 'db_objects': db_objects, 'dt':dt})
#             file = ownership_dir / f"{user_name}.sql"
#             file.touch()
#             file.write_text(content)
#
#
# class TestCode(EntryPoint):
#
#     def __init__(self, config_path) -> None:
#         self.pc = ProjectContext()
#         self.je = self.pc.get_jinja_env()
#         self.co = self.pc.get_config()
#         super(TestCode, self).__init__(config_path=config_path)
#         db_connection = self.rsterm.get_db_connection('redscope')
#         self.dbc = introspect_redshift(db_connection, 'ownership', verbose=True)
#         db_connection.close()
#
#     def run(self) -> None:
#
#         ownership = self.dbc.ownership
#         ownership.sort(key=lambda x: x.owner)
#
#         groups = {}
#         for key, group in groupby(ownership, lambda x: x.owner):
#             groups[key] = list(group)

from datetime import datetime
from gatekeeper.entrypoints.base import GateKeeperSingleActionEntryPoint


class Render(GateKeeperSingleActionEntryPoint):

    discover = True

    def action(self) -> None:
        jinja = self.environment.get_jinja_env()
        gatekeeper = self.project.get_gatekeeper()
        rendered_dir = self.project.dirs.get('rendered')

        for access_config_key, access_configs in gatekeeper.access_configs.items():

            if access_config_key == 'roles':
                continue

            template = jinja.get_template(f"{access_config_key}.sql")
            rendered_path = rendered_dir / access_config_key

            for access_name, access_value in access_configs.items():
                rendered_file_path = rendered_path / f"{access_name}.sql"
                content = template.render(**{access_config_key.rstrip('s'): access_value})
                rendered_file_path.parent.mkdir(exist_ok=True, parents=True)
                rendered_file_path.write_text(content)

        print(f"permissions files rendered under {rendered_dir.absolute().as_posix()}")
