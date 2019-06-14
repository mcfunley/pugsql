---
title: Tutorial
id: tutorial
---
This primer covers the basics of using PugSQL.

### Installation

To install the latest version of PugSQL, use something like:

```bash
pip install pugsql
```

### Writing SQL Files

The premise of PugSQL is that the best way to cope with the reality of database
ownership is to write SQL. In a PugSQL project, you'll just have a set of `.sql`
files in a directory. Like this:

```bash
$ ls queries/
search_users.sql    update_username.sql    user_for_id.sql
```

PugSQL SQL files use special leading comments to specify the names of the queries,
and the desired return types. Queries can return a single row:

```sql
-- :name user_for_id :one
select * from users where user_id = :user_id
```

Or many rows:

```sql
-- :name search_users :many
select * from users where username like :pattern
```

Or they can return the number of affected rows:

```sql
-- :name update_username :affected
update users set username = :username
where user_id = :user_id
```

The `:scalar` return type returns the first value in the first row:

```sql
-- :name get_username :scalar
select username from users where user_id = :user_id
```

The `:insert` return type returns the ID of the row inserted. In engines that
support `lastrowid`, this works:

```sql
-- :name update_username :insert
insert into users (username) values (:username)
```

With engines that do not support `lastrowid`, `:insert` falls back to the same
behavior as `:scalar`.


### Making a PugSQL Module

The SQL files we've created are parsed into a `Module` by PugSQL. The `Module` object exposes all of your queries as functions, taking keyword parameters. To create a module using the example above,

```python
import pugsql

# Load all of the *sql files in the queries/ directory into a single module.
queries = pugsql.module('queries/')
```

More complicated projects can obviously have many modules and sub-modules.

It is safe to call `pugsql.module` using the same path multiple times--PugSQL will not recompile the queries every time you do this.

### Connecting to a Database

The easiest way to connect to a database is to just call the `connect` method on your PugSQL module and give it a [SQLAlchemy-compatible connection string](https://docs.sqlalchemy.org/en/13/core/engines.html).

```python
queries.connect('postgresql://mcfunley@localhost/dbname')
```

For more advanced uses, you can also pass a [SQLAlchemy Engine object](https://docs.sqlalchemy.org/en/13/core/connections.html#sqlalchemy.engine.Engine) to the `set_engine` method on the module instead.

### Running Queries

You can call queries like any other python function, passing them keyword parameters.

```python
queries.update_username(user_id=42, username='joestrummer')
```

The return values depend on the result type specified in the SQL file. Records are returned as Python dictionaries, and the number of affected rows is returned as an integer.

### Transactions

You can use the `transaction` method on `Module` objects to define a transaction block:

```python
with queries.transaction():
    c = queries.get_counter(counter_id=1234)
    queries.update_counter(counter_id=1234, value=c+1)
```

The return value of the `transaction` method is a [SQLAlchemy Session object](https://docs.sqlalchemy.org/en/13/orm/session.html). So, for example, to manually roll back you could write:

```python
with queries.transaction() as t:
    queries.foo()
    t.rollback()
```

Transactions can be nested, when the underlying engine supports `SAVEPOINT`.


### Resetting PugSQL

If for some reason you need to reset PugSQL, you can empty it out like so:

```python
import pugsql

pugsql.get_modules().clear()
```

That's it! Good luck!
