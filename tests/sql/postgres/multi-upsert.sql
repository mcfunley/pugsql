-- :name multi_upsert :many
insert into test.test (id, foo)
values (:id, :foo)
on conflict (id) do update set foo = excluded.foo
returning *
