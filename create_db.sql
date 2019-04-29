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

create table if not exists problems.cart
(
	task_id integer not null
		constraint cart_task_id_fkey
			references tasks,
	login text not null
		constraint cart_login_fkey
			references users,
	constraint cart_pkey
		primary key (task_id, login)
);


