from pugsql import parser
from pugsql.query import Query
from unittest import TestCase, skip


class BasicTest(TestCase):
    def setUp(self):
        self.sql = open('tests/sql/basic.sql', 'r').read()

    def test_returns_query(self):
        self.assertIsInstance(parser.parse(self.sql), Query)

    def test_sets_name(self):
        self.assertEqual(parser.parse(self.sql).name, 'username_for_id')
