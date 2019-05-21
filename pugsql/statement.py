from dataclasses import dataclass


class Command(object):
    pass

class Query(Command):
    pass

class Execute(Command):
    pass

class ReturningExecute(Command):
    pass

class Insert(Command):
    pass


class Result(object):
    pass

class One(Result):
    pass

class Many(Result):
    pass

class Affected(Result):
    pass

class Raw(Result):
    pass


@dataclass
class Statement:
    name: str
    sql: str
    doc: str
    command: Command
    result: Result
