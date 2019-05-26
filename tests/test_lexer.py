from pugsql import lexer, context
from unittest import TestCase


ctx = context.Context('<literal>')


def at(l, c):
    return context.Context(ctx.sqlfile, l, c)


class LexTest(TestCase):
    def test_basic(self):
        l1 = lexer.Token('C', '-- :name username_for_id :1', at(1, 1))
        l2 = lexer.Token(
            'Q', 'select username from users where user_id = :user_id',
            at(2, 1))
        self.assertEqual(
            [l1, l2],
            lexer.lex(open('tests/sql/basic.sql', 'r').read(), ctx))

    def test_leading_comment_whitespace(self):
        l1 = lexer.Token('C', '-- :name username_for_id :1', at(1, 4))
        l2 = lexer.Token(
            'Q', 'select username from users where user_id = :user_id',
            at(2, 1))
        self.assertEqual(
            [l1, l2],
            lexer.lex(
                '   -- :name username_for_id :1\n'
                'select username from users where user_id = :user_id', ctx))

    def test_whitespace(self):
        l1 = lexer.Token('C', '-- :name username_for_id :1', at(1, 2))
        l2 = lexer.Token(
            'Q', 'select username from users where user_id = :user_id',
            at(2, 2))
        self.assertEqual(
            [l1, l2],
            lexer.lex(
                ' -- :name username_for_id :1  \n'
                ' select username from users where user_id = :user_id  ', ctx))

    def test_blank_lines(self):
        l1 = lexer.Token('C', '-- :name username_for_id :1', at(1, 1))
        l2 = lexer.Token('Q', '', at(2, 1))
        l3 = lexer.Token(
            'Q', 'select username from users where user_id = :user_id',
            at(3, 1))
        self.assertEqual(
            [l1, l2, l3],
            lexer.lex(
                '-- :name username_for_id :1  \n'
                '\n'
                'select username from users where user_id = :user_id  ', ctx))


class LexCommentTest(TestCase):
    def tok(self, comment):
        return lexer.Token('C', comment, at(1, 1))

    def test_no_keywords(self):
        self.assertIsNone(lexer.lex_comment(self.tok('-- foobar baz')))

    def test_not_a_comment(self):
        self.assertIsNone(lexer.lex_comment(self.tok('select 1')))

    def test_internal_keyword(self):
        self.assertIsNone(lexer.lex_comment(self.tok('-- stuff :foo bar')))

    def test_works(self):
        self.assertEqual({
            'keyword': lexer.Token('K', ':foo', at(1, 4)),
            'rest': lexer.Token('S', 'bar baz', at(1, 9)),
        }, lexer.lex_comment(self.tok('-- :foo bar baz')))

    def test_multiple_keywords(self):
        self.assertEqual({
            'keyword': lexer.Token('K', ':foo', at(1, 4)),
            'rest': lexer.Token('S', 'bar :baz', at(1, 9)),
        }, lexer.lex_comment(self.tok('-- :foo bar :baz')))

    def test_leading_whitespace(self):
        self.assertEqual({
            'keyword': lexer.Token('K', ':foo', at(1, 9)),
            'rest': lexer.Token('S', 'bar :baz', at(1, 14)),
        }, lexer.lex_comment(self.tok('--      :foo bar :baz')))

    def test_internal_whitespace(self):
        self.assertEqual({
            'keyword': lexer.Token('K', ':foo', at(1, 5)),
            'rest': lexer.Token('S', 'bar :baz', at(1, 12)),
        }, lexer.lex_comment(self.tok('--  :foo   bar :baz')))

    def test_keyword_only(self):
        self.assertEqual({
            'keyword': lexer.Token('K', ':foo', at(1, 4)),
            'rest': lexer.Token('S', '', at(1, 8)),
        }, lexer.lex_comment(self.tok('-- :foo')))

    def test_no_space(self):
        self.assertEqual({
            'keyword': lexer.Token('K', ':foo', at(1, 3)),
            'rest': lexer.Token('S', '', at(1, 7)),
        }, lexer.lex_comment(self.tok('--:foo')))


class LexNameTest(TestCase):
    def tok(self, rest):
        return lexer.Token('S', rest, at(1, 1))

    def test_name_only(self):
        self.assertEqual({
            'name': lexer.Token('N', 'foo', at(1, 1)),
            'keyword': lexer.Token('K', None, at(1, 4)),
            'rest': lexer.Token('S', None, at(1, 4)),
        }, lexer.lex_name(self.tok('foo')))

    def test_name_rest_no_keyword(self):
        self.assertEqual({
            'name': lexer.Token('N', 'foo', at(1, 1)),
            'keyword': lexer.Token('K', None, at(1, 5)),
            'rest': lexer.Token('S', 'other stuff', at(1, 5)),
        }, lexer.lex_name(self.tok('foo other stuff')))

    def test_with_keyword(self):
        self.assertEqual({
            'name': lexer.Token('N', 'foo', at(1, 1)),
            'keyword': lexer.Token('K', ':bar', at(1, 5)),
            'rest': lexer.Token('S', None, at(1, 9)),
        }, lexer.lex_name(self.tok('foo :bar')))

    def test_with_rest(self):
        self.assertEqual({
            'name': lexer.Token('N', 'foo', at(1, 1)),
            'keyword': lexer.Token('K', ':bar', at(1, 5)),
            'rest': lexer.Token('S', 'other stuff', at(1, 10)),
        }, lexer.lex_name(self.tok('foo :bar other stuff')))

    def test_leading_whitespace(self):
        self.assertEqual({
            'name': lexer.Token('N', 'foo', at(1, 4)),
            'keyword': lexer.Token('K', ':bar', at(1, 8)),
            'rest': lexer.Token('S', 'other stuff', at(1, 13)),
        }, lexer.lex_name(self.tok('   foo :bar other stuff')))

    def test_trailing_whitespace(self):
        self.assertEqual({
            'name': lexer.Token('N', 'foo', at(1, 4)),
            'keyword': lexer.Token('K', ':bar', at(1, 8)),
            'rest': lexer.Token('S', 'other stuff', at(1, 13)),
        }, lexer.lex_name(self.tok('   foo :bar other stuff   ')))

    def test_name_only_trailing_whitespace(self):
        self.assertEqual({
            'name': lexer.Token('N', 'foo', at(1, 1)),
            'keyword': lexer.Token('K', None, at(1, 4)),
            'rest': lexer.Token('S', None, at(1, 4)),
        }, lexer.lex_name(self.tok('foo    ')))

    def test_with_keyword_trailing_whitespace(self):
        self.assertEqual({
            'name': lexer.Token('N', 'foo', at(1, 1)),
            'keyword': lexer.Token('K', ':bar', at(1, 5)),
            'rest': lexer.Token('S', None, at(1, 9)),
        }, lexer.lex_name(self.tok('foo :bar    ')))

    def test_no_name(self):
        self.assertIsNone(lexer.lex_name(self.tok('   ')))

    def test_empty(self):
        self.assertIsNone(lexer.lex_name(self.tok('')))


class LexResultTest(TestCase):
    def tok(self, s):
        return lexer.Token('S', s, at(1, 1))

    def test_works(self):
        self.assertEqual({
            'keyword': lexer.Token('K', ':raw', at(1, 1)),
            'rest': lexer.Token('S', None, at(1, 5)),
        }, lexer.lex_result(self.tok(':raw')))

    def test_rest(self):
        self.assertEqual({
            'keyword': lexer.Token('K', ':raw', at(1, 1)),
            'rest': lexer.Token('S', ' stuff', at(1, 5)),
        }, lexer.lex_result(self.tok(':raw stuff')))

    def test_no_keyword(self):
        self.assertIsNone(lexer.lex_result(self.tok('thing')))
