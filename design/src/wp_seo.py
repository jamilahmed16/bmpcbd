"""Write the WordPress SEO handoff (wordpress/seo/) from design/src/seo.py.
Run: python3 design/src/wp_seo.py"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import seo, pages2
ROOT = os.path.dirname(os.path.dirname(HERE)); OUT = os.path.join(ROOT, "wordpress", "seo")
for it in pages2.news_items(os.path.join(ROOT, "content")): seo.news_entry(it)
news = {it["slug"]: it for it in pages2.news_items(os.path.join(ROOT, "content"))}
def prod(o): return json.loads(json.dumps(o, ensure_ascii=False).replace(seo.PREVIEW + "img/", seo.PROD + "wp-content/uploads/"))
rows = []
for f, (path, title, desc, typ, img, label) in seo.PAGES.items():
    g = prod(seo.graph(f, news.get(f)))
    json.dump(g, open(os.path.join(OUT, "schema", f.replace(".html", ".json")), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    rows.append(f"| {label} | `/{path}` | {title} | {desc} | {typ} |")
people = [p for p in seo.PEOPLE.values()]
json.dump({"@context": "https://schema.org", "@graph": [prod(seo.ORG)] + [prod(p) for p in people]},
          open(os.path.join(OUT, "schema", "_organization-and-people.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(os.path.join(OUT, "pages.md"), "w", encoding="utf-8").write(
    "# Page titles, descriptions and slugs\n\nGenerated from `design/src/seo.py`. Copy each into Rank Math (page editor → Rank Math → Edit Snippet).\n\n"
    "| Page | Slug | SEO title | Meta description | Schema type |\n|---|---|---|---|---|\n" + "\n".join(rows) + "\n")
print("wrote", OUT)
