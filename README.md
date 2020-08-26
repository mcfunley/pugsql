# PugSQL

[![Build Status](https://travis-ci.org/mcfunley/pugsql.svg?branch=master)](https://travis-ci.org/mcfunley/pugsql)

PugSQL is a simple Python interface for using parameterized SQL, in files.

See [pugsql.org](https://pugsql.org) for the documentation.

To install:

    pip install pugsql

## Development Setup

To set up a development environment, create a virtual environment. [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)
is a good way to do this:

    brew install pyenv-virtualenv
    pyenv virtualenv 3.8.2 pugsql
    pyenv activate pugsql

Development of the library is done with [poetry](https://python-poetry.org/). Install poetry
to your virtualenv:

    pip install --upgrade pip
    pip install poetry

To run the tests and the linter:

    poetry run pytest
    poetry run flake8
