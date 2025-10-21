import sys
from unittest import TestCase

import pytest

from pugsql import compiler, exceptions, statement


class BasicCompilerTest(TestCase):
    def test_setsattr(self):
        m = compiler.Module("tests/sql")
        self.assertEqual(m.username_for_id.name, "username_for_id")

    def test_sets_sqlpaths(self):
        m = compiler.Module("tests/sql")
        self.assertEqual(
            {
                "tests/sql",
            },
            m.sqlpaths,
        )

    def test_function_redefinition(self):
        msg = (
            "Error loading tests/sql/duplicate-name/foo2.sql - a SQL function "
            "named foo was already defined in "
            "tests/sql/duplicate-name/foo.sql."
        )
        with pytest.raises(ValueError, match=msg):
            compiler.Module("tests/sql/duplicate-name")

    def test_reserved_function_name(self):
        msg = (
            "Error loading tests/sql/reserved/disconnect.sql - the function "
            'name "disconnect" is reserved. Please choose another name.'
        )
        with pytest.raises(ValueError, match=msg):
            compiler.Module("tests/sql/reserved")

    @pytest.mark.skipif(
        sys.version_info[:2] < (3, 10), reason="requires Python 3.10"
    )
    def test_filename_in_sql_header_comment(self):
        m = compiler.Module("tests/sql")
        self.assertEqual(
            m.username_for_id.sql,
            "-- pugsql function username_for_id in file "
            "\"tests/sql/basic.sql\" at line 1\n"
            "select username from users where user_id = :user_id"
        )
        self.assertEqual(
            m.multiline_syntax.sql,
            "-- pugsql function multiline_syntax in file "
            "\"tests/sql/multi-statement.sql\" at line 8\n"
            "select * from foo where bar = :bar;"
        )

    def test_multiple_statements_per_file(self):
        m = compiler.Module("tests/sql")
        self.assertEqual(m.basic_statement.name, "basic_statement")
        self.assertEqual(m.multiline_statement.name, "multiline_statement")
        self.assertEqual(m.extra_comments.name, "extra_comments")
        self.assertEqual(m.interstitial_comments.name, "interstitial_comments")
        self.assertEqual(m.multiline_syntax.name, "multiline_syntax")
        self.assertIsInstance(m.multiline_syntax.result, statement.Many)


class ModuleTest(TestCase):
    def test_dialect_no_connection(self):
        m = compiler.Module("tests/sql")
        with pytest.raises(exceptions.NoConnectionError):
            _ = m._dialect

    def test_dialect_works(self):
        m = compiler.Module("tests/sql")
        m.connect("sqlite:///./tests/data/fixtures.sqlite3")
        self.assertEqual(m._dialect.paramstyle, "qmark")

    def test_add_queries(self):
        m = compiler.Module("tests/sql/mod1")
        m.add_queries("tests/sql/mod2")
        self.assertEqual({"tests/sql/mod1", "tests/sql/mod2"}, m.sqlpaths)
        self.assertIsInstance(m.scalar, statement.Statement)
        self.assertIsInstance(m.insert, statement.Statement)
