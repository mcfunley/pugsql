"""
Code that processes SQL files and returns modules of database functions.
"""
from . import parser, context
from glob import glob
import os
from sqlalchemy import create_engine


__pdoc__ = {}


class Module(object):
    """
    Holds a set of SQL functions loaded from files.
    """
    sqlpath = None

    def __init__(self, sqlpath):
        """
        Loads functions found in the *sql files specified by `sqlpath` into
        properties on this object.

        The named sql functions in files should be unique.
        """
        if not os.path.isdir(sqlpath):
            raise ValueError('Directory not found: %s' % sqlpath)

        self.sqlpath = sqlpath
        self._statements = {}

        for sqlfile in glob(os.path.join(self.sqlpath, '*sql')):
            with open(sqlfile, 'r') as f:
                pugsql = f.read()
            s = parser.parse(pugsql, ctx=context.Context(sqlfile))

            if hasattr(self, s.name):
                raise ValueError(
                    'Error loading %s - a SQL function named %s was already '
                    'defined in %s.' % (
                        sqlfile, s.name, self._statements[s.name].filename))

            setattr(self, s.name, s)
            self._statements[s.name] = s

    def connect(self, connstr):
        """
        Sets the connection string for SQL functions on this module.

        See https://docs.sqlalchemy.org/en/13/core/engines.html for examples of
        legal connection strings for different databases.
        """
        self.set_engine(create_engine(connstr))

    def set_engine(self, engine):
        """
        Sets the SQLAlchemy engine for SQL functions on this module. This can
        be used instead of the connect method, when more customization of the
        connection engine is desired.

        See also: https://docs.sqlalchemy.org/en/13/core/connections.html
        """
        for s in self._statements.values():
            s.set_engine(engine)


__pdoc__['Module.sqlpath'] = (
    'The path that the `pugsql.compiler.Module` was loaded from.')


modules = {}


def _module(sqlpath):
    """
    Compiles a new `pugsql.compiler.Module`, or returns a cached one. Use the
    `pugsql.module` function instead of this one.
    """
    global modules
    if sqlpath not in modules:
        modules[sqlpath] = Module(sqlpath)
    return modules[sqlpath]
