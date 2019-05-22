-- :name username_for_id
-- :command :execute
-- :result :affected
delete from users where user_id = :user_id
