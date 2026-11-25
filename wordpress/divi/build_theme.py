"""Build the BMPC Divi child theme from the design pages.
Run from the repo root:  python3 wordpress/divi/build_theme.py
Output: wordpress/divi/bmpc-child/ and wordpress/divi/bmpc-child.zip"""
import json, os, re, shutil, subprocess, sys
from bs4 import BeautifulSoup
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DESIGN = os.path.join(ROOT, "design"); SRC = os.path.join(DESIGN, "src")
HERE = os.path.dirname(os.path.abspath(__file__)); TPL = os.path.join(HERE, "theme-src")
OUT = os.path.join(HERE, "bmpc-child")
sys.path.insert(0, SRC)
subprocess.run([sys.executable, "-I", os.path.join(SRC, "build.py"), DESIGN, os.path.join(ROOT, "content/objectives.md"),
                os.path.join(ROOT, "content/membership-policy.md")], check=True, cwd=ROOT, capture_output=True)
import seo, pages2  # noqa: E402

DV = "4.27.4"
# design file -> WordPress page slug
PAGES = [("home-concept.html", "home", "হোম"), ("about.html", "about", "আমাদের সম্পর্কে"),
         ("manifesto.html", "manifesto", "ঘোষণাপত্র"), ("constitution.html", "constitution", "গঠনতন্ত্র"),
         ("objectives.html", "objectives", "লক্ষ্য ও উদ্দেশ্য"), ("chairman.html", "chairman-message", "চেয়ারম্যানের বাণী"),
         ("secretary.html", "secretary-general-message", "মহাসচিবের বাণী"), ("join.html", "join", "সদস্য হোন"),
         ("news.html", "news", "সর্বশেষ সংবাদ")]
SLUG = {f: s for f, s, _ in PAGES}
NEWS = pages2.news_items(os.path.join(ROOT, "content"))
POSTSTEM = {n["slug"]: re.sub(r"^\d{4}-\d{2}-\d{2}-", "", n["stem"]) for n in NEWS}

def link(href):
    if href.startswith(("http", "mailto:", "tel:")): return href
    base, _, frag = href.partition("#")
    if base == "": return "#" + frag
    if base == "index.html": base = "home-concept.html"
    if base in SLUG: u = "{{URL:%s}}" % SLUG[base]
    elif base in POSTSTEM: u = "{{POST:%s}}" % POSTSTEM[base]
    elif base == "news-post.html": u = "{{POST:%s}}" % POSTSTEM[NEWS[0]["slug"]]
    else: u = href
    return u + ("#" + frag if frag else "")

# ---------- CSS prefixer (rules, @media, @keyframes) ----------
def prefix_css(css, pre):
    out, i, n = [], 0, len(css)
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    def blocks(s):
        res, depth, start, sel_start = [], 0, 0, 0
        j = 0
        while j < len(s):
            c = s[j]
            if c == "{":
                if depth == 0: sel = s[sel_start:j].strip(); start = j + 1
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0: res.append((sel, s[start:j])); sel_start = j + 1
            j += 1
        return res
    def walk(s):
        o = []
        for sel, body in blocks(s):
            if sel.startswith("@media") or sel.startswith("@supports"): o.append(sel + "{" + walk(body) + "}")
            elif sel.startswith("@"): o.append(sel + "{" + body + "}")
            else:
                parts = []
                for p in sel.split(","):
                    p = p.strip()
                    if p.startswith(":root") or p.startswith("html"): parts.append(p)
                    elif p.startswith("body"): parts.append(p.replace("body", "body" + pre, 1))
                    else: parts.append(pre + " " + p)
                o.append(",".join(parts) + "{" + body + "}")
        return "".join(o)
    return walk(css)

def drop_rules(css, pattern):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S); out = []; depth = 0; buf = ""
    for ch in css:
        buf += ch
        if ch == "{": depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                sel = buf.split("{", 1)[0].strip()
                if sel.startswith("@media"):
                    inner = buf[buf.index("{") + 1:-1]
                    kept = drop_rules(inner, pattern)
                    if kept.strip(): out.append(sel + "{" + kept + "}")
                elif not re.search(pattern, sel): out.append(buf)
                buf = ""
    return "".join(out)

def divi_section(html, first=False):
    chk = html.replace("[bmpc_latest_news]", "")
    if "[" in chk or "]" in chk:
        i = max(chk.find("["), chk.find("]")); raise SystemExit("bracket in content: " + chk[max(0, i - 80):i + 40])
    return (f'[et_pb_section fb_built="1" fullwidth="on" _builder_version="{DV}" module_class="bmpc-sec" '
            f'custom_padding="0px||0px||false|false" background_color="rgba(0,0,0,0)"]'
            f'[et_pb_fullwidth_code _builder_version="{DV}" module_class="bmpc-code"]{html}[/et_pb_fullwidth_code][/et_pb_section]')

page_css, pages_out = [], []
for fname, slug, title in PAGES:
    soup = BeautifulSoup(open(os.path.join(DESIGN, fname), encoding="utf-8").read(), "html.parser")
    css = soup.find("style").string
    if slug == "join":   # the real form is Fluent Forms: drop the mock-form styles, keep hero/layout/aside
        css = drop_rules(css, r"(^|[\s,>])(form|fieldset|legend|input|select|textarea|label|\.f\b|\.f\.|\.seg|\.check|\.drop-f|\.err|\.req|\.opt|\.row|\.submit-row|\.done-panel|\.hint|details\.policy|\.pol)")
    page_css.append(f"/* ---- page: {slug} ---- */\n" + prefix_css(css, f".bmpc-page-{slug}"))
    main = soup.find("main")
    for el in main.select(".note-draft, .draft, #done"): el.decompose()
    for a in main.find_all("a", href=True): a["href"] = link(a["href"])
    for im in main.find_all("img", src=True):
        if im["src"].startswith("img/"): im["src"] = "{{IMG:%s}}" % os.path.basename(im["src"])
    if slug == "home":
        ns = main.select_one("a.nstory")
        if ns: ns.replace_with("[bmpc_latest_news]")
    if slug == "join":
        f = main.find("form")
        if f: f.replace_with("{{FLUENTFORM}}")
    if slug == "news":   # the blog index uses the theme template; keep the page empty
        sections = []
    else:
        sections = [str(c) for c in main.children if getattr(c, "name", None)]
    content = "".join(divi_section(s, i == 0) for i, s in enumerate(sections))
    key = "index.html" if slug == "home" else fname
    p = seo.PAGES.get(key)
    pages_out.append({"slug": slug, "title": title, "content": content,
                      "seo_title": p[1] if p else title, "seo_desc": p[2] if p else ""})

# ---------- news posts ----------
posts = []
for n in NEWS:
    body = "".join(f"<p>{p}</p>" for p in n["body"])
    if n["gallery"]:
        body += '<div class="gallery">' + "".join(
            f'<figure><img src="{{{{IMG:{os.path.basename(s)}}}}}" alt="{a}" loading="lazy"><figcaption>{a}</figcaption></figure>' for a, s in n["gallery"]) + "</div>"
    seo.news_entry(n)
    posts.append({"stem": POSTSTEM[n["slug"]], "title": n["title"], "date": n["date"] + " 16:00:00", "content": body,
                  "image": n["image_file"], "alt": n["alt"], "category": n.get("category", "সর্বশেষ"),
                  "event": n.get("event", ""), "place": n.get("place", ""), "summary": n.get("summary", ""),
                  "seo_title": seo.PAGES[n["slug"]][1], "seo_desc": seo.PAGES[n["slug"]][2]})

# ---------- assemble theme ----------
shutil.rmtree(OUT, ignore_errors=True)
shutil.copytree(TPL, OUT)
os.makedirs(os.path.join(OUT, "assets/img"), exist_ok=True); os.makedirs(os.path.join(OUT, "data"), exist_ok=True)
imgs = {}
for f in sorted(os.listdir(os.path.join(DESIGN, "img"))):
    shutil.copy(os.path.join(DESIGN, "img", f), os.path.join(OUT, "assets/img", f))
ALTS = {"logo.png": seo.ORG_NAME + " লোগো", "logo-full.jpg": seo.ORG_NAME + " লোগো",
        "chairman.jpg": "রহিমুল ফারুক বাবু, চেয়ারম্যান", "secretary.jpg": "মোঃ আল আমিন, মহাসচিব",
        "welcome-banner.jpg": "মুক্তিযোদ্ধা প্রজন্মের একমাত্র অরাজনৈতিক সংগঠনে আপনাকে স্বাগতম",
        "news-press-club.jpg": "জাতীয় প্রেসক্লাবের সামনে কাউন্সিলের মানববন্ধন ও প্রতিবাদ সমাবেশ",
        "news-press-club-2.jpg": "জাতীয় প্রেসক্লাবের সামনে মানববন্ধনে কাউন্সিলের সদস্যরা", "news-press-club-3.jpg": "মানববন্ধন ও প্রতিবাদ সমাবেশে বক্তব্য",
        "news-press-club-poster.jpg": "মানববন্ধন ও প্রতিবাদ সমাবেশের পোস্টার", "og-default.jpg": seo.ORG_NAME}
images = [{"file": f, "alt": ALTS.get(f, "")} for f in sorted(os.listdir(os.path.join(DESIGN, "img"))) if not f.startswith("icon-")]
people = [seo.PEOPLE["chairman.html"], seo.PEOPLE["secretary.html"]]
json.dump({"pages": pages_out, "posts": posts, "images": images,
           "people": {"chairman-message": people[0], "secretary-general-message": people[1]},
           "org": seo.ORG}, open(os.path.join(OUT, "data/site.json"), "w", encoding="utf-8"), ensure_ascii=False)

# CSS: design system + Divi resets + menu + page styles + blog/post templates
site_css = open(os.path.join(SRC, "site.css"), encoding="utf-8").read()
tmpl_css = ("/* ---- templates: news list + single post ---- */\n" +
            prefix_css(pages2.NEWS_CSS, "body.blog") + "\n" + prefix_css(pages2.POST_CSS, "body.single-post") + "\n" +
            prefix_css(pages2.COMMON_CSS, "body.single-post") + "\n" + prefix_css(pages2.COMMON_CSS, "body.blog"))
divi_css = open(os.path.join(TPL, "assets/css/divi-overrides.css"), encoding="utf-8").read()
ff_css = re.sub(r"@import[^;]+;", "", open(os.path.join(ROOT, "wordpress/fluentforms/bmpc-fluentforms.css"), encoding="utf-8").read())
open(os.path.join(OUT, "assets/css/bmpc.css"), "w", encoding="utf-8").write(
    "/* Generated by wordpress/divi/build_theme.py from design/src. Edit there, not here. */\n" +
    site_css + "\n" + divi_css + "\n" + ff_css + "\n" + tmpl_css + "\n" + "\n".join(page_css))
os.remove(os.path.join(OUT, "assets/css/divi-overrides.css"))
shutil.copy(os.path.join(SRC, "motion.js"), os.path.join(OUT, "assets/js/motion.js"))
# theme screenshot (1200x900) from the social image
from PIL import Image
im = Image.open(os.path.join(DESIGN, "img/og-default.jpg")).convert("RGB")
canvas = Image.new("RGB", (1200, 900), (11, 91, 62)); canvas.paste(im, (0, 135)); canvas.save(os.path.join(OUT, "screenshot.png"))
# zip
zp = os.path.join(HERE, "bmpc-child.zip")
if os.path.exists(zp): os.remove(zp)
subprocess.run(["zip", "-qr", zp, "bmpc-child"], cwd=HERE, check=True)
print("pages", len(pages_out), "posts", len(posts), "images", len(images), "->", os.path.relpath(zp, ROOT))
