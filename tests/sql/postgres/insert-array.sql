-- :name insert_array :one
insert into test.test (id, arr) values (:id, :arr) returning *;
