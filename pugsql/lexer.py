"""
Functions that take strings and yield streams / dicts of tokens, keeping
track of source location.
"""
from . import context
from collections import namedtuple
import re


Token = namedtuple('Token', ['tag', 'value', 'context'])


def lex(pugsql, ctx):
    def generate(pugsql, ctx):
        for l in pugsql.splitlines():
            ctx = context.advance(ctx, lines=1)
            yield categorize(l, ctx)
    return list(generate(pugsql, ctx))


def categorize(line, ctx):
    ctx = context.advance(ctx, cols=len(line) - len(line.lstrip()))
    line = line.strip()

    if line.startswith('--'):
        return Token('C', line, ctx)
    return Token('Q', line, ctx)


def lex_comment(token):
    m = re.match(
        r'(?P<lead>--\s+)'
        r'(?P<keyword>\:[^ ]+)'
        r'(?P<internalws>\s+)?'
        r'(?P<rest>.*)?', token.value)

    if not m:
        return None

    d = m.groupdict()
    restbegin = sum(len(d[k] or '') for k in d.keys() if k != 'rest')

    return {
        'keyword': Token(
            'K',
            d['keyword'],
            context.advance(token.context, cols=len(d['lead']))),

        'rest': Token(
            'S',
            d['rest'],
            context.advance(token.context, cols=restbegin))
    }


def lex_name(nameline):
    name, *rest = re.split(r'\s+', nameline.strip())
    return name, [k for k in rest if k.startswith(':')]
