create table dicts (
uid integer primary key,
name text NOT NULL DEFAULT '',
translate text NOT NULL DEFAULT '',
new tinyint NOT NULL DEFAULT 0,
ctime real NOT NULL
);

create table sentences (
id integer primary key autoincrement not null,
sentence text NOT NULL DEFAULT '',
ctime real NOT NULL
);