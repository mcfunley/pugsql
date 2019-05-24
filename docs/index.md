---
title: SQL is Extremely Good, Actually
description: PugSQL is a Python library for interacting with your database using SQL.
---

```python
import pugsql

# Create a module of database functions from a set of sql files on disk.
queries = pugsql.create_module('resources/sql')

# Point the module at your database.
queries.set_connection_string('sqlite:///foo.db')

# Invoke parameterized queries, receive dicts!
user = queries.find_user(user_id=42)

# -> { 'user_id': 42, 'username': 'mcfunley' }
```

https://docs.sqlalchemy.org/en/13/core/engines.html
