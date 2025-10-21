"""
Code that processes SQL files and returns modules of database functions.
"""

import os
import re
import threading
from contextlib import contextmanager, suppress
from glob import glob
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.exc import ResourceClosedError
from sqlalchemy.orm import sessionmaker

from . import context, parser
from .exceptions import NoConnectionError

__pdoc__ = {}


class Module(object):
    """
    Holds a set of SQL functions loaded from files.
    """

    sqlpaths: set
    engine = None

    def __init__(self, sqlpath: str, encoding: Optional[str] = None):
        """
        Loads functions found in the *sql files specified by `sqlpath` into
        properties on this object. An `encoding` for the files can optionally
        be provided.

        The named sql functions in files should be unique.
        """
        self.sqlpaths = set()
        self._statements = {}
        self._sessionmaker = None
        self._locals = threading.local()

        self.add_queries(sqlpath, encoding=encoding)

    def add_queries(self, *paths: str, encoding: Optional[str] = None):
        """
        Adds queries from *sql files in one or more `paths` to the module.
        An `encoding` for the files can optionally be provided.

        The named sql functions in files should be unique.
        """
        for p in paths:
            self._add_path(p, encoding=encoding)
        self.sqlpaths |= set(paths)

    def _add_path(self, sqlpath: str, encoding: Optional[str] = None):
        if not os.path.isdir(sqlpath):
            raise ValueError("Directory not found: %s" % sqlpath)

        for sqlfile in sorted(glob(os.path.join(sqlpath, "*sql"))):
            with open(sqlfile, "r", encoding=encoding) as f:
                pugsql = f.read()

            # handle multiple statements per file
            statements = re.split(r"\n+(?=--+\s*:name)", pugsql)
            statement_line = 0
            for statement in statements:
                s = parser.parse(statement, ctx=context.Context(sqlfile,
                                 line=statement_line))
                statement_line += len(statement.splitlines()) + 1

                if hasattr(self, s.name):
                    if s.name not in self._statements:
                        raise ValueError(
                            'Error loading %s - the function name "%s" is '
                            "reserved. Please choose another name."
                            % (sqlfile, s.name)
                        )
                    raise ValueError(
                        "Error loading %s - a SQL function named %s was "
                        "already defined in %s."
                        % (sqlfile, s.name, self._statements[s.name].filename)
                    )

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
        if not getattr(self._locals, "session", None):
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
        else:
            session = self._locals.session.begin_nested()
            try:
                yield session
            except Exception as e:
                session.rollback()
                raise e
            else:
                with suppress(ResourceClosedError):
                    session.commit()

    def _execute(self, clause, *multiparams, **params):
        if getattr(self._locals, "session", None):
            if multiparams:
                return self._locals.session.execute(clause, *multiparams)
            else:
                return self._locals.session.execute(clause, params)

        if not self.engine:
            raise NoConnectionError()

        with self.engine.connect() as conn:
            if multiparams:
                result = conn.execute(clause, *multiparams)
            else:
                result = conn.execute(clause, params)
            conn.commit()
            return result

    @property
    def _dialect(self):
        """
        Gets the dialect for the SQLAlchemy engine.
        """
        if not self.engine:
            raise NoConnectionError()
        return self.engine.dialect

    def connect(self, connstr, **kwargs):
        """
        Sets the connection string for SQL functions on this module.

        See https://docs.sqlalchemy.org/en/13/core/engines.html for examples of
        legal connection strings for different databases.
        """
        self.setengine(create_engine(connstr, **kwargs))

    def setengine(self, engine):
        """
        Sets the SQLAlchemy engine for SQL functions on this module. This can
        be used instead of the connect method, when more customization of the
        connection engine is desired.

        See also: https://docs.sqlalchemy.org/en/13/core/connections.html
        """
        self.engine = engine
        self._sessionmaker = sessionmaker(bind=engine)

    def disconnect(self):
        """
        Disassociates the module from any connection it was previously given.
        """
        self.engine = None
        self._sessionmaker = None

    def __iter__(self):
        return iter(self._statements.values())


__pdoc__["Module.sqlpaths"] = (
    "A list of paths that the `pugsql.compiler.Module` was loaded from."
)
__pdoc__["Module.engine"] = (
    "The sqlalchemy engine object being used by the `pugsql.compiler.Module`."
)
