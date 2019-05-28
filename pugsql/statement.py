"""
Compiled SQL function objects.
"""
import sqlalchemy


class Result(object):
    def transform(self, r):
        raise NotImplementedError()

    @property
    def display_type(self):
        raise NotImplemented()


class One(Result):
    def transform(self, r):
        return { k: v for k, v in zip(r.keys(), r.first()) }

    @property
    def display_type(self):
        return 'row'


class Many(Result):
    def transform(self, r):
        ks = r.keys()
        return ({ k: v for k, v in zip(ks, row)} for row in r.fetchall())

    @property
    def display_type(self):
        return 'rows'


class Affected(Result):
    def transform(self, r):
        return r.rowcount

    @property
    def display_type(self):
        return 'rowcount'


class Raw(Result):
    def transform(self, r):
        return r

    @property
    def display_type(self):
        return 'raw'


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
        self._text = sqlalchemy.sql.text(self.sql)


    def set_engine(self, engine):
        self.engine = engine

    def __call__(self, **params):
        if self.engine is None:
            raise RuntimeError(
                'No connection engine is configured. Pass a connection string '
                "to the module's connect method, or pass a SQLAlchemy engine "
                'to the set_engine method.')

        r = self.engine.execute(self._text, **params)
        return self.result.transform(r)

    def _param_names(self):
        kfn = lambda p: self.sql.index(':' + p)
        return sorted(self._text._bindparams.keys(), key=kfn)

    def __str__(self):
        paramstr = ', '.join(['%s=None' % k for k in self._param_names()])
        return 'pugsql.statement.Statement: %s(%s) :: %s' % (
            self.name, paramstr, self.result.display_type)

    def __repr__(self):
        return str(self)
