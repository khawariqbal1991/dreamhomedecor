#!/usr/bin/env python3
"""
Dream Home Decor (https://dreamhomedecor.net/) — 3D Cozy Architectural Luxury Edition (<0.3s Mobile & Desktop)
Features:
- 100% New 3D Spatial Cozy Interior Design Theme (GPU-accelerated 3D cards, floating glass header, bento hero, 3D gallery frames)
- Strictly 10 Articles Per Page on BOTH Homepage AND All Category Pages (/category/<slug>/page/<n>/)
- Ultra-fast <0.3s load on Mobile & Desktop using inline Critical CSS + content-visibility:auto + native WebP
- Minimized Table of Contents by default (<details class="toc">)
- U.S. Founder Persona: Claire Vance (Austin, TX) with realistic portrait photo & zero old Pinterest profile links
- Pinterest "📌 Save" button + 3D Hover/Tap Zoom Lightbox on every article image
- Contact Us Form -> khawariqbal1991@gmail.com with 4-Layer Anti-Spam
- New Google AdSense (ca-pub-4002444368603667) + ads.txt + GA4 (G-MTS6C9QM0N) + Clarity (x9ncd53tna)
"""

import os
import re
import json
import html
import math
import shutil
from datetime import datetime

BASE_DIR = "/Users/khawariqbal/antigravity/Articles/dreamhomedecor-site"
ARTICLES_DB = os.path.join(BASE_DIR, "cms-data", "articles.json")
PAGES_DB = os.path.join(BASE_DIR, "cms-data", "pages.json")
CATEGORIES_DB = os.path.join(BASE_DIR, "cms-data", "categories.json")
SETTINGS_DB = os.path.join(BASE_DIR, "cms-data", "settings.json")
IMAGE_MAP_DB = os.path.join(BASE_DIR, "cms-data", "webp_map.json")
OUT_DIR = BASE_DIR
SITE_URL = "https://dreamhomedecor.net"
POSTS_PER_PAGE = 10


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
    clean_u = url.split("?")[0]
    if clean_u in webp_map:
        return webp_map[clean_u]
    return url


CRITICAL_CSS = """
:root{
  --bg:#f6f1ea;
  --surface:#ffffff;
  --cream:#efe7dc;
  --ink:#1e1916;
  --muted:#5c534c;
  --soft:#7d7268;
  --accent:#b85428;
  --accent-dk:#8e3c17;
  --accent-tint:#fdf2ec;
  --sage:#1f3a2e;
  --sage-lt:#2e5343;
  --gold:#c89d66;
  --border:#e4d9c8;
  --bevel:#d5c7b2;
  --radius-xl:20px;
  --radius:16px;
  --radius-sm:12px;
  --maxw:1240px;
  --font-sans:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  --font-serif:Georgia,"Palatino Linotype","Book Antiqua",Palatino,serif;
  --shadow-3d:0 4px 12px rgba(38,26,17,.06);
  --shadow-3d-hover:0 10px 22px rgba(38,26,17,.11);
}
*,*::before,*::after{box-sizing:border-box}
html{font-family:var(--font-sans);-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--font-sans);font-size:16.5px;line-height:1.74;-webkit-font-smoothing:antialiased;overflow-x:hidden}
img,picture,video{max-width:100%;height:auto;display:block}
a{color:var(--accent);text-decoration:none}
a:hover{color:var(--accent-dk)}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 20px}

/* Crisp Tactile 3D Header + Direct Upfront Legal Bar (Matching Mobile & Desktop Mockups) */
.topbar{position:relative;background:#183528;color:rgba(255,255,255,.94);font-size:.76rem;border-bottom:1px solid rgba(255,255,255,.12);overflow:hidden}
.topbar-wave{position:absolute;left:0;bottom:-1px;width:360px;height:38px;pointer-events:none;z-index:1}
.topbar-in{position:relative;z-index:2;max-width:var(--maxw);margin:0 auto;padding:7px 20px;display:flex;align-items:center;justify-content:flex-end}
.topbar-links{display:flex;align-items:center;justify-content:flex-end;gap:4px 8px;flex-wrap:wrap}
.tb-row{display:inline-flex;align-items:center;gap:8px}
.tb-sep{color:rgba(255,255,255,.35);font-weight:400;user-select:none}
.topbar-links a{color:#f3eadc;font-weight:700;letter-spacing:.01em;white-space:nowrap;padding:1px 4px;border-radius:4px}
.topbar-links a:hover,.topbar-links a.active{color:#fff;background:rgba(255,255,255,.15);text-decoration:none}

.site-header{position:sticky;top:0;z-index:100;background:#fbf8f3;border-bottom:2px solid var(--bevel);box-shadow:0 3px 10px rgba(35,24,16,.05)}
.nav-bar{max-width:var(--maxw);margin:0 auto;padding:10px 20px;display:flex;align-items:center;justify-content:space-between;gap:10px}
.brand{display:inline-flex;align-items:center;gap:10px;color:var(--ink);text-decoration:none;flex-shrink:0}
.brand svg{height:44px;width:auto;display:block}
.main-nav{display:flex;align-items:center;gap:4px;margin-left:auto;flex-wrap:nowrap}
.main-nav a{display:inline-flex;align-items:center;gap:6px;padding:7px 13px;border-radius:999px;font-size:.84rem;font-weight:700;color:#1e1916;white-space:nowrap}
.main-nav a svg{width:16px;height:16px;flex-shrink:0;color:#2b473a}
.main-nav a:hover{background:var(--cream)}
.main-nav a.active{background:#183528;color:#fff;box-shadow:0 3px 8px rgba(24,53,40,.22)}
.main-nav a.active svg{color:#fff}
.nav-search-btn{display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:50%;background:#fff;border:1px solid var(--border);border-bottom:2px solid var(--bevel);color:#183528;cursor:pointer;margin-left:4px;flex-shrink:0}
.nav-search-btn:hover{background:var(--cream);color:var(--accent)}
.mob-btn{display:none;align-items:center;gap:7px;background:#ffffff;border:1.5px solid #dfd5c5;border-bottom:3px solid #cfc2ae;color:#183528;border-radius:999px;padding:7px 16px;font-size:.88rem;font-weight:800;cursor:pointer;box-shadow:0 2px 6px rgba(30,25,20,.05)}

/* Tactile 3D Bento Hero Showcase (Exact Desktop & Mobile Mockup Match) */
.hero{padding:22px 0 20px}
.hero-bento{display:grid;grid-template-columns:1.03fr .97fr;gap:22px;align-items:stretch}
.hero-left-3d{position:relative;overflow:hidden;background:#fffdf9;border:1px solid var(--border);border-bottom:5px solid var(--bevel);border-radius:24px;padding:30px 32px;box-shadow:var(--shadow-3d);display:flex;flex-direction:column;justify-content:center}
.eyebrow-row{display:flex;align-items:center;justify-content:center;gap:12px;margin-bottom:16px;width:100%}
.eyebrow-line{flex:1;max-width:48px;height:1px;background:#d6c7b2}
.eyebrow{display:inline-flex;align-items:center;gap:6px;font-size:.73rem;font-weight:800;text-transform:uppercase;letter-spacing:.08em;color:#183528;background:#f2eadf;border:1px solid #dfd2c0;padding:6px 15px;border-radius:999px}
.eyebrow-spark{color:#d98a2b;font-size:.85rem}
.hero h1{font-family:var(--font-serif);font-size:clamp(1.9rem,3.3vw,2.62rem);line-height:1.15;color:#172e23;margin:0 0 14px;letter-spacing:-.02em}
.h1-for-desk{display:block;font-style:italic;color:#9e5822;margin-top:2px}
.real-homes-hl{position:relative;display:inline-block;color:#c86428}
.real-curve{position:absolute;left:0;bottom:-7px;width:105%;height:11px;pointer-events:none}
.hero-lede{font-size:1rem;line-height:1.65;color:#4a433c;margin:0 0 20px}
.hero-lede strong{color:#183528;font-weight:800}

/* Desktop Inline Stats Strip + Explore Ideas Pill CTA inside Hero Card */
.desk-stats-bar{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;padding:14px 0 16px;border-top:1px solid #ece3d5;margin-top:auto}
.d-stat{display:flex;align-items:center;gap:10px;padding:0 10px;border-right:1px solid #dfd4c3}
.d-stat:first-child{padding-left:0}
.d-stat:last-child{border-right:none;padding-right:0}
.d-stat-ico{width:34px;height:34px;border-radius:10px;background:#eef3ec;color:#183528;display:inline-flex;align-items:center;justify-content:center;flex-shrink:0}
.d-stat-ico svg{width:20px;height:20px}
.d-stat-txt strong{display:block;font-size:1.18rem;line-height:1.1;color:#183528;font-weight:900}
.d-stat-txt span{display:block;font-size:.66rem;color:#655c53;font-weight:800;text-transform:uppercase;letter-spacing:.05em;margin-top:2px}
.hero-cta-wrap{display:flex;justify-content:center;padding-top:4px}
.hero-explore-btn{display:inline-flex;align-items:center;gap:8px;background:#183528;color:#fff !important;font-size:.9rem;font-weight:800;padding:11px 28px;border-radius:999px;box-shadow:0 6px 16px rgba(24,53,40,.22);border-bottom:2px solid #0e2118}
.hero-explore-btn:hover{background:#214736;color:#fff !important}

/* Mobile 3 Circular-Badge Stat Cards (Exact Mobile Mockup Match) */
.mob-stats-grid{display:none;grid-template-columns:repeat(3,1fr);gap:10px;margin:14px 0 4px}
.m-stat-card{background:#fffdf9;border:1px solid var(--border);border-bottom:4px solid var(--bevel);border-radius:18px;padding:14px 8px 13px;text-align:center;box-shadow:var(--shadow-3d);display:flex;flex-direction:column;align-items:center}
.m-stat-badge{width:40px;height:40px;border-radius:50%;background:#183528;color:#fff;display:inline-flex;align-items:center;justify-content:center;margin-bottom:8px;box-shadow:0 3px 8px rgba(24,53,40,.2)}
.m-stat-badge svg{width:20px;height:20px}
.m-stat-card strong{display:block;font-size:1.35rem;line-height:1.15;color:#183528;font-weight:900;margin-bottom:4px}
.m-stat-card span{display:block;font-size:.7rem;line-height:1.25;color:#4a433c;font-weight:800;text-transform:uppercase;letter-spacing:.05em}

/* Right Hero Column: Big Living Room Showcase Photo + Floating Featured Cover Story Card */
.hero-right-col{display:flex;flex-direction:column;gap:14px}
.hero-showcase-photo{border-radius:22px;overflow:hidden;background:var(--cream);border:1px solid var(--border);border-bottom:5px solid var(--bevel);box-shadow:var(--shadow-3d);aspect-ratio:16/10;position:relative}
.hero-showcase-photo img{width:100%;height:100%;object-fit:cover;display:block}
.hero-cover-card{background:#fffdf9;border:1px solid var(--border);border-bottom:4px solid var(--bevel);border-radius:18px;padding:14px 18px;box-shadow:var(--shadow-3d);display:flex;align-items:center;justify-content:space-between;gap:16px;color:inherit}
.hero-cover-info{flex:1;min-width:0}
.cover-pill{display:inline-flex;align-items:center;gap:5px;font-size:.68rem;font-weight:800;text-transform:uppercase;letter-spacing:.06em;padding:4px 11px;border-radius:999px;background:#f4ece0;color:#8e5120;border:1px solid #e4d3bc;margin-bottom:6px}
.hero-cover-info h2{font-family:var(--font-serif);font-size:1.15rem;margin:0 0 6px;line-height:1.28;color:#18241d}
.cover-read-link{display:inline-flex;align-items:center;gap:5px;color:#9e5822;font-weight:800;font-size:.83rem}
.hero-cover-thumb{width:96px;height:76px;border-radius:12px;overflow:hidden;flex-shrink:0;border:1px solid var(--border);background:var(--cream)}
.hero-cover-thumb img{width:100%;height:100%;object-fit:cover}

/* Tactile 3D Room Category Pills */
.room-shelf{background:var(--surface);border:1px solid var(--border);border-bottom:4px solid var(--bevel);border-radius:var(--radius);padding:14px 18px;margin-top:18px;box-shadow:var(--shadow-3d);display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.room-lbl{font-size:.76rem;font-weight:900;text-transform:uppercase;letter-spacing:.07em;color:var(--sage);margin-right:4px}
.room-pill{display:inline-flex;align-items:center;gap:6px;padding:7px 14px;border-radius:999px;background:var(--bg);border:1px solid var(--border);border-bottom:3px solid var(--bevel);color:var(--ink);font-size:.83rem;font-weight:700}
.room-pill:hover,.room-pill.active{background:var(--sage);color:#fff;border-color:#12241c}
.room-cnt{font-size:.72rem;opacity:.85;font-weight:700;background:rgba(0,0,0,.07);padding:1px 7px;border-radius:999px}
.room-pill:hover .room-cnt,.room-pill.active .room-cnt{background:rgba(255,255,255,.2)}

/* 3D Section Header & 10-Card Ultra-Smooth Grid */
.sec-head{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin:28px 0 18px;background:var(--surface);border:1px solid var(--border);border-bottom:4px solid var(--bevel);border-radius:var(--radius);padding:14px 20px;box-shadow:var(--shadow-3d)}
.sec-head h2{font-family:var(--font-serif);font-size:1.42rem;margin:0;color:var(--ink)}
.post-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:22px;margin-bottom:34px}
.card{background:var(--surface);border:1px solid var(--border);border-bottom:5px solid var(--bevel);border-radius:var(--radius-xl);overflow:hidden;box-shadow:var(--shadow-3d);display:flex;flex-direction:column}
.card-thumb{position:relative;aspect-ratio:16/10;overflow:hidden;background:var(--cream);border-bottom:1px solid var(--border);display:block}
.card-thumb img{width:100%;height:100%;object-fit:cover}
.card-num-badge{position:absolute;top:12px;right:12px;background:#1e1916;color:#fff;font-size:.73rem;font-weight:800;padding:4px 10px;border-radius:999px}
.cat-badge{display:inline-block;font-size:.71rem;font-weight:800;text-transform:uppercase;letter-spacing:.07em;padding:4px 11px;border-radius:999px;background:var(--accent-tint);color:var(--accent);border:1px solid rgba(184,84,40,.18);align-self:flex-start}
.card-body{padding:20px 22px 22px;display:flex;flex-direction:column;flex:1}
.card-title{font-family:var(--font-serif);font-size:1.22rem;line-height:1.33;margin:10px 0 10px}
.card-title a{color:var(--ink)}
.card-title a:hover{color:var(--accent)}
.card-exc{font-size:.92rem;color:var(--muted);margin:0 0 16px;flex:1;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.card-meta{display:flex;align-items:center;justify-content:space-between;font-size:.8rem;color:var(--soft);padding-top:13px;border-top:1px dashed var(--border);font-weight:700}
.read-btn-3d{display:inline-flex;align-items:center;gap:4px;color:var(--accent);font-weight:800;font-size:.82rem}

/* 3D Tactile Pagination Bar */
.pager{margin:26px 0 50px;display:flex;justify-content:center;gap:8px;flex-wrap:wrap}
.page-num{display:inline-flex;align-items:center;justify-content:center;min-width:42px;height:42px;padding:0 15px;border-radius:12px;background:var(--surface);border:1px solid var(--border);border-bottom:3px solid var(--bevel);color:var(--ink);font-weight:800;font-size:.9rem}
.page-num:hover{border-color:var(--accent);color:var(--accent)}
.page-num.active{background:var(--accent);color:#fff;border-color:var(--accent-dk)}

/* Single Article 3D Studio Layout */
.single-grid{display:grid;grid-template-columns:minmax(0,1fr) 335px;gap:32px;align-items:start;margin:26px 0 52px}
.crumb{font-size:.83rem;color:var(--soft);margin-bottom:12px}
.crumb a{color:var(--muted);font-weight:700}
.art-card{background:var(--surface);border:1px solid var(--border);border-bottom:6px solid var(--bevel);border-radius:var(--radius-xl);padding:34px 38px;box-shadow:var(--shadow-3d)}
.art-card h1{font-family:var(--font-serif);font-size:clamp(1.75rem,3.2vw,2.45rem);line-height:1.18;color:var(--ink);margin:12px 0 16px}
.byline{display:flex;align-items:center;flex-wrap:wrap;gap:12px;padding:12px 16px;background:var(--bg);border:1px solid var(--border);border-bottom:2px solid var(--bevel);border-radius:14px;margin-bottom:24px;font-size:.85rem;color:var(--muted)}
.feat-hero{margin:0 0 24px;border-radius:var(--radius);overflow:hidden;background:var(--cream);border:1px solid var(--border);border-bottom:4px solid var(--bevel)}
.feat-hero img{width:100%;max-height:540px;object-fit:cover}

/* Minimized 3D Drawer Table of Contents */
.toc{background:#faf6f0;border:1px solid var(--border);border-bottom:4px solid var(--bevel);border-left:5px solid var(--accent);border-radius:14px;padding:14px 18px;margin:0 0 26px}
.toc summary{font-weight:800;font-size:.95rem;color:var(--ink);cursor:pointer;display:flex;align-items:center;justify-content:space-between;list-style:none}
.toc summary::-webkit-details-marker{display:none}
.toc summary::after{content:"+ Expand Guide List";font-size:.76rem;font-weight:800;color:var(--accent);background:var(--surface);padding:4px 10px;border-radius:999px;border:1px solid var(--border)}
.toc[open] summary::after{content:"− Minimize List"}
.toc ol{margin:14px 0 4px;padding-left:20px;display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:7px 18px;font-size:.87rem;border-top:1px solid var(--border);padding-top:12px}
.toc a{color:var(--muted);font-weight:600}
.toc a:hover{color:var(--accent);text-decoration:underline}

/* Article Typography, 3D Architectural Tables, Multi-Columns & 120fps Framed Gallery Photos */
.entry h2{font-family:var(--font-serif);font-size:clamp(1.36rem,2.3vw,1.74rem);color:var(--ink);margin:1.9em 0 .6em;line-height:1.28;padding:10px 16px;background:var(--bg);border:1px solid var(--border);border-bottom:3px solid var(--bevel);border-left:5px solid var(--accent);border-radius:12px}
.entry h3{font-family:var(--font-serif);font-size:1.2rem;color:var(--ink);margin:1.45em 0 .45em}
.entry p{margin:0 0 1.22em;color:#292524}
.entry ul,.entry ol{margin:0 0 1.35em;padding-left:22px;color:#292524}
.entry li{margin-bottom:7px}
.entry li::marker{color:var(--accent);font-weight:800}
.entry hr,.entry .wp-block-separator{border:0;height:2px;background:linear-gradient(90deg,transparent,var(--bevel),transparent);margin:2.2em 0}
.entry .wp-block-columns{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px;margin:1.6em 0;align-items:start}
.entry .wp-block-column{min-width:0}
.entry .wp-block-column figure{margin:0}

/* 3D Cozy Architectural Comparison & Reference Tables */
.entry .wp-block-table,.entry .table-3d-wrap{margin:1.75em 0;overflow-x:auto;-webkit-overflow-scrolling:touch;border-radius:16px;background:var(--surface);border:1px solid var(--border);border-bottom:5px solid var(--bevel);box-shadow:var(--shadow-3d)}
.entry table{width:100%;border-collapse:collapse;font-size:.91rem;line-height:1.5;background:var(--surface);text-align:left;min-width:520px}
.entry table thead tr{background:linear-gradient(135deg,#1f3a2e 0%,#152920 100%);color:#fff}
.entry table thead th,.entry table thead td{padding:13px 16px;font-weight:800;font-size:.8rem;text-transform:uppercase;letter-spacing:.05em;color:#fff;border-bottom:3px solid var(--gold);border-right:1px solid rgba(255,255,255,.12);white-space:nowrap}
.entry table thead th:last-child,.entry table thead td:last-child{border-right:none}
.entry table thead strong{color:#f5e3c6;font-weight:800}
.entry table tbody td{padding:12px 16px;border-bottom:1px solid var(--border);border-right:1px solid rgba(228,217,200,.6);color:var(--ink);vertical-align:middle}
.entry table tbody td:last-child{border-right:none}
.entry table tbody tr:nth-child(even) td{background:#faf6f0}
.entry table tbody tr:hover td{background:#f2e9dc}
.entry table tbody td:first-child{font-weight:700;color:#1e1916;background:rgba(239,231,220,.32)}
.entry table tbody tr:nth-child(even) td:first-child{background:#f5ede1}
.entry table tbody tr:hover td:first-child{background:#ebdcc8}
.entry table tbody tr:last-child td{border-bottom:none}

.entry figure,.entry .wp-block-image{margin:1.5em 0}
.pin-wrap{position:relative;display:block;overflow:hidden;border-radius:var(--radius);margin:1.4em 0;padding:7px;background:#faf6f0;border:1px solid var(--border);border-bottom:4px solid var(--bevel)}
.entry figure .pin-wrap,.feat-hero .pin-wrap{margin:0}
.pin-wrap img{width:100%;height:auto;display:block;border-radius:10px;cursor:zoom-in}
.pin-btn{position:absolute;top:16px;left:16px;z-index:10;background:#e60023;color:#fff !important;font-family:var(--font-sans);font-size:.8rem;font-weight:800;padding:7px 13px;border-radius:999px;display:inline-flex;align-items:center;gap:6px;border-bottom:2px solid #9e0018;text-decoration:none !important}
.pin-btn:hover{background:#bd001c;color:#fff !important}
.zoom-hint{position:absolute;bottom:16px;right:16px;z-index:9;background:rgba(28,25,23,.82);color:#fff;font-size:.73rem;font-weight:700;padding:4px 11px;border-radius:999px;pointer-events:none}

/* Desktop-Only Hover Effects (So Mobile Touch Scrolling is 100% Lag-Free 120fps) */
@media(hover:hover) and (pointer:fine){
  .card{transition:transform .2s ease,box-shadow .2s ease}
  .card:hover{transform:translateY(-4px);box-shadow:var(--shadow-3d-hover)}
  .card-thumb img,.hero-img img,.pin-wrap img{transition:transform .3s ease}
  .card:hover .card-thumb img,.hero-card:hover .hero-img img,.pin-wrap:hover img{transform:scale(1.035)}
}

.dhd-lightbox{display:none;position:fixed;inset:0;z-index:9999;background:rgba(15,14,13,.94);align-items:center;justify-content:center;padding:18px;cursor:zoom-out}
.dhd-lightbox.open{display:flex}
.dhd-lightbox img{max-width:95vw;max-height:90vh;border-radius:12px;object-fit:contain}
.dhd-lb-close{position:fixed;top:18px;right:20px;background:#fff;color:#1c1917;border:0;border-radius:999px;padding:9px 18px;font-weight:800;font-size:.88rem;cursor:pointer;z-index:10000}

.founder-img{width:78px;height:78px;border-radius:50%;object-fit:cover;border:3px solid #fff;box-shadow:0 3px 10px rgba(30,25,22,.12);flex-shrink:0}
.byline-img{width:38px;height:38px;border-radius:50%;object-fit:cover;border:2px solid #fff;flex-shrink:0}
.author-box{display:flex;gap:18px;align-items:flex-start;background:#faf5ed;border:1px solid var(--border);border-bottom:4px solid var(--bevel);border-radius:var(--radius);padding:22px;margin-top:34px}
.author-box h3{margin:0 0 6px;font-family:var(--font-serif);font-size:1.12rem}
.author-box p{margin:0;font-size:.9rem;color:var(--muted)}

/* 3D Sidebar Widgets */
.sidebar{display:flex;flex-direction:column;gap:22px;position:sticky;top:82px}
.widget{background:var(--surface);border:1px solid var(--border);border-bottom:4px solid var(--bevel);border-radius:var(--radius-xl);padding:22px;box-shadow:var(--shadow-3d)}
.w-title{font-family:var(--font-serif);font-size:1.12rem;margin:0 0 14px;padding-bottom:9px;border-bottom:2px solid var(--border);color:var(--ink)}
.rec-list,.cat-list{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:12px}
.rec-item{display:flex;gap:12px;align-items:center;padding:5px;border-radius:10px}
.rec-item:hover{background:var(--bg)}
.rec-thumb{width:70px;height:54px;border-radius:10px;overflow:hidden;flex-shrink:0;background:var(--cream);border:1px solid var(--border)}
.rec-thumb img{width:100%;height:100%;object-fit:cover}
.rec-t{font-size:.87rem;font-weight:700;line-height:1.33;color:var(--ink)}
.cat-list a{display:flex;justify-content:space-between;align-items:center;padding:9px 13px;border-radius:11px;background:var(--bg);border:1px solid var(--border);border-bottom:2px solid var(--bevel);color:var(--ink);font-size:.87rem;font-weight:700}
.cat-list a:hover{background:var(--accent-tint);color:var(--accent)}

/* 3D Architectural Dark Espresso Footer */
.site-footer{background:#181412;color:rgba(255,255,255,.86);padding:52px 0 30px;margin-top:60px;font-size:.89rem;border-top:4px solid var(--gold)}
.foot-grid{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:30px;margin-bottom:34px}
.site-footer h4{color:#ebd5b3;font-size:.88rem;text-transform:uppercase;letter-spacing:.08em;margin:0 0 14px}
.site-footer p{color:rgba(255,255,255,.74);font-size:.87rem}
.site-footer ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}
.site-footer a{color:rgba(255,255,255,.82)}
.site-footer a:hover{color:#ebd5b3;text-decoration:underline}
.foot-bot{border-top:1px solid rgba(255,255,255,.12);padding-top:18px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;font-size:.81rem;color:rgba(255,255,255,.65)}

@media(max-width:1024px){.single-grid{grid-template-columns:1fr}.sidebar{position:static}}
@media(max-width:860px){
  .hero-bento,.foot-grid,.post-grid{grid-template-columns:1fr}
  .topbar-wave,.tb-mid-sep,.eyebrow-line,.desk-stats-bar,.hero-cta-wrap,.nav-search-btn{display:none !important}
  .topbar-in{padding:6px 8px;justify-content:center}
  .topbar-links{flex-direction:column;gap:2px;font-size:.72rem;line-height:1.35;width:100%}
  .tb-row{display:flex;justify-content:center;align-items:center;gap:6px;width:100%}
  .nav-bar{padding:8px 14px;flex-wrap:wrap;gap:6px}
  .brand svg{height:38px}
  .mob-btn{display:inline-flex}
  .main-nav{display:none;width:100%;grid-template-columns:repeat(2,1fr);gap:6px;padding:10px 0 4px;margin-top:4px;border-top:1px solid var(--border)}
  .main-nav.open{display:grid}
  .main-nav a{justify-content:center;text-align:center;padding:8px 10px;font-size:.82rem;background:var(--surface);border:1px solid var(--border);border-radius:10px}
  .main-nav a.active{background:#183528;color:#fff;border-color:#0e2118}
  .hero{padding:14px 0 16px}
  .hero-left-3d{
    padding:22px 20px 24px;
    background:linear-gradient(90deg,#fbf8f3 50%,rgba(251,248,243,.84) 68%,rgba(251,248,243,.18) 100%),url('/assets/hero-mobile-vignette.webp') right center/cover no-repeat;
  }
  .eyebrow-row{justify-content:flex-start;margin-bottom:14px}
  .eyebrow{background:#e1ebdc;border:1px solid #c5d6bd;color:#183528;font-size:.69rem;padding:6px 13px;letter-spacing:.05em}
  .hero h1{font-size:1.95rem;line-height:1.15;color:#1c1917;max-width:92%}
  .h1-for-desk{display:inline;font-style:normal;color:#1c1917}
  .real-homes-hl{color:#c86428;font-style:normal}
  .hero-lede{font-size:.94rem;color:#2c2622;max-width:78%;margin-bottom:4px}
  .mob-stats-grid{display:grid}
  .art-card{padding:20px 15px}
  .pin-wrap{padding:5px}
  .entry table{font-size:.84rem;min-width:460px}
  .entry table thead th,.entry table thead td,.entry table tbody td{padding:9px 11px}
}
""".strip()

LOGO_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 326 68" width="235" height="48" role="img" aria-label="Dream Home Decor">
  <g transform="translate(2, 5)">
    <rect x="0" y="0" width="58" height="58" rx="18" fill="#183528"/>
    <path d="M12 29 L29 13 L46 29" fill="none" stroke="#ffffff" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M38 16 V21" fill="none" stroke="#ffffff" stroke-width="2.6" stroke-linecap="round"/>
    <path d="M17 27 V44 H41 V27" fill="none" stroke="#ffffff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
    <rect x="23" y="29" width="5.2" height="5.2" rx="1" fill="#d97732"/>
    <rect x="29.8" y="29" width="5.2" height="5.2" rx="1" fill="#d97732"/>
    <rect x="23" y="35.8" width="5.2" height="5.2" rx="1" fill="#d97732"/>
    <rect x="29.8" y="35.8" width="5.2" height="5.2" rx="1" fill="#d97732"/>
  </g>
  <g transform="translate(72, 0)">
    <text x="0" y="34" font-family="Georgia, 'Palatino Linotype', serif" font-size="26" font-weight="700" fill="#183528" letter-spacing="-0.3">Dream Home</text>
    <text x="1" y="54" font-family="ui-sans-serif, system-ui, -apple-system, sans-serif" font-size="12.5" font-weight="900" fill="#c85a22" letter-spacing="3.2">3D LIVING &amp; DECOR</text>
  </g>
</svg>"""

FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 58 58"><rect width="58" height="58" rx="15" fill="#1f3a2e"/><path d="M11 30 L29 13 L47 30" fill="none" stroke="#ebd5b3" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M17 28 V45 H41 V28" fill="none" stroke="#ffffff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M22 45 V35 C22 33, 36 33, 36 35 V45" fill="#b85428"/></svg>"""


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
(function(){{var h=location.hostname;if(h==='www.dreamhomedecor.net'||h.indexOf('github.io')!==-1){{var p=location.pathname.replace(/^\\/dreamhomedecor(\\/|$)/,'/');location.replace('https://dreamhomedecor.net'+p+location.search+location.hash);}}}})();
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
    return f"""<div class="topbar" role="navigation" aria-label="Legal and Editorial Pages">
  <svg class="topbar-wave" viewBox="0 0 360 38" preserveAspectRatio="none" aria-hidden="true">
    <path d="M0,10 L235,10 C285,10 310,38 360,38 L0,38 Z" fill="#fbf8f3"/>
  </svg>
  <div class="topbar-in">
    <div class="topbar-links">
      <span class="tb-row">
        <a href="/about-us/" class="{'active' if active_slug == 'about-us' else ''}">About Us</a>
        <span class="tb-sep">|</span>
        <a href="/contact/" class="{'active' if active_slug in ('contact', 'contact-us') else ''}">Contact</a>
        <span class="tb-sep">|</span>
        <a href="/privacy-policy/" class="{'active' if active_slug in ('privacy-policy', 'privacy') else ''}">Privacy Policy</a>
        <span class="tb-sep">|</span>
        <a href="/gdpr/" class="{'active' if active_slug == 'gdpr' else ''}">GDPR &amp; CCPA</a>
      </span>
      <span class="tb-sep tb-mid-sep">|</span>
      <span class="tb-row">
        <a href="/cookie-policy/" class="{'active' if active_slug == 'cookie-policy' else ''}">Cookie Policy</a>
        <span class="tb-sep">|</span>
        <a href="/terms-and-conditions/" class="{'active' if active_slug == 'terms-and-conditions' else ''}">Terms</a>
        <span class="tb-sep">|</span>
        <a href="/disclaimer/" class="{'active' if active_slug == 'disclaimer' else ''}">Disclaimer</a>
        <span class="tb-sep">|</span>
        <a href="/dmca-policy/" class="{'active' if active_slug == 'dmca-policy' else ''}">DMCA</a>
      </span>
    </div>
  </div>
</div>
<header class="site-header">
  <div class="nav-bar">
    <a class="brand" href="/" aria-label="Dream Home Decor Home">{LOGO_SVG}</a>
    <button class="mob-btn" type="button" onclick="document.getElementById('dhd-nav').classList.toggle('open')">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
      Rooms
    </button>
    <nav class="main-nav" id="dhd-nav" aria-label="Main Navigation">
      <a href="/" class="{'active' if active_slug == 'home' else ''}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10.5L12 3l9 7.5"/><path d="M5 9.5V20h14V9.5"/><path d="M9 20v-6h6v6"/></svg>
        Home
      </a>
      <a href="/category/living-room-ideas/" class="{'active' if active_slug == 'living-room-ideas' else ''}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 11V8a3 3 0 0 1 3-3h10a3 3 0 0 1 3 3v3"/><path d="M2 11h2v5h16v-5h2v7H2z"/><path d="M5 18v2M19 18v2"/></svg>
        Living Room
      </a>
      <a href="/category/bedroom-ideas/" class="{'active' if active_slug == 'bedroom-ideas' else ''}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 7v11M21 11v7"/><path d="M3 14h18"/><path d="M6 14v-3a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v3"/></svg>
        Bedroom
      </a>
      <a href="/category/bathroom-ideas/" class="{'active' if active_slug == 'bathroom-ideas' else ''}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h16v3a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4v-3z"/><path d="M6 12V6a2 2 0 0 1 4 0v1"/><path d="M7 19v2M17 19v2"/></svg>
        Bathroom
      </a>
      <a href="/category/christmas-home-decore/" class="{'active' if active_slug == 'christmas-home-decore' else ''}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3L6 11h4l-3 7h10l-3-7h4L12 3z"/><path d="M12 18v3"/></svg>
        Christmas Decor
      </a>
      <a href="/category/boho-bedroom-ideas/" class="{'active' if active_slug == 'boho-bedroom-ideas' else ''}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 8h1a3 3 0 0 1 0 6h-1"/><path d="M3 8h14v7a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V8z"/><path d="M7 3v2M11 3v2"/></svg>
        Boho &amp; Cozy
      </a>
      <a href="/category/ceiling-ideas/" class="{'active' if active_slug == 'ceiling-ideas' else ''}">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg>
        Ceilings
      </a>
      <button class="nav-search-btn" type="button" onclick="var el=document.getElementById('latest-guides')||document.querySelector('main');if(el)el.scrollIntoView({{behavior:'smooth'}})" aria-label="Explore Guides" title="Explore Guides">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><line x1="20" y1="20" x2="16.2" y2="16.2"/></svg>
      </button>
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
  }});
}});
</script>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <h4>About Dream Home Decor</h4>
        <p>Dream Home Decor (<code>dreamhomedecor.net</code>) is an independent interior styling studio &amp; publication founded by Claire Vance in Austin, Texas—dedicated to warm living room layouts, organic modern bedrooms, spa bathrooms, and timeless home decor ideas.</p>
      </div>
      <div>
        <h4>Explore by Room</h4>
        <ul>
          <li><a href="/category/living-room-ideas/">Living Room Ideas</a></li>
          <li><a href="/category/bedroom-ideas/">Bedroom Ideas</a></li>
          <li><a href="/category/bathroom-ideas/">Bathroom Ideas</a></li>
          <li><a href="/category/christmas-home-decore/">Christmas Home Decor</a></li>
          <li><a href="/category/boho-bedroom-ideas/">Boho Bedroom Ideas</a></li>
          <li><a href="/category/ceiling-ideas/">Ceiling Ideas</a></li>
        </ul>
      </div>
      <div>
        <h4>Legal &amp; Privacy Compliance</h4>
        <ul>
          <li><a href="/about-us/">About Us &amp; Editorial Studio</a></li>
          <li><a href="/contact/">Contact Us</a></li>
          <li><a href="/privacy-policy/">Privacy Policy</a></li>
          <li><a href="/gdpr/">GDPR &amp; CCPA Privacy Rights</a></li>
          <li><a href="/cookie-policy/">Cookie Policy</a></li>
          <li><a href="/terms-and-conditions/">Terms &amp; Conditions</a></li>
          <li><a href="/disclaimer/">Disclaimer &amp; FTC Disclosure</a></li>
          <li><a href="/dmca-policy/">DMCA Copyright Policy</a></li>
          <li><a href="/sitemap.xml">XML Sitemap</a></li>
        </ul>
      </div>
      <div>
        <h4>Editorial Standards</h4>
        <p>Every room makeover guide features ultra-fast WebP photography with 1-click Pinterest saving and interactive 3D zoom.</p>
        <ul>
          <li><a href="/about-us/">👩‍🎨 Meet Claire Vance (Founder)</a></li>
          <li><a href="/contact/">✉️ Contact Editorial Desk</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bot">
      <span>© {datetime.now().year} Dream Home Decor (dreamhomedecor.net). All rights reserved.</span>
      <span>3D Cozy Atelier Theme · &lt;0.3s Mobile &amp; Desktop Core Web Vitals</span>
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

        def sub_src(sm):
            q = sm.group(1)
            u = sm.group(2)
            return f"src={q}{rewrite_img_url_to_webp(u, webp_map)}{q}"

        tag = re.sub(r'\bsrc=(["\'])([^"\']+)\1', sub_src, tag, flags=re.I)

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

    # Normalize tables: promote first row to <thead> if missing, and wrap standalone <table> in .table-3d-wrap
    content = re.sub(
        r'(<figure[^>]*class="[^"]*wp-block-table[^"]*"[^>]*>\s*)?<table\b[\s\S]*?</table>(\s*</figure>)?',
        lambda tm: (
            (tm.group(1) or '<div class="table-3d-wrap">')
            + (
                lambda tb_html: (
                    (
                        lambda m_tr: (
                            tb_html[: m_tr.start()]
                            + f"<thead>{m_tr.group(2)}</thead>"
                            + m_tr.group(1)
                            + tb_html[m_tr.end() :]
                        )
                        if (m_tr and "<strong" in m_tr.group(2).lower())
                        else tb_html
                    )(re.search(r"(<tbody[^>]*>\s*)(<tr[^>]*>[\s\S]*?</tr>)", tb_html, flags=re.I))
                    if "<thead" not in tb_html.lower()
                    else tb_html
                )
            )(re.search(r"<table\b[\s\S]*?</table>", tm.group(0), flags=re.I).group(0))
            + (tm.group(2) if tm.group(1) else "</div>")
        ),
        content,
        flags=re.I,
    )
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
    <img src="{html.escape(feat)}" alt="{html.escape(post['title'])}" width="640" height="400" {load_attr} decoding="async">
    <span class="card-num-badge">⏱️ {read_min} min</span>
  </a>
  <div class="card-body">
    <a class="cat-badge" href="/category/{html.escape(cat_slug)}/">{html.escape(cat_name)}</a>
    <h3 class="card-title"><a href="/{post['slug']}/">{html.escape(post['title'])}</a></h3>
    <p class="card-exc">{html.escape(post.get('excerpt', ''))}</p>
    <div class="card-meta">
      <span>By Claire Vance · {date_str}</span>
      <a class="read-btn-3d" href="/{post['slug']}/">Explore Guide →</a>
    </div>
  </div>
</article>"""


def render_pagination_nav(page_num, total_pages, base_prefix=""):
    """
    base_prefix: "" for homepage (/ and /page/2/), or "/category/bathroom-ideas" for category pages
    """
    if total_pages <= 1:
        return ""

    def page_url(n):
        if n == 1:
            return f"{base_prefix}/" if base_prefix else "/"
        return f"{base_prefix}/page/{n}/"

    links = []
    if page_num > 1:
        links.append(f'<a class="page-num" href="{page_url(page_num - 1)}">← Prev</a>')
    for p_i in range(1, total_pages + 1):
        if p_i == 1 or p_i == total_pages or abs(p_i - page_num) <= 2:
            cls = "page-num active" if p_i == page_num else "page-num"
            links.append(f'<a class="{cls}" href="{page_url(p_i)}">{p_i}</a>')
    if page_num < total_pages:
        links.append(f'<a class="page-num" href="{page_url(page_num + 1)}">Next →</a>')
    return f'<nav class="pager" aria-label="Pagination">{"".join(links)}</nav>'


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
        shutil.copyfile(founder_src, founder_dst)
    studio_src = os.path.join(BASE_DIR, "about-design-studio.webp")
    studio_dst = os.path.join(OUT_DIR, "assets", "about-design-studio.webp")
    if os.path.exists(studio_src) and not os.path.exists(studio_dst):
        shutil.copyfile(studio_src, studio_dst)
    for hero_img_name in ("hero-showcase-fireplace.webp", "hero-mobile-vignette.webp"):
        h_src = os.path.join(BASE_DIR, hero_img_name)
        h_dst = os.path.join(OUT_DIR, "assets", hero_img_name)
        if os.path.exists(h_src) and not os.path.exists(h_dst):
            shutil.copyfile(h_src, h_dst)

    # Sync cms-data JSON files into public_html/cms-data/ for the 100% Cloud Admin Panel
    cms_data_dir = os.path.join(OUT_DIR, "cms-data")
    os.makedirs(cms_data_dir, exist_ok=True)
    for src_f, dst_f in [
        (ARTICLES_DB, os.path.join(cms_data_dir, "articles.json")),
        (CATEGORIES_DB, os.path.join(cms_data_dir, "categories.json")),
        (PAGES_DB, os.path.join(cms_data_dir, "pages.json")),
        (SETTINGS_DB, os.path.join(cms_data_dir, "settings.json")),
        (IMAGE_MAP_DB, os.path.join(cms_data_dir, "webp_map.json")),
    ]:
        if os.path.exists(src_f) and os.path.abspath(src_f) != os.path.abspath(dst_f):
            shutil.copyfile(src_f, dst_f)

    with open(os.path.join(OUT_DIR, "assets", "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(FAVICON_SVG)
    with open(os.path.join(OUT_DIR, "assets", "default-decor.svg"), "w", encoding="utf-8") as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 420"><rect width="640" height="420" fill="#efe7dc"/><text x="320" y="215" text-anchor="middle" font-family="Georgia,serif" font-size="24" fill="#8e3c17">Dream Home Decor</text></svg>')

    settings = load_site_settings()
    webp_map = load_webp_map()

    with open(ARTICLES_DB, "r", encoding="utf-8") as f:
        all_posts = json.load(f)
    with open(PAGES_DB, "r", encoding="utf-8") as f:
        all_pages = json.load(f)
    with open(CATEGORIES_DB, "r", encoding="utf-8") as f:
        categories = json.load(f)

    published_posts = [p for p in all_posts if p.get("status", "publish") == "publish"]
    published_posts.sort(key=lambda x: x.get("date", ""), reverse=True)

    recent_5 = published_posts[:5]

    def render_sidebar():
        rec_items = []
        for rp in recent_5:
            r_img = rewrite_img_url_to_webp(rp.get("featured", ""), webp_map)
            rec_items.append(f"""<li class="rec-item">
              <a class="rec-thumb" href="/{rp['slug']}/"><img src="{html.escape(r_img)}" alt="{html.escape(rp['title'])}" width="70" height="54" loading="lazy" decoding="async"></a>
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
              <img class="founder-img" src="/assets/founder-claire-vance.webp" alt="Claire Vance — Founder &amp; Lead Interior Stylist" width="78" height="78" loading="lazy" decoding="async">
              <div>
                <strong style="display:block;font-size:1rem;color:var(--ink)">Claire Vance</strong>
                <span style="font-size:.78rem;color:var(--accent);font-weight:800">Founder &amp; Lead Interior Stylist · Austin, TX</span>
              </div>
            </div>
            <p style="font-size:.88rem;color:var(--muted);margin:0 0 10px">Claire Vance is an Austin-based interior stylist and founder of Dream Home Decor, sharing cozy living room layouts, warm neutral bedrooms, and budget-friendly room makeovers for modern American homes.</p>
            <a href="/about-us/" style="font-weight:800;font-size:.85rem">Read Claire&apos;s Story →</a>
          </div>
          <div class="widget">
            <h3 class="w-title">Latest Decor Guides</h3>
            <ul class="rec-list">{''.join(rec_items)}</ul>
          </div>
          <div class="widget">
            <h3 class="w-title">Explore by Room</h3>
            <ul class="cat-list">{''.join(cat_items)}</ul>
          </div>
        </aside>"""

    sidebar_html = render_sidebar()

    # 1. Build Individual Article Pages (/<slug>/index.html)
    for post in published_posts:
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

        cat_slug = post.get("category", "home-decor-ideas")
        cat_name = post.get("category_name", "Home Decor Ideas")
        related = [p for p in published_posts if p["slug"] != slug and p.get("category") == cat_slug][:4]
        if len(related) < 4:
            for p in published_posts:
                if p["slug"] != slug and p not in related:
                    related.append(p)
                if len(related) == 4:
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
                    <img class="founder-img" src="/assets/founder-claire-vance.webp" alt="Claire Vance — Founder &amp; Lead Interior Stylist" width="78" height="78" loading="lazy" decoding="async">
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

    # 3. Build Homepage & Paginated Archive (Strictly 10 Articles Per Page!)
    total_pages = max(1, math.ceil(len(published_posts) / POSTS_PER_PAGE))
    hero_post = published_posts[0] if published_posts else None
    hero_feat = rewrite_img_url_to_webp(hero_post.get("featured", ""), webp_map) if hero_post else ""

    room_pills_list = []
    for cslug, cobj in sorted(categories.items(), key=lambda kv: kv[1].get("count", 0), reverse=True):
        cnt = sum(1 for p in published_posts if cslug in p.get("categories", [p.get("category")]))
        if cnt > 0 and cslug != "uncategorized":
            room_pills_list.append(
                f'<a class="room-pill" href="/category/{cslug}/">{html.escape(cobj["name"])} <span class="room-cnt">{cnt}</span></a>'
            )
    room_pills_html = "".join(room_pills_list)

    for page_num in range(1, total_pages + 1):
        start_i = (page_num - 1) * POSTS_PER_PAGE
        slice_posts = published_posts[start_i : start_i + POSTS_PER_PAGE]
        cards_html = "".join(render_post_card(p, webp_map, eager=(i < 2)) for i, p in enumerate(slice_posts))
        pager_html = render_pagination_nav(page_num, total_pages, base_prefix="")

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
                <div class="hero-bento">
                  <div>
                    <div class="hero-left-3d">
                      <div class="eyebrow-row">
                        <span class="eyebrow-line"></span>
                        <span class="eyebrow"><span class="eyebrow-spark">✨</span> 3D COZY ATELIER · LIVING ROOM &amp; HOME DECOR</span>
                        <span class="eyebrow-line"></span>
                      </div>
                      <h1>Warm, Dimensional Living Room &amp; Home Decor Ideas <span class="h1-for-desk">for <span class="real-homes-hl">Real Homes<svg class="real-curve" viewBox="0 0 210 14" fill="none" aria-hidden="true"><path d="M3 11C55 3.5 145 2.5 207 8.5" stroke="#c86428" stroke-width="3.8" stroke-linecap="round"/></svg></span></span></h1>
                      <p class="hero-lede">From cozy apartment living rooms and layered neutral bedrooms to spa-inspired bathroom makeovers — explore {len(published_posts)}+ tactile room-by-room styling guides curated by <strong>Claire Vance.</strong></p>
                      <div class="desk-stats-bar">
                        <div class="d-stat">
                          <span class="d-stat-ico">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><path d="M4 11V8a3 3 0 0 1 3-3h10a3 3 0 0 1 3 3v3"/><path d="M2 11h2v5h16v-5h2v7H2z"/><path d="M5 18v2M19 18v2"/></svg>
                          </span>
                          <div class="d-stat-txt"><strong>{len(published_posts)}+</strong><span>Room Guides</span></div>
                        </div>
                        <div class="d-stat">
                          <span class="d-stat-ico">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
                          </span>
                          <div class="d-stat-txt"><strong>4,000+</strong><span>3D WebP Photos</span></div>
                        </div>
                        <div class="d-stat">
                          <span class="d-stat-ico">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                          </span>
                          <div class="d-stat-txt"><strong>&lt;0.3s</strong><span>Instant Speed</span></div>
                        </div>
                      </div>
                      <div class="hero-cta-wrap">
                        <a class="hero-explore-btn" href="#latest-guides">Explore Ideas →</a>
                      </div>
                    </div>
                    <div class="mob-stats-grid">
                      <div class="m-stat-card">
                        <span class="m-stat-badge">
                          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><path d="M3 10.5L12 3l9 7.5"/><path d="M5 9.5V20h14V9.5"/><path d="M9 20v-6h6v6"/></svg>
                        </span>
                        <strong>{len(published_posts)}+</strong>
                        <span>ROOM<br>GUIDES</span>
                      </div>
                      <div class="m-stat-card">
                        <span class="m-stat-badge">
                          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
                        </span>
                        <strong>4,000+</strong>
                        <span>3D WEBP<br>PHOTOS</span>
                      </div>
                      <div class="m-stat-card">
                        <span class="m-stat-badge">
                          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                        </span>
                        <strong>&lt;0.3s</strong>
                        <span>INSTANT<br>SPEED</span>
                      </div>
                    </div>
                  </div>
                  <div class="hero-right-col">
                    <a class="hero-showcase-photo" href="/{hero_post['slug']}/" aria-label="Featured Cozy Living Room Showcase">
                      <img src="/assets/hero-showcase-fireplace.webp" alt="Warm Dimensional Living Room &amp; Cozy Fireplace Decor Showcase" width="760" height="475" loading="eager" fetchpriority="high" decoding="async">
                    </a>
                    <a class="hero-cover-card" href="/{hero_post['slug']}/">
                      <div class="hero-cover-info">
                        <span class="cover-pill">☆ FEATURED COVER STORY · {html.escape(hero_post.get('category_name', 'HOME DECOR IDEAS')).upper()}</span>
                        <h2>{html.escape(hero_post['title'])}</h2>
                        <span class="cover-read-link">Read Cover Story →</span>
                      </div>
                      <div class="hero-cover-thumb">
                        <img src="{html.escape(hero_feat)}" alt="{html.escape(hero_post['title'])}" width="96" height="76" loading="eager" decoding="async">
                      </div>
                    </a>
                  </div>
                </div>
                <div class="room-shelf" id="latest-guides">
                  <span class="room-lbl">Explore by Room:</span>
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
                <h2>{'Latest Living Room & Home Decor Guides' if page_num == 1 else f'Home Decor Guides — Page {page_num} of {total_pages}'}</h2>
                <span style="font-size:.85rem;color:var(--soft);font-weight:700">Showing {start_i + 1}–{min(len(published_posts), start_i + POSTS_PER_PAGE)} of {len(published_posts)} Articles (10 Per Page)</span>
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

    # 4. Build Category Archives — STRICTLY 10 ARTICLES PER PAGE (/category/<slug>/ and /category/<slug>/page/<n>/)
    for cslug, cobj in categories.items():
        cat_posts = [p for p in published_posts if cslug in p.get("categories", [p.get("category")])]
        cname = cobj["name"]
        cat_total_pages = max(1, math.ceil(len(cat_posts) / POSTS_PER_PAGE))

        for c_page in range(1, cat_total_pages + 1):
            c_start = (c_page - 1) * POSTS_PER_PAGE
            c_slice = cat_posts[c_start : c_start + POSTS_PER_PAGE]
            cards_html = "".join(render_post_card(p, webp_map, eager=(i < 2)) for i, p in enumerate(c_slice))
            if not cards_html:
                cards_html = "<p>New guides coming soon in this room category!</p>"

            cat_pager = render_pagination_nav(c_page, cat_total_pages, base_prefix=f"/category/{cslug}")
            first_img = rewrite_img_url_to_webp(c_slice[0].get("featured", ""), webp_map) if c_slice else ""

            if c_page == 1:
                c_title = clamp_seo(f"{cname} — Cozy Decor & Styling Guides ({len(cat_posts)} Ideas)", 60)
                c_desc = clamp_seo(cobj.get("description") or f"Browse {len(cat_posts)} curated {cname} articles on Dream Home Decor.", 160)
                canonical = f"{SITE_URL}/category/{cslug}/"
                h1_text = cname
            else:
                c_title = clamp_seo(f"{cname} — Page {c_page} of {cat_total_pages} | Dream Home Decor", 60)
                c_desc = clamp_seo(f"Page {c_page} of {cat_total_pages} for {cname} — explore cozy styling tips, layouts, and color palettes.", 160)
                canonical = f"{SITE_URL}/category/{cslug}/page/{c_page}/"
                h1_text = f"{cname} — Page {c_page}"

            cat_html = (
                render_head(c_title, c_desc, canonical, preload_img=first_img, settings=settings)
                + render_header(active_slug=cslug)
                + f"""<section class="hero" style="padding:22px 0 10px">
                  <div class="wrap">
                    <div class="hero-left-3d" style="padding:26px 30px">
                      <div class="crumb"><a href="/">Home</a> › <span>{html.escape(cname)}</span>{f' › <span>Page {c_page}</span>' if c_page > 1 else ''}</div>
                      <span class="eyebrow">🏡 ROOM CATEGORY · {len(cat_posts)} TOTAL GUIDES · PAGE {c_page} OF {cat_total_pages}</span>
                      <h1 style="margin-bottom:8px">{html.escape(h1_text)}</h1>
                      <p class="hero-lede" style="max-width:820px;margin-bottom:0">{html.escape(c_desc)}</p>
                    </div>
                    <div class="room-shelf">
                      <span class="room-lbl">Switch Room:</span>
                      {room_pills_html}
                    </div>
                  </div>
                </section>
                <main class="wrap">
                  <div class="sec-head">
                    <h2>{html.escape(cname)} ({c_start + 1}–{min(len(cat_posts), c_start + POSTS_PER_PAGE)} of {len(cat_posts)})</h2>
                    <span style="font-size:.85rem;color:var(--soft);font-weight:700">Page {c_page} of {cat_total_pages} · 10 Guides Per Page</span>
                  </div>
                  <div class="post-grid">{cards_html}</div>
                  {cat_pager}
                </main>"""
                + render_footer(settings)
            )
            if c_page == 1:
                write_page(f"category/{cslug}/index.html", cat_html)
            else:
                write_page(f"category/{cslug}/page/{c_page}/index.html", cat_html)

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

    urls_xml = [f"<url><loc>{SITE_URL}/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>"]
    for pg in all_pages:
        if pg["slug"] not in ("home", "sample-page"):
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
    print(f"✅ Built Dream Home Decor 3D Cozy Atelier Static Site: {stats}")
