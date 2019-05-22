from pugsql import parser
from pugsql import statement
from unittest import TestCase, skip


def sql(path):
    return open('tests/sql/%s.sql' % path, 'r').read()

def parse(path):
    return parser.parse(sql(path))


class BasicTest(TestCase):
    def test_returns_stmt(self):
        self.assertIsInstance(parse('basic'), statement.Statement)

    def test_sets_name(self):
        self.assertEqual(parse('basic').name, 'username_for_id')


class OneLinerTest(TestCase):
    def parse(self, path):
        return parse('oneliners/%s' % path)

    def test_short_query(self):
        self.assertIsInstance(
            self.parse('short-query-short-one').command, statement.Query)

    def test_short_one(self):
        self.assertIsInstance(
            self.parse('short-query-short-one').result, statement.One)

    def test_long_query(self):
        self.assertIsInstance(
            self.parse('long-query-long-one').command, statement.Query)

    def test_long_one(self):
        self.assertIsInstance(
            self.parse('long-query-long-one').result, statement.One)

    def test_short_execute(self):
        self.assertIsInstance(
            self.parse('short-exec-short-affected').command, statement.Execute)

    def test_short_affected(self):
        self.assertIsInstance(
            self.parse('short-exec-short-affected').result, statement.Affected)

    def test_long_execute(self):
        self.assertIsInstance(
            self.parse('long-exec-long-affected').command, statement.Execute)

    def test_long_affected(self):
        self.assertIsInstance(
            self.parse('long-exec-long-affected').result, statement.Affected)

    def test_short_many(self):
        self.assertIsInstance(
            self.parse('short-query-short-many').result, statement.Many)

    def test_long_many(self):
        self.assertIsInstance(
            self.parse('long-query-long-many').result, statement.Many)

    def test_raw_default(self):
        self.assertIsInstance(
            self.parse('long-query-default').result, statement.Raw)

    def test_long_raw(self):
        self.assertIsInstance(
            self.parse('long-query-raw').result, statement.Raw)


class MultilineTest(TestCase):
    def parse(self, path):
        return parse('multiline/%s' % path)

    def test_short_query(self):
        self.assertIsInstance(
            self.parse('short-query-short-one').command, statement.Query)

    def test_short_one(self):
        self.assertIsInstance(
            self.parse('short-query-short-one').result, statement.One)

    def test_long_query(self):
        self.assertIsInstance(
            self.parse('long-query-long-one').command, statement.Query)

    def test_long_one(self):
        self.assertIsInstance(
            self.parse('long-query-long-one').result, statement.One)

    def test_short_execute(self):
        self.assertIsInstance(
            self.parse('short-exec-short-affected').command, statement.Execute)

    def test_short_affected(self):
        self.assertIsInstance(
            self.parse('short-exec-short-affected').result, statement.Affected)

    def test_long_execute(self):
        self.assertIsInstance(
            self.parse('long-exec-long-affected').command, statement.Execute)

    def test_long_affected(self):
        self.assertIsInstance(
            self.parse('long-exec-long-affected').result, statement.Affected)

    def test_short_many(self):
        self.assertIsInstance(
            self.parse('short-query-short-many').result, statement.Many)

    def test_long_many(self):
        self.assertIsInstance(
            self.parse('long-query-long-many').result, statement.Many)

    def test_raw_default(self):
        self.assertIsInstance(
            self.parse('long-query-default').result, statement.Raw)

    def test_long_raw(self):
        self.assertIsInstance(
            self.parse('long-query-raw').result, statement.Raw)
