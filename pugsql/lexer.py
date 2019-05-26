from . import context
from collections import namedtuple
import re


Token = namedtuple('Token', ['value', 'context'])


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
        return ('C', Token(line, ctx))
    return ('Q', Token(line, ctx))


def lex_comment(token):
    m = re.match(
        r'--(?P<leading_whitespace>\s+)'
        r'\:(?P<keyword>[^ ]+)'
        r'\s+(?P<rest>.*)', token.value)
    return m.groupdict() if m else None


def lex_name(nameline):
    name, *rest = re.split(r'\s+', nameline.strip())
    return name, [k for k in rest if k.startswith(':')]
