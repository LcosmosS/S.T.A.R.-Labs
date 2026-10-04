-- migrations/0002_schema.sql — example for a todos app; use YOUR app's tables
create table if not exists todos (
  id         serial primary key,
  user_id    text not null,
  title      text not null,
  done       boolean not null default false,
  created_at timestamptz not null default now()
);
create index if not exists todos_user_id_idx on todos (user_id);
