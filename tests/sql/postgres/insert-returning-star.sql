-- :name insert_returning_star :one
insert into test (foo) values (:foo) returning *;
