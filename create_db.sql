create table if not exists problems.tasks
(
  task_id    serial not null
    constraint tasks_pkey
      primary key,
  name       text,
  topic      text,
  difficulty integer,
  statement  text,
  solution   text,
  answer     text
);

alter table problems.tasks
  owner to postgres;

create table if not exists problems.users
(
  login    text not null
    constraint users_pkey
      primary key,
  password text,
  name     text,
  surname  text,
  role     integer
);

alter table problems.users
  owner to postgres;

create table if not exists problems.users_tasks
(
  task_id integer not null
    constraint users_tasks_task_id_fkey
      references tasks
      on delete cascade,
  login   text    not null
    constraint users_tasks_login_fkey
      references users
      on delete cascade,
  constraint task_login
    primary key (task_id, login)
);

alter table problems.users_tasks
  owner to postgres;

