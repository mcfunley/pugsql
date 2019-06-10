from pugsql import parser, exceptions
from pugsql.statement import Raw, Statement
import pytest
from unittest import TestCase
from unittest.mock import Mock


def test_raw():
    assert Raw().transform('x') == 'x'


class StatementTest(TestCase):
    def test_no_module(self):
        with pytest.raises(
                RuntimeError,
                match='This statement is not associated with a module'):
            s = Statement('foo', 'select 1', '', Raw())
            s()

    def test_no_name(self):
        with pytest.raises(ValueError, match='Statement must have a name.'):
            Statement(None, 'foo', '', Raw())

    def test_name_empty(self):
        with pytest.raises(ValueError, match='Statement must have a name.'):
            Statement('', 'foo', '', Raw())

    def test_sql_none(self):
        with pytest.raises(
                ValueError,
                match='Statement must have a SQL string.'):
            Statement('foo', None, '', Raw())

    def test_sql_empty(self):
        with pytest.raises(ValueError, match='SQL string cannot be empty.'):
            Statement('foo', '', '', Raw())

    def test_sql_whitespace(self):
        with pytest.raises(ValueError, match='SQL string cannot be empty.'):
            Statement('foo', '   ', '', Raw())

    def test_result_none(self):
        with pytest.raises(
                ValueError,
                match='Statement must have a result type.'):
            Statement('foo', 'select 1', '', None)

    def test_sets_module(self):
        m = Mock()
        s = Statement('foo', 'select 1', '', Raw())
        s.set_module(m)
        self.assertEqual(m, s._module)

    def test_filename(self):
        s = Statement('foo', 'select 1', '', Raw(), 'path/foobar.sql')
        self.assertEqual('path/foobar.sql', s.filename)


class StrTest(TestCase):
    def test_no_params(self):
        s = parser.parse('-- :name foo\nselect * from users')
        self.assertEqual('pugsql.statement.Statement: foo() :: raw', str(s))

    def test_repr(self):
        s = parser.parse('-- :name foo\nselect * from users')
        self.assertEqual('pugsql.statement.Statement: foo() :: raw', repr(s))

    def test_multiple_params(self):
        s = parser.parse(
            '-- :name foo\n'
            'select * from users where x=:x and y=:y')
        self.assertEqual(
            'pugsql.statement.Statement: foo(x=None, y=None) :: raw',
            str(s))

    def test_param_order(self):
        s = parser.parse(
            '-- :name foo\n'
            'select * from users where y=:y and z=:b and a=:a')
        self.assertEqual(
            'pugsql.statement.Statement: foo(y=None, b=None, a=None) :: raw',
            str(s))

    def test_row(self):
        s = parser.parse('-- :name foo :1\nselect * from users limit 1')
        self.assertEqual('pugsql.statement.Statement: foo() :: row', str(s))

    def test_rows(self):
        s = parser.parse('-- :name foo :*\nselect * from users')
        self.assertEqual('pugsql.statement.Statement: foo() :: rows', str(s))

    def test_rowcount(self):
        s = parser.parse('-- :name foo :affected\nselect * from users')
        self.assertEqual(
            'pugsql.statement.Statement: foo() :: rowcount',
            str(s))
