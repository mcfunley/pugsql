# Release History

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
