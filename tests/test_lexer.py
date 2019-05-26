from pugsql import lexer, context
from unittest import TestCase


ctx = context.Context('<literal>')


def at(l, c):
    return context.Context(ctx.sqlfile, l, c)


class LexTest(TestCase):
    def test_basic(self):
        self.assertEqual([
            ('C', '-- :name username_for_id :1', at(1, 1)),
            ('Q', 'select username from users where user_id = :user_id',
             at(2, 1)),
        ], lexer.lex(open('tests/sql/basic.sql', 'r').read(), ctx))

    def test_leading_comment_whitespace(self):
        self.assertEqual([
            ('C', '-- :name username_for_id :1', at(1, 4)),
            ('Q', 'select username from users where user_id = :user_id',
             at(2, 1)),
        ], lexer.lex(
            '   -- :name username_for_id :1\n'
            'select username from users where user_id = :user_id', ctx))

    def test_whitespace(self):
        expect = [
            ('C', '-- :name username_for_id :1', at(1, 2)),
            ('Q', 'select username from users where user_id = :user_id',
             at(2, 2)),
        ]
        self.assertEqual(expect, lexer.lex(
            ' -- :name username_for_id :1  \n'
            ' select username from users where user_id = :user_id  ', ctx))

    def test_blank_lines(self):
        expect = [
            ('C', '-- :name username_for_id :1', at(1, 1)),
            ('Q', '', at(2, 1)),
            ('Q', 'select username from users where user_id = :user_id',
             at(3, 1)),
        ]
        self.assertEqual(expect, lexer.lex(
            '-- :name username_for_id :1  \n'
            '\n'
            'select username from users where user_id = :user_id  ', ctx))
