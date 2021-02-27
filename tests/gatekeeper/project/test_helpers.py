from unittest import TestCase
from typing import NamedTuple
from gatekeeper.src.helpers import (
    format_template_name,
    format_model_name,
    format_render_key,
    create_key_list
)


class DummyOrder(NamedTuple):
    name: str


class TestHelpers(TestCase):

    def test_format_template_name(self) -> None:
        formatted = format_template_name('Freds')
        self.assertEqual(formatted, 'fred.sql')

    def test_format_model_name(self) -> None:
        formatted = format_model_name('fred')
        self.assertEqual(formatted, 'Fred')

    def test_format_render_key(self) -> None:
        formatted = format_render_key('Foods')
        self.assertEqual(formatted, 'food')

    def test_key_list_generator(self) -> None:
        keys = ['spam', 'eggs', 'beans']
        keys.sort()
        orders = [DummyOrder(key) for key in keys]
        key_list = create_key_list(orders, 'name')
        key_list.sort()
        self.assertEqual(keys, key_list)
