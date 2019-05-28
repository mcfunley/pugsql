[PugSQL](https://pugsql.org) is a simple Python interface for using parameterized SQL, in files, with [any  SQLAlchemy-supported database](https://docs.sqlalchemy.org/en/13/dialects/index.html).

For more information and full documentation, visit [pugsql.org](https://pugsql.org).

```
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

```
--- :name find_user :one
select * from users where user_id = :user_id
```

So _throw away_ your bulky ORM and talk to your database the way the gods intended! Install PugSQL today!
