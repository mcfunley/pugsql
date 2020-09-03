from pugsql import compiler, exceptions, statement
import pytest
from unittest import TestCase


class BasicCompilerTest(TestCase):
    def test_setsattr(self):
        m = compiler.Module('tests/sql')
        self.assertEqual(m.username_for_id.name, 'username_for_id')

    def test_sets_sqlpath(self):
        m = compiler.Module('tests/sql')
        self.assertEqual('tests/sql', m.sqlpath)

    def test_function_redefinition(self):
        msg = (
            'Error loading tests/sql/duplicate-name/foo.sql - a SQL function '
            'named foo was already defined in '
            'tests/sql/duplicate-name/foo2.sql.')
        with pytest.raises(ValueError, match=msg):
            compiler.Module('tests/sql/duplicate-name')

    def test_reserved_function_name(self):
        msg = (
            'Error loading tests/sql/reserved/disconnect.sql - the function '
            'name "disconnect" is reserved. Please choose another name.')
        with pytest.raises(ValueError, match=msg):
            compiler.Module('tests/sql/reserved')

    def test_multiple_statements_per_file(self):
        m = compiler.Module('tests/sql')
        self.assertEqual(m.basic_statement.name, 'basic_statement')
        self.assertEqual(m.multiline_statement.name, 'multiline_statement')
        self.assertEqual(m.extra_comments.name, 'extra_comments')
        self.assertEqual(m.interstitial_comments.name, 'interstitial_comments')
        self.assertEqual(m.multiline_syntax.name, 'multiline_syntax')
        self.assertIsInstance(m.multiline_syntax.result, statement.Many)


class ModuleTest(TestCase):
    def test_dialect_no_connection(self):
        m = compiler.Module('tests/sql')
        with pytest.raises(exceptions.NoConnectionError):
            _ = m._dialect

    def test_dialect_works(self):
        m = compiler.Module('tests/sql')
        m.connect('sqlite:///./tests/data/fixtures.sqlite3')
        self.assertEqual(m._dialect.paramstyle, 'qmark')
