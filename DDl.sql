create schema auth;
CREATE
EXTENSION IF NOT EXISTS "uuid-ossp";

create table auth.user
(
    user_id  serial primary key not null,
    name     varchar(250)       not null,
    email    varchar(250)       not null,
    password text               not null,
    salt     text               not null,
    status   boolean            not null default true
);

create table auth.audit
(
    audit_id      serial primary key not null,
    user_id       int,
    url           varchar(250),
    creation_date timestamp,
    payload       text
);

create table auth.module
(
    module_id   serial primary key not null,
    module_name varchar(500)       not null,
    key         varchar(250)       not null
);


create table auth.module_action
(
    module_action_id   serial primary key not null,
    module_action_name varchar(250)       not null,
    key         varchar(250)       not null,
    module_id   int                not null,
    foreign key (module_id) references auth.module (module_id)
)
