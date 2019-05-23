from dataclasses import dataclass
from sqlalchemy.sql import text


class Result(object):
    def transform(self, r):
        raise NotImplementedError()

class One(Result):
    def transform(self, r):
        return { k: v for k, v in zip(r.keys(), r.first()) }

class Many(Result):
    def transform(self, r):
        ks = r.keys()
        return ({ k: v for k, v in zip(ks, row)} for row in r.fetchall())

class Affected(Result):
    def transform(self, r):
        return r.rowcount

class Raw(Result):
    def transform(self, r):
        return r


@dataclass
class Statement:
    name: str
    sql: str
    doc: str
    result: Result

    def set_engine(self, engine):
        self.engine = engine

    def __call__(self, **params):
        if self.engine is None:
            raise Exception('TODO')

        r = self.engine.execute(text(self.sql), **params)
        return self.result.transform(r)
