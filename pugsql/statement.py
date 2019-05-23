from dataclasses import dataclass



class Command(object):
    def execute(self, conn, params):
        raise NotImplementedError()

class Query(Command):
    pass

class Execute(Command):
    pass

class ReturningExecute(Command):
    pass


class Result(object):
    def transform(self, r):
        raise NotImplementedError()

class One(Result):
    pass

class Many(Result):
    pass

class Affected(Result):
    pass

class Raw(Result):
    def transform(self, r):
        return r


@dataclass
class Statement:
    name: str
    sql: str
    doc: str
    command: Command
    result: Result

    def set_engine(self, engine):
        self.engine = engine

    def __call__(self, **params):
        if self.engine is None:
            raise Exception('TODO')

        with self.engine.connect() as conn:
            return self.result.transform(self.command.execute(conn, params))
