from . import parser
from glob import glob
import os


class Module(object):
    def __init__(self, sqlpath):
        self.sqlpath = sqlpath

        for sqlfile in glob(os.path.join(self.sqlpath, '*sql')):
            with open(sqlfile, 'r') as f:
                pugsql = f.read()
            s = parser.parse(pugsql)

            if hasattr(self, s.name):
                raise Exception('TODO')

            setattr(self, s.name, s)


modules = {}


def create_module(sqlpath):
    global modules
    if sqlpath not in modules:
        modules[sqlpath] = Module(sqlpath)
    return modules[sqlpath]
