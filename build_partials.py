"""
Generador de partials reutilizables: header, footer, meta SEO, schema base.
Se usa desde build.py
"""
from urllib.parse import quote

# ────────────────────────────────────────────────────────────────────
# Config del sitio — el único sitio donde editar dominio, nombres, etc.
# ────────────────────────────────────────────────────────────────────
SITE = {
    'domain':  'https://anhnguvn.com',
    'name':    'Anh Ngữ Việt Nam',
    'slogan':  'Danh bạ trung tâm Anh ngữ hàng đầu 2026',
    'lang':    'vi',
    'og_image': '/img/og-default.jpg',
}


def meta_head(title, description, canonical_path, og_image=None, noindex=False):
    """Genera las meta tags estándar de <head>. canonical_path empieza con '/'"""
    abs_canonical = SITE['domain'].rstrip('/') + canonical_path
    og_img_path = og_image or SITE['og_image']
    abs_og = SITE['domain'].rstrip('/') + og_img_path if og_img_path.startswith('/') else og_img_path
    robots = '<meta name="robots" content="noindex,nofollow">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">'
    # GTM script — se mantiene fuera del f-string para no tener que escapar las llaves de JS
    gtm_script = (
        "  <!-- Google Tag Manager -->\n"
        "  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\n"
        "  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],\n"
        "  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\n"
        "  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\n"
        "  })(window,document,'script','dataLayer','GTM-NKLFP824');</script>\n"
        "  <!-- End Google Tag Manager -->"
    )
    return f'''  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
{gtm_script}
  <meta name="google-site-verification" content="kuaIq8DDYo98l7mhePwrJ1jQHknPK9EJsbSI1rBrw78">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{abs_canonical}">
  {robots}
  <meta property="og:type" content="website">
  <meta property="og:locale" content="vi_VN">
  <meta property="og:site_name" content="{SITE['name']}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{abs_canonical}">
  <meta property="og:image" content="{abs_og}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{abs_og}">
  <link rel="stylesheet" href="__CSSPATH__styles.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preconnect" href="https://lh3.googleusercontent.com">
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;900&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&display=swap" rel="stylesheet">'''


def header_html(base='/'):
    """Header con rutas relativas. base es prefijo desde la página actual."""
    b = base
    return f'''  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-NKLFP824"
  height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <!-- End Google Tag Manager (noscript) -->
  <a class="announcement-bar" href="https://vanec.vn/english/" target="_blank" rel="noopener" data-action="announcement">
    <div class="container ann-inner">
      <span class="ann-pulse" aria-hidden="true"></span>
      <span class="ann-text">
        <strong>Làm nhà hàng — khách sạn mà tiếng Anh còn ngập ngừng?</strong>
        <span class="ann-sub">Khóa học chuyên ngành dịch vụ của <strong>VANEC English</strong> — học là dùng được ngay với khách quốc tế</span>
      </span>
      <span class="ann-cta">Tìm hiểu ngay <span aria-hidden="true">→</span></span>
    </div>
  </a>
  <header id="siteHeader">
    <div class="container header-inner">
      <a href="{b}" class="logo" aria-label="{SITE['name']} - Trang chủ">
        <span class="logo-mark" aria-hidden="true">AN</span>
        <span class="logo-text">Anh Ngữ <em>Việt Nam</em></span>
      </a>
      <nav class="desktop-nav" aria-label="Menu chính">
        <a href="{b}danh-muc/">Danh mục</a>
        <a href="{b}thanh-pho/ho-chi-minh.html">Hồ Chí Minh</a>
        <a href="{b}thanh-pho/da-nang.html">Đà Nẵng</a>
        <a href="{b}thanh-pho/ha-noi.html">Hà Nội</a>
        <a href="{b}them-trung-tam.html" class="nav-cta">Thêm trung tâm</a>
      </nav>
      <button class="mobile-toggle" id="mobileToggle" aria-label="Mở menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>
  <nav id="mobileNav" class="mobile-nav" aria-hidden="true">
    <a href="{b}danh-muc/">Danh mục</a>
    <a href="{b}thanh-pho/ho-chi-minh.html">Hồ Chí Minh</a>
    <a href="{b}thanh-pho/da-nang.html">Đà Nẵng</a>
    <a href="{b}thanh-pho/ha-noi.html">Hà Nội</a>
    <a href="{b}them-trung-tam.html">Thêm trung tâm</a>
  </nav>'''


def footer_html(base='/'):
    b = base
    return f'''  <footer>
    <div class="container">
      <div class="footer-top">
        <div class="footer-brand">
          <a href="{b}" class="logo">
            <span class="logo-mark">AN</span>
            <span class="logo-text">Anh Ngữ <em>Việt Nam</em></span>
          </a>
          <p>Cẩm nang của bạn về trung tâm Anh ngữ tại Việt Nam. Thông tin minh bạch, cập nhật thường xuyên.</p>
        </div>
        <div class="footer-links">
          <div class="footer-col">
            <h4>Điều hướng</h4>
            <a href="{b}">Trang chủ</a>
            <a href="{b}danh-muc/">Tất cả danh mục</a>
            <a href="{b}gioi-thieu.html">Giới thiệu</a>
            <a href="{b}them-trung-tam.html">Thêm trung tâm</a>
          </div>
          <div class="footer-col">
            <h4>Thành phố</h4>
            <a href="{b}thanh-pho/ho-chi-minh.html">Hồ Chí Minh</a>
            <a href="{b}thanh-pho/da-nang.html">Đà Nẵng</a>
            <a href="{b}thanh-pho/ha-noi.html">Hà Nội</a>
          </div>
          <div class="footer-col">
            <h4>Pháp lý</h4>
            <a href="{b}chinh-sach-bao-mat.html">Quyền riêng tư</a>
            <a href="{b}dieu-khoan.html">Điều khoản</a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 Anh Ngữ Việt Nam. Mọi quyền được bảo lưu.</p>
      </div>
    </div>
  </footer>'''


def mobile_toggle_script():
    """Script mínimo inline para menú móvil y scroll del header"""
    return '''  <script>
  (function(){
    var h = document.getElementById('siteHeader');
    if (h) window.addEventListener('scroll', function(){
      h.classList.toggle('scrolled', window.scrollY > 40);
    }, {passive:true});
    var t = document.getElementById('mobileToggle');
    var n = document.getElementById('mobileNav');
    if (t && n) t.addEventListener('click', function(){
      var open = n.classList.toggle('open');
      t.classList.toggle('active', open);
      t.setAttribute('aria-expanded', String(open));
      n.setAttribute('aria-hidden', String(!open));
    });
  })();
  </script>'''


def stars_html(rating):
    """Estrellas HTML accesibles"""
    if not rating:
        return '<span class="stars stars-none" aria-label="Chưa có đánh giá">─</span>'
    r = round(rating)
    full = '★' * r
    empty = '☆' * (5 - r)
    return f'<span class="stars" aria-label="{rating} trên 5 sao">{full}{empty}</span>'
