from . import compiler

__version__ = '0.1.0'

def create_module(sqlpath):
    return compiler.create_module(sqlpath)

__all__ = ['__version__', 'create_module',]
