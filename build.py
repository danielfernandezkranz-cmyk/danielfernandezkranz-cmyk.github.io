# -*- coding: utf-8 -*-
"""
Builds the static personal web site from the JSON files in data/ into docs/.

Usage:  python build.py

Edit the files in data/ (site.json, working_papers.json, publications.json,
teaching.json, cv.json), drop an updated "CV Daniel Fernandez-Kranz.pdf" in
this folder, run the script again, and commit + push the result.
GitHub Pages serves the docs/ folder.
"""
import json, html, datetime, os, shutil, hashlib

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
SITE = os.path.join(ROOT, "docs")
CV_SOURCE = os.path.join(ROOT, "CV Daniel Fernandez-Kranz.pdf")


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


def esc(s):
    return html.escape(s or "", quote=True)


def link(text, url, cls=None, new_tab=True):
    if not url:
        return esc(text)
    c = f' class="{cls}"' if cls else ""
    tgt = ' target="_blank" rel="noopener"' if new_tab else ""
    return f'<a href="{esc(url)}"{c}{tgt}>{esc(text)}</a>'


SITE_DATA = load("site.json")
with open(os.path.join(ROOT, "style.css"), "rb") as _f:
    CSS_VERSION = hashlib.md5(_f.read()).hexdigest()[:8]
YEAR = datetime.date.today().year

NAV = [
    ("index.html", "About Me"),
    ("research.html", "Research"),
    ("working-papers.html", "Working Papers"),
    ("cv.html", "CV"),
    ("teaching.html", "Teaching"),
    ("contact.html", "Contact"),
]

# ---------------------------------------------------------------- icons
ICONS = {
    "email": '<svg viewBox="0 0 24 24"><path d="M2 5.5A2.5 2.5 0 0 1 4.5 3h15A2.5 2.5 0 0 1 22 5.5v13a2.5 2.5 0 0 1-2.5 2.5h-15A2.5 2.5 0 0 1 2 18.5v-13zm2.3-.5 7.7 6.2L19.7 5H4.3zM20 7.4l-8 6.4-8-6.4v11.1c0 .3.2.5.5.5h15c.3 0 .5-.2.5-.5V7.4z"/></svg>',
    "linkedin": '<svg viewBox="0 0 24 24"><path d="M20.4 2H3.6A1.6 1.6 0 0 0 2 3.6v16.8A1.6 1.6 0 0 0 3.6 22h16.8a1.6 1.6 0 0 0 1.6-1.6V3.6A1.6 1.6 0 0 0 20.4 2zM8 19H5V9.5h3V19zM6.5 8.2a1.7 1.7 0 1 1 0-3.5 1.7 1.7 0 0 1 0 3.5zM19 19h-3v-4.6c0-1.1 0-2.5-1.5-2.5s-1.8 1.2-1.8 2.4V19h-3V9.5h2.9v1.3h.1a3.2 3.2 0 0 1 2.8-1.5c3 0 3.5 2 3.5 4.5V19z"/></svg>',
    "scholar": '<svg viewBox="0 0 24 24"><path d="M12 3 1 9l11 6 9-4.9V17h2V9L12 3zm-7 10.6V17c0 2.2 3.1 4 7 4s7-1.8 7-4v-3.4l-7 3.8-7-3.8z"/></svg>',
    "orcid": '<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zM8.2 17H6.7V8.6h1.5V17zm-.8-9.6a1 1 0 1 1 0-2 1 1 0 0 1 0 2zm3 1.2h3.3c3.1 0 4.5 2.2 4.5 4.2 0 2.2-1.7 4.2-4.5 4.2h-3.3V8.6zm1.5 1.4v5.6h1.7c2 0 2.9-1.4 2.9-2.8 0-1.4-.9-2.8-2.9-2.8h-1.7z"/></svg>',
    "researchgate": '<svg viewBox="0 0 24 24"><path d="M13.9 3c-1.6 0-2.7.4-3.4 1.2-.7.8-1 2-1 3.5v.9c0 1.5.3 2.6 1 3.4.5.6 1.2 1 2 1.2l2.7 4.6h2.2l-2.9-4.8c1.6-.5 2.5-1.8 2.5-3.9V7.7c0-1.5-.3-2.7-1-3.5-.7-.8-1.7-1.2-2.1-1.2zm-.1 1.7c.5 0 .9.2 1.2.6.3.4.4 1.1.4 2.2v1.4c0 1-.1 1.7-.4 2.1-.3.4-.7.6-1.3.6-.6 0-1-.2-1.3-.6-.3-.4-.4-1.1-.4-2.1V7.5c0-1.1.1-1.8.4-2.2.3-.4.8-.6 1.4-.6zM5.5 10.5c-1 0-1.8.3-2.4.8-.6.6-.9 1.3-.9 2.3v.8c0 1 .3 1.8.9 2.3.6.6 1.4.8 2.4.8.8 0 1.5-.2 2.1-.6v-3.4H5v1.3h1.1v1.4c-.2.1-.4.1-.6.1-.5 0-.9-.2-1.2-.5-.3-.3-.4-.8-.4-1.5v-.8c0-.7.1-1.2.4-1.5.3-.3.6-.5 1.2-.5.5 0 1 .2 1.4.6l.9-1c-.6-.6-1.4-.9-2.3-.9z"/></svg>',
    "ssrn": '<svg viewBox="0 0 24 24"><path d="M4 3h11l5 5v13H4V3zm10 1.5V9h4.5L14 4.5zM6.5 12v1.5h11V12h-11zm0 3v1.5h11V15h-11zm0 3v1.5h7V18h-7z"/></svg>',
    "iza": '<svg viewBox="0 0 24 24"><path d="M3 20h18v2H3v-2zM5 10h3v8H5v-8zm5.5-4h3v12h-3V6zM16 2h3v16h-3V2z"/></svg>',
    "repec": '<svg viewBox="0 0 24 24"><path d="M4 4h16v2H4V4zm0 14h16v2H4v-2zm1-10h3l2 3 2.5-4 2 3 3-2h2.5v6H5V8z"/></svg>',
    "ie": '<svg viewBox="0 0 24 24"><path d="M3 5h3v14H3V5zm6 0h11v3h-8v2.5h7v3h-7V16h8v3H9V5z"/></svg>',
    "ieerg": '<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm6.9 9h-3a15 15 0 0 0-1.3-5.4A8 8 0 0 1 18.9 11zM12 4c.9 1.2 1.7 3.6 1.9 7h-3.8c.2-3.4 1-5.8 1.9-7zm-2.6 1.6A15 15 0 0 0 8.1 11h-3a8 8 0 0 1 4.3-5.4zM5.1 13h3c.1 2 .6 3.9 1.3 5.4A8 8 0 0 1 5.1 13zm6.9 7c-.9-1.2-1.7-3.6-1.9-7h3.8c-.2 3.4-1 5.8-1.9 7zm2.6-1.6c.7-1.5 1.2-3.4 1.3-5.4h3a8 8 0 0 1-4.3 5.4z"/></svg>',
}

PROFILE_LABELS = [
    ("email", "Email"),
    ("linkedin", "LinkedIn"),
    ("scholar", "Google Scholar"),
    ("orcid", "ORCID"),
    ("researchgate", "ResearchGate"),
    ("ssrn", "SSRN"),
    ("iza", "IZA"),
    ("repec", "RePEc / IDEAS"),
    ("ie", "IE School of Politics, Economics & Global Affairs"),
    ("ieerg", "IE Economics Research Group"),
]


def social_list(cls="social"):
    out = [f'<ul class="{cls}">']
    for key, label in PROFILE_LABELS:
        url = SITE_DATA["profiles"].get(key)
        if not url:
            continue
        tgt = "" if url.startswith("mailto:") else ' target="_blank" rel="noopener"'
        out.append(
            f'<li><a href="{esc(url)}"{tgt} aria-label="{esc(label)}" title="{esc(label)}">'
            f'<span class="icon">{ICONS[key]}</span><span class="label">{esc(label)}</span></a></li>'
        )
    out.append("</ul>")
    return "\n".join(out)


# ---------------------------------------------------------------- layout
def page(fname, title, body, description, extra_head="", body_class=""):
    name = SITE_DATA["name"]
    full_title = name if fname == "index.html" else f"{title} – {name}"
    nav = []
    for href, label in NAV:
        cls = ' class="current"' if href == fname else ""
        nav.append(f'<li{cls}><a href="{href}">{esc(label)}</a></li>')
    canonical = f'{SITE_DATA["domain"]}/{"" if fname == "index.html" else fname}'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(canonical)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{SITE_DATA["domain"]}/img/daniel-fernandez-kranz.jpg">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v={CSS_VERSION}">
{extra_head}
</head>
<body class="{body_class}">
<a class="skip" href="#content">Skip to content</a>
<header class="site-header">
  <p class="site-title"><a href="index.html">{esc(name)}</a></p>
  <button class="nav-toggle" aria-expanded="false" aria-controls="main-menu" aria-label="Open menu">
    <span></span><span></span><span></span>
  </button>
  <nav class="main-nav" aria-label="Main Menu">
    <ul id="main-menu">
      {''.join(nav)}
    </ul>
  </nav>
</header>
<div class="container">
<main id="content">
{body}
</main>
</div>
<footer class="site-footer">
  <div class="footer-inner">
    <div class="copyright">Copyright © {YEAR} <span>{esc(name)}</span></div>
    {social_list("social footer-social")}
  </div>
</footer>
<script>
(function(){{
  var b=document.querySelector('.nav-toggle'),n=document.querySelector('.main-nav');
  if(b&&n){{b.addEventListener('click',function(){{var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');}});}}
}})();
</script>
</body>
</html>
"""


def write(fname, content):
    os.makedirs(SITE, exist_ok=True)
    with open(os.path.join(SITE, fname), "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


# ---------------------------------------------------------------- pages
def build_home():
    s = SITE_DATA
    paras = "\n".join(f"<p>{p}</p>" for p in s["intro"])
    news = "\n".join(
        f'<li><span class="news-date">{esc(n["date"])}</span> {n["html"]}</li>' for n in s["news"]
    )
    address = "<br>".join(esc(a) for a in s["address_lines"])
    body = f"""
<article class="about">
  <h1 class="page-title">About Me</h1>
  <div class="about-grid">
    <div class="about-text">
      <h2>Welcome to my webpage!</h2>
      {paras}
      <p class="news-label">NEWS:</p>
      <ul class="news">
        {news}
      </ul>
    </div>
    <div class="about-photo">
      <img src="img/daniel-fernandez-kranz.jpg" alt="Portrait of {esc(s['name'])}" width="900" height="1350">
      <div class="contact-card">
        <h6>{esc(s['address_lines'][0])}</h6>
        <p>{address.split('<br>',1)[1]}</p>
        <p><a href="mailto:{esc(s['email'])}">{esc(s['email'])}</a></p>
        <p>{esc(s['phone'])}</p>
        <p><a class="button" href="{esc(s['cv_file'])}" target="_blank" rel="noopener">Download CV (PDF)</a></p>
      </div>
    </div>
  </div>
</article>
"""
    desc = ("Daniel Fernández-Kranz is Associate Professor of Economics at IE University, Madrid, "
            "and Research Fellow at IZA & LISER. Empirical microeconomics: family, gender, health and public policy.")
    write("index.html", page("index.html", "About Me", body, desc))


def pub_entry(p):
    title = link(p["title"], p["url"])
    co = f" (with {esc(p['coauthors'])})" if p.get("coauthors") else ""
    details = f", {esc(p['details'])}" if p.get("details") else ""
    doi = f' <a class="doi" href="{esc(p["doi"])}" target="_blank" rel="noopener">{esc(p["doi"])}</a>' if p.get("doi") else ""
    extras = "".join(f'<p class="pub-extra">{e}</p>' for e in p.get("extras", []))
    return (f'<div class="pub"><p>“{title}”{co}. <em>{esc(p["journal"])}</em>{details} ({esc(p["year"])}).{doi}</p>'
            f'{extras}</div>')


def build_research():
    pubs = load("publications.json")
    refereed = "\n".join(pub_entry(p) for p in pubs["refereed"])
    other = "\n".join(f'<li>{o}</li>' for o in pubs["other"])
    body = f"""
<article>
  <h1 class="page-title">Research</h1>
  <p class="lead">My research lies at the intersection of empirical microeconomics and public policy, with a focus on
  family economics, labor markets, gender economics and health economics. I study how institutions, laws and economic
  incentives shape individual behavior and outcomes within households and the labor market. Current working papers,
  with abstracts, are listed on the <a href="working-papers.html">Working Papers</a> page.</p>

  <h2>Main publications</h2>
  {refereed}

  <h2>Other publications</h2>
  <ul class="other-pubs">
    {other}
  </ul>

  <h2>Conferences and presentations</h2>
  <p>{esc(pubs["conferences"])}</p>
  <p>Invited seminars: {esc(pubs["seminars"])}</p>
</article>
"""
    desc = "Publications of Daniel Fernández-Kranz in refereed journals (Journal of Human Resources, Journal of Health Economics, Journal of Public Economics, JEBO, ILR Review and others) and other outlets."
    write("research.html", page("research.html", "Research", body, desc))


def coauthor_line(wp):
    if wp.get("coauthors_text"):
        return f'<p class="wp-authors">with {esc(wp["coauthors_text"])}</p>'
    cos = wp.get("coauthors") or []
    if not cos:
        return ""
    parts = [link(c["name"], c.get("url")) for c in cos]
    if len(parts) == 1:
        joined = parts[0]
    else:
        joined = ", ".join(parts[:-1]) + ", and " + parts[-1] if len(parts) > 2 else " and ".join(parts)
    return f'<p class="wp-authors">with {joined}</p>'


def wp_entry(wp, with_abstract=True):
    status = f' <span class="wp-status">({esc(wp["status"])})</span>' if wp.get("status") else ""
    first = (wp.get("links") or [{}])[0].get("url")
    title = link(wp["title"], first, new_tab=True) if first else esc(wp["title"])
    out = [f'<div class="mf-paper">', f'<h3>{title}{status}</h3>', coauthor_line(wp)]
    if with_abstract and wp.get("abstract"):
        out.append(f'<details class="abstract"><summary>abstract</summary><p>{esc(wp["abstract"])}</p></details>')
    links = wp.get("links") or []
    if links:
        out.append('<p class="wp-links">' + " · ".join(link(l["label"], l["url"]) for l in links) + "</p>")
    if wp.get("note"):
        out.append(f'<p class="wp-note">{wp["note"]}</p>')
    out.append("</div>")
    return "\n".join(out)


def build_working_papers():
    d = load("working_papers.json")
    wps = "\n".join(wp_entry(w) for w in d["working_papers"])
    wip = "\n".join(wp_entry(w) for w in d["work_in_progress"])
    body = f"""
<article class="mf-research">
  <h1 class="mf-title">Working Papers</h1>
  {wps}
  <h2 class="mf-subtitle">Work in progress</h2>
  {wip}
</article>
"""
    desc = "Working papers of Daniel Fernández-Kranz, with abstracts: single-sex schooling, maternity benefits, joint custody reforms, private schooling and fertility in India, broadband and work organization."
    write("working-papers.html", page("working-papers.html", "Working Papers", body, desc, body_class="wp-page"))


def build_cv():
    cv = load("cv.json")
    s = SITE_DATA
    secs = []
    for sec in cv["sections"]:
        secs.append(f'<h2>{esc(sec["title"])}</h2>')
        if sec.get("text"):
            secs.append(f'<p class="cv-text">{esc(sec["text"])}</p>')
        if sec.get("items"):
            rows = "".join(
                f'<tr><td>{esc(a)}</td><td class="cv-date">{esc(b)}</td></tr>' for a, b in sec["items"]
            )
            secs.append(f'<table class="cv-table">{rows}</table>')
    body = f"""
<article>
  <h1 class="page-title">CV</h1>
  <p>Click <a href="{esc(s['cv_file'])}" target="_blank" rel="noopener">here</a> to download my full CV (PDF, updated {esc(cv['updated'])}).</p>
  <p><a class="button" href="{esc(s['cv_file'])}" target="_blank" rel="noopener">Download CV (PDF)</a></p>
  {''.join(secs)}
  <h2>Full CV</h2>
  <div class="pdf-embed">
    <iframe src="{esc(s['cv_file'])}#view=FitH" title="CV of {esc(s['name'])}" loading="lazy"></iframe>
  </div>
</article>
"""
    desc = "Curriculum vitae of Daniel Fernández-Kranz: education, appointments, affiliations, awards, funded projects and publications."
    write("cv.html", page("cv.html", "CV", body, desc))


def build_teaching():
    t = load("teaching.json")
    grad = "".join(f"<li>{esc(x)}</li>" for x in t["graduate"])
    ug = "".join(f"<li>{esc(x)}</li>" for x in t["undergraduate"])
    aw = "".join(f"<li>{esc(x)}</li>" for x in t["awards"])
    body = f"""
<article>
  <h1 class="page-title">Teaching</h1>
  <p>{esc(t['intro'])}</p>
  <h2>Graduate level</h2>
  <ul class="plain">{grad}</ul>
  <h2>Undergraduate level</h2>
  <ul class="plain">{ug}</ul>
  <h2>Teaching awards</h2>
  <ul class="plain">{aw}</ul>
</article>
"""
    desc = "Teaching of Daniel Fernández-Kranz at IE University (International MBA, Master of International Management, Advanced Management Program) and earlier at Saint Louis University and the University of Chicago."
    write("teaching.html", page("teaching.html", "Teaching", body, desc))


def build_contact():
    s = SITE_DATA
    address = "<br>".join(esc(a) for a in s["address_lines"])
    body = f"""
<article>
  <h1 class="page-title">Contact</h1>
  <div class="contact-grid">
    <div>
      <h6><a href="{esc(s['office_url'])}" target="_blank" rel="noopener">IE School of Politics, Economics &amp; Global Affairs</a> · Office M-1012</h6>
      <p>{address}</p>
      <p>Phone: {esc(s['phone'])}</p>
      <p>Email: <a href="mailto:{esc(s['email'])}">{esc(s['email'])}</a></p>
    </div>
    <div>
      <h6>Profiles</h6>
      {social_list("social contact-social")}
    </div>
  </div>
</article>
"""
    desc = "Contact details for Daniel Fernández-Kranz, IE University, Madrid."
    write("contact.html", page("contact.html", "Contact", body, desc))


def build_404():
    body = """
<article>
  <h1 class="page-title">Page not found</h1>
  <p>The page you were looking for does not exist. Go back to the <a href="/">home page</a>.</p>
</article>
"""
    write("404.html", page("404.html", "Page not found", body, "Page not found"))


def build_extras():
    dom = SITE_DATA["domain"]
    today = datetime.date.today().isoformat()
    urls = "".join(
        f"<url><loc>{dom}/{'' if f == 'index.html' else f}</loc><lastmod>{today}</lastmod></url>" for f, _ in NAV
    )
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {dom}/sitemap.xml\n")
    write(".nojekyll", "")
    write("favicon.svg", (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
        '<rect width="64" height="64" rx="12" fill="#0274be"/>'
        '<text x="32" y="43" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="30" font-weight="700" '
        'fill="#fff" text-anchor="middle">DF</text></svg>'
    ))
    # assets
    os.makedirs(os.path.join(SITE, "img"), exist_ok=True)
    os.makedirs(os.path.join(SITE, "files"), exist_ok=True)
    shutil.copyfile(os.path.join(DATA, "photo.jpg"), os.path.join(SITE, "img", "daniel-fernandez-kranz.jpg"))
    if os.path.exists(CV_SOURCE):
        shutil.copyfile(CV_SOURCE, os.path.join(SITE, "files", "CV_Daniel_Fernandez-Kranz.pdf"))
    shutil.copyfile(os.path.join(ROOT, "style.css"), os.path.join(SITE, "style.css"))


if __name__ == "__main__":
    build_home()
    build_research()
    build_working_papers()
    build_cv()
    build_teaching()
    build_contact()
    build_404()
    build_extras()
    print("Site built into", SITE)
