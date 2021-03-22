from argparse import ArgumentParser

from .project import ProjectCommand
from .database import DatabaseCommand
from .users import UsersCommand
from .secrets import KeyCommands
from .database import DatabaseCommand
# from .query import query
# from .cat import cat
# from .audit import audit
# from .rewind import rewind


def parse_args():
    parser = ArgumentParser()
    sub_parsers = parser.add_subparsers(dest='noun')
    sub_parsers.required = True

    project_parser = sub_parsers.add_parser('project')
    project_parser.set_defaults(func=ProjectCommand)
    project_parser.add_argument('action', choices=['init'])

    database_parser = sub_parsers.add_parser('database')
    database_parser.set_defaults(func=DatabaseCommand)
    database_parser.add_argument('action', choices=['init', 'drop'])

    users_parser = sub_parsers.add_parser('users')
    users_parser.set_defaults(func=UsersCommand)
    users_parser.add_argument('action', choices=['plan'])

    keys_parser = sub_parsers.add_parser('key')
    keys_parser.set_defaults(func=KeyCommands)
    keys_parser.add_argument('action', choices=['generate', 'status', 'delete'])

    return parser.parse_args()
