-- Ejecutar en Supabase: Project -> SQL Editor -> New query

create table if not exists published_posts (
    id bigint generated always as identity primary key,
    url_hash text unique not null,
    source_url text not null,
    slug text not null,
    published_at timestamptz not null default now()
);

create index if not exists idx_published_posts_url_hash on published_posts (url_hash);

-- (Opcional, fase 2 de monetización) tabla de tracking de clics en afiliados
create table if not exists affiliate_clicks (
    id bigint generated always as identity primary key,
    slug text not null,
    clicked_at timestamptz not null default now(),
    user_agent text,
    referrer text
);

-- RLS: para el free tier, activa RLS y permite insert/select solo con la service_role key
alter table published_posts enable row level security;
alter table affiliate_clicks enable row level security;

create policy "service_role_full_access_posts" on published_posts
    for all using (true) with check (true);

create policy "service_role_full_access_clicks" on affiliate_clicks
    for all using (true) with check (true);
