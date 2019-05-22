-- :name search_usernames :query :many
select * from users where username = :username
