"""
Code that processes SQL files and returns modules of database functions.
"""
from . import parser, context
from .exceptions import NoConnectionError
from contextlib import contextmanager
from glob import glob
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import threading


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

        self._engine = None
        self._sessionmaker = None

        self._locals = threading.local()

        for sqlfile in glob(os.path.join(self.sqlpath, '*sql')):
            with open(sqlfile, 'r') as f:
                pugsql = f.read()
            s = parser.parse(pugsql, ctx=context.Context(sqlfile))

            if hasattr(self, s.name):
                raise ValueError(
                    'Error loading %s - a SQL function named %s was already '
                    'defined in %s.' % (
                        sqlfile, s.name, self._statements[s.name].filename))

            s.set_module(self)

            setattr(self, s.name, s)
            self._statements[s.name] = s

    @contextmanager
    def transaction(self):
        """
        Returns a session that manages a transaction scope, in which
        many statements can be run. Statements run on this module will
        automatically use this transaction. The normal use case  is to use this
        like a context manager, rather than interact with the result:

            foo = pugsql.module('sql/foo')
            with foo.transaction():
                x = foo.get_x(x_id=1234)
                foo.update_x(x_id=1234, x+1)

            # when the context manager exits, the transaction is committed.
            # if an exception occurs, it is rolled back.

        The transaction is active for statements executed on the current thread
        only.

        For engines that support SAVEPOINT, calling this method a second time
        begins a nested transaction.

        For more info, see here:
        https://docs.sqlalchemy.org/en/13/orm/session_transaction.html
        """
        if not getattr(self._locals, 'session', None):
            if not self._sessionmaker:
                raise NoConnectionError()

            self._locals.session = self._sessionmaker()

        session = self._locals.session
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
            self._locals.session = None

    def _execute(self, clause, **params):
        if getattr(self._locals, 'session', None):
            return self._locals.session.execute(clause, params)

        if not self._engine:
            raise NoConnectionError()

        return self._engine.execute(clause, **params)

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
        self._engine = engine
        self._sessionmaker = sessionmaker(bind=engine)

    def disconnect(self):
        """
        Disassociates the module from any connection it was previously given.
        """
        self._engine = None
        self._sessionmaker = None


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
