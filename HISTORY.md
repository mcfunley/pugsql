# Release History

## HEAD
* Multi-row inserts are always passed as a single list argument, e.g. `module.create([ { 'x': 1 }, { 'x': 2 }])`. Previously this was inconsisent when running inside or outside a transaction. See [#73](https://github.com/mcfunley/pugsql/issues/73) for discussion. Thanks to [Guillaume Pelletier](https://github.com/epgui)!

## 0.3.0
* Upgraded sqlalchemy version to >2.0.
* Dropped support for Python before 3.8.1.
* Now accepting interstitial whitespace in the leading comment block.

## 0.2.4
* Transactions are now automatically committed when leaving a transaction context when using nested transactions, thanks to [Oleksandr Fedorov](https://github.com/o-fedorov/).
* Improved feedback when mistakenly passing positional arguments to statements that don't support it.
* Dropped support for Python 3.5 and 3.6.
* Added test coverage for some postgres-specific tests.
* Migrated test suite from TravisCI to GitHub Actions.
* Fixed broken test suite on Python 3.10

## 0.2.3
* Fixes Python 3.5 tests which were broken in 0.2.2. Began release testing with 3.8.

## 0.2.2
* Support for nested transactions [#40](https://github.com/mcfunley/pugsql/issues/40) thanks to [Hosein Yeganloo](https://github.com/Yeganloo).
* Modules expose the [SQLAlchemy engine](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Engine) they are using ([#5](https://github.com/mcfunley/pugsql/issues/5)).

## 0.2.1
* Added support for adding queries from another path to a module (see [#29](https://github.com/mcfunley/pugsql/issues/29)).

## 0.2.0
* Dropped automatic caching of modules. See [#19](https://github.com/mcfunley/pugsql/issues/19) for discussion.

## 0.1.19
* An `encoding` parameter for interpreting sql files can be passed when creating a pugsql module, thanks to [newturok](https://github.com/newturok).
* Better exception feedback when calling statements incorrectly with positional arguments.
* Added some development setup notes to the README.

## 0.1.18
* Custom connection `kwargs` are passed through to `create_engine`, thanks to [Brad Greenlee](https://github.com/bgreenlee).

## 0.1.17
* Added support for multiple statements per file thanks to [Brad Greenlee](https://github.com/bgreenlee).

## 0.1.16
* Fixed [#28](https://github.com/mcfunley/pugsql/issues/28) - better errors when trying to use a query name that is already defined as a method on the `Module` class.
* Modules are now iterable (thanks to [Haoyu Qiu](https://github.com/timothyqiu)).

## 0.1.15
* Better error messages from malformed SQL files.

## 0.1.14
* `IN` clauses also accept `set` parameters (in addition to `tuple` and `list`).

## 0.1.13
* `IN` clauses now work. Passing a tuple or a list as the value of a named parameter will automatically treat the parameter as an expanding (i.e. `(?, ?, ?, ?)`, etc) bind parameter.

## 0.1.12
* Added support for passing `multiparams` through to SQLAlchemy's `execute` method, which among other things makes multi-row inserts work ([#9](https://github.com/mcfunley/pugsql/issues/9)).
* Parsed statements use very slightly less memory.

## 0.1.11
* Added the `:scalar` return type, which returns the first value in the first row.
* The `:insert` return type defaults to `:scalar` behavior when a DBAPI does not support `lastrowid` ([#7](https://github.com/mcfunley/pugsql/issues/7)).

## 0.1.10
* Fixed [#11](https://github.com/mcfunley/pugsql/issues/11), exception when a PugSQL module is initialized on another thread.
* Documentation fixes.

## 0.1.9
* Added support for `Module.transaction()`, which returns a context manager which maintains thread-local transaction scope.

## 0.1.8
* Effective function signature is shown with `str(statement)` or `repr(statement)`.
* Added an `:insert` return type which returns the ID of the last row inserted, for engines which support it (thanks to [Jelle Besseling](https://jelle.besseli.ng/)).
* `:one` queries resulting in null no longer break (#10)

## 0.1.7
* Added the `pugsql.get_modules()` API.
* Dropped support for Python 3.4.
* Greatly improved docstrings throughout (in progress).
* Now generating module documentation with [https://pypi.org/project/pdoc3/](pdoc3).
* Better PyPI package page.
* Improved homepage.

## 0.1.6
* PugSQL now provides detailed file/line/column syntax errors.
* Illegal characters in Python function names will now fail to parse.
* Duplicate function names in one library will now fail.

## 0.1.5
* Fixed broken flake8 tests in 0.1.4 release.

## 0.1.4
* Improved exception feedback.
* Improved docstrings on public interface and important objects.
* Added some PyPI project metadata.

## 0.1.3
* Starting to keep track of release history.
* Supporting python 3.4 through 3.7
