#!/usr/bin/env python3
"""
Pipeline de Programmatic SEO — Zero-Budget
Trigger -> RSS Scraping -> Dedupe (Supabase) -> Rewrite (Groq LLM) -> Markdown (Astro) -> Supabase log

Variables de entorno requeridas (se inyectan como GitHub Secrets):
  GROQ_API_KEY      -> https://console.groq.com (gratis, sin tarjeta)
  SUPABASE_URL      -> https://app.supabase.com (gratis, sin tarjeta)
  SUPABASE_KEY      -> service_role o anon key con permisos de insert/select

Dependencias (requirements.txt):
  feedparser==6.0.11
  groq==0.11.0
  supabase==2.7.4
  python-slugify==8.0.4
  python-frontmatter==1.1.0
"""

import os
import sys
import json
import hashlib
from datetime import datetime, timezone

import feedparser
from groq import Groq
from supabase import create_client, Client
from slugify import slugify
import frontmatter

# --------------------------------------------------------------------------
# CONFIG — Ajusta esto a tu nicho. Usa feeds RSS públicos, sin API key.
# Ejemplos de nichos con feeds gratuitos ilimitados:
#   - Google News RSS: https://news.google.com/rss/search?q=<TEMA>&hl=es&gl=ES
#   - Reddit RSS: https://www.reddit.com/r/<subreddit>/.rss
#   - Feeds nativos de blogs del nicho (busca "site:ejemplo.com rss")
# --------------------------------------------------------------------------
NICHE = "gadgets tecnologia"  # <-- cambia esto por tu nicho de afiliación
RSS_FEEDS = [
    f"https://news.google.com/rss/search?q={NICHE.replace(' ', '+')}&hl=es&gl=ES&ceid=ES:es",
    "https://www.reddit.com/r/gadgets/.rss",
]
MAX_ARTICLES_PER_RUN = 5          # límite para no agotar rate-limit gratuito de Groq
GROQ_MODEL = "llama-3.3-70b-versatile"  # modelo gratuito de alta calidad en Groq
CONTENT_DIR = "site/src/content/posts"  # ruta dentro de tu repo Astro
AFFILIATE_CTA = os.environ.get(
    "AFFILIATE_CTA_HTML",
    '<p>👉 Mira las mejores ofertas relacionadas <a href="https://tu-link-afiliado.com" rel="sponsored nofollow">aquí</a>.</p>'
)

# --------------------------------------------------------------------------
# CLIENTES
# --------------------------------------------------------------------------
def get_clients():
    groq_key = os.environ["GROQ_API_KEY"]
    supabase_url = os.environ["SUPABASE_URL"]
    supabase_key = os.environ["SUPABASE_KEY"]

    groq_client = Groq(api_key=groq_key)
    supabase_client: Client = create_client(supabase_url, supabase_key)
    return groq_client, supabase_client


# --------------------------------------------------------------------------
# 1. SCRAPING
# --------------------------------------------------------------------------
def fetch_candidates():
    """Devuelve lista de dicts {title, link, summary, source} desde los RSS."""
    candidates = []
    for feed_url in RSS_FEEDS:
        parsed = feedparser.parse(feed_url)
        for entry in parsed.entries[:10]:
            candidates.append({
                "title": entry.get("title", "").strip(),
                "link": entry.get("link", "").strip(),
                "summary": entry.get("summary", "")[:1000],
                "source": feed_url,
            })
    return candidates


def url_hash(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------
# 2. DEDUPE CONTRA SUPABASE
# --------------------------------------------------------------------------
def filter_new_items(supabase: Client, items: list) -> list:
    """Descarta items ya publicados según tabla `published_posts`."""
    new_items = []
    for item in items:
        h = url_hash(item["link"])
        res = supabase.table("published_posts").select("id").eq("url_hash", h).execute()
        if len(res.data) == 0:
            item["url_hash"] = h
            new_items.append(item)
        if len(new_items) >= MAX_ARTICLES_PER_RUN:
            break
    return new_items


# --------------------------------------------------------------------------
# 3. REESCRITURA CON GROQ (SEO + estructura)
# --------------------------------------------------------------------------
REWRITE_SYSTEM_PROMPT = """Eres un redactor SEO experto en español. 
Recibirás un titular y un resumen de una noticia/fuente.
Debes generar un artículo ORIGINAL (no copiar frases literales de la fuente),
optimizado para SEO, en formato JSON estricto con esta forma exacta:

{
  "seo_title": "Título optimizado <= 60 caracteres",
  "meta_description": "Descripción meta <= 155 caracteres",
  "h1": "Encabezado principal del artículo",
  "body_markdown": "Cuerpo del artículo en Markdown, 500-800 palabras, con subtítulos H2, tono útil y natural",
  "tags": ["tag1", "tag2", "tag3"]
}

Responde SOLO con el JSON, sin texto adicional, sin backticks de markdown.
"""

def rewrite_article(groq_client: Groq, item: dict) -> dict:
    user_prompt = f"Titular original: {item['title']}\nResumen original: {item['summary']}"
    completion = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": REWRITE_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=2000,
        response_format={"type": "json_object"},
    )
    raw = completion.choices[0].message.content
    return json.loads(raw)


# --------------------------------------------------------------------------
# 4. GENERAR ARCHIVO MARKDOWN (Astro content collections)
# --------------------------------------------------------------------------
def write_markdown_file(article: dict, source_link: str):
    os.makedirs(CONTENT_DIR, exist_ok=True)
    slug = slugify(article["seo_title"])[:80]
    filepath = os.path.join(CONTENT_DIR, f"{slug}.md")

    post = frontmatter.Post(
        content=f"{article['body_markdown']}\n\n---\n{AFFILIATE_CTA}\n",
    )
    post["title"] = article["seo_title"]
    post["description"] = article["meta_description"]
    post["pubDate"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    post["tags"] = article["tags"]
    post["sourceRef"] = source_link

    with open(filepath, "wb") as f:
        frontmatter.dump(post, f)

    return slug, filepath


# --------------------------------------------------------------------------
# 5. REGISTRAR EN SUPABASE
# --------------------------------------------------------------------------
def log_published(supabase: Client, item: dict, slug: str):
    supabase.table("published_posts").insert({
        "url_hash": item["url_hash"],
        "source_url": item["link"],
        "slug": slug,
        "published_at": datetime.now(timezone.utc).isoformat(),
    }).execute()


# --------------------------------------------------------------------------
# MAIN
# --------------------------------------------------------------------------
def main():
    groq_client, supabase = get_clients()

    print("[1/4] Scraping RSS feeds...")
    candidates = fetch_candidates()
    print(f"  -> {len(candidates)} candidatos encontrados")

    print("[2/4] Filtrando duplicados via Supabase...")
    new_items = filter_new_items(supabase, candidates)
    print(f"  -> {len(new_items)} items nuevos a procesar (máx {MAX_ARTICLES_PER_RUN})")

    if not new_items:
        print("Nada nuevo que publicar en esta ejecución. Fin.")
        sys.exit(0)

    generated_files = []
    for item in new_items:
        try:
            print(f"[3/4] Reescribiendo: {item['title'][:60]}...")
            article = rewrite_article(groq_client, item)
            slug, filepath = write_markdown_file(article, item["link"])
            log_published(supabase, item, slug)
            generated_files.append(filepath)
            print(f"  -> Generado: {filepath}")
        except Exception as e:
            print(f"  !! Error procesando '{item['title'][:50]}': {e}", file=sys.stderr)
            continue

    print(f"[4/4] Listo. {len(generated_files)} artículos generados.")
    # GitHub Actions leerá estos archivos nuevos y hará commit+push automáticamente


if __name__ == "__main__":
    main()
