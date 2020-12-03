import yaml
from gatekeeper.project.helpers import format_model_name
from gatekeeper.project.file_manager import get_config_path
from gatekeeper.project.models import (
    User, Group, Role
)


def parse_project_configs():

    group_config = yaml.safe_load(get_config_path('groups').open())['groups']



    # group_config = yaml.safe_load(get_config_path('groups').open())['groups']
    # groups = {key: Group(name=key, **values) for key, values in group_config.items()}
    # print(groups)
#
    # role_config = yaml.safe_load(get_config_path('roles').open())['roles']
    # print(role_config)
    # exit()
#
    # group_membership = {name: list(map(lambda x: groups.get(x) , params['groups'])) for name, params in role_config.items()}
#
    # print(group_membership)
    # exit()
#
    # for group_name, group_members in group_membership.items():
    #     role_config[group_name] = group_members
#
    # roles = {key: Role(name=key, **values) for key, values in group_membership.items()}
#
    # user_config = yaml.safe_load(get_config_path('users').open())['users']
#
    # role_membership = {name: list(map(roles.get, params['roles'])) for name, params in user_config.items()}
#
    # for user_name, user_roles in role_membership.items():
    #     user_config[user_name]['roles'] = user_roles
#
    # return {key: User(name=key, **values) for key, values in user_config.items()}
