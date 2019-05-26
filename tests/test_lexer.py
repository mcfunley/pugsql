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
            'Q',
            'select username from users where user_id = :user_id',
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
            'Q',
            'select username from users where user_id = :user_id',
             at(3, 1))
        self.assertEqual(
            [l1, l2, l3],
            lexer.lex(
                '-- :name username_for_id :1  \n'
                '\n'
                'select username from users where user_id = :user_id  ', ctx))


class LexCommentTest(TestCase):
    def tok(self, comment):
        return lexer.Token('C', comment, ctx)

    def test_no_keywords(self):
        self.assertIsNone(lexer.lex_comment(self.tok('-- foobar baz')))

    def test_not_a_comment(self):
        self.assertIsNone(lexer.lex_comment(self.tok('select 1')))

    def test_internal_keyword(self):
        self.assertIsNone(lexer.lex_comment(self.tok('-- stuff :foo bar')))

    def test_works(self):
        self.assertEqual({
            'keyword': ':foo',
            'rest': 'bar baz',
        }, lexer.lex_comment(self.tok('-- :foo bar baz')))

    def test_multiple_keywords(self):
        self.assertEqual({
            'keyword': ':foo',
            'rest': 'bar :baz',
        }, lexer.lex_comment(self.tok('-- :foo bar :baz')))

    def test_leading_whitespace(self):
        self.assertEqual({
            'keyword': ':foo',
            'rest': 'bar :baz',
        }, lexer.lex_comment(self.tok('--      :foo bar :baz')))
