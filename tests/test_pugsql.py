import pugsql
from pugsql import exceptions
import pytest
import threading
from unittest import TestCase


def test_module():
    assert pugsql.module('tests/sql').sqlpaths == {'tests/sql',}


class PugsqlTest(TestCase):
    def setUp(self):
        self.fixtures = pugsql.module('tests/sql/fixtures')
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

    def test_where_in(self):
        result = self.fixtures.find_by_usernames(usernames=('oscar', 'dottie'))
        self.assertEqual(
            [{'user_id': 2, 'username': 'oscar'},
             {'user_id': 3, 'username': 'dottie'}],
            list(result))

    def test_where_in_list(self):
        result = self.fixtures.find_by_usernames(usernames=['oscar', 'dottie'])
        self.assertEqual(
            [{'user_id': 2, 'username': 'oscar'},
             {'user_id': 3, 'username': 'dottie'}],
            list(result))

    def test_where_in_set(self):
        result = self.fixtures.find_by_usernames(usernames={'oscar', 'dottie'})
        self.assertEqual(
            [{'user_id': 2, 'username': 'oscar'},
             {'user_id': 3, 'username': 'dottie'}],
            list(result))

    def test_where_in_multiple_parameters(self):
        result = self.fixtures.find_by_username_or_id(
            user_id=1,
            usernames=('oscar', 'dottie'))
        self.assertEqual(
            [{'user_id': 1, 'username': 'mcfunley'},
             {'user_id': 2, 'username': 'oscar'},
             {'user_id': 3, 'username': 'dottie'}],
            list(result))

    def test_multi_insert(self):
        with self.fixtures.transaction() as t:
            self.fixtures.insert_user(
                { 'username': 'joe' },
                { 'username': 'paul' },
                { 'username': 'topper' },
                { 'username': 'mick' })

            sr = list(self.fixtures.search_users(username='topper'))
            self.assertEqual('topper', sr[0]['username'])
            t.rollback()

    def test_insert(self):
        with self.fixtures.transaction() as t:
            pk = self.fixtures.insert_user(username='little_pug')
            self.assertEqual(
                {'username': 'little_pug', 'user_id': pk},
                self.fixtures.user_for_id(user_id=pk))
            t.rollback()

    def test_scalar(self):
        self.assertEqual('mcfunley', self.fixtures.username_for_id(user_id=1))

    def test_scalar_null(self):
        self.assertIsNone(self.fixtures.username_for_id(user_id=666))

    def test_bad_path(self):
        with pytest.raises(
                ValueError,
                match='Directory not found: does/not/exist'):
            pugsql.module('does/not/exist')

    def test_empty_many(self):
        self.assertEqual(
            [],
            list(self.fixtures.search_users(username='asdfjasdj')))

    def test_null_one(self):
        self.assertIsNone(self.fixtures.user_for_id(user_id=4123423))

    def test_rolling_back_transaction(self):
        class FooException(RuntimeError):
            pass

        try:
            with self.fixtures.transaction():
                self.fixtures.update_username(user_id=1, username='foo')
                self.assertEqual(
                    { 'username': 'foo', 'user_id': 1 },
                    self.fixtures.user_for_id(user_id=1))

                raise FooException()
        except FooException:
            pass

        self.assertEqual(
            { 'username': 'mcfunley', 'user_id': 1 },
            self.fixtures.user_for_id(user_id=1))

    def test_nesting_transactions(self):
        with self.fixtures.transaction():
            with self.fixtures.transaction():
                self.assertEqual(
                    { 'username': 'mcfunley', 'user_id': 1 },
                    self.fixtures.user_for_id(user_id=1))

    def test_transaction_not_connected(self):
        fixtures = pugsql.module('tests/sql/fixtures')
        fixtures.disconnect()
        with pytest.raises(exceptions.NoConnectionError):
            with fixtures.transaction():
                pass

    def test_not_connected(self):
        fixtures = pugsql.module('tests/sql/fixtures')
        fixtures.disconnect()
        with pytest.raises(exceptions.NoConnectionError):
            fixtures.user_for_id(user_id=1)

    def test_initialized_other_thread(self):
        self.fixtures = None

        def init():
            self.fixtures = pugsql.module('tests/sql/fixtures')
            self.fixtures.connect('sqlite:///./tests/data/fixtures.sqlite3')

        t = threading.Thread(target=init)
        t.start()
        t.join()

        self.assertEqual(
            { 'username': 'mcfunley', 'user_id': 1 },
            self.fixtures.user_for_id(user_id=1))

    def test_iterable(self):
        self.assertEqual(
            {
                self.fixtures.find_by_username_or_id,
                self.fixtures.find_by_usernames,
                self.fixtures.insert_user,
                self.fixtures.search_users,
                self.fixtures.update_username,
                self.fixtures.user_for_id,
                self.fixtures.username_for_id,
                self.fixtures.find_date,
            },
            set(q for q in self.fixtures)
        )

    def test_pass_connect_args(self):
        import sqlite3
        from datetime import datetime

        self.fixtures.disconnect()
        self.fixtures.connect(
            'sqlite:///./tests/data/fixtures.sqlite3',
            connect_args={'detect_types': sqlite3.PARSE_DECLTYPES})
        date = self.fixtures.find_date(id=1)
        self.assertIs(datetime, type(date['created']))

    def test_positional_args_mistake(self):
        with pytest.raises(
                exceptions.InvalidArgumentError,
                match='Pass keyword arguments to statements'):
            self.fixtures.find_by_username_or_id(
                1, ('oscar', 'dottie'))

    def test_three_dashes(self):
        pytest.skip('fails - see issue #13')
        pugsql.module('tests/sql/extra-dashes')
