from . import compiler

__version__ = '0.1.1'

def module(sqlpath):
    return compiler.module(sqlpath)

__all__ = ['__version__', 'module',]
