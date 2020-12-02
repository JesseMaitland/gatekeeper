from argparse import ArgumentParser

from .init import init
from .render import render
from .digest import digest
from .fetch import fetch
from .stage import stage
from .query import query


def parse_args():

    parser = ArgumentParser()
    sub_parsers = parser.add_subparsers(dest='command')
    sub_parsers.required = True

    init_parser = sub_parsers.add_parser('init')
    init_parser.set_defaults(func=init)

    render_parser = sub_parsers.add_parser('render')
    render_parser.set_defaults(func=render)

    digest_parser = sub_parsers.add_parser('digest')
    digest_parser.set_defaults(func=digest)

    fetch_parser = sub_parsers.add_parser('fetch')
    fetch_parser.add_argument('name')
    fetch_parser.add_argument('type_')
    fetch_parser.set_defaults(func=fetch)

    staging_parser = sub_parsers.add_parser('stage')
    staging_parser.set_defaults(func=stage)

    query_parser = sub_parsers.add_parser('query')
    query_parser.add_argument('query')
    query_parser.set_defaults(func=query)

    return parser.parse_args()
