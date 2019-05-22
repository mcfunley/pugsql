from pugsql import __version__, create_module, compiler


def test_version():
    assert __version__ == '0.1.0'


def test_create_module():
    compiler.modules.clear()
    assert create_module('tests/sql').sqlpath == 'tests/sql'
