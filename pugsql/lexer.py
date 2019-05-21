import re


def lex(pugsql):
    return compress([categorize(l) for l in pugsql.splitlines()])


def categorize(line):
    line = line.strip()
    return ('C', line) if line.startswith('--') else ('Q', line)


def compress(stream):
    return stream


def lex_comment(c):
    m = re.match(
        r'--(?P<leading_whitespace>\s+)'
        r'\:(?P<keyword>[^ ]+)'
        r'\s+(?P<rest>.*)', c)
    return m.groupdict() if m else None


def lex_name(nameline):
    name, *rest = re.split('\s+', nameline.strip())
    return name, [k for k in rest if k.startswith(':')]
