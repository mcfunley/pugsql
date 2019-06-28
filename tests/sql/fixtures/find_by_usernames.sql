-- :name find_by_usernames :many
select *
from users
where username in :usernames
order by user_id asc
