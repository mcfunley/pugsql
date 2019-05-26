from pugsql import parser
from pugsql import statement
from unittest import TestCase


def sql(path):
    return open('tests/sql/%s.sql' % path, 'r').read()


def parse(path):
    return parser.parse(sql(path))


class SqlTests(TestCase):
    def test_query(self):
        self.assertEqual(
            parse('basic').sql,
            'select username from users where user_id = :user_id')

    def test_extra_comments(self):
        self.assertEqual(
            parse('extra-comments').sql,
            '-- some extra commentary\nselect * from foo where bar = :bar')


class BasicTest(TestCase):
    def test_returns_stmt(self):
        self.assertIsInstance(parse('basic'), statement.Statement)

    def test_sets_name(self):
        self.assertEqual(parse('basic').name, 'username_for_id')


class OneLinerTest(TestCase):
    def parse(self, path):
        return parse('oneliners/%s' % path)

    def test_name_only_raw(self):
        self.assertIsInstance(self.parse('default').result, statement.Raw)

    def test_name_only_name(self):
        self.assertEqual(self.parse('default').name, 'username_for_id')

    def test_short_one(self):
        self.assertIsInstance(self.parse('short-one').result, statement.One)

    def test_long_one(self):
        self.assertIsInstance(self.parse('long-one').result, statement.One)

    def test_short_affected(self):
        self.assertIsInstance(
            self.parse('short-affected').result, statement.Affected)

    def test_long_affected(self):
        self.assertIsInstance(
            self.parse('long-affected').result, statement.Affected)

    def test_short_many(self):
        self.assertIsInstance(self.parse('short-many').result, statement.Many)

    def test_long_many(self):
        self.assertIsInstance(self.parse('long-many').result, statement.Many)

    def test_long_raw(self):
        self.assertIsInstance(self.parse('long-raw').result, statement.Raw)


class MultilineTest(TestCase):
    def parse(self, path):
        return parse('multiline/%s' % path)

    def test_short_one(self):
        self.assertIsInstance(
            self.parse('short-one').result, statement.One)

    def test_long_one(self):
        self.assertIsInstance(
            self.parse('long-one').result, statement.One)

    def test_short_affected(self):
        self.assertIsInstance(
            self.parse('short-affected').result, statement.Affected)

    def test_long_affected(self):
        self.assertIsInstance(
            self.parse('long-affected').result, statement.Affected)

    def test_short_many(self):
        self.assertIsInstance(
            self.parse('short-many').result, statement.Many)

    def test_long_many(self):
        self.assertIsInstance(
            self.parse('long-many').result, statement.Many)

    def test_long_raw(self):
        self.assertIsInstance(
            self.parse('raw').result, statement.Raw)


class ParserErrorTest(TestCase):
    pass
