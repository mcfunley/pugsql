-- :name insert_returning_star :one
insert into test.test (foo) values (:foo) returning *;
