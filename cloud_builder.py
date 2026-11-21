#!/usr/bin/env python3
"""
Dream Home Decor (https://dreamhomedecor.net/) — Ultra-Fast (<0.5s) Living Room & Home Decor Static Site Builder
Builds complete static site into /Users/khawariqbal/antigravity/Articles/dreamhomedecor-site/public_html
"""

import os
import re
import json
import html
import math
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CMS_DIR = os.path.join(BASE_DIR, "cms-data")
ARTICLES_DB = os.path.join(CMS_DIR, "articles.json")
PAGES_DB = os.path.join(CMS_DIR, "pages.json")
CATEGORIES_DB = os.path.join(CMS_DIR, "categories.json")
SETTINGS_DB = os.path.join(CMS_DIR, "settings.json")
IMAGE_MAP_DB = os.path.join(CMS_DIR, "webp_map.json")
OUT_DIR = BASE_DIR
SITE_URL = "https://dreamhomedecor.net"
POSTS_PER_PAGE = 12


def load_site_settings():
    default_settings = {
        "ga4_id": "G-MTS6C9QM0N",
        "clarity_id": "x9ncd53tna",
        "new_adsense_code": '<meta name="google-adsense-account" content="ca-pub-4002444368603667">\n<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4002444368603667" crossorigin="anonymous"></script>',
        "header_code": "<!-- Custom Header Verification / Scripts -->",
        "footer_code": "<!-- Custom Footer Scripts -->",
        "ads_txt": "google.com, pub-4002444368603667, DIRECT, f08c47fec0942fa0\n",
        "robots_txt": f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n",
    }
    if os.path.exists(SETTINGS_DB):
        try:
            with open(SETTINGS_DB, "r", encoding="utf-8") as f:
                saved = json.load(f)
            default_settings.update(saved)
        except Exception:
            pass
    else:
        with open(SETTINGS_DB, "w", encoding="utf-8") as f:
            json.dump(default_settings, f, indent=2, ensure_ascii=False)
    return default_settings


def load_webp_map():
    if os.path.exists(IMAGE_MAP_DB):
        try:
            with open(IMAGE_MAP_DB, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def strip_tags(s):
    if not s:
        return ""
    t = re.sub(r"<[^>]+>", " ", s)
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t).strip()


def clamp_seo(text, max_len):
    text = strip_tags(text)
    if len(text) <= max_len:
        return text
    cut = text[:max_len]
    sp = cut.rfind(" ")
    if sp > max_len - 16:
        cut = cut[:sp]
    return cut.rstrip(" ,;:-—|")


def rewrite_img_url_to_webp(url, webp_map):
    if not url:
        return "/assets/default-decor.svg"
    url = url.replace("http://dreamhomedecor.net", "https://dreamhomedecor.net")
    if url in webp_map:
        return webp_map[url]
    # Check without query string
    clean_u = url.split("?")[0]
    if clean_u in webp_map:
        return webp_map[clean_u]
    return url


CRITICAL_CSS = """
:root{--bg:#faf8f5;--surface:#ffffff;--cream:#f3efe9;--ink:#1c1917;--muted:#57534e;--soft:#78716c;--accent:#b4532a;--accent-dk:#8f3e1c;--accent-tint:#fdf3ee;--sage:#233d31;--sage-tint:#eef3f0;--border:#e7e1d8;--radius:16px;--radius-sm:10px;--maxw:1220px;--font-sans:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;--font-serif:Georgia,"Palatino Linotype","Book Antiqua",Palatino,serif;--shadow:0 2px 6px rgba(28,25,23,.04),0 10px 24px rgba(28,25,23,.05);--shadow-hover:0 8px 20px rgba(28,25,23,.09),0 18px 36px rgba(28,25,23,.07)}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth;font-family:var(--font-sans);-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--font-sans);font-size:16.5px;line-height:1.72;-webkit-font-smoothing:antialiased;overflow-x:hidden}
img,picture,video{max-width:100%;height:auto;display:block}
a{color:var(--accent);text-decoration:none;transition:color .15s ease}
a:hover{color:var(--accent-dk)}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 20px}
.topbar{background:var(--sage);color:rgba(255,255,255,.9);font-size:.78rem;border-bottom:1px solid rgba(255,255,255,.12)}
.topbar-in{max-width:var(--maxw);margin:0 auto;padding:6px 20px;display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
.topbar-tag{font-weight:700;letter-spacing:.03em;color:#e6f0ea}
.topbar-links{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.topbar-links a{color:rgba(255,255,255,.86);font-weight:600}
.topbar-links a:hover{color:#fff;text-decoration:underline}
.site-header{position:sticky;top:0;z-index:100;background:rgba(250,248,245,.96);backdrop-filter:blur(10px);border-bottom:1px solid var(--border)}
.nav-bar{max-width:var(--maxw);margin:0 auto;padding:11px 20px;display:flex;align-items:center;justify-content:space-between;gap:14px}
.brand{display:inline-flex;align-items:center;gap:10px;color:var(--ink);text-decoration:none;flex-shrink:0}
.brand svg{height:46px;width:auto;display:block}
.main-nav{display:flex;align-items:center;gap:3px;margin-left:auto;flex-wrap:nowrap}
.main-nav a{display:inline-block;padding:7px 12px;border-radius:999px;font-size:.87rem;font-weight:600;color:var(--ink);white-space:nowrap;transition:background .15s ease,color .15s ease}
.main-nav a:hover,.main-nav a.active{background:var(--accent);color:#fff}
.mob-btn{display:none;background:var(--cream);border:1px solid var(--border);color:var(--ink);border-radius:999px;padding:7px 14px;font-size:.86rem;font-weight:700;cursor:pointer}
.hero{background:linear-gradient(180deg,var(--cream) 0%,var(--bg) 100%);border-bottom:1px solid var(--border);padding:32px 0 36px}
.hero-grid{display:grid;grid-template-columns:1.08fr .92fr;gap:32px;align-items:center}
.eyebrow{display:inline-block;font-size:.75rem;font-weight:800;text-transform:uppercase;letter-spacing:.09em;color:var(--accent);background:var(--accent-tint);border:1px solid rgba(180,83,42,.22);padding:4px 12px;border-radius:999px;margin-bottom:12px}
.hero h1{font-family:var(--font-serif);font-size:clamp(1.9rem,3.6vw,2.75rem);line-height:1.16;color:var(--ink);margin:0 0 14px;letter-spacing:-.02em}
.hero-lede{font-size:1.04rem;color:var(--muted);margin:0 0 18px}
.hero-card{border-radius:var(--radius);overflow:hidden;background:var(--surface);border:1px solid var(--border);box-shadow:var(--shadow-hover);display:block;color:inherit}
.hero-img{aspect-ratio:16/10;overflow:hidden;background:var(--cream)}
.hero-img img{width:100%;height:100%;object-fit:cover;transition:transform .35s ease}
.hero-card:hover .hero-img img{transform:scale(1.03)}
.hero-body{padding:16px 20px}
.hero-body h2{font-family:var(--font-serif);font-size:1.22rem;margin:6px 0 6px;line-height:1.3;color:var(--ink)}
.room-pills{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:22px;padding-top:18px;border-top:1px solid var(--border)}
.room-lbl{font-size:.76rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-right:4px}
.room-pill{display:inline-flex;align-items:center;gap:6px;padding:6px 13px;border-radius:999px;background:var(--surface);border:1px solid var(--border);color:var(--ink);font-size:.84rem;font-weight:700;transition:all .15s ease}
.room-pill:hover,.room-pill.active{background:var(--sage);color:#fff;border-color:var(--sage)}
.room-cnt{font-size:.73rem;opacity:.8;font-weight:600}
.sec-head{display:flex;align-items:baseline;justify-content:space-between;gap:12px;margin:32px 0 18px;border-bottom:2px solid var(--border);padding-bottom:10px}
.sec-head h2{font-family:var(--font-serif);font-size:1.5rem;margin:0;color:var(--ink)}
.post-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-bottom:36px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow);display:flex;flex-direction:column;transition:transform .18s ease,box-shadow .18s ease}
.card:hover{transform:translateY(-3px);box-shadow:var(--shadow-hover)}
.card-thumb{position:relative;aspect-ratio:16/10.5;overflow:hidden;background:var(--cream);border-bottom:1px solid var(--border);display:block}
.card-thumb img{width:100%;height:100%;object-fit:cover;transition:transform .3s ease}
.card:hover .card-thumb img{transform:scale(1.04)}
.cat-badge{display:inline-block;font-size:.71rem;font-weight:800;text-transform:uppercase;letter-spacing:.07em;padding:3px 10px;border-radius:999px;background:var(--accent-tint);color:var(--accent);align-self:flex-start}
.card-body{padding:18px 20px 20px;display:flex;flex-direction:column;flex:1}
.card-title{font-family:var(--font-serif);font-size:1.15rem;line-height:1.34;margin:8px 0 10px}
.card-title a{color:var(--ink)}
.card-title a:hover{color:var(--accent)}
.card-exc{font-size:.9rem;color:var(--muted);margin:0 0 14px;flex:1;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.card-meta{display:flex;align-items:center;justify-content:space-between;font-size:.78rem;color:var(--soft);padding-top:12px;border-top:1px solid var(--border);font-weight:600}
.pager{margin:24px 0 48px;display:flex;justify-content:center;gap:8px;flex-wrap:wrap}
.page-num{display:inline-flex;align-items:center;justify-content:center;min-width:40px;height:40px;padding:0 14px;border-radius:999px;background:var(--surface);border:1px solid var(--border);color:var(--ink);font-weight:700;font-size:.88rem}
.page-num.active,.page-num:hover{background:var(--accent);color:#fff;border-color:var(--accent)}
.single-grid{display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:34px;align-items:start;margin:26px 0 52px}
.crumb{font-size:.83rem;color:var(--soft);margin-bottom:12px}
.crumb a{color:var(--muted);font-weight:600}
.art-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:34px 40px;box-shadow:var(--shadow)}
.art-card h1{font-family:var(--font-serif);font-size:clamp(1.75rem,3.2vw,2.4rem);line-height:1.2;color:var(--ink);margin:10px 0 16px}
.byline{display:flex;align-items:center;flex-wrap:wrap;gap:12px;padding:12px 0;border-top:1px solid var(--border);border-bottom:1px solid var(--border);margin-bottom:24px;font-size:.85rem;color:var(--muted)}
.avatar{width:36px;height:36px;border-radius:50%;background:var(--sage);color:#fff;font-weight:800;font-size:.85rem;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0}
.feat-hero{margin:0 0 24px;border-radius:var(--radius-sm);overflow:hidden;background:var(--cream)}
.feat-hero img{width:100%;max-height:540px;object-fit:cover}
.toc{background:var(--bg);border:1px solid var(--border);border-left:4px solid var(--accent);border-radius:var(--radius-sm);padding:16px 20px;margin:0 0 24px}
.toc summary{font-weight:800;font-size:.94rem;color:var(--ink);cursor:pointer}
.toc ol{margin:10px 0 0;padding-left:20px;display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:6px 18px;font-size:.87rem}
.toc a{color:var(--muted);font-weight:600}
.toc a:hover{color:var(--accent);text-decoration:underline}
.entry h2{font-family:var(--font-serif);font-size:clamp(1.36rem,2.3vw,1.72rem);color:var(--ink);margin:1.85em 0 .55em;line-height:1.28;padding-bottom:6px;border-bottom:1px solid var(--border)}
.entry h3{font-family:var(--font-serif);font-size:1.2rem;color:var(--ink);margin:1.45em 0 .45em}
.entry p{margin:0 0 1.2em;color:#292524}
.entry figure,.entry .wp-block-image{margin:1.5em 0;border-radius:var(--radius-sm);overflow:hidden}
.entry img{border-radius:var(--radius-sm);background:var(--cream)}
.pin-wrap{position:relative;display:block;overflow:hidden;border-radius:var(--radius-sm);background:var(--cream);margin:1.4em 0}
.entry figure .pin-wrap,.feat-hero .pin-wrap{margin:0}
.pin-wrap img{width:100%;height:auto;display:block;transition:transform .38s cubic-bezier(.22,1,.36,1);cursor:zoom-in}
.pin-wrap:hover img,.pin-wrap.touch-zoom img{transform:scale(1.045)}
.pin-btn{position:absolute;top:12px;left:12px;z-index:10;background:#e60023;color:#fff !important;font-family:var(--font-sans);font-size:.8rem;font-weight:800;padding:7px 13px;border-radius:999px;display:inline-flex;align-items:center;gap:6px;box-shadow:0 4px 14px rgba(0,0,0,.25);opacity:.94;transition:transform .15s ease,opacity .15s ease,background .15s ease;text-decoration:none !important}
.pin-btn:hover{background:#ad081b;color:#fff !important;transform:scale(1.05);opacity:1}
.zoom-hint{position:absolute;bottom:10px;right:10px;z-index:9;background:rgba(28,25,23,.72);color:#fff;font-size:.72rem;font-weight:700;padding:4px 10px;border-radius:999px;pointer-events:none;backdrop-filter:blur(4px)}
.dhd-lightbox{display:none;position:fixed;inset:0;z-index:9999;background:rgba(15,14,13,.92);align-items:center;justify-content:center;padding:18px;cursor:zoom-out}
.dhd-lightbox.open{display:flex}
.dhd-lightbox img{max-width:95vw;max-height:90vh;border-radius:12px;box-shadow:0 20px 60px rgba(0,0,0,.5);object-fit:contain}
.dhd-lb-close{position:fixed;top:18px;right:20px;background:#fff;color:#1c1917;border:0;border-radius:999px;padding:8px 16px;font-weight:800;font-size:.88rem;cursor:pointer;z-index:10000}
.founder-img{width:76px;height:76px;border-radius:50%;object-fit:cover;border:2px solid var(--accent);flex-shrink:0}
.byline-img{width:38px;height:38px;border-radius:50%;object-fit:cover;border:1.5px solid var(--accent);flex-shrink:0}
.author-box{display:flex;gap:18px;align-items:flex-start;background:var(--cream);border:1px solid var(--border);border-radius:var(--radius-sm);padding:22px;margin-top:34px}
.author-box .avatar{width:54px;height:54px;font-size:1.05rem}
.author-box h3{margin:0 0 6px;font-family:var(--font-serif);font-size:1.1rem}
.author-box p{margin:0 0 10px;font-size:.89rem;color:var(--muted)}
.sidebar{display:flex;flex-direction:column;gap:22px;position:sticky;top:84px}
.widget{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px;box-shadow:var(--shadow)}
.w-title{font-family:var(--font-serif);font-size:1.1rem;margin:0 0 14px;padding-bottom:8px;border-bottom:2px solid var(--border);color:var(--ink)}
.rec-list,.cat-list{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:12px}
.rec-item{display:flex;gap:12px;align-items:center}
.rec-thumb{width:68px;height:52px;border-radius:8px;overflow:hidden;flex-shrink:0;background:var(--cream)}
.rec-thumb img{width:100%;height:100%;object-fit:cover}
.rec-t{font-size:.87rem;font-weight:700;line-height:1.32;color:var(--ink)}
.cat-list a{display:flex;justify-content:space-between;align-items:center;padding:8px 12px;border-radius:8px;background:var(--bg);color:var(--ink);font-size:.87rem;font-weight:600}
.cat-list a:hover{background:var(--accent-tint);color:var(--accent)}
.site-footer{background:#1c1917;color:rgba(255,255,255,.86);padding:50px 0 30px;margin-top:56px;font-size:.89rem}
.foot-grid{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:30px;margin-bottom:34px}
.site-footer h4{color:#fff;font-size:.9rem;text-transform:uppercase;letter-spacing:.07em;margin:0 0 14px}
.site-footer p{color:rgba(255,255,255,.75);font-size:.87rem}
.site-footer ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}
.site-footer a{color:rgba(255,255,255,.82)}
.site-footer a:hover{color:#fff;text-decoration:underline}
.foot-bot{border-top:1px solid rgba(255,255,255,.14);padding-top:18px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;font-size:.81rem;color:rgba(255,255,255,.68)}
@media(max-width:1024px){.post-grid{grid-template-columns:repeat(2,1fr)}.single-grid{grid-template-columns:1fr}.sidebar{position:static}}
@media(max-width:860px){.hero-grid,.foot-grid{grid-template-columns:1fr}.mob-btn{display:inline-flex}.main-nav{display:none;width:100%;flex-direction:column;align-items:flex-start;padding-top:10px}.main-nav.open{display:flex}.nav-bar{flex-wrap:wrap}.art-card{padding:22px 18px}}
@media(max-width:580px){.post-grid{grid-template-columns:1fr}}
""".strip()

LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 68" width="235" height="50" role="img" aria-label="Dream Home Decor">
  <g transform="translate(2, 4)">
    <rect x="0" y="0" width="58" height="58" rx="14" fill="#233d31"/>
    <path d="M12 30 L29 14 L46 30" fill="none" stroke="#e8c39e" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M17 28 V45 H41 V28" fill="none" stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M22 45 V36 C22 34, 36 34, 36 36 V45" fill="#b4532a"/>
    <circle cx="29" cy="23" r="2.5" fill="#e8c39e"/>
  </g>
  <g transform="translate(72, 0)">
    <text x="0" y="34" font-family="Georgia, 'Palatino Linotype', serif" font-size="26" font-weight="700" fill="#1c1917" letter-spacing="-0.4">Dream Home</text>
    <text x="1" y="55" font-family="ui-sans-serif, system-ui, -apple-system, sans-serif" font-size="14.5" font-weight="800" fill="#b4532a" letter-spacing="3.8">LIVING &amp; DECOR</text>
  </g>
</svg>"""

FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 58 58"><rect width="58" height="58" rx="14" fill="#233d31"/><path d="M12 30 L29 14 L46 30" fill="none" stroke="#e8c39e" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M17 28 V45 H41 V28" fill="none" stroke="#ffffff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M22 45 V36 C22 34, 36 34, 36 36 V45" fill="#b4532a"/></svg>"""


def render_head(title, desc, canonical_url, preload_img="", settings=None, json_ld=None):
    settings = settings or {}
    safe_title = html.escape(clamp_seo(title, 60))
    safe_desc = html.escape(clamp_seo(desc, 160))
    ga4 = settings.get("ga4_id", "G-MTS6C9QM0N")
    clarity = settings.get("clarity_id", "x9ncd53tna")
    new_ads = settings.get("new_adsense_code", "")
    extra_head = settings.get("header_code", "")

    preload_tag = ""
    if preload_img:
        preload_tag = f'<link rel="preload" as="image" href="{html.escape(preload_img)}" fetchpriority="high">\n'

    schema_tag = ""
    if json_ld:
        schema_tag = f'<script type="application/ld+json">{json.dumps(json_ld, ensure_ascii=False)}</script>\n'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{safe_title}</title>
<meta name="description" content="{safe_desc}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{html.escape(canonical_url)}">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Dream Home Decor">
<meta property="og:title" content="{safe_title}">
<meta property="og:description" content="{safe_desc}">
<meta property="og:url" content="{html.escape(canonical_url)}">
{f'<meta property="og:image" content="{html.escape(preload_img)}">' if preload_img else ''}
{preload_tag}<style id="dhd-critical-css">{CRITICAL_CSS}</style>
{schema_tag}<script>
window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());
{f"gtag('config','{ga4}');" if ga4 else ""}
window.addEventListener('load',function(){{setTimeout(function(){{
{f"var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id={ga4}';document.head.appendChild(s);" if ga4 else ""}
{f'(function(c,l,a,r,i,t,y){{c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);}})(window,document,"clarity","script","{clarity}");' if clarity else ""}
}},1000);}});
</script>
{new_ads}
{extra_head}
</head>
<body>
"""


def render_header(active_slug=""):
    return f"""<div class="topbar">
  <div class="topbar-in">
    <span class="topbar-tag">✨ Curated Living Room &amp; Cozy Home Decor Inspiration</span>
    <div class="topbar-links">
      <a href="/about-us/">About Us</a>
      <a href="/contact/">Contact</a>
      <a href="/privacy-policy/">Privacy Policy</a>
      <a href="/disclaimer/">Disclaimer</a>
      <a href="/terms-and-conditions/">Terms</a>
    </div>
  </div>
</div>
<header class="site-header">
  <div class="nav-bar">
    <a class="brand" href="/" aria-label="Dream Home Decor Home">{LOGO_SVG}</a>
    <button class="mob-btn" type="button" onclick="document.getElementById('dhd-nav').classList.toggle('open')">☰ Menu</button>
    <nav class="main-nav" id="dhd-nav" aria-label="Main Navigation">
      <a href="/" class="{'active' if active_slug == 'home' else ''}">Home</a>
      <a href="/category/living-room-ideas/" class="{'active' if active_slug == 'living-room-ideas' else ''}">Living Room</a>
      <a href="/category/bedroom-ideas/" class="{'active' if active_slug == 'bedroom-ideas' else ''}">Bedroom</a>
      <a href="/category/bathroom-ideas/" class="{'active' if active_slug == 'bathroom-ideas' else ''}">Bathroom</a>
      <a href="/category/home-decor-ideas/" class="{'active' if active_slug == 'home-decor-ideas' else ''}">Home Decor</a>
      <a href="/category/boho-bedroom-ideas/" class="{'active' if active_slug == 'boho-bedroom-ideas' else ''}">Boho &amp; Cozy</a>
      <a href="/category/ceiling-ideas/" class="{'active' if active_slug == 'ceiling-ideas' else ''}">Ceiling Ideas</a>
      <a href="/about-us/" class="{'active' if active_slug == 'about-us' else ''}">About</a>
      <a href="/contact/" class="{'active' if active_slug == 'contact' else ''}">Contact</a>
    </nav>
  </div>
</header>
"""


def render_footer(settings=None):
    settings = settings or {}
    extra_foot = settings.get("footer_code", "")
    return f"""<div class="dhd-lightbox" id="dhd-lb" onclick="closeDhdZoom()">
  <button type="button" class="dhd-lb-close" onclick="closeDhdZoom()">✕ Close Zoom</button>
  <img id="dhd-lb-img" src="" alt="Zoomed interior view">
</div>
<script>
function openDhdZoom(src, alt) {{
  var lb = document.getElementById('dhd-lb');
  var im = document.getElementById('dhd-lb-img');
  if (lb && im) {{ im.src = src; im.alt = alt || ''; lb.classList.add('open'); }}
}}
function closeDhdZoom() {{
  var lb = document.getElementById('dhd-lb');
  if (lb) lb.classList.remove('open');
}}
document.addEventListener('DOMContentLoaded', function() {{
  var pageUrl = encodeURIComponent(window.location.href);
  var pageTitle = document.title;
  document.querySelectorAll('.entry img, .feat-hero img').forEach(function(img) {{
    if (img.closest('.pin-wrap') || img.width === 140) return;
    var wrap = document.createElement('div');
    wrap.className = 'pin-wrap';
    img.parentNode.insertBefore(wrap, img);
    wrap.appendChild(img);

    var rawSrc = img.getAttribute('src') || '';
    var fullMedia = rawSrc.indexOf('http') === 0 ? rawSrc : (window.location.origin + rawSrc);
    var desc = encodeURIComponent(img.getAttribute('alt') || pageTitle);
    var pinHref = 'https://www.pinterest.com/pin/create/button/?url=' + pageUrl + '&media=' + encodeURIComponent(fullMedia) + '&description=' + desc;

    var pinBtn = document.createElement('a');
    pinBtn.className = 'pin-btn';
    pinBtn.href = pinHref;
    pinBtn.target = '_blank';
    pinBtn.rel = 'noopener noreferrer';
    pinBtn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.373 0 0 5.372 0 12c0 5.084 3.163 9.426 7.627 11.174-.105-.949-.2-2.405.042-3.441.218-.937 1.407-5.965 1.407-5.965s-.359-.719-.359-1.782c0-1.668.967-2.914 2.171-2.914 1.023 0 1.518.769 1.518 1.69 0 1.029-.655 2.568-.994 3.995-.283 1.194.599 2.169 1.777 2.169 2.133 0 3.772-2.249 3.772-5.495 0-2.873-2.064-4.882-5.012-4.882-3.414 0-5.418 2.561-5.418 5.207 0 1.031.397 2.138.893 2.738a.36.36 0 01.083.345l-.333 1.36c-.053.22-.174.267-.402.161-1.499-.698-2.436-2.889-2.436-4.649 0-3.785 2.75-7.262 7.929-7.262 4.163 0 7.398 2.967 7.398 6.931 0 4.136-2.607 7.464-6.227 7.464-1.216 0-2.359-.631-2.75-1.378l-.748 2.853c-.271 1.043-1.002 2.35-1.492 3.146C9.57 23.812 10.763 24 12 24c6.627 0 12-5.373 12-12 0-6.628-5.373-12-12-12z"/></svg> Save';
    pinBtn.addEventListener('click', function(ev) {{ ev.stopPropagation(); }});
    wrap.appendChild(pinBtn);

    var hint = document.createElement('span');
    hint.className = 'zoom-hint';
    hint.textContent = '🔍 Tap to Zoom';
    wrap.appendChild(hint);

    img.addEventListener('click', function() {{
      openDhdZoom(img.src, img.alt);
    }});
    wrap.addEventListener('touchstart', function() {{
      wrap.classList.add('touch-zoom');
      setTimeout(function() {{ wrap.classList.remove('touch-zoom'); }}, 900);
    }}, {{passive: true}});
  }});
}});
</script>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <h4>About Dream Home Decor</h4>
        <p>Dream Home Decor (<code>dreamhomedecor.net</code>) is an independent interior styling publication founded by Claire Vance in Austin, Texas—dedicated to cozy living room layouts, warm neutral bedrooms, spa bathrooms, and practical home decor ideas.</p>
      </div>
      <div>
        <h4>Explore by Room</h4>
        <ul>
          <li><a href="/category/living-room-ideas/">Living Room Ideas</a></li>
          <li><a href="/category/bedroom-ideas/">Bedroom Ideas</a></li>
          <li><a href="/category/bathroom-ideas/">Bathroom Ideas</a></li>
          <li><a href="/category/home-decor-ideas/">Home Decor Ideas</a></li>
          <li><a href="/category/boho-bedroom-ideas/">Boho Bedroom Ideas</a></li>
          <li><a href="/category/ceiling-ideas/">Ceiling Ideas</a></li>
          <li><a href="/category/christmas-home-decore/">Seasonal &amp; Holiday Decor</a></li>
        </ul>
      </div>
      <div>
        <h4>Legal &amp; Editorial</h4>
        <ul>
          <li><a href="/about-us/">About Us &amp; Editorial Team</a></li>
          <li><a href="/contact/">Contact Us</a></li>
          <li><a href="/privacy-policy/">Privacy Policy</a></li>
          <li><a href="/disclaimer/">Disclaimer</a></li>
          <li><a href="/terms-and-conditions/">Terms &amp; Conditions</a></li>
          <li><a href="/sitemap.xml">XML Sitemap</a></li>
        </ul>
      </div>
      <div>
        <h4>Editorial Standards</h4>
        <p>Every room makeover guide features high-resolution photography with 1-click Pinterest saving and room-by-room layout tips.</p>
        <ul>
          <li><a href="/about-us/">👩‍🎨 Meet Claire Vance (Founder)</a></li>
          <li><a href="/contact/">✉️ Contact Editorial Desk</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bot">
      <span>© {datetime.now().year} Dream Home Decor (dreamhomedecor.net). All rights reserved.</span>
      <span>Designed for &lt;0.5s Ultra-Fast Core Web Vitals</span>
    </div>
  </div>
</footer>
{extra_foot}
</body>
</html>
"""


def optimize_article_html(raw_html, webp_map):
    if not raw_html:
        return "", []
    headings = []
    h_idx = [0]

    def repl_h2(m):
        h_idx[0] += 1
        attrs = m.group(1) or ""
        inner = m.group(2) or ""
        plain = strip_tags(inner)
        slug = re.sub(r"[^a-z0-9]+", "-", plain.lower()).strip("-") or f"idea-{h_idx[0]}"
        slug = f"{slug}-{h_idx[0]}"
        headings.append((slug, plain))
        if "id=" not in attrs.lower():
            attrs += f' id="{slug}"'
        return f"<h2{attrs}>{inner}</h2>"

    content = re.sub(r"<h2([^>]*)>([\s\S]*?)</h2>", repl_h2, raw_html, flags=re.I)

    img_idx = [0]

    def repl_img(m):
        img_idx[0] += 1
        tag = m.group(0)
        # Replace src with WebP URL
        def sub_src(sm):
            q = sm.group(1)
            u = sm.group(2)
            return f"src={q}{rewrite_img_url_to_webp(u, webp_map)}{q}"

        tag = re.sub(r'\bsrc=(["\'])([^"\']+)\1', sub_src, tag, flags=re.I)
        # Replace srcset urls
        def sub_srcset(sm):
            q = sm.group(1)
            val = sm.group(2)
            parts = []
            for item in val.split(","):
                item = item.strip()
                if not item:
                    continue
                sp = item.split(" ")
                sp[0] = rewrite_img_url_to_webp(sp[0], webp_map)
                parts.append(" ".join(sp))
            return f"srcset={q}{', '.join(parts)}{q}"

        tag = re.sub(r'\bsrcset=(["\'])([^"\']+)\1', sub_srcset, tag, flags=re.I)

        if "decoding=" not in tag.lower():
            tag = tag.replace("<img ", '<img decoding="async" ', 1)
        if img_idx[0] == 1:
            tag = re.sub(r'\bloading=(["\'])lazy\1', 'loading="eager" fetchpriority="high"', tag, flags=re.I)
            if "loading=" not in tag.lower():
                tag = tag.replace("<img ", '<img loading="eager" fetchpriority="high" ', 1)
        else:
            if "loading=" not in tag.lower():
                tag = tag.replace("<img ", '<img loading="lazy" ', 1)
        return tag

    content = re.sub(r"<img\b[^>]*>", repl_img, content, flags=re.I)
    return content, headings


def render_post_card(post, webp_map, eager=False):
    feat = rewrite_img_url_to_webp(post.get("featured", ""), webp_map)
    load_attr = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    cat_slug = post.get("category", "home-decor-ideas")
    cat_name = post.get("category_name", "Home Decor Ideas")
    date_str = (post.get("date", "") or "")[:10]
    words = len(strip_tags(post.get("content", "")).split())
    read_min = max(2, round(words / 220))
    return f"""<article class="card">
  <a class="card-thumb" href="/{post['slug']}/">
    <img src="{html.escape(feat)}" alt="{html.escape(post['title'])}" width="640" height="420" {load_attr} decoding="async">
  </a>
  <div class="card-body">
    <a class="cat-badge" href="/category/{html.escape(cat_slug)}/">{html.escape(cat_name)}</a>
    <h3 class="card-title"><a href="/{post['slug']}/">{html.escape(post['title'])}</a></h3>
    <p class="card-exc">{html.escape(post.get('excerpt', ''))}</p>
    <div class="card-meta">
      <span>By Claire Vance</span>
      <span>{date_str} · {read_min} min read</span>
    </div>
  </div>
</article>"""


def write_page(rel_path, html_content):
    full_path = os.path.join(OUT_DIR, rel_path.lstrip("/"))
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(html_content)


def build_all():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(OUT_DIR, "assets"), exist_ok=True)
    founder_src = os.path.join(BASE_DIR, "founder-claire-vance.webp")
    founder_dst = os.path.join(OUT_DIR, "assets", "founder-claire-vance.webp")
    if os.path.exists(founder_src) and not os.path.exists(founder_dst):
        import shutil
        shutil.copyfile(founder_src, founder_dst)

    # Write favicon & default fallback SVG
    with open(os.path.join(OUT_DIR, "assets", "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(FAVICON_SVG)
    with open(os.path.join(OUT_DIR, "assets", "default-decor.svg"), "w", encoding="utf-8") as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 420"><rect width="640" height="420" fill="#f3efe9"/><text x="320" y="215" text-anchor="middle" font-family="Georgia,serif" font-size="24" fill="#8f3e1c">Dream Home Decor</text></svg>')

    settings = load_site_settings()
    webp_map = load_webp_map()

    with open(ARTICLES_DB, "r", encoding="utf-8") as f:
        all_posts = json.load(f)
    with open(PAGES_DB, "r", encoding="utf-8") as f:
        all_pages = json.load(f)
    with open(CATEGORIES_DB, "r", encoding="utf-8") as f:
        categories = json.load(f)

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    published_posts = [p for p in all_posts if p.get("status", "publish") == "publish"]
    published_posts.sort(key=lambda x: x.get("date", ""), reverse=True)

    recent_5 = published_posts[:5]

    def render_sidebar():
        rec_items = []
        for rp in recent_5:
            r_img = rewrite_img_url_to_webp(rp.get("featured", ""), webp_map)
            rec_items.append(f"""<li class="rec-item">
              <a class="rec-thumb" href="/{rp['slug']}/"><img src="{html.escape(r_img)}" alt="{html.escape(rp['title'])}" width="68" height="52" loading="lazy" decoding="async"></a>
              <a class="rec-t" href="/{rp['slug']}/">{html.escape(rp['title'])}</a>
            </li>""")
        cat_items = []
        for cslug, cobj in sorted(categories.items(), key=lambda kv: kv[1].get("count", 0), reverse=True):
            cnt = sum(1 for p in published_posts if cslug in p.get("categories", [p.get("category")]))
            if cnt > 0 and cslug != "uncategorized":
                cat_items.append(f'<li><a href="/category/{cslug}/"><span>{html.escape(cobj["name"])}</span><span>({cnt})</span></a></li>')
        return f"""<aside class="sidebar">
          <div class="widget">
            <h3 class="w-title">About the Founder</h3>
            <div style="display:flex;gap:14px;align-items:center;margin-bottom:12px">
              <img class="founder-img" src="/assets/founder-claire-vance.webp" alt="Claire Vance — Founder &amp; Lead Interior Stylist" width="76" height="76" loading="lazy" decoding="async">
              <div>
                <strong style="display:block;font-size:.98rem;color:var(--ink)">Claire Vance</strong>
                <span style="font-size:.78rem;color:var(--accent);font-weight:700">Founder &amp; Lead Interior Stylist · Austin, TX</span>
              </div>
            </div>
            <p style="font-size:.88rem;color:var(--muted);margin:0 0 10px">Claire Vance is an Austin-based interior stylist and founder of Dream Home Decor, sharing cozy living room layouts, warm neutral bedrooms, and budget-friendly room makeovers for modern American homes.</p>
            <a href="/about-us/" style="font-weight:700;font-size:.85rem">Read Claire&apos;s Story →</a>
          </div>
          <div class="widget">
            <h3 class="w-title">Latest Decor Guides</h3>
            <ul class="rec-list">{''.join(rec_items)}</ul>
          </div>
          <div class="widget">
            <h3 class="w-title">Browse by Room</h3>
            <ul class="cat-list">{''.join(cat_items)}</ul>
          </div>
        </aside>"""

    sidebar_html = render_sidebar()

    # 1. Build Individual Article Pages (/<slug>/index.html)
    for idx, post in enumerate(published_posts):
        slug = post["slug"]
        title = post["title"]
        seo_title = clamp_seo(post.get("seo_title") or title, 60)
        seo_desc = clamp_seo(post.get("seo_description") or post.get("excerpt") or title, 160)
        canonical = f"{SITE_URL}/{slug}/"
        feat = rewrite_img_url_to_webp(post.get("featured", ""), webp_map)
        opt_content, headings = optimize_article_html(post.get("content", ""), webp_map)

        toc_html = ""
        if len(headings) >= 3:
            li_tags = "".join(f'<li><a href="#{h_id}">{html.escape(h_txt)}</a></li>' for h_id, h_txt in headings)
            toc_html = f"""<details class="toc">
              <summary>📋 Quick Jump — In This Home Decor Guide ({len(headings)} Ideas)</summary>
              <ol>{li_tags}</ol>
            </details>"""

        # Related posts in same category
        cat_slug = post.get("category", "home-decor-ideas")
        cat_name = post.get("category_name", "Home Decor Ideas")
        related = [p for p in published_posts if p["slug"] != slug and p.get("category") == cat_slug][:3]
        if len(related) < 3:
            for p in published_posts:
                if p["slug"] != slug and p not in related:
                    related.append(p)
                if len(related) == 3:
                    break
        rel_cards = "".join(render_post_card(rp, webp_map) for rp in related)

        words = len(strip_tags(post.get("content", "")).split())
        read_min = max(2, round(words / 220))
        date_str = (post.get("date", "") or "")[:10]

        json_ld = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": seo_title,
            "description": seo_desc,
            "image": [feat] if feat else [],
            "datePublished": post.get("date", ""),
            "dateModified": post.get("modified", post.get("date", "")),
            "author": {"@type": "Person", "name": "Claire Vance", "url": f"{SITE_URL}/about-us/"},
            "publisher": {"@type": "Organization", "name": "Dream Home Decor", "url": SITE_URL},
            "mainEntityOfPage": canonical,
        }

        feat_block = ""
        # Only render separate featured image banner if content doesn't already start with the same image
        if feat and feat not in opt_content[:600]:
            feat_block = f'<div class="feat-hero"><img src="{html.escape(feat)}" alt="{html.escape(title)}" width="1080" height="680" loading="eager" fetchpriority="high" decoding="async"></div>'

        page_html = (
            render_head(seo_title, seo_desc, canonical, preload_img=feat, settings=settings, json_ld=json_ld)
            + render_header(active_slug=cat_slug)
            + f"""<main class="wrap">
              <div class="single-grid">
                <article class="art-card">
                  <div class="crumb"><a href="/">Home</a> › <a href="/category/{html.escape(cat_slug)}/">{html.escape(cat_name)}</a> › <span>{html.escape(title)}</span></div>
                  <a class="cat-badge" href="/category/{html.escape(cat_slug)}/">{html.escape(cat_name)}</a>
                  <h1>{html.escape(title)}</h1>
                  <div class="byline">
                    <img class="byline-img" src="/assets/founder-claire-vance.webp" alt="Claire Vance" width="38" height="38">
                    <span>By <strong>Claire Vance</strong> (Founder &amp; Lead Interior Stylist)</span>
                    <span>· Updated {date_str}</span>
                    <span>· {read_min} min read</span>
                  </div>
                  {feat_block}
                  {toc_html}
                  <div class="entry">{opt_content}</div>
                  <div class="author-box">
                    <img class="founder-img" src="/assets/founder-claire-vance.webp" alt="Claire Vance — Founder &amp; Lead Interior Stylist" width="76" height="76" loading="lazy" decoding="async">
                    <div>
                      <h3>Written by Claire Vance — Founder &amp; Lead Interior Stylist</h3>
                      <p>Based in Austin, Texas, Claire Vance curates practical living room layouts, warm neutral bedrooms, and timeless interior styling guides for modern homes. Hover or tap any photo above and click <strong>📌 Save</strong> to pin your favorite ideas directly to Pinterest.</p>
                    </div>
                  </div>
                </article>
                {sidebar_html}
              </div>
              <section>
                <div class="sec-head"><h2>More {html.escape(cat_name)} You Will Love</h2></div>
                <div class="post-grid">{rel_cards}</div>
              </section>
            </main>"""
            + render_footer(settings)
        )
        write_page(f"{slug}/index.html", page_html)

    # 2. Build Static Legal & Trust Pages
    for pg in all_pages:
        pslug = pg["slug"]
        if pslug in ("home", "sample-page"):
            continue
        ptitle = pg["title"]
        seo_title = clamp_seo(pg.get("seo_title") or f"{ptitle} — Dream Home Decor", 60)
        seo_desc = clamp_seo(pg.get("seo_description") or f"{ptitle} for Dream Home Decor (dreamhomedecor.net).", 160)
        canonical = f"{SITE_URL}/{pslug}/"
        opt_content, _ = optimize_article_html(pg.get("content", ""), webp_map)
        page_html = (
            render_head(seo_title, seo_desc, canonical, settings=settings)
            + render_header(active_slug=pslug)
            + f"""<main class="wrap">
              <div class="single-grid">
                <article class="art-card">
                  <div class="crumb"><a href="/">Home</a> › <span>{html.escape(ptitle)}</span></div>
                  <h1>{html.escape(ptitle)}</h1>
                  <div class="entry">{opt_content}</div>
                </article>
                {sidebar_html}
              </div>
            </main>"""
            + render_footer(settings)
        )
        write_page(f"{pslug}/index.html", page_html)
        if pslug == "privacy":
            write_page("privacy-policy/index.html", page_html)
        elif pslug == "contact-us":
            write_page("contact/index.html", page_html)

    # 3. Build Homepage & Paginated Archive (/index.html and /page/2/index.html...)
    total_pages = max(1, math.ceil(len(published_posts) / POSTS_PER_PAGE))
    hero_post = published_posts[0] if published_posts else None
    hero_feat = rewrite_img_url_to_webp(hero_post.get("featured", ""), webp_map) if hero_post else ""

    room_pills_list = []
    for cslug, cobj in sorted(categories.items(), key=lambda kv: kv[1].get("count", 0), reverse=True):
        cnt = sum(1 for p in published_posts if cslug in p.get("categories", [p.get("category")]))
        if cnt > 0 and cslug != "uncategorized":
            room_pills_list.append(
                f'<a class="room-pill" href="/category/{cslug}/">{html.escape(cobj["name"])} <span class="room-cnt">({cnt})</span></a>'
            )
    room_pills_html = "".join(room_pills_list)

    for page_num in range(1, total_pages + 1):
        start_i = (page_num - 1) * POSTS_PER_PAGE
        slice_posts = published_posts[start_i : start_i + POSTS_PER_PAGE]
        cards_html = "".join(render_post_card(p, webp_map, eager=(i < 3)) for i, p in enumerate(slice_posts))

        # Pagination links
        pager_links = []
        if page_num > 1:
            prev_url = "/" if page_num == 2 else f"/page/{page_num - 1}/"
            pager_links.append(f'<a class="page-num" href="{prev_url}">← Prev</a>')
        for p_i in range(1, total_pages + 1):
            if p_i == 1 or p_i == total_pages or abs(p_i - page_num) <= 2:
                p_url = "/" if p_i == 1 else f"/page/{p_i}/"
                cls = "page-num active" if p_i == page_num else "page-num"
                pager_links.append(f'<a class="{cls}" href="{p_url}">{p_i}</a>')
        if page_num < total_pages:
            pager_links.append(f'<a class="page-num" href="/page/{page_num + 1}/">Next →</a>')
        pager_html = f'<nav class="pager" aria-label="Pagination">{"".join(pager_links)}</nav>' if total_pages > 1 else ""

        if page_num == 1:
            h_title = "Dream Home Decor — Cozy Living Room & Home Styling Ideas"
            h_desc = "Explore 230+ curated living room ideas, cozy bedroom layouts, modern bathroom makeovers, and warm home decor guides on Dream Home Decor."
            canonical = f"{SITE_URL}/"
        else:
            h_title = clamp_seo(f"Dream Home Decor Ideas — Page {page_num} of {total_pages}", 60)
            h_desc = clamp_seo(f"Browse page {page_num} of Dream Home Decor's 234+ living room, bedroom, bathroom, and home styling guides.", 160)
            canonical = f"{SITE_URL}/page/{page_num}/"

        hero_section = ""
        if page_num == 1 and hero_post:
            hero_section = f"""<section class="hero">
              <div class="wrap">
                <div class="hero-grid">
                  <div>
                    <span class="eyebrow">LIVING ROOM &amp; HOME DECOR MAGAZINE</span>
                    <h1>Warm, Timeless Living Room &amp; Home Decor Ideas for Real Homes</h1>
                    <p class="hero-lede">From cozy apartment living rooms and layered neutral bedrooms to spa-inspired bathroom makeovers — explore {len(published_posts)}+ room-by-room styling guides curated by Claire Vance.</p>
                  </div>
                  <a class="hero-card" href="/{hero_post['slug']}/">
                    <div class="hero-img">
                      <img src="{html.escape(hero_feat)}" alt="{html.escape(hero_post['title'])}" width="720" height="450" loading="eager" fetchpriority="high" decoding="async">
                    </div>
                    <div class="hero-body">
                      <span class="cat-badge">Featured Guide · {html.escape(hero_post.get('category_name', 'Home Decor'))}</span>
                      <h2>{html.escape(hero_post['title'])}</h2>
                    </div>
                  </a>
                </div>
                <div class="room-pills">
                  <span class="room-lbl">Browse by Room:</span>
                  {room_pills_html}
                </div>
              </div>
            </section>"""

        home_html = (
            render_head(h_title, h_desc, canonical, preload_img=(hero_feat if page_num == 1 else ""), settings=settings)
            + render_header(active_slug="home")
            + hero_section
            + f"""<main class="wrap">
              <div class="sec-head">
                <h2>{'Latest Living Room & Home Decor Guides' if page_num == 1 else f'Home Decor Guides — Page {page_num}'}</h2>
                <span style="font-size:.86rem;color:var(--soft);font-weight:600">Showing {start_i + 1}–{min(len(published_posts), start_i + POSTS_PER_PAGE)} of {len(published_posts)} Articles</span>
              </div>
              <div class="post-grid">{cards_html}</div>
              {pager_html}
            </main>"""
            + render_footer(settings)
        )
        if page_num == 1:
            write_page("index.html", home_html)
        else:
            write_page(f"page/{page_num}/index.html", home_html)

    # 4. Build Category Archives (/category/<slug>/index.html)
    for cslug, cobj in categories.items():
        cat_posts = [p for p in published_posts if cslug in p.get("categories", [p.get("category")])]
        cname = cobj["name"]
        c_title = clamp_seo(f"{cname} — Cozy Decor & Styling Guides ({len(cat_posts)} Ideas)", 60)
        c_desc = clamp_seo(cobj.get("description") or f"Browse {len(cat_posts)} curated {cname} articles on Dream Home Decor.", 160)
        canonical = f"{SITE_URL}/category/{cslug}/"
        cards_html = "".join(render_post_card(p, webp_map, eager=(i < 3)) for i, p in enumerate(cat_posts))
        if not cards_html:
            cards_html = "<p>New guides coming soon in this category!</p>"

        cat_html = (
            render_head(c_title, c_desc, canonical, settings=settings)
            + render_header(active_slug=cslug)
            + f"""<section class="hero" style="padding:26px 0">
              <div class="wrap">
                <div class="crumb"><a href="/">Home</a> › <span>{html.escape(cname)}</span></div>
                <span class="eyebrow">ROOM CATEGORY · {len(cat_posts)} GUIDES</span>
                <h1>{html.escape(cname)}</h1>
                <p class="hero-lede" style="max-width:780px;margin-bottom:0">{html.escape(c_desc)}</p>
              </div>
            </section>
            <main class="wrap" style="margin-top:28px">
              <div class="post-grid">{cards_html}</div>
            </main>"""
            + render_footer(settings)
        )
        write_page(f"category/{cslug}/index.html", cat_html)

    # 5. Build 404.html, CNAME, robots.txt, ads.txt, and XML Sitemap
    not_found_html = (
        render_head("Page Not Found — Dream Home Decor", "Explore our latest living room, bedroom, and bathroom decor guides.", f"{SITE_URL}/404.html", settings=settings)
        + render_header()
        + f"""<main class="wrap" style="padding:48px 20px;text-align:center">
          <h1>Page Not Found (404)</h1>
          <p>The page you are looking for may have moved. Explore our newest decor guides below:</p>
          <div class="post-grid" style="text-align:left;margin-top:28px">{''.join(render_post_card(p, webp_map) for p in published_posts[:6])}</div>
        </main>"""
        + render_footer(settings)
    )
    write_page("404.html", not_found_html)
    write_page("CNAME", "dreamhomedecor.net\n")
    write_page("robots.txt", settings.get("robots_txt", f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n"))
    write_page("ads.txt", settings.get("ads_txt", ""))

    # Build sitemap.xml
    urls_xml = [f"<url><loc>{SITE_URL}/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>"]
    for pg in all_pages:
        urls_xml.append(f"<url><loc>{SITE_URL}/{pg['slug']}/</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>")
    for cslug in categories:
        urls_xml.append(f"<url><loc>{SITE_URL}/category/{cslug}/</loc><changefreq>weekly</changefreq><priority>0.7</priority></url>")
    for p in published_posts:
        urls_xml.append(f"<url><loc>{SITE_URL}/{p['slug']}/</loc><changefreq>weekly</changefreq><priority>0.9</priority></url>")
    sitemap_content = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls_xml)
        + "\n</urlset>\n"
    )
    write_page("sitemap.xml", sitemap_content)
    write_page("post-sitemap.xml", sitemap_content)

    return {
        "published": len(published_posts),
        "pages": len(all_pages),
        "categories": len(categories),
    }


if __name__ == "__main__":
    stats = build_all()
    print(f"✅ Built Dream Home Decor Static Site: {stats}")
