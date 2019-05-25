from pugsql import statement
from unittest import TestCase


def test_raw():
    assert statement.Raw().transform('x') == 'x'


class StatementTest(TestCase):
    def test_no_engine(self):
        s = statement.Statement('foo', 'select 1', '', statement.Raw())
        self.assertRaises(RuntimeError, lambda: s())
