from argparse import ArgumentParser

from .init import init
from .render import render
from .digest import digest

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

    return parser.parse_args()
