-- :name search_usernames
-- :result :many
select * from users where username = :username
