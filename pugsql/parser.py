"""
Code that consumes PugSQL-dialect sql strings and returns validated
`pugsql.statement.Statement` objects.
"""
from . import lexer, statement, context
from .exceptions import ParserError
from itertools import takewhile
import re


def parse(pugsql, ctx=None):
    """
    Processes the SQL string given in `pugsql` and returns a valid
    `pugsql.statement.Statement` object.

    Will raise a `pugsql.exceptions.ParserError` in any number of cases in
    which the PugSQL metadata isn't valid. However, this does not parse and
    validate the SQL statement.

    `ctx` is a context object provided by the `pugsql.context.Context`
    function, or `None`. If it is `None` a default context is created which
    will indicate that the SQL is being parsed from a literal string.
    """
    ctx = ctx or context.Context('<literal>')

    stream = lexer.lex(pugsql, ctx)
    leading_comments = list(takewhile(lambda t: t.tag == 'C', stream))
    rest = stream[len(leading_comments):]

    cpr = _parse_comments(leading_comments)
    sql = '\n'.join(cpr['unconsumed'] + [token.value for token in rest])

    return statement.Statement(
        name=cpr['name'],
        sql=sql,
        doc=cpr['doc'],
        result=cpr['result'],
        filename=ctx.sqlfile if ctx.sqlfile != '<literal>' else None)


def _parse_comments(comments):
    cpr = {
        'name': None,
        'result': statement.Raw(),
        'doc': None,
        'unconsumed': [],
    }

    for comment_token in comments:
        toks = lexer.lex_comment(comment_token)
        if not toks:
            cpr['unconsumed'].append(comment_token.value)
        elif toks['keyword'].value == ':name':
            _consume_name(cpr, toks['rest'])
        elif toks['keyword'].value == ':result':
            _consume_result(cpr, toks['rest'])
        else:
            cpr['unconsumed'].append(comment_token.value)

    return cpr


def _consume_result(cpr, rest):
    if not rest.value:
        raise ParserError('expected keyword', rest)
    _set_result(cpr, rest)


def _consume_name(cpr, rest):
    tokens = lexer.lex_name(rest)
    if not tokens:
        raise ParserError('expected a query name.', rest)

    name = tokens['name'].value
    if not _is_legal_name(name):
        raise ParserError(
            "'%s' is not a legal Python function name." % name,
            tokens['name'])

    cpr['name'] = name

    if not tokens['keyword'].value:
        if tokens['rest'].value:
            raise ParserError(
                'encountered unexpected input after query name.',
                tokens['rest'])
        return

    if tokens['rest'].value:
        raise ParserError(
            'encountered unexpected input after result type.',
            tokens['rest'])

    _set_result(cpr, tokens['keyword'])


def _set_result(cpr, ktok):
    tokens = lexer.lex_result(ktok)
    if not tokens:
        raise ParserError('expected keyword', ktok)

    if tokens['rest'].value:
        raise ParserError(
            'encountered unexpected input after result type',
            tokens['rest'])

    keyword = tokens['keyword'].value

    if keyword == ':one' or keyword == ':1':
        cpr['result'] = statement.One()
    elif keyword == ':many' or keyword == ':*':
        cpr['result'] = statement.Many()
    elif keyword == ':affected' or keyword == ':n':
        cpr['result'] = statement.Affected()
    elif keyword == ':insert':
        cpr['result'] = statement.Insert()
    elif keyword != ':raw':
        raise ParserError("unrecognized keyword '%s'" % keyword, ktok)


def _is_legal_name(value):
    return re.match(r'^[a-zA-Z_][a-zA-Z0-9_]+$', value) is not None
