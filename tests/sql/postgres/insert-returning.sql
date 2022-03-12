-- :name insert_returning :insert
insert into test.test (foo) values (:foo) returning id;
