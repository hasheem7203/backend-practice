create table if not exists tasks (
    id serial primary key,
    title text not null,
    done boolean not null default false
)

