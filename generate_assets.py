"""
generate_assets.py — Genera los assets que faltan: favicon, logo, og-default, apple-touch-icon
Coherente con la identidad del directorio: marca "AN" con fondo gradiente.
Se ejecuta una sola vez para crear los assets en /img/ y la raíz.
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(ROOT, 'img')
os.makedirs(IMG_DIR, exist_ok=True)

# Paleta — coherente con la marca: navy oscuro + acento dorado/cremoso
BG_DARK = (15, 23, 42)        # slate-900
BG_MID  = (30, 41, 59)        # slate-800
ACCENT  = (217, 175, 119)     # dorado suave (Playfair Display feel)
TEXT_W  = (248, 250, 252)     # blanco hueso

def load_font(size, bold=False):
    """Carga una fuente que tenga buen soporte para texto latino."""
    candidates = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    ]
    for c in candidates:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


def gradient_bg(w, h, c1, c2):
    """Crea un degradado vertical c1 (top) → c2 (bottom)."""
    img = Image.new('RGB', (w, h), c1)
    draw = ImageDraw.Draw(img)
    for y in range(h):
        ratio = y / max(1, h - 1)
        r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
        g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
        b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    return img


# ─────────────────────────────────────────────────────
# 1) OG default — 1200x630 (estándar Open Graph)
# ─────────────────────────────────────────────────────
def build_og():
    w, h = 1200, 630
    img = gradient_bg(w, h, BG_DARK, BG_MID)
    draw = ImageDraw.Draw(img)

    # Mark "AN" arriba a la izquierda
    mark_size = 90
    mark = load_font(mark_size, bold=True)
    draw.text((80, 80), 'AN', font=mark, fill=ACCENT)

    # Título grande
    title = load_font(78, bold=True)
    draw.text((80, 220), 'Anh Ngữ Việt Nam', font=title, fill=TEXT_W)

    # Subtítulo
    sub = load_font(36, bold=False)
    draw.text((80, 330), 'Danh bạ trung tâm Anh ngữ', font=sub, fill=(203, 213, 225))
    draw.text((80, 380), 'tại Hồ Chí Minh, Đà Nẵng, Hà Nội', font=sub, fill=(203, 213, 225))

    # Línea acento
    draw.rectangle([(80, 470), (200, 478)], fill=ACCENT)

    # Footer del banner
    footer = load_font(28, bold=False)
    draw.text((80, 510), 'anhnguvn.com', font=footer, fill=ACCENT)

    out = os.path.join(IMG_DIR, 'og-default.jpg')
    img.save(out, 'JPEG', quality=88, optimize=True)
    print(f'  ✓ {out}')


# ─────────────────────────────────────────────────────
# 2) Logo — 512x512 con marca "AN" centrada
# ─────────────────────────────────────────────────────
def build_logo():
    size = 512
    img = gradient_bg(size, size, BG_DARK, BG_MID)
    draw = ImageDraw.Draw(img)

    # Borde redondeado simulado con un margen + texto centrado
    font = load_font(280, bold=True)
    text = 'AN'
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - tw) // 2 - bbox[0]
    y = (size - th) // 2 - bbox[1] - 20
    draw.text((x, y), text, font=font, fill=ACCENT)

    out = os.path.join(IMG_DIR, 'logo.png')
    img.save(out, 'PNG', optimize=True)
    print(f'  ✓ {out}')


# ─────────────────────────────────────────────────────
# 3) Favicon — multi-size .ico + .svg
# ─────────────────────────────────────────────────────
def build_favicon():
    # Versión bitmap multi-size
    sizes = [16, 32, 48]
    images = []
    for s in sizes:
        img = gradient_bg(s, s, BG_DARK, BG_MID)
        draw = ImageDraw.Draw(img)
        # Tamaño de fuente proporcional
        font_size = int(s * 0.7)
        font = load_font(font_size, bold=True)
        # Usar "A" sola en tamaños pequeños
        text = 'A' if s <= 16 else 'AN'
        if text == 'AN':
            font = load_font(int(s * 0.55), bold=True)
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = (s - tw) // 2 - bbox[0]
        y = (s - th) // 2 - bbox[1] - 1
        draw.text((x, y), text, font=font, fill=ACCENT)
        images.append(img)

    out = os.path.join(ROOT, 'favicon.ico')
    images[0].save(out, format='ICO', sizes=[(s, s) for s in sizes],
                   append_images=images[1:])
    print(f'  ✓ {out}')

    # Versión SVG simple — más nítida en pantallas HiDPI
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>
  </defs>
  <rect width="32" height="32" rx="6" fill="url(#g)"/>
  <text x="16" y="22" text-anchor="middle" font-family="Georgia,serif" font-weight="700"
        font-size="18" fill="#d9af77">A</text>
</svg>'''
    out_svg = os.path.join(ROOT, 'favicon.svg')
    with open(out_svg, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f'  ✓ {out_svg}')


# ─────────────────────────────────────────────────────
# 4) Apple touch icon — 180x180
# ─────────────────────────────────────────────────────
def build_apple_icon():
    size = 180
    img = gradient_bg(size, size, BG_DARK, BG_MID)
    draw = ImageDraw.Draw(img)
    font = load_font(100, bold=True)
    text = 'AN'
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - tw) // 2 - bbox[0]
    y = (size - th) // 2 - bbox[1] - 5
    draw.text((x, y), text, font=font, fill=ACCENT)

    out = os.path.join(ROOT, 'apple-touch-icon.png')
    img.save(out, 'PNG', optimize=True)
    print(f'  ✓ {out}')


if __name__ == '__main__':
    print('Generando assets...')
    build_og()
    build_logo()
    build_favicon()
    build_apple_icon()
    print('Done.')
