from . import parser
from glob import glob
import os
from sqlalchemy import create_engine


class Module(object):
    def __init__(self, sqlpath):
        self.sqlpath = sqlpath
        self._statements = {}

        for sqlfile in glob(os.path.join(self.sqlpath, '*sql')):
            with open(sqlfile, 'r') as f:
                pugsql = f.read()
            s = parser.parse(pugsql)

            if hasattr(self, s.name):
                raise Exception('TODO')

            setattr(self, s.name, s)
            self._statements[s.name] = s

    def set_connection_string(self, connstr):
        self.set_engine(create_engine(connstr))

    def set_engine(self, engine):
        for s in self._statements.values():
            s.set_engine(engine)


modules = {}


def create_module(sqlpath):
    global modules
    if sqlpath not in modules:
        modules[sqlpath] = Module(sqlpath)
    return modules[sqlpath]
