-- :name delete_by_usernames :affected
delete from users where username in :usernames
