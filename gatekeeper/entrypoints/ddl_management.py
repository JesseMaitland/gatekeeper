from typing import Dict
from datetime import datetime
from rsterm import EntryPoint
from gatekeeper.project import ProjectContext
from redscope.api import introspect_redshift


class CreateDdl(EntryPoint):

    config_choices = ['users', 'groups', 'ownership', 'all']

    entry_point_args = {
        ('--config', '-c'): {
            'help': "the name of the config you would like to build. default is all",
            'choices': config_choices,
            'default': 'all'
        }
    }

    def __init__(self, config_path) -> None:
        self.pc = ProjectContext()
        self.je = self.pc.get_jinja_env()
        self.co = self.pc.get_config()
        super(CreateDdl, self).__init__(config_path=config_path)
        db_connection = self.rsterm.get_db_connection('redscope')
        self.dbc = introspect_redshift(db_connection)
        db_connection.close()

    def run(self) -> None:

        if self.cmd_args.config == 'all':
            for config_choice in self.config_choices:
                self.create(config_choice)
        else:
            self.create(self.cmd_args.config)

    def create(self, name: str) -> None:

        # exclude these options
        if name == 'all':
            return

        print(f"generating sql for {name}......")
        self.pc.clean_dir(name)
        p_dir = self.pc.dirs[name]
        template = self.je.get_template(f"{name}.sql")
        dt = datetime.now().replace(microsecond=0)

        for key, value in self.co.items[name].items():

            if name == 'ownership':
                params = {
                    'users':
                }
            else:
                params = {
                    name: value,
                    'dt': dt
                }


            content = template.render(**{name: value, 'dt': })
            fp = p_dir / f"{value.name}.sql"
            fp.touch()
            fp.write_text(content)


