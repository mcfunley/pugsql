"""
Objects and methods used to keep track of positions in source files.
"""
from collections import namedtuple


_Context = namedtuple('Context', ['sqlfile', 'line', 'col'])


def Context(sqlfile, line=0, col=1):
    """
    Returns a context object, which is a named tuple with the following fields:

      * `sqlfile` - the path of the .sql file that is being processed.
      * `line` - the line number currently being processed.
      * `col` - the column number currently being processed.

    Context objects are not mutable. Use the `pugsql.context.advance` method or
    create new copies to change source context.
    """
    return _Context(sqlfile, line, col)


def advance(context, lines=0, cols=0):
    """
    Advances the provided context object to indicate a farther position in the
    same file. Passing `lines` advances lines, and passing `cols` advances
    columns.

    Returns a new Context object.

    When advancing `lines`, e.g.

        context.advance(ctx, lines=1)

    The current `cols` is reset to zero.
    """
    c = context.col + cols if lines == 0 else 1
    return _Context(context.sqlfile, context.line + lines, c)
