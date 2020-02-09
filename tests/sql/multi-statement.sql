-- :name basic_statement
select username from users where user_id = :user_id

-- :name multiline_statement :insert
insert into foobar (foo, bar)
values (:foo, :bar);

-- :name multiline_syntax
-- :result :many
select * from foo where bar = :bar;

-- :name extra_comments :*
-- some extra commentary
select * from foo where bar = :bar

-- :name interstitial_comments :*
select * from foo
-- some extra commentary
where bar = :bar
