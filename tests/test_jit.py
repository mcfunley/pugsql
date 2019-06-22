from pugsql import jit
from sqlalchemy import create_engine
from unittest import TestCase


dialect = create_engine('sqlite:///./tests/data/fixtures.sqlite3').dialect


class CompileTest(TestCase):
    def test_nothing_required(self):
        self.assertIsNone(
            jit.compile('select * from foo where bar = :bar',
                        dialect))
