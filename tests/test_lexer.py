from pugsql import lexer
from unittest import TestCase


class LexerTest(TestCase):
    def test_basic(self):
        self.assertEqual([
            ('C', '-- :name username_for_id :? :1'),
            ('Q', 'select username from users where user_id = :user_id'),
        ], lexer.lex(open('tests/sql/basic.sql', 'r').read()))
