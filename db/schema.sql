drop table if exists kbase;
create table kbase (
  id integer primary key autoincrement,
  question text not null,
  question1 text not null,
  answer text not null,
  question2 text not null
);
