from . import context
import re


def lex(pugsql, ctx):
    def generate(pugsql, ctx):
        for l in pugsql.splitlines():
            ctx = context.advance(ctx, lines=1)
            yield categorize(l, ctx)
    return list(generate(pugsql, ctx))


def categorize(line, ctx):
    ctx = context.advance(ctx, cols=len(line) - len(line.lstrip()))
    line = line.strip()
    return ('C', line, ctx) if line.startswith('--') else ('Q', line, ctx)


def lex_comment(c):
    m = re.match(
        r'--(?P<leading_whitespace>\s+)'
        r'\:(?P<keyword>[^ ]+)'
        r'\s+(?P<rest>.*)', c)
    return m.groupdict() if m else None


def lex_name(nameline):
    name, *rest = re.split(r'\s+', nameline.strip())
    return name, [k for k in rest if k.startswith(':')]
