# Anh Ngữ Việt Nam — Directorio estático

Directorio SEO programático de 108 trung tâm Anh ngữ en Vietnam. Sitio estático HTML puro, sin backend, listo para desplegar en Vercel, Netlify, Cloudflare Pages o GitHub Pages.

## Estructura

```
├── index.html                 # Home
├── 404.html                   # Página de error
├── sitemap.xml                # Sitemap para Google
├── robots.txt                 # Directivas para crawlers
├── styles.css                 # Estilos del sitio
├── popup.js                   # Popup de captación (entry + exit intent)
├── data.json                  # Datos fuente (108 centros, 11 categorías, 3 ciudades)
│
├── trung-tam/                 # 108 fichas de centros (HTML estático, indexable)
│   └── {slug}.html
├── danh-muc/                  # 11 páginas de categoría + index
│   ├── index.html
│   └── {slug}.html
├── thanh-pho/                 # 3 páginas de ciudad
│   └── {slug}.html
│
├── build.py                   # Generador estático (ver "Regenerar el sitio")
├── build_partials.py          # Partials reutilizables (header, footer, meta)
├── scrape_images.py           # Scraper de imágenes de Google Maps
└── img_cache.json             # Cache de scraping (no tocar)
```

## Despliegue

### Opción A: Vercel / Netlify / Cloudflare Pages
Conecta este repo y ya está. No hay build step — es HTML estático puro.

### Opción B: GitHub Pages
Settings → Pages → Source: Deploy from branch → `main` / `root`.

### Opción C: servidor tradicional
Sube todo el contenido por FTP al directorio público de tu servidor.

## Configurar antes de desplegar

### 1. Dominio real en build_partials.py

Abre `build_partials.py` y cambia:

```python
SITE = {
    'domain':  'https://anhnguvn.example.com',  # ← Cambia aquí al dominio real
    ...
}
```

Luego regenera el sitio con `python build.py` (ver abajo).

### 2. Popup de captación en data.json

El popup es el elemento de conversión del sitio. Promociona tu academia propia.
Abre `data.json` y edita la sección `popup`:

```json
"popup": {
  "academy_name": "TU ACADEMIA",
  "academy_url": "https://tuacademia.com",
  "entry": {
    "enabled": true,
    "cta_text": "Tìm hiểu khóa học →",
    "cta_url": "https://tuacademia.com/inscripcion",  ← AQUÍ el destino
    ...
  },
  "exit": {
    "cta_url": "https://tuacademia.com/lead-magnet",  ← AQUÍ el destino
    ...
  }
}
```

- `entry`: aparece 4s después de entrar a cualquier página.
- `exit`: aparece cuando el usuario mueve el ratón fuera del navegador (intent de salida).

Si quieres desactivar alguno, pon `"enabled": false`.

**No hace falta regenerar el sitio al cambiar el popup** — se sirve dinámicamente.

## Regenerar el sitio

Cuando cambies `data.json` (añadir centros, editar categorías, etc.) o el dominio:

```bash
python build.py
```

Regenera los 123 HTMLs + sitemap + robots en pocos segundos.

## Actualizar imágenes de centros

Para volver a scrapear fotos desde Google Maps (por ejemplo tras añadir centros nuevos):

```bash
pip install playwright
python -m playwright install chromium
python scrape_images.py
```

El script usa el `maps_url` de cada centro en `data.json` para extraer la URL de la foto de portada de Google. Es seguro relanzar — reanuda desde el cache (`img_cache.json`).

Después:

```bash
python build.py
```

para que los nuevos HTMLs usen las nuevas imágenes.

## SEO implementado

- ✅ **108 URLs indexables** (una por centro) — no SPA, HTML estático renderizado
- ✅ **Schema.org**: `EducationalOrganization`, `BreadcrumbList`, `FAQPage`, `CollectionPage`, `WebSite`, `Organization` — con `@id`, `geo`, `aggregateRating`, `address`, `telephone`, `sameAs`
- ✅ **Canonical tags** en todas las páginas
- ✅ **Open Graph + Twitter Cards** con imagen real del centro
- ✅ **Sitemap XML** con prioridades y lastmod
- ✅ **Robots.txt** con referencia a sitemap
- ✅ **Breadcrumbs accesibles** con schema y visuales
- ✅ **Meta description dinámica** por centro, categoría y ciudad
- ✅ **Imágenes `<img>`** (no `background-image`) con `alt`, `loading`, `fetchpriority`, `decoding`
- ✅ **Preconnect** a Google Fonts y lh3.googleusercontent.com
- ✅ **Internal linking** coherente (breadcrumbs + related + city/category chips)

## Accesibilidad

- `lang="vi"` correcto
- `aria-label`, `aria-hidden`, `aria-expanded` en elementos interactivos
- `:focus-visible` con outline dorado
- Contraste alto en hero (textos blancos sobre fondo oscuro sólido)
- `prefers-reduced-motion` respetado
- Estructura semántica: `<main>`, `<nav>`, `<article>`, `<section>`, `<aside>`, `<footer>`

## Performance

- Imágenes lazy load (excepto hero con fetchpriority="high")
- Dimensiones explícitas (evita CLS)
- Fuentes con `display=swap` + preconnect
- CSS en un solo archivo (sin imports externos en runtime)
- JavaScript mínimo, diferido (`defer`)
- HTML estático servido directamente (TTFB bajísimo)

## Licencia

MIT
