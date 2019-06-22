from pugsql import jit
from unittest import TestCase


class CompileTest(TestCase):
    def test_nothing_required(self):
        self.assertIsNone(jit.compile('select * from foo where bar = :bar'))
