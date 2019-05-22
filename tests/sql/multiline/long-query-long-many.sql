-- :name search_usernames
-- :command :query
-- :result :many
select * from users where username = :username
