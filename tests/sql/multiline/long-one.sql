-- :name username_for_id
-- :result :one
select username from users where user_id = :user_id
