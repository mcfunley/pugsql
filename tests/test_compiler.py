from pugsql import compiler
from unittest import TestCase


class BasicCompilerTest(TestCase):
    def setUp(self):
        compiler.modules.clear()

    def test_setsattr(self):
        m = compiler.module('tests/sql')
        self.assertEqual(m.username_for_id.name, 'username_for_id')

    def test_sets_sqlpath(self):
        m = compiler.module('tests/sql')
        self.assertEqual('tests/sql', m.sqlpath)

    def test_caches_modules(self):
        self.assertEqual(
            compiler.module('tests/sql'),
            compiler.module('tests/sql'))
