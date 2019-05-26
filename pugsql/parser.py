from . import lexer, statement, context
from itertools import takewhile


def parse(pugsql, ctx=None):
    ctx = ctx or context.Context('<literal>')

    stream = lexer.lex(pugsql, ctx)
    leading_comments = list(takewhile(lambda x: x[0] == 'C', stream))
    rest = stream[len(leading_comments):]

    cpr = parse_comments(leading_comments)
    sql = '\n'.join(cpr['unconsumed'] + [qtok.value for _, qtok in rest])

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

    for _, comment_token in comments:
        toks = lexer.lex_comment(comment_token)
        if not toks:
            cpr['unconsumed'].append(comment_token.value)
        elif toks['keyword'] == 'name':
            consume_name(cpr, toks)
        elif toks['keyword'] == 'result':
            consume_result(cpr, toks)
        else:
            cpr['unconsumed'].append(comment_token.value)

    return cpr


def consume_result(cpr, tokens):
    if len(tokens['rest']) == 0:
        raise Exception('TODO')
    set_result(cpr, tokens['rest'])


def consume_name(cpr, tokens):
    # TODO deal with no name
    name, keywords = lexer.lex_name(tokens['rest'])
    cpr['name'] = name

    if len(keywords) == 0:
        return

    set_result(cpr, keywords[0])


def set_result(cpr, keyword):
    if keyword == ':one' or keyword == ':1':
        cpr['result'] = statement.One()
    elif keyword == ':many' or keyword == ':*':
        cpr['result'] = statement.Many()
    elif keyword == ':affected' or keyword == ':n':
        cpr['result'] = statement.Affected()
    elif keyword != ':raw':
        raise Exception('todo')
