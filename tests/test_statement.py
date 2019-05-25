from pugsql import statement


def test_raw():
    assert statement.Raw().transform('x') == 'x'
