"""
Pre-processes SQL right before its executed. This is necessary to support
certain features that depend on the dialect, which is not known in the first
parse/compile phase.
"""

def compile(sql):
    """
    JIT-compiles the given raw SQL string. Returns a prepared statement,
    or None if no transformation is necessary.
    """
    return None
