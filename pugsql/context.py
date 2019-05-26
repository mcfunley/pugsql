from collections import namedtuple


_Context = namedtuple('Context', ['sqlfile', 'line', 'col'])


def Context(sqlfile, line=0, col=1):
    return _Context(sqlfile, line, col)


def advance(context, lines=0, cols=0):
    c = context.col + cols if lines == 0 else 1
    return _Context(context.sqlfile, context.line + lines, c)
