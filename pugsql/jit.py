"""
Pre-processes SQL right before its executed. This is necessary to support
certain features that depend on the dialect, which is not known in the first
parse/compile phase.
"""
import sqlparse


def compile(sql, dialect):
    """
    JIT-compiles the given raw SQL string. Returns a prepared statement,
    or None if no transformation is necessary.
    """
    jitted = _perform_substitutions(sqlparse.parse(sql), dialect)
    if jitted:
        return str(jitted)
    return None


def _perform_substitutions(parse_result, dialect):
    """
    Given a sqlparse parse result, does supported substitutions on any
    of the contained statements.

    Returns None if no substitutions were performed. Otherwise returns
    the new parse result, which can be unparsed into a prepared statement.
    """
    results = []
    found_sub = False
    for statement in parse_result:
        subst, st = _substitute(statement, dialect)
        found_sub = found_sub or subst
        results.append(st)
    return results if found_sub else None


def _substitute(statement, dialect):
    tpl, statement = _substitute_tuple(statement, dialect)
    return tpl, statement


def _substitute_tuple(statement, dialect):
    return False, statement
