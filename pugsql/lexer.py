"""
Functions that take strings and yield streams or dicts of `pugsql.lexer.Token`
objects, keeping track of source location.
"""

import re
from collections import namedtuple
from typing import Dict, Iterable, Optional, Tuple

from . import context

__pdoc__ = {}


Token = namedtuple("Token", ["tag", "value", "context"])
__pdoc__["Token"] = "A tagged string produced by the lexer."
__pdoc__["Token.tag"] = "A character indicating the meaning of the `value`."
__pdoc__["Token.value"] = "The string value of the `Token`."
__pdoc__["Token.context"] = (
    "A `pugsql.context.Context` for tracking source " "code information."
)


def lex(pugsql: str, ctx: context.Context) -> list[Token]:
    """
    Splits the provided multiline PugSQL string into Tokens.
    """

    def generate(pugsql: str, ctx: context.Context) -> Iterable[Token]:
        for line in pugsql.splitlines():
            ctx = context.advance(ctx, lines=1)
            yield _categorize(line, ctx)

    return list(generate(pugsql, ctx))


def _categorize(line, ctx) -> Token:
    line, ctx = _whitespace_advance(line, ctx)

    if line.startswith("--"):
        return Token("C", line, ctx)
    return Token("Q", line, ctx)


def lex_comment(token: Token) -> Optional[Dict[str, Token]]:
    m = re.match(
        r"(?P<lead>--+\s*)"
        r"(?P<keyword>\:[^ ]+)"
        r"(?P<internalws>\s+)?"
        r"(?P<rest>.*)?",
        token.value,
    )

    if not m:
        return None

    d = m.groupdict()
    restbegin = sum(len(d[k] or "") for k in d.keys() if k != "rest")

    return {
        "keyword": Token(
            "K",
            d["keyword"],
            context.advance(token.context, cols=len(d["lead"])),
        ),
        "rest": Token(
            "S", d["rest"], context.advance(token.context, cols=restbegin)
        ),
    }


def lex_name(token: Token) -> Optional[Dict[str, Token]]:
    line, ctx = _whitespace_advance(token.value, token.context)

    m = re.match(
        r"(?P<name>[^ ]+)"
        r"(?P<internalws>\s+)?"
        r"(?P<keyword>\:[^ ]+)?"
        r"(?P<internalws2>\s+)?"
        r"(?P<rest>.+)?",
        line,
    )

    if not m:
        return None

    d = m.groupdict()

    kwbegin = len(d["name"]) + len(d["internalws"] or "")
    kwctx = context.advance(ctx, cols=kwbegin)
    restbegin = sum(len(d[k] or "") for k in d.keys() if k != "rest")
    restctx = context.advance(ctx, cols=restbegin)
    return {
        "name": Token("N", d["name"], ctx),
        "keyword": Token("K", d["keyword"], kwctx),
        "rest": Token("S", d["rest"], restctx),
    }


def lex_result(token: Token) -> Optional[Dict[str, Token]]:
    line, ctx = _whitespace_advance(token.value, token.context)
    m = re.match(r"(?P<keyword>\:[^ ]+)" r"(?P<rest>.+)?", line)

    if not m:
        return None

    d = m.groupdict()
    restctx = context.advance(ctx, cols=len(d["keyword"]))

    return {
        "keyword": Token("K", d["keyword"], ctx),
        "rest": Token("S", d["rest"], restctx),
    }


def _whitespace_advance(
    line: str, ctx: context.Context
) -> Tuple[str, context.Context]:
    ctx = context.advance(ctx, cols=len(line) - len(line.lstrip()))
    return line.strip(), ctx
