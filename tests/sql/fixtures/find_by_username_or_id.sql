-- :name find_by_username_or_id :many
select *
from users
where username in :usernames or user_id = :user_id
order by user_id asc
