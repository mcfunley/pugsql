from getpass import getuser
import os
import pugsql
from unittest import TestCase


class PostgresqlTest(TestCase):
    def setUp(self):
        user = os.getenv('PGUSER') or getuser()
        pw = os.getenv('PGPASS')
        user_pass = user if pw is None else f'{user}:{pw}'
        self.fixtures = pugsql.module('tests/sql/postgres')
        self.fixtures.connect(f'postgresql+pg8000://{user_pass}@127.0.0.1')
        self.fixtures.setup()

    def test_multi_upsert(self):
        self.fixtures.multi_upsert([
            { 'id': 1, 'foo': 'abcd' },
            { 'id': 2, 'foo': '99999' },
            { 'id': 1000, 'foo': 'asdf' }])

        self.assertEqual('abcd', self.fixtures.get_foo(id=1))

        self.fixtures.multi_upsert([
            { 'id': 1, 'foo': 'xxxx' },
            { 'id': 7, 'foo': 'bloop' }
        ])

        self.assertEqual('xxxx', self.fixtures.get_foo(id=1))

    def test_where_in(self):
        self.fixtures.multi_upsert([
            { 'id': 1, 'foo': 'abcd' },
            { 'id': 2, 'foo': '99999' },
            { 'id': 1000, 'foo': 'asdf' }])

        ids = [r['id'] for r in self.fixtures.where_in(foo=('abcd', '99999',))]
        self.assertEqual({ 1, 2 }, set(ids))
