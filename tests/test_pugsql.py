from pugsql import module, compiler
import pytest
from unittest import TestCase


def test_module():
    compiler.modules.clear()
    assert module('tests/sql').sqlpath == 'tests/sql'


class PugsqlTest(TestCase):
    def setUp(self):
        compiler.modules.clear()
        self.fixtures = module('tests/sql/fixtures')
        self.fixtures.connect('sqlite:///./tests/data/fixtures.sqlite3')

    def test_get_one(self):
        self.assertEqual(
            { 'username': 'mcfunley', 'user_id': 1 },
            self.fixtures.user_for_id(user_id=1))

    def test_many(self):
        self.assertEqual(
            [{ 'username': 'oscar', 'user_id': 2 },],
            list(self.fixtures.search_users(username='oscar')))

    def test_update(self):
        self.assertEqual(
            1,
            self.fixtures.update_username(user_id=3, username='dottie'))

    def test_insert(self):
        pk = self.fixtures.insert_user(username='little_pug')
        self.assertEqual(
            {'username': 'little_pug', 'user_id': pk},
            self.fixtures.user_for_id(user_id=pk))

    def test_bad_path(self):
        with pytest.raises(
                ValueError,
                match='Directory not found: does/not/exist'):
            module('does/not/exist')

    def test_empty_many(self):
        self.assertEqual(
            [],
            list(self.fixtures.search_users(username='asdfjasdj')))

    def test_null_one(self):
        self.assertIsNone(self.fixtures.user_for_id(user_id=4123423))
