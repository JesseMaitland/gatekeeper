from argparse import ArgumentParser

from .init import init
from .render import render
from .query import query
# from .cat import cat
from .audit import audit
# from .rewind import rewind


def parse_args():
    parser = ArgumentParser()
    sub_parsers = parser.add_subparsers(dest='command')
    sub_parsers.required = True

    # cat_parser = sub_parsers.add_parser('cat')
    # cat_parser.set_defaults(func=cat)

    init_parser = sub_parsers.add_parser('init')
    init_parser.set_defaults(func=init)

    render_parser = sub_parsers.add_parser('render')
    render_parser.set_defaults(func=render)

    query_parser = sub_parsers.add_parser('query')
    query_parser.add_argument('query')
    query_parser.set_defaults(func=query)
#
    audit_parser = sub_parsers.add_parser('audit')
    audit_parser.add_argument('kind', choices=['users', 'groups'])
    audit_parser.set_defaults(func=audit)

    return parser.parse_args()
