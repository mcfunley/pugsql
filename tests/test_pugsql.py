from pugsql import __version__, create_module, compiler
from unittest import TestCase


def test_version():
    assert __version__ == '0.1.0'


def test_create_module():
    compiler.modules.clear()
    assert create_module('tests/sql').sqlpath == 'tests/sql'



class PugsqlTest(TestCase):
    def setUp(self):
        compiler.modules.clear()
        self.fixtures = create_module('tests/sql/fixtures')
        self.fixtures.set_connection_string(
            'sqlite:///./tests/data/fixtures.sqlite3')

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
