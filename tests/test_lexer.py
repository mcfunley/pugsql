from pugsql import lexer, context
from unittest import TestCase


ctx = context.Context('<literal>')


def at(l, c):
    return context.Context(ctx.sqlfile, l, c)


class LexTest(TestCase):
    def test_basic(self):
        l1 = lexer.Token('-- :name username_for_id :1', at(1, 1))
        l2 = lexer.Token(
            'select username from users where user_id = :user_id',
            at(2, 1))
        self.assertEqual(
            [('C', l1), ('Q', l2),],
            lexer.lex(open('tests/sql/basic.sql', 'r').read(), ctx))

    def test_leading_comment_whitespace(self):
        l1 = lexer.Token('-- :name username_for_id :1', at(1, 4))
        l2 = lexer.Token(
            'select username from users where user_id = :user_id',
             at(2, 1))
        self.assertEqual(
            [('C', l1), ('Q', l2),],
            lexer.lex(
                '   -- :name username_for_id :1\n'
                'select username from users where user_id = :user_id', ctx))

    def test_whitespace(self):
        l1 = lexer.Token('-- :name username_for_id :1', at(1, 2))
        l2 = lexer.Token(
            'select username from users where user_id = :user_id',
            at(2, 2))
        expect = [('C', l1), ('Q', l2),]
        self.assertEqual(expect, lexer.lex(
            ' -- :name username_for_id :1  \n'
            ' select username from users where user_id = :user_id  ', ctx))

    def test_blank_lines(self):
        l1 = lexer.Token('-- :name username_for_id :1', at(1, 1))
        l2 = lexer.Token('', at(2, 1))
        l3 = lexer.Token(
            'select username from users where user_id = :user_id',
             at(3, 1))
        expect = [('C', l1), ('Q', l2), ('Q', l3),]
        self.assertEqual(expect, lexer.lex(
            '-- :name username_for_id :1  \n'
            '\n'
            'select username from users where user_id = :user_id  ', ctx))


class LexCommentTest(TestCase):
    pass
