from pugsql import statement
from unittest import TestCase
from unittest.mock import Mock


class StatementTest(TestCase):
    def test_sets_engine(self):
        eng = Mock()
        s = statement.Statement(
            name='foo',
            sql='sql',
            doc=None,
            command=Mock(),
            result=Mock())
        s.set_engine(eng)
        self.assertEqual(s.engine, eng)

    def test_works(self):
        conn = Mock()
        context = Mock(__enter__=Mock(return_value=conn), __exit__=Mock())
        eng = Mock(connect=Mock(return_value=context))

        s = statement.Statement(
            name='foo',
            sql='sql',
            doc=None,
            command=Mock(execute=Mock(return_value=[42,43])),
            result=Mock(transform=Mock(return_value=42)))
        s.set_engine(eng)

        r = s(x=1, y=2)

        s.command.execute.assert_called_once_with(conn, { 'x': 1, 'y': 2 })
        s.result.transform.assert_called_once_with([42, 43])
        self.assertEqual(r, 42)


def test_raw():
    assert statement.Raw().transform('x') == 'x'
