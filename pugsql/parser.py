from . import lexer, statement
from more_itertools import split_at

# TODO query should be the default command

def parse(pugsql):
    stream = lexer.lex(pugsql)
    leading_comments, *rest = split_at(stream, lambda x: x[0] != 'C')

    cpr = parse_comments(leading_comments)

    return statement.Statement(
        name=cpr['name'],
        sql='TODO',
        doc=cpr['doc'],
        command=cpr['command'],
        result=cpr['result'])


def parse_comments(comments):
    cpr = {
        'name': None,
        'command': statement.Query(),
        'result': statement.Raw(),
        'doc': None,
    }

    for _, c in comments:
        consume_comment(cpr, c)

    return cpr


def consume_comment(cpr, c):
    toks = lexer.lex_comment(c)

    if toks['keyword'] == 'name':
        consume_name(cpr, toks)

    if toks['keyword'] == 'command':
        consume_command(cpr, toks)

    if toks['keyword'] == 'result':
        consume_result(cpr, toks)


def consume_command(cpr, tokens):
    if len(tokens['rest']) == 0:
        raise Exception('TODO')
    set_command(cpr, tokens['rest'])


def consume_result(cpr, tokens):
    if len(tokens['rest']) == 0:
        raise Exception('TODO')
    set_result(cpr, tokens['rest'])


def set_command(cpr, keyword):
    if keyword == ':query' or keyword == ':?':
        cpr['command'] = statement.Query()
    elif keyword == ':execute' or keyword == ':!':
        cpr['command'] = statement.Execute()
    elif keyword == ':returning-execute' or keyword == ':<!':
        cpr['command'] = statement.ReturningExecute()
    else:
        raise Exception('todo')


def consume_name(cpr, tokens):
    # TODO deal with no name
    name, keywords = lexer.lex_name(tokens['rest'])
    cpr['name'] = name

    if len(keywords) == 0:
        return

    set_command(cpr, keywords[0])

    if len(keywords) == 1:
        return

    set_result(cpr, keywords[1])


def set_result(cpr, keyword):
    if keyword == ':one' or keyword == ':1':
        cpr['result'] = statement.One()
    elif keyword == ':many' or keyword == ':*':
        cpr['result'] = statement.Many()
    elif keyword == ':affected' or keyword == ':n':
        cpr['result'] = statement.Affected()
    elif keyword != ':raw':
        raise Exception('todo')
