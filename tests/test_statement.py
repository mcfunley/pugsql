from pugsql import statement
from unittest import TestCase
from unittest.mock import Mock


def test_raw():
    assert statement.Raw().transform('x') == 'x'
