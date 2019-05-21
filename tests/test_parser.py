from pugsql import parser
from pugsql import statement
from unittest import TestCase, skip


class BasicTest(TestCase):
    def setUp(self):
        self.sql = open('tests/sql/basic.sql', 'r').read()

    def test_returns_stmt(self):
        self.assertIsInstance(parser.parse(self.sql), statement.Statement)

    def test_sets_name(self):
        self.assertEqual(parser.parse(self.sql).name, 'username_for_id')

    def test_command(self):
        self.assertIsInstance(parser.parse(self.sql).command, statement.Query)

    def test_result(self):
        self.assertIsInstance(parser.parse(self.sql).result, statement.One)
