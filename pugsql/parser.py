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

    return cpr


def consume_comment(cpr, c):
    toks = lexer.lex_comment(c)

    if toks['keyword'] == 'name':
        consume_name(cpr, toks)


def consume_name(cpr, tokens):
    name, keywords = lexer.lex_name(tokens['rest'])
    cpr['name'] = name

    for k in keywords:
        # todo handle single-line
        pass
