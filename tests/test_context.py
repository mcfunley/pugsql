from unittest import TestCase

from pugsql.context import Context, advance


class ContextTest(TestCase):
    def test_default_line(self):
        self.assertEqual(Context("<literal>").line, 0)

    def test_default_col(self):
        self.assertEqual(Context("<literal>").col, 1)

    def test_advance_col(self):
        self.assertEqual(advance(Context("<literal>"), cols=4).col, 5)

    def test_advance_lines(self):
        self.assertEqual(advance(Context("<literal>"), lines=2).line, 2)

    def test_advance_lines_from_indent(self):
        self.assertEqual(advance(Context("<literal>", col=3), lines=2).col, 1)
