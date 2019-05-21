from dataclasses import dataclass


class Command(object):
    pass


class Result(object):
    pass


@dataclass
class Query:
    name: str
    sql: str
    doc: str
    command: Command
    result: Result
