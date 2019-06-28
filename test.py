#!/usr/bin/env python
from sqlalchemy import create_engine, text
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import BindParameter
import sys

e = create_engine('postgresql+pg8000://dmckinley@127.0.0.1')

dicts = [{ 'foo': 'abcd'}, { 'foo': 'asdf' }]
tpl = ('abcd', 'asdf',)

@compiles(BindParameter)
def visit_param(element, compiler, **kw):
    element.expanding = True
    return compiler.visit_bindparam(element)

t = text('select * from public.test where foo in :foo_values or id = :id')
r = e.execute(t, foo_values=tpl, id=(2,))
print(r.fetchall())
