-- :name setup :raw
begin;

drop schema if exists test cascade;

create schema test;

create table test.test (
  id bigint not null primary key,
  foo text
);

commit;
