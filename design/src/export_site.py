"""Copy the design pages into a static folder for GitHub Pages.
Usage: python3 design/src/export_site.py _site"""
import os, re, shutil, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "design"); OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "_site")
NOINDEX = '<meta name="robots" content="noindex, nofollow">'
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
shutil.copytree(os.path.join(SRC, "img"), os.path.join(OUT, "img"))
shutil.copy(os.path.join(SRC, "site.css"), OUT)
for f in os.listdir(SRC):
    if not f.endswith(".html"): continue
    html = open(os.path.join(SRC, f), encoding="utf-8").read()
    if f == "home-concept.html":   # artifact page: add the document skeleton
        html = ('<!doctype html><html lang="bn"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
                + html.replace("<header", "</head><body><header", 1) + "</body></html>")
        sys.path.insert(0, os.path.join(ROOT, "design", "src")); import seo
        html = html.replace("<title>BMPC Home Concept</title>", "<title>" + seo.PAGES["index.html"][1] + "</title>", 1)
        f = "index.html"
    html = html.replace('<meta charset="utf-8">', '<meta charset="utf-8">' + NOINDEX, 1)
    open(os.path.join(OUT, f), "w", encoding="utf-8").write(html)
open(os.path.join(OUT, ".nojekyll"), "w").close()
open(os.path.join(OUT, "robots.txt"), "w").write("User-agent: *\nDisallow: /\n")  # preview only; the live site has its own
print("exported", len([x for x in os.listdir(OUT) if x.endswith(".html")]), "pages to", OUT)
