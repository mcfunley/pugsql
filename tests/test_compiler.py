from pugsql import compiler
import pytest
from unittest import TestCase


class BasicCompilerTest(TestCase):
    def setUp(self):
        compiler.modules.clear()

    def test_setsattr(self):
        m = compiler._module('tests/sql')
        self.assertEqual(m.username_for_id.name, 'username_for_id')

    def test_sets_sqlpath(self):
        m = compiler._module('tests/sql')
        self.assertEqual('tests/sql', m.sqlpath)

    def test_caches_modules(self):
        self.assertEqual(
            compiler._module('tests/sql'),
            compiler._module('tests/sql'))

    def test_function_redefinition(self):
        msg = (
            'Error loading tests/sql/duplicate-name/foo.sql - a SQL function '
            'named foo was already defined in '
            'tests/sql/duplicate-name/foo2.sql.')
        with pytest.raises(ValueError, match=msg):
            compiler._module('tests/sql/duplicate-name')
