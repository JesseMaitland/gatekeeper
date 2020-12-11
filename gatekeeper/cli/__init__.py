from argparse import ArgumentParser

from .init import init
from .render import render
from .digest import digest
from .fetch import fetch
from .stage import stage
from .query import query
from .cat import cat
from .audit import audit
from .commit import commit
from .status import status
from .rewind import rewind


def parse_args():
    parser = ArgumentParser()
    sub_parsers = parser.add_subparsers(dest='command')
    sub_parsers.required = True

    cat_parser = sub_parsers.add_parser('cat')
    cat_parser.set_defaults(func=cat)

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
    staging_parser.set_defaults(func=[render, stage])

    commit_parser = sub_parsers.add_parser('commit')
    commit_parser.set_defaults(func=[digest, commit])

    status_parser = sub_parsers.add_parser('status')
    status_parser.set_defaults(func=status)

    rewind_parser = sub_parsers.add_parser('rewind')
    rewind_parser.set_defaults(func=rewind)

    query_parser = sub_parsers.add_parser('query')
    query_parser.add_argument('query')
    query_parser.set_defaults(func=query)

    audit_parser = sub_parsers.add_parser('audit')
    audit_parser.add_argument('kind', choices=['users', 'groups'])
    audit_parser.set_defaults(func=audit)

    return parser.parse_args()
