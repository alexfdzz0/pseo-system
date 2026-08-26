# Sistema PSEO Zero-Budget — Guía de despliegue

## 1. Arquitectura (flujo de datos)

```
[CRON GitHub Actions cada 6h]
        │
        ▼
[1. Scraping RSS] ──> lista de candidatos JSON
{
  "title": "Xiaomi lanza nuevo smartwatch con...",
  "link": "https://fuente.com/noticia-123",
  "summary": "...",
  "source": "https://news.google.com/rss/..."
}
        │
        ▼
[2. Dedupe contra Supabase] ──> descarta ya publicados (hash SHA256 de la URL)
        │
        ▼
[3. Reescritura con Groq LLM] ──> JSON estructurado
{
  "seo_title": "Xiaomi Watch Pro: precio y specs 2026",
  "meta_description": "...",
  "h1": "...",
  "body_markdown": "## Introducción\n...",
  "tags": ["xiaomi", "smartwatch", "gadgets"]
}
        │
        ▼
[4. Generar .md con frontmatter] ──> site/src/content/posts/xiaomi-watch-pro.md
        │
        ▼
[5. Log en Supabase] (tabla published_posts)
        │
        ▼
[6. git commit + push automático] (GitHub Action)
        │
        ▼
[7. Vercel detecta push -> build Astro -> deploy automático]
        │
        ▼
[Web en producción con nuevo artículo indexable por Google]
```

## 2. Paso a paso (una sola vez, ~20 minutos)

### A. Crear el sitio Astro (gratis, sin tarjeta)
```bash
npm create astro@latest site -- --template blog --no-install
cd site && npm install
```
Copia el resultado dentro de la misma carpeta de este repo (junto a `pipeline.py`), de forma que `site/src/content/posts/` sea la ruta de destino del script.

### B. Supabase (gratis, sin tarjeta)
1. Crea cuenta en https://supabase.com y un nuevo proyecto.
2. Ve a **SQL Editor** y ejecuta el contenido de `supabase_schema.sql`.
3. Ve a **Project Settings -> API** y copia:
   - `Project URL` -> será `SUPABASE_URL`
   - `service_role key` -> será `SUPABASE_KEY`

### C. Groq (gratis, sin tarjeta)
1. Crea cuenta en https://console.groq.com
2. Genera una API Key -> será `GROQ_API_KEY`.
3. Límite gratuito actual: suficiente para procesar decenas de artículos/día con el modelo `llama-3.3-70b-versatile` (verifica el límite vigente en tu panel, Groq lo actualiza).

### D. GitHub
1. Crea un repo nuevo y sube todo este contenido (`pipeline.py`, `requirements.txt`, `.github/workflows/pipeline.yml`, `site/`).
2. Ve a **Settings -> Secrets and variables -> Actions** y añade:
   - `GROQ_API_KEY`
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
3. Ve a la pestaña **Actions** y lanza el workflow manualmente una vez (`Run workflow`) para verificar que todo funciona.

### E. Vercel (gratis, sin tarjeta)
1. Entra a https://vercel.com, conecta tu cuenta de GitHub.
2. Importa el repo, selecciona el subdirectorio `site/` como root del proyecto (Framework Preset: Astro).
3. Deploy. A partir de aquí, cada `git push` (incluido el automático del cron) dispara un rebuild y deploy.

### F. Cierre del bucle 24/7
No hay que hacer nada más. El cron de `.github/workflows/pipeline.yml` corre cada 6h automáticamente, sube artículos nuevos, y Vercel los publica solo. Coste: **0 $/mes** (dentro de los límites free de GitHub Actions ~2000 min/mes, Supabase 500MB DB, Vercel 100GB bandwidth).

## 3. Monetización (conecta esto tú mismo, requiere aprobación externa)
- Sustituye `AFFILIATE_CTA_HTML` (variable de entorno opcional en el workflow) por tu link de Amazon Afiliados / Awin / u otro programa al que te hayas dado de alta.
- Añade Google AdSense al layout de Astro (`site/src/layouts/`) una vez el sitio tenga tráfico suficiente para ser aprobado.

## 4. Ejemplo cURL directo a Groq (por si prefieres no usar el SDK)
```bash
curl https://api.groq.com/openai/v1/chat/completions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3.3-70b-versatile",
    "messages": [
      {"role": "system", "content": "Eres un redactor SEO..."},
      {"role": "user", "content": "Titular: ..."}
    ],
    "response_format": {"type": "json_object"}
  }'
```
