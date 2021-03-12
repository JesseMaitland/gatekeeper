from argparse import ArgumentParser

from .init import init
from .plan import plan, users, groups
# from .query import query
# from .cat import cat
# from .audit import audit
# from .rewind import rewind


def parse_args():
    parser = ArgumentParser()
    sub_parsers = parser.add_subparsers(dest='command')
    sub_parsers.required = True

    # cat_parser = sub_parsers.add_parser('cat')
    # cat_parser.set_defaults(func=cat)

    init_parser = sub_parsers.add_parser('init')
    init_parser.set_defaults(func=init)

    plan_parser = sub_parsers.add_parser('plan')
    plan_parser.set_defaults(func=plan)

    plan_sub_parser = plan_parser.add_subparsers(dest='sub_command')
    user_plan_parser = plan_sub_parser.add_parser('users')
    user_plan_parser.add_argument('--rotate-passwords', action='store_true', default=False)
    user_plan_parser.set_defaults(func=users)

    group_plan_parser = plan_sub_parser.add_parser('groups')
    group_plan_parser.set_defaults(func=groups)

    users_parser = sub_parsers.add_parser('users')
    users_parser.add_argument('--new', '-n', action='store_true', default=False)
    users_parser.add_argument('--update')
    users_parser.set_defaults(func=users)

    # query_parser = sub_parsers.add_parser('query')
    # query_parser.add_argument('query')
    # query_parser.set_defaults(func=query)

    # audit_parser = sub_parsers.add_parser('audit')
    # audit_parser.add_argument('kind', choices=['users', 'groups'])
    # audit_parser.set_defaults(func=audit)

    return parser.parse_args()
