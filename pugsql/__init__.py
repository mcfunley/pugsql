"""
PugSQL is an anti-ORM that facilitates interacting with databases using SQL
in files. A minimal usage example:

    # create a module from sql files on disk
    queries = pugsql.module('path/to/sql/files')

    # connect to the database and use the sql queries as functions
    queries.connect(connection_string)
    queries.update_username(user_id=42, username='mcfunley')

"""
from . import compiler


__version__ = '0.1.11'


def module(sqlpath):
    """
    Compiles a set of SQL files in the directory specified by sqlpath, and
    returns a module. The module contains a function for each named query
    found in the files.

        # create a module from sql files on disk
        queries = pugsql.module('path/to/sql/files')

        # connect to the database and use the sql queries as functions
        queries.connect(connection_string)
        queries.update_username(user_id=42, username='mcfunley')

    The results of this function are cached, so multiple calls giving the same
    sqlpath are safe and return the same module object.
    """
    return compiler._module(sqlpath)


def get_modules():
    """
    Returns a dict of all modules currently loaded by pugsql. Clearing or
    otherwise modifying this dict will reset (or modify) the underlying data.

    For example, this call would reset pugsql so that repeated calls to
    `pugsql.module` will reload files from disk:

        pugsql.get_modules().clear()
    """
    return compiler.modules


__all__ = ['__version__', 'module', 'get_modules',]
