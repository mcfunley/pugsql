-- :name username_for_id
-- :command :query
select username from users where user_id = :user_id
