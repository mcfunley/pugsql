-- :name username_for_id :one
select username from users where user_id = :user_id
