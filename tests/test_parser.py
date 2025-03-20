import sys
from unittest import TestCase

import pytest

from pugsql import parser, statement
from pugsql.exceptions import ParserError


def sql(path):
    return open("tests/sql/%s.sql" % path, "r").read()


def parse(path):
    return parser.parse(sql(path))


class SqlTests(TestCase):
    @pytest.mark.skipif(
        sys.version_info[:2] < (3, 10), reason="requires Python 3.10"
    )
    def test_query(self):
        self.assertEqual(
            parse("basic").sql,
            "-- pugsql function username_for_id in file <literal>\n"
            "select username from users where user_id = :user_id",
        )

    @pytest.mark.skipif(
        sys.version_info[:2] < (3, 10), reason="requires Python 3.10"
    )
    def test_extra_comments(self):
        self.assertEqual(
            parse("extra-comments").sql,
            "-- pugsql function foobar in file <literal>\n"
            "-- some extra commentary\nselect * from foo where bar = :bar",
        )


class BasicTest(TestCase):
    def test_returns_stmt(self):
        self.assertIsInstance(parse("basic"), statement.Statement)

    def test_sets_name(self):
        self.assertEqual(parse("basic").name, "username_for_id")


class OneLinerTest(TestCase):
    def parse(self, path):
        return parse("oneliners/%s" % path)

    def test_name_only_raw(self):
        self.assertIsInstance(self.parse("default").result, statement.Raw)

    def test_name_only_name(self):
        self.assertEqual(self.parse("default").name, "username_for_id")

    def test_short_one(self):
        self.assertIsInstance(self.parse("short-one").result, statement.One)

    def test_long_one(self):
        self.assertIsInstance(self.parse("long-one").result, statement.One)

    def test_short_affected(self):
        self.assertIsInstance(
            self.parse("short-affected").result, statement.Affected
        )

    def test_long_affected(self):
        self.assertIsInstance(
            self.parse("long-affected").result, statement.Affected
        )

    def test_short_many(self):
        self.assertIsInstance(self.parse("short-many").result, statement.Many)

    def test_long_many(self):
        self.assertIsInstance(self.parse("long-many").result, statement.Many)

    def test_long_raw(self):
        self.assertIsInstance(self.parse("long-raw").result, statement.Raw)

    def test_insert(self):
        self.assertIsInstance(self.parse("insert").result, statement.Insert)

    def test_scalar(self):
        self.assertIsInstance(self.parse("scalar").result, statement.Scalar)


class MultilineTest(TestCase):
    def parse(self, path):
        return parse("multiline/%s" % path)

    def test_short_one(self):
        self.assertIsInstance(self.parse("short-one").result, statement.One)

    def test_long_one(self):
        self.assertIsInstance(self.parse("long-one").result, statement.One)

    def test_short_affected(self):
        self.assertIsInstance(
            self.parse("short-affected").result, statement.Affected
        )

    def test_long_affected(self):
        self.assertIsInstance(
            self.parse("long-affected").result, statement.Affected
        )

    def test_short_many(self):
        self.assertIsInstance(self.parse("short-many").result, statement.Many)

    def test_long_many(self):
        self.assertIsInstance(self.parse("long-many").result, statement.Many)

    def test_long_raw(self):
        self.assertIsInstance(self.parse("raw").result, statement.Raw)

    def test_insert(self):
        self.assertIsInstance(self.parse("insert").result, statement.Insert)

    def test_scalar(self):
        self.assertIsInstance(self.parse("scalar").result, statement.Scalar)

    def test_has_commentary(self):
        s = self.parse("has-commentary")
        self.assertIsInstance(s.result, statement.Scalar)
        self.assertEqual(s.name, "has_commentary")

    def test_has_commentary_whitespace(self):
        s = self.parse("has-commentary-whitespace")
        self.assertIsInstance(s.result, statement.Scalar)
        self.assertEqual(s.name, "has_commentary_whitespace")


class ParserErrorTest(TestCase):
    def test_no_name(self):
        msg = "Error in <literal>:1:9 - expected a query name."
        with pytest.raises(ParserError, match=msg):
            parser.parse("-- :name \n" "select 1;")

    def test_name_only_extra(self):
        msg = (
            "Error in <literal>:1:14 - encountered "
            "unexpected input after query name."
        )
        with pytest.raises(ParserError, match=msg):
            parser.parse("-- :name foo and some other stuff\n" "select 1")

    def test_extra_after_result_nameline(self):
        msg = (
            "Error in <literal>:1:24 - encountered "
            "unexpected input after result type."
        )
        with pytest.raises(ParserError, match=msg):
            parser.parse("-- :name foo :affected things\n" "select 1")

    def test_unrecognized_keyword_nameline(self):
        msg = "Error in <literal>:1:14 - unrecognized keyword ':wrong'"
        with pytest.raises(ParserError, match=msg):
            parser.parse("-- :name foo :wrong\n" "select 1")

    def test_unrecognized_keyword_resultline(self):
        msg = "Error in <literal>:2:12 - unrecognized keyword ':nope'"
        with pytest.raises(ParserError, match=msg):
            parser.parse("-- :name foo\n" "-- :result :nope\n" "select 1")

    def test_missing_result_type_result_line(self):
        msg = "Error in <literal>:2:11 - expected keyword"
        with pytest.raises(ParserError, match=msg):
            parser.parse("-- :name foo\n" "-- :result \n" "select 1")

    def test_result_type_not_keyword_result_line(self):
        msg = r"Error in <literal>:2:12 - expected keyword"
        with pytest.raises(ParserError, match=msg):
            parser.parse("-- :name foo\n" "-- :result raw\n" "select 1")

    def test_extra_after_result_result_line(self):
        msg = (
            "Error in <literal>:2:16 - encountered unexpected input after "
            "result type"
        )
        with pytest.raises(ParserError, match=msg):
            parser.parse("-- :name foo\n" "-- :result :raw thing\n" "select 1")


class ResultLineWhitespaceTest(TestCase):
    def test_works_leading_whitespace(self):
        s = parser.parse("-- :name foo\n" "--   :result :1\n" "select 1")
        self.assertIsInstance(s.result, statement.One)

    def test_works_trailing_whitespace(self):
        s = parser.parse("-- :name foo\n" "--   :result :1   \n" "select 1")
        self.assertIsInstance(s.result, statement.One)

    def test_works_internal_whitespace(self):
        s = parser.parse(
            "-- :name foo\n" "--   :result     :1   \n" "select 1"
        )
        self.assertIsInstance(s.result, statement.One)


class LegalFunctionNameTest(TestCase):
    def errmsg(self, name):
        return (
            "Error in <literal>:1:10 - '%s' is not a legal Python "
            "function name." % name
        )

    def test_nonalphaunderscore(self):
        with pytest.raises(ParserError, match=self.errmsg("foo#")):
            parser.parse("-- :name foo#\n" "select 1")

    def test_begins_with_number(self):
        with pytest.raises(ParserError, match=self.errmsg("9foo")):
            parser.parse("-- :name 9foo\n" "select 1")

    def test_dashes(self):
        with pytest.raises(ParserError, match=self.errmsg("foo-bar")):
            parser.parse("-- :name foo-bar\n" "select 1")

    def test_numbers(self):
        s = parser.parse("-- :name foo1\n" "select 1")
        self.assertEqual("foo1", s.name)

    def test_underscores(self):
        s = parser.parse("-- :name foo_bar\n" "select 1")
        self.assertEqual("foo_bar", s.name)

    def test_leading_underscores(self):
        s = parser.parse("-- :name _foo_bar\n" "select 1")
        self.assertEqual("_foo_bar", s.name)

    def test_uppercase(self):
        s = parser.parse("-- :name _FOO_BAR\n" "select 1")
        self.assertEqual("_FOO_BAR", s.name)
