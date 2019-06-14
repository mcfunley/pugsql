-- :name username_for_id :scalar
select username from users where user_id = :user_id
