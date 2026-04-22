"""
Scraper de imágenes de Google Maps para el directorio de Vietnam.

USO (desde la carpeta del proyecto, donde está data.json):
    python scrape_images.py

Es seguro relanzarlo: si se interrumpe, reanuda desde donde lo dejó
gracias al cache (img_cache.json).
"""
import json, re, sys, time, os
from concurrent.futures import ThreadPoolExecutor, as_completed
from playwright.sync_api import sync_playwright

# Rutas relativas al directorio actual
HERE   = os.path.dirname(os.path.abspath(__file__))
INPUT  = os.path.join(HERE, 'data.json')
OUTPUT = os.path.join(HERE, 'data.json')
CACHE  = os.path.join(HERE, 'img_cache.json')

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

WORKERS = 4  # Paralelismo. Sube a 6-8 si tu máquina aguanta.


def normalize(url: str) -> str:
    """Normaliza URL al tamaño w408-h272 (estándar para cards)."""
    base = re.split(r'=[wsh]\d', url, maxsplit=1)[0]
    return base + '=w408-h272-k-no'


def scrape_one(center):
    slug = center['slug']
    maps_url = center.get('maps_url')
    if not maps_url:
        return slug, None

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            ctx = browser.new_context(
                viewport={'width': 1280, 'height': 900},
                user_agent=UA,
                locale='en-US',
            )
            page = ctx.new_page()

            preview_bodies = []
            def on_response(r):
                if '/maps/preview/place' in r.url:
                    try:
                        preview_bodies.append(r.body())
                    except Exception:
                        pass
            page.on('response', on_response)

            try:
                page.goto(maps_url, timeout=20000)
            except Exception:
                pass
            page.wait_for_timeout(4000)
            browser.close()
    except Exception:
        return slug, None

    if not preview_bodies:
        return slug, None

    all_urls = []
    for body in preview_bodies:
        txt = body.decode('utf-8', errors='ignore')
        if txt.startswith(")]}'"):
            txt = txt[4:]
        urls = re.findall(r'https://lh\d\.googleusercontent\.com/[^"\\,\]\s]+', txt)
        all_urls.extend(urls)

    if not all_urls:
        return slug, None

    # Formato clásico /p/AF1Q... > /gps-cs-s/ > /gps-proxy/
    classic = [u for u in all_urls if '/p/AF1Q' in u]
    gps     = [u for u in all_urls if '/gps-cs-s/' in u]
    proxy   = [u for u in all_urls if '/gps-proxy/' in u]
    chosen  = (classic or gps or proxy or all_urls)[0]
    return slug, normalize(chosen)


def main():
    if not os.path.exists(INPUT):
        print(f'ERROR: No encuentro data.json en {HERE}')
        print('Ejecuta este script DENTRO de la carpeta del proyecto.')
        sys.exit(1)

    with open(INPUT, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cache = {}
    if os.path.exists(CACHE):
        with open(CACHE, 'r', encoding='utf-8') as f:
            cache = json.load(f)
        print(f'Cache cargado: {len(cache)} entradas')

    centers = data['centers']
    pending = [c for c in centers if not cache.get(c['slug'])]
    print(f'Total: {len(centers)} | Pendientes: {len(pending)}')

    if pending:
        t0 = time.time()
        done = 0
        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            futures = {ex.submit(scrape_one, c): c for c in pending}
            for fut in as_completed(futures):
                try:
                    slug, img = fut.result()
                except Exception:
                    c = futures[fut]
                    slug, img = c['slug'], None
                cache[slug] = img
                done += 1
                status = 'OK' if img else '--'
                if done % 3 == 0 or done == len(pending):
                    elapsed = time.time() - t0
                    rate = done / elapsed if elapsed > 0 else 0
                    eta = (len(pending) - done) / rate if rate > 0 else 0
                    print(f'  [{done:3d}/{len(pending)}] {status} {slug[:55]:55s}  ({rate:.1f}/s, ETA {eta:4.0f}s)',
                          flush=True)
                if done % 10 == 0:
                    with open(CACHE, 'w', encoding='utf-8') as f:
                        json.dump(cache, f, ensure_ascii=False, indent=2)
        with open(CACHE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
        print(f'\nScraping terminado en {time.time()-t0:.1f}s')

    # Inyectar en data.json
    found = 0
    for c in centers:
        img = cache.get(c['slug'])
        if img:
            c['image'] = img
            found += 1
        else:
            c['image'] = None

    print(f'\n=== Resumen ===')
    print(f'  Total:       {len(centers)}')
    print(f'  Con imagen:  {found}  ({100*found/len(centers):.0f}%)')
    print(f'  Sin imagen:  {len(centers)-found}')

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'\nGuardado: {OUTPUT}')
    print('Ahora abre index.html en el navegador y deberias ver las imagenes.')


if __name__ == '__main__':
    main()
