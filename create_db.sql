create schema if not exists problems;

create table problems.users
(
	login text not null
		constraint users_pkey
			primary key,
	password text,
	name text,
	surname text,
	role integer
);

create table problems.topics
(
	topic_id text not null
		constraint topics_pkey
			primary key,
	name text
);

create table problems.tasks
(
	task_id serial not null
		constraint tasks_pkey
			primary key,
	name text,
	topic text
		constraint fk_topic
			references topics
				on delete cascade,
	difficulty integer,
	statement text,
	solution text,
	answer text
);

create table problems.users_tasks
(
	task_id integer not null
		constraint users_tasks_task_id_fkey
			references tasks
				on delete cascade,
	login text not null
		constraint users_tasks_login_fkey
			references users
				on delete cascade,
	constraint task_login
		primary key (task_id, login)
);

create table problems.cart
(
	task_id integer not null
		constraint cart_task_id_fkey
			references tasks
				on delete cascade,
	login text not null
		constraint cart_login_fkey
			references users
				on delete cascade,
	constraint cart_pkey
		primary key (task_id, login)
);
