"""
Compiled SQL function objects.
"""
from .exceptions import InvalidArgumentError
from contextlib import contextmanager
import sqlalchemy
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import BindParameter
import threading


_locals = threading.local()


@contextmanager
def _compile_context(multiparams, params):
    _locals.compile_context = {
        'multiparams': multiparams,
        'params': params,
    }
    try:
        yield
    finally:
        _locals.compile_context = None


@compiles(BindParameter)
def _visit_bindparam(element, compiler, **kw):
    cc = getattr(_locals, 'compile_context', None)
    if cc:
        if _is_expanding_param(element, cc):
            element.expanding = True
    return compiler.visit_bindparam(element)


def _is_expanding_param(element, cc):
    if element.key not in cc['params']:
        return False
    return isinstance(cc['params'][element.key], (tuple, list))


class Result(object):
    def transform(self, r):
        raise NotImplementedError()

    @property
    def display_type(self):
        raise NotImplementedError()


class One(Result):
    def transform(self, r):
        row = r.first()
        if row:
            return { k: v for k, v in zip(r.keys(), row) }
        return None

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


class Scalar(Result):
    def transform(self, r):
        row = r.first()
        if not row:
            return None
        return row[0]

    @property
    def display_type(self):
        return 'scalar'


class Insert(Scalar):
    def transform(self, r):
        if hasattr(r, 'lastrowid'):
            return r.lastrowid
        return super(Insert, self).transform(r)

    @property
    def display_type(self):
        return 'insert'


class Raw(Result):
    def transform(self, r):
        return r

    @property
    def display_type(self):
        return 'raw'


class Statement(object):
    def __init__(self, name, sql, doc, result, filename=None):
        self.filename = filename

        if not name:
            self._value_err('Statement must have a name.')

        if sql is None:
            self._value_err('Statement must have a SQL string.')
        sql = sql.strip()
        if not len(sql):
            self._value_err('SQL string cannot be empty.')

        if not result:
            self._value_err('Statement must have a result type.')

        self.name = name
        self.sql = sql
        self.doc = doc
        self.result = result
        self.filename = filename
        self._module = None
        self._text = sqlalchemy.sql.text(self.sql)

    def _value_err(self, msg):
        if self.filename:
            raise ValueError('%s In: %s' % (msg, self.filename))
        raise ValueError(msg)

    def set_module(self, module):
        self._module = module

    def _assert_module(self):
        if self._module is None:
            raise RuntimeError(
                'This statement is not associated with a module')

    def __call__(self, *multiparams, **params):
        self._assert_module()
        multiparams, params = self._convert_params(multiparams, params)
        with _compile_context(multiparams, params):
            try:
                r = self._module._execute(self._text, *multiparams, **params)
            except AttributeError as e:
                if str(e) == "'tuple' object has no attribute 'keys'":
                    raise InvalidArgumentError(
                        'Pass keyword arguments to statements (received '
                        'positional arguments).')
                raise
        return self.result.transform(r)

    def _convert_params(self, multiparams, params):
        def conv(x):
            if isinstance(x, set):
                return tuple(x)
            return x
        return (
            [conv(p) for p in multiparams],
            { k: conv(v) for k, v in params.items() })

    def _param_names(self):
        def kfn(p):
            return self.sql.index(':' + p)
        return sorted(self._text._bindparams.keys(), key=kfn)

    def __str__(self):
        paramstr = ', '.join(['%s=None' % k for k in self._param_names()])
        return 'pugsql.statement.Statement: %s(%s) :: %s' % (
            self.name, paramstr, self.result.display_type)

    def __repr__(self):
        return str(self)
