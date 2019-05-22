-- :name username_for_id :query :raw
select username from users where user_id = :user_id
