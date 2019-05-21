from dataclasses import dataclass


class Command(object):
    pass


class Result(object):
    pass


@dataclass
class Statement:
    name: str
    sql: str
    doc: str
    command: Command
    result: Result
