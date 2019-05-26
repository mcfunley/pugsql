from . import lexer, statement, context
from .exceptions import ParserError
from itertools import takewhile


def parse(pugsql, ctx=None):
    ctx = ctx or context.Context('<literal>')

    stream = lexer.lex(pugsql, ctx)
    leading_comments = list(takewhile(lambda t: t.tag == 'C', stream))
    rest = stream[len(leading_comments):]

    cpr = parse_comments(leading_comments)
    sql = '\n'.join(cpr['unconsumed'] + [token.value for token in rest])

    return statement.Statement(
        name=cpr['name'],
        sql=sql,
        doc=cpr['doc'],
        result=cpr['result'],
        filename=ctx.sqlfile if ctx.sqlfile != '<literal>' else None)


def parse_comments(comments):
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
            consume_name(cpr, toks['rest'])
        elif toks['keyword'].value == ':result':
            consume_result(cpr, toks['rest'])
        else:
            cpr['unconsumed'].append(comment_token.value)

    return cpr


def consume_result(cpr, rest):
    if not rest.value:
        raise ParserError('expected keyword', rest)
    set_result(cpr, rest)


def consume_name(cpr, rest):
    tokens = lexer.lex_name(rest)
    if not tokens:
        raise ParserError('expected a query name.', rest)

    cpr['name'] = tokens['name'].value

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

    set_result(cpr, tokens['keyword'])


def set_result(cpr, ktok):
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
    elif keyword != ':raw':
        raise ParserError("unrecognized keyword '%s'" % keyword, ktok)
