-- :name insert_returning :insert
insert into test (foo) values (:foo) returning id;
