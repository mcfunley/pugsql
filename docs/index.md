---
title: SQL is Extremely Good, Actually
description: PugSQL is a Python library for interacting with your database using SQL.
---

PugSQL is a simple Python interface for using parameterized SQL, in files, with [any  SQLAlchemy-supported database](https://docs.sqlalchemy.org/en/13/dialects/index.html).

```python
import pugsql

# Create a module of database functions from a set of sql files on disk.
queries = pugsql.module('resources/sql')

# Point the module at your database.
queries.connect('sqlite:///foo.db')

# Invoke parameterized queries, receive dicts!
user = queries.find_user(user_id=42)

# -> { 'user_id': 42, 'username': 'mcfunley' }
```

In the example above, the query would be specified like this:

```sql
--- :name find_user :one
select * from users where user_id = :user_id
```

So _throw away_ your bulky ORM and talk to your database the way the gods intended! Install PugSQL today!

```bash
$ pip install pugsql
```

PugSQL was inspired by the amazing [HugSQL](https://hugsql.org) library for the [Clojure](https://clojure.org) programming language.

<div class="tutorial-link"><a href="/tutorial">Take the Tutorial</a></div>
