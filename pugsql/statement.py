import sqlalchemy


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


class Statement(object):
    def __init__(self, name, sql, doc, result, filename=None):
        if not name:
            raise ValueError('Statement must have a name.')

        if sql is None:
            raise ValueError('Statement must have a SQL string.')
        sql = sql.strip()
        if not len(sql):
            raise ValueError('SQL string cannot be empty.')

        if not result:
            raise ValueError('Statement must have a result type.')

        self.name = name
        self.sql = sql
        self.doc = doc
        self.result = result
        self.filename = filename
        self.engine = None

    def set_engine(self, engine):
        self.engine = engine

    def __call__(self, **params):
        if self.engine is None:
            raise RuntimeError(
                'No connection engine is configured. Pass a connection string '
                "to the module's connect method, or pass a SQLAlchemy engine "
                'to the set_engine method.')

        t = sqlalchemy.sql.text(self.sql)
        r = self.engine.execute(t, **params)
        return self.result.transform(r)
