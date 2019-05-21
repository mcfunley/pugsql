from . import lexer, statement
from more_itertools import split_at


def parse(pugsql):
    stream = lexer.lex(pugsql)
    leading_comments, *rest = split_at(stream, lambda x: x[0] != 'C')

    cpr = parse_comments(leading_comments)

    return statement.Statement(
        name=cpr['name'],
        sql='TK',
        doc=cpr['doc'],
        command=cpr['command'],
        result=cpr['result'])


def parse_comments(comments):
    cpr = {
        'name': None,
        'command': None,
        'result': None,
        'doc': None,
    }

    for _, c in comments:
        consume_comment(cpr, c)

    cpr.setdefault('result', statement.Raw())
    return cpr


def consume_comment(cpr, c):
    toks = lexer.lex_comment(c)

    if toks['keyword'] == 'name':
        consume_name(cpr, toks)


def consume_name(cpr, tokens):
    name, keywords = lexer.lex_name(tokens['rest'])
    cpr['name'] = name

    if len(keywords) == 0:
        return

    k = keywords[0]
    if k == ':query' or k == ':?':
        cpr['command'] = statement.Query()
    elif k == ':execute' or k == ':!':
        cpr['command'] = statement.Execute()
    elif k == ':returning-execute' or k == ':<!':
        cpr['command'] = statement.ReturningExecute()
    elif k == ':insert' or k == ':!':
        cpr['command'] = statement.Insert()
    else:
        raise Exception('todo')

    if len(keywords) == 1:
        return

    k = keywords[1]
    if k == ':one' or k == ':1':
        cpr['result'] = statement.One()
    elif k == ':many' or k == ':*':
        cpr['result'] = statement.Many()
    elif k == ':affected' or k == ':n':
        cpr['result'] = statement.Affected()
