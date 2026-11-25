"""Extra pages: about, manifesto, constitution, chairman/secretary messages, news list + post."""
import re, os
import art
from art import bn

def fm(path):
    raw=open(path,encoding="utf-8").read()
    m=re.match(r"---\n(.*?)\n---\n(.*)",raw,re.S); meta={}
    for line in m.group(1).split("\n"):
        k,_,v=line.partition(":"); meta[k.strip()]=v.strip()
    return meta, m.group(2).strip()
def paras(body): return [p.strip() for p in body.split("\n\n") if p.strip() and not p.startswith("#")]

COMMON_CSS='''
.phero .wrap{display:grid;gap:14px;padding-block:44px 52px}
.phero h1{font-size:clamp(40px,6vw,78px);font-weight:800;font-stretch:76%;line-height:1.05}
.phero .lede{font-size:19px;max-width:42em;opacity:.95}
.phero.with-art .wrap{grid-template-columns:minmax(0,1.4fr) minmax(0,.6fr);align-items:center}
.phero .art svg{display:block;width:100%;max-width:300px;margin-left:auto;height:auto}
@media (max-width:820px){.phero.with-art .wrap{grid-template-columns:1fr}.phero .art{display:none}}
.cta{background:#167452;color:#FBF3E6}
.cta .wrap{display:flex;flex-wrap:wrap;gap:24px;align-items:center;justify-content:space-between;padding-block:48px}
.cta h2{font-size:clamp(28px,3.4vw,40px);font-weight:800;font-stretch:80%}
.cta p{opacity:.85;margin-top:6px}
.meta{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;font:500 14.5px/1.3 var(--f-body);color:var(--ink-soft)}
.chip-cat{font:700 13px/1 var(--f-body);background:var(--red);color:#fff;padding:7px 10px}
.note-draft{display:inline-flex;gap:10px;align-items:center;font:600 14px/1.4 var(--f-body);background:var(--paper-2);border:1px dashed var(--ink-soft);padding:10px 14px;color:var(--ink-soft)}
'''
def cta(t="এই অঙ্গীকারে আপনিও যুক্ত হোন", p="বীর মুক্তিযোদ্ধার সন্তান ও প্রজন্মের জন্য সদস্যপদ উন্মুক্ত।"):
    return f'<section class="cta" style="padding-block:0"><div class="wrap"><div><h2>{t}</h2><p>{p}</p></div><a class="btn btn-paper" href="join.html">সদস্য আবেদন করুন</a></div></section>'
def phero(crumb, title, lede="", art_svg=""):
    cls="hero phero with-art" if art_svg else "hero phero"
    a=f'<div class="art poster">{art_svg}</div>' if art_svg else ""
    l=f'<p class="lede">{lede}</p>' if lede else ""
    return f'''<section class="{cls}"><div class="wrap"><div style="display:grid;gap:14px"><nav class="crumbs" aria-label="অবস্থান"><a href="index.html">হোম</a><span aria-hidden="true">/</span>{crumb}</nav><h1>{title}</h1>{l}</div>{a}</div></section>'''

# ---------- ABOUT
def about(content):
    _,ab=fm(f"{content}/about.md"); about_txt=paras(ab)[0]
    _,pol=fm(f"{content}/membership-policy.md")
    cards=""
    for h,body in re.findall(r"## (.*?)\n(.*?)(?=\n## |\Z)",pol,re.S):
        num,_,name=h.partition(". ")
        lis="".join(f"<li>{l[2:].strip()}</li>" for l in body.strip().split("\n") if l.startswith("- "))
        cards+=f'<article class="rule"><span class="n">{num}</span><h3>{name}</h3><ul>{lis}</ul></article>'
    css=COMMON_CSS+'''
.intro .wrap{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:56px;align-items:center}
.intro p.big{font:600 clamp(21px,2.2vw,27px)/1.75 var(--f-display);font-stretch:92%}
.intro p.big strong{color:var(--green)}
.intro figure{margin:0;border:2px solid var(--ink);box-shadow:8px 8px 0 var(--green);background:#fff}
.intro figure img{display:block;width:100%;height:auto}
.intro figcaption{font-size:13.5px;color:var(--ink-soft);padding:10px 14px;border-top:1px solid var(--rule);background:var(--field)}
@media (max-width:880px){.intro .wrap{grid-template-columns:1fr;gap:32px}}
.rules{background:var(--paper-2);border-block:1px solid var(--rule)}
.rule-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}
.rule{background:var(--field);border:2px solid var(--ink);padding:24px 24px 26px;display:grid;gap:10px;align-content:start}
.rule .n{font:800 46px/1 var(--f-display);font-stretch:75%;color:var(--red)}
.rule h3{font-size:24px;font-weight:700}
.rule ul{margin:0;padding-left:20px;font-size:15.5px;line-height:1.8}
.rule li{margin:4px 0}
@media (max-width:980px){.rule-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:620px){.rule-grid{grid-template-columns:1fr}}
'''
    body=phero('<span>আমাদের সম্পর্কে</span>','আমাদের সম্পর্কে','মুক্তিযুদ্ধের চেতনা ধারণকারী, বীর মুক্তিযোদ্ধার সন্তান ও প্রজন্মের অরাজনৈতিক সংগঠন।', art.torch_svg())+f'''
<section class="intro"><div class="wrap">
 <div><span class="script">পরিচিতি</span><p class="big" style="margin-top:12px">{about_txt.replace("অরাজনৈতিক","<strong>অরাজনৈতিক</strong>",1)}</p></div>
 <figure><img src="img/welcome-banner.jpg" alt="বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিল (BMPC): মুক্তিযোদ্ধা প্রজন্মের একমাত্র অরাজনৈতিক সংগঠনে আপনাকে স্বাগতম" width="960" height="354" loading="lazy"><figcaption>স্বাগত ব্যানার (লাইভ সাইট থেকে, মূল ফাইল দিয়ে প্রতিস্থাপন করুন)</figcaption></figure>
</div></section>
<section class="rules" id="policy"><div class="wrap">
 <div class="sec-head"><span class="script">সদস্য নীতিমালা</span><h2>গ্রুপের সদস্য হওয়ার নীতিমালা</h2></div>
 <div class="rule-grid">{cards}</div>
</div></section>'''+cta("নীতিমালা মেনে সদস্য হোন")
    return css, body

# ---------- MANIFESTO
def manifesto(content):
    _,b=fm(f"{content}/manifesto.md")
    pre=paras(b.split("## ")[0].split("\n",1)[1])[0]
    secs=re.findall(r"## (.*?)\n(.*?)(?=\n## |\Z)",b,re.S)
    arts=""; closing=""; slogan=""
    for h,t in secs:
        t=t.strip()
        if h.startswith("সমাপনী"):
            closing,_,q=t.partition("\n\n>"); slogan=q.strip().strip('"“” ')
            continue
        num,_,name=h.partition(". ")
        arts+=f'<article class="pledge"><span class="n">{num}</span><div><h2>{name}</h2><p>{t}</p></div></article>'
    css=COMMON_CSS+'''
.doc{padding-block:72px 88px}
.doc .sheet{max-width:860px;margin:0 auto;background:var(--field);border:2px solid var(--ink);box-shadow:10px 10px 0 var(--green);padding:56px clamp(20px,5vw,64px);position:relative}
.seal{position:absolute;top:-38px;right:clamp(16px,4vw,48px);width:84px;height:84px;border-radius:50%;background:#fff;box-shadow:0 0 0 3px var(--green),0 0 0 6px var(--paper)}
.seal img{width:100%;height:100%;border-radius:50%;display:block}
.doc .pre{font:500 clamp(19px,2vw,22px)/1.9 var(--f-body);padding-bottom:32px;border-bottom:2px solid var(--ink)}
.pledge{display:grid;grid-template-columns:72px minmax(0,1fr);gap:20px;padding:30px 0;border-bottom:1px solid var(--rule)}
.pledge .n{font:800 64px/.9 var(--f-display);font-stretch:75%;color:var(--red)}
.pledge h2{font-size:clamp(24px,2.6vw,30px);font-weight:800;font-stretch:84%;margin-bottom:10px}
.pledge p{font-size:17px;line-height:1.9}
@media (max-width:560px){.pledge{grid-template-columns:48px minmax(0,1fr);gap:12px}.pledge .n{font-size:46px}}
.closing{margin-top:34px;font:600 20px/1.75 var(--f-display);background:var(--green);color:#FBF3E6;padding:26px 28px}
.slogan{background:var(--green-deep);color:#FBF3E6;position:relative;overflow:hidden;text-align:center}
.slogan::before{content:"";position:absolute;inset:0;background:repeating-conic-gradient(from 0deg at 50% 120%,rgba(0,0,0,.2) 0 4deg,transparent 4deg 8deg)}
.slogan::after{content:"";position:absolute;left:50%;bottom:-170px;width:340px;height:340px;margin-left:-170px;border-radius:50%;background:#E8362E}
.slogan .wrap{position:relative;z-index:1;padding-block:72px 120px}
.slogan q{display:block;font:800 clamp(30px,4.6vw,58px)/1.25 var(--f-display);font-stretch:80%;max-width:20em;margin:0 auto;quotes:"“" "”"}
.slogan p{margin-top:16px;opacity:.8}
'''
    body=phero('<a href="about.html">আমাদের সম্পর্কে</a><span aria-hidden="true">/</span><span>ঘোষণাপত্র</span>','বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিলের ঘোষণাপত্র')+f'''
<section class="doc"><div class="wrap"><div class="sheet">
 <div class="seal" aria-hidden="true"><img src="img/logo.png" alt=""></div>
 <p class="pre">{pre}</p>{arts}
 <p class="closing">{closing}</p>
</div></div></section>
<section class="slogan"><div class="wrap"><span class="script" style="color:#FFC9C4">আমাদের মূলমন্ত্র</span><q>{slogan}</q></div></section>'''+cta()
    return css, body

# ---------- CONSTITUTION
def constitution(content):
    css=COMMON_CSS+'''
.wait{padding-block:72px 96px}
.wait .card{max-width:760px;margin:0 auto;border:2px dashed var(--ink);background:var(--field);padding:44px clamp(20px,5vw,52px);display:grid;gap:18px;justify-items:start}
.wait h2{font-size:clamp(28px,3.4vw,38px);font-weight:800;font-stretch:82%}
.wait p{font-size:17px;color:var(--ink-soft)}
.wait .links{display:flex;flex-wrap:wrap;gap:12px;margin-top:6px}
.btn-line{color:var(--ink)}.btn-line:hover{background:var(--ink);color:var(--paper)}
'''
    body=phero('<a href="about.html">আমাদের সম্পর্কে</a><span aria-hidden="true">/</span><span>গঠনতন্ত্র</span>','গঠনতন্ত্র','বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিলের সাংগঠনিক কাঠামো, সদস্যপদ ও পরিচালনার নিয়মাবলী।')+'''
<section class="wait"><div class="wrap"><div class="card">
 <span class="script">শীঘ্রই</span><h2>গঠনতন্ত্রের পূর্ণ লেখা শীঘ্রই যুক্ত হবে</h2>
 <p>কেন্দ্রীয় কাউন্সিল কর্তৃক অনুমোদিত গঠনতন্ত্র এখানে ধারা অনুযায়ী প্রকাশ করা হবে। ততক্ষণ সংগঠনের ঘোষণাপত্র এবং লক্ষ্য ও উদ্দেশ্য পড়ুন।</p>
 <div class="links"><a class="btn btn-green" href="manifesto.html">ঘোষণাপত্র পড়ুন</a><a class="btn btn-line" href="objectives.html">লক্ষ্য ও উদ্দেশ্য</a></div>
 <p class="note-draft">নকশার নমুনা: গঠনতন্ত্রের লেখা পেলে প্রতিটি ধারা সূচিপত্রসহ এই পাতায় সাজানো হবে।</p>
</div></div></section>'''
    return css, body

# ---------- MESSAGES
MSG_CSS=COMMON_CSS+'''
.msg .wrap{display:grid;grid-template-columns:340px minmax(0,1fr);gap:64px;align-items:start;padding-block:72px 96px}
.who{position:sticky;top:calc(env(safe-area-inset-top,0px) + 96px);display:grid;gap:18px}
.who figure{margin:0;border:2px solid var(--ink);box-shadow:10px 10px 0 var(--green);background:var(--field)}
.who img{display:block;width:100%;height:auto;aspect-ratio:4/5;object-fit:cover;object-position:top}
.who .card{border-left:6px solid var(--red);padding:4px 0 4px 16px}
.who b{display:block;font:800 28px/1.15 var(--f-display);font-stretch:84%}
.who span{display:block;color:var(--ink-soft);font-size:15px;margin-top:4px}
.who .role{font:700 17px/1.2 var(--f-display);color:var(--green);margin-top:6px}
.letter{max-width:720px;min-width:0}
.letter .salute{font-family:var(--f-script);font-size:clamp(24px,2.6vw,30px);line-height:1.4;color:var(--green)}
.letter p{font-size:18px;line-height:1.95;margin-top:18px}
.letter p.greet{margin-top:6px;color:var(--ink-soft)}
.letter blockquote{margin:30px 0;padding:22px 26px;background:var(--green);color:#FBF3E6;font:700 clamp(20px,2.2vw,25px)/1.6 var(--f-display);border-left:8px solid var(--red)}
.sign{margin-top:40px;padding-top:22px;border-top:2px solid var(--ink);display:grid;gap:2px}
.sign .sig{font-family:var(--f-script);font-size:34px;color:var(--ink);line-height:1.2}
.sign b{font:800 20px/1.3 var(--f-display)}
.sign span{color:var(--ink-soft);font-size:15.5px}
@media (max-width:900px){.msg .wrap{grid-template-columns:1fr;gap:36px}.who{position:static;grid-template-columns:160px minmax(0,1fr);align-items:end}.who figure{box-shadow:6px 6px 0 var(--green)}}
@media (max-width:420px){.who{grid-template-columns:120px minmax(0,1fr)}.who b{font-size:22px}}
.other{background:var(--paper-2);border-top:1px solid var(--rule)}
.other .wrap{padding-block:48px;display:flex;flex-wrap:wrap;gap:20px;align-items:center;justify-content:space-between}
.other a.card2{display:grid;grid-template-columns:72px minmax(0,1fr) auto;gap:16px;align-items:center;text-decoration:none;border:2px solid var(--ink);background:var(--field);padding:12px 18px 12px 12px;min-width:0;max-width:520px;width:100%}
.other a.card2:hover{box-shadow:6px 6px 0 var(--green)}
.other img{width:72px;height:72px;object-fit:cover;object-position:top}
.other small{display:block;color:var(--ink-soft);font-size:13.5px}
.other strong{font:800 21px/1.2 var(--f-display)}
.other .arr{font:800 24px/1 var(--f-display);color:var(--green)}
'''
def message(content, fname, other):
    meta,b=fm(f"{content}/{fname}"); ps=paras(b)
    om,_=fm(f"{content}/{other[0]}")
    sal, greet, rest = ps[0], ps[1], ps[2:]
    closing=rest[-1]; rest=rest[:-1]
    out=""
    for p in rest:
        if "কেবল একটি" in p and "BMPC" in p:
            q,_,tail=p.partition("আন্দোলনের নাম।")
            out+=f"<blockquote>{q}আন্দোলনের নাম।</blockquote>"
            if tail.strip(): out+=f"<p>{tail.strip()}</p>"
        else: out+=f"<p>{p}</p>"
    out+=f"<p>{closing}</p>"
    photo="img/"+os.path.basename(meta["photo"])
    oph="img/"+os.path.basename(om["photo"])
    body=phero(f'<span>বাণী</span><span aria-hidden="true">/</span><span>{meta["title"]}</span>', meta["title"])+f'''
<section class="msg"><div class="wrap">
 <aside class="who"><figure><img src="{photo}" alt="{meta["name"]}, {meta["role"]}" width="480" height="600"></figure>
  <div class="card"><b>{meta["name"]}</b><p class="role">{meta["role"]}</p><span>বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিল (BMPC)</span><span>কেন্দ্রীয় কাউন্সিল</span></div></aside>
 <article class="letter"><p class="salute">{sal}</p><p class="greet">{greet}</p>{out}
  <div class="sign">{"<span>ধন্যবাদান্তে,</span>" if "secretary" in fname else ""}<span class="sig">{meta["name"]}</span><b>{meta["role"]}</b><span>বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিল (BMPC)</span><span>কেন্দ্রীয় কাউন্সিল</span></div>
 </article>
</div></section>
<section class="other"><div class="wrap"><div><span class="script">আরও পড়ুন</span></div>
 <a class="card2" href="{other[1]}"><img src="{oph}" alt=""><span><small>{om["title"]}</small><strong>{om["name"]}</strong></span><span class="arr" aria-hidden="true">→</span></a></div></section>'''+cta("ঐক্যবদ্ধ হওয়ার আহ্বানে সাড়া দিন")
    return MSG_CSS, body

# ---------- NEWS
MONTHS=["জানুয়ারি","ফেব্রুয়ারি","মার্চ","এপ্রিল","মে","জুন","জুলাই","আগস্ট","সেপ্টেম্বর","অক্টোবর","নভেম্বর","ডিসেম্বর"]
def bdate(iso):
    y,m,d=iso.split("-"); return f"{bn(int(d))} {MONTHS[int(m)-1]} {bn(y)}"
def news_items(content):
    d=f"{content}/news"; out=[]
    for f in sorted(os.listdir(d),reverse=True):
        if not f.endswith(".md") or f == "README.md": continue
        meta,b=fm(f"{d}/{f}"); stem=f[:-3]
        meta.update(stem=stem, slug=f"news-{stem}.html", image_file=os.path.basename(meta.get("image","og-default.jpg")))
        meta["alt"]=meta.get("alt") or meta["title"]
        blocks=paras(b); meta["body"]=[re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", p) for p in blocks if not p.startswith("![")]
        meta["summary"]=meta.get("summary",""); meta["gallery"]=re.findall(r"!\[(.*?)\]\((.*?)\)",b)
        out.append(meta)
    return out
def card(n, big=False):
    return (f'<a class="story{" big" if big else ""}" href="{n["slug"]}"><img src="img/{n["image_file"]}" alt="{n["alt"]}" width="795" height="497" loading="{"eager" if big else "lazy"}">'
            f'<div class="txt"><div class="meta"><span class="chip-cat">{n.get("category","সংবাদ")}</span><time datetime="{n["date"]}">{bdate(n["date"])}</time></div>'
            f'<h2>{n["title"]}</h2>{"<p>"+n["body"][0]+"</p>" if big else ""}<span class="more">পুরো সংবাদ পড়ুন →</span></div></a>')
def home_news(content):
    n=news_items(content)[0]
    return (f'<a class="nstory" href="{n["slug"]}"><img src="img/{n["image_file"]}" alt="{n["alt"]}" width="795" height="497" loading="lazy"><div>'
            f'<span class="ndate">{bdate(n["date"])}{" · "+n["place"] if n.get("place") else ""}</span><h3>{n["title"]}</h3><p>{n.get("summary") or n["body"][0][:160]}</p></div></a>')
NEWS_CSS=COMMON_CSS+'''
.feat{padding-block:64px 40px}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.grid-sec{padding-block:8px 88px}
.ngrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,320px),1fr));gap:24px}
.ngrid a.story{display:grid;grid-template-rows:auto 1fr;text-decoration:none;border:2px solid var(--ink);background:var(--field)}
.ngrid img{display:block;width:100%;aspect-ratio:16/10;object-fit:cover}
.ngrid .txt{padding:18px 20px 22px;display:grid;gap:10px;align-content:start;border-top:2px solid var(--ink)}
.ngrid h2{font-size:22px;font-weight:800;font-stretch:86%;line-height:1.3}
.ngrid a.story:hover{box-shadow:6px 6px 0 var(--green)}
.feat a.story{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);text-decoration:none;border:2px solid var(--ink);background:var(--field);box-shadow:10px 10px 0 var(--green)}
.feat a.story:hover h2{text-decoration:underline;text-underline-offset:6px}
.feat a.story img{display:block;width:100%;height:100%;object-fit:cover;min-height:260px}
.feat a.story .txt{padding:32px clamp(20px,3vw,40px);display:grid;gap:14px;align-content:center;border-left:2px solid var(--ink)}
.feat h2{font-size:clamp(28px,3.2vw,40px);font-weight:800;font-stretch:82%;line-height:1.2}
.feat p{font-size:16.5px;line-height:1.85}
.feat .more{font:700 16px/1 var(--f-display);color:var(--green)}
@media (max-width:860px){.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.grid-sec{padding-block:8px 88px}
.ngrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,320px),1fr));gap:24px}
.ngrid a.story{display:grid;grid-template-rows:auto 1fr;text-decoration:none;border:2px solid var(--ink);background:var(--field)}
.ngrid img{display:block;width:100%;aspect-ratio:16/10;object-fit:cover}
.ngrid .txt{padding:18px 20px 22px;display:grid;gap:10px;align-content:start;border-top:2px solid var(--ink)}
.ngrid h2{font-size:22px;font-weight:800;font-stretch:86%;line-height:1.3}
.ngrid a.story:hover{box-shadow:6px 6px 0 var(--green)}
.feat a.story{grid-template-columns:1fr}.feat a.story .txt{border-left:0;border-top:2px solid var(--ink)}}
.empty{padding-block:0 88px}
.empty .box{border:2px dashed var(--ink-soft);padding:28px;display:flex;flex-wrap:wrap;gap:16px;align-items:center;justify-content:space-between;color:var(--ink-soft)}
.empty b{font:700 20px/1.3 var(--f-display);color:var(--ink)}
'''
def news_list(content):
    it=news_items(content); first, rest = it[0], it[1:]
    grid = ('<section class="grid-sec"><div class="wrap"><h2 class="sr">আরও সংবাদ</h2><div class="ngrid">' + "".join(card(n) for n in rest) + '</div></div></section>') if rest else \
           '<section class="empty"><div class="wrap"><div class="box"><div><b>আরও সংবাদ শীঘ্রই</b><p>নতুন পোস্ট প্রকাশ হলে এখানে তালিকা আকারে দেখা যাবে।</p></div><a class="btn btn-green" href="join.html">সদস্য হোন</a></div></div></section>'
    body=phero('<span>সর্বশেষ সংবাদ</span>','সর্বশেষ সংবাদ','কাউন্সিলের কর্মসূচি, মানববন্ধন, দিবস পালন ও সাংগঠনিক কার্যক্রমের খবর।')+ \
        f'<section class="feat"><div class="wrap">{card(first, True)}</div></section>' + grid
    return NEWS_CSS, body
POST_CSS=COMMON_CSS+'''
.post .wrap{max-width:860px;padding-block:56px 88px;display:grid;gap:24px}
.post figure{margin:0;border:2px solid var(--ink);box-shadow:10px 10px 0 var(--green)}
.post figure img{display:block;width:100%;height:auto}
.post figcaption{font-size:13.5px;color:var(--ink-soft);padding:10px 14px;background:var(--field);border-top:1px solid var(--rule)}
.gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,240px),1fr));gap:16px}
.gallery figure{margin:0;border:2px solid var(--ink);box-shadow:none}
.gallery img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover}
.event{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,180px),1fr));border:2px solid var(--ink);background:var(--field)}
.event div{padding:12px 16px;border-left:1px solid var(--rule)}
.event div:first-child{border-left:0}
.event small{display:block;font:600 12.5px/1 var(--f-body);letter-spacing:.06em;color:var(--red);margin-bottom:6px}
.event b{font:700 18px/1.3 var(--f-display)}

.post .body p{font-size:18.5px;line-height:1.95}
.post .body p+p{margin-top:1.1em}
.post .body strong{color:var(--green);font-weight:600}
.back{font:700 16px/1 var(--f-display);color:var(--green)}
'''
def news_post(n):
    ev=""
    if n.get("event"):
        parts=[x.strip() for x in n["event"].split("·")]
        labels=["কর্মসূচি","তারিখ","সময়","স্থান"]
        ev='<div class="event" aria-label="কর্মসূচির তথ্য">'+"".join(f'<div><small>{labels[i] if i<4 else ""}</small><b>{p}</b></div>' for i,p in enumerate(parts))+'</div>'
    gal=""
    if n["gallery"]:
        gal='<div class="gallery">'+"".join(f'<figure><img src="img/{os.path.basename(src)}" alt="{alt}" loading="lazy"><figcaption>{alt}</figcaption></figure>' for alt,src in n["gallery"])+'</div>'
    note=f'<p class="note-draft">নকশার নমুনা: লাইভ সাইটের তালিকা থেকে শুধু সারাংশ নেওয়া হয়েছে; পূর্ণ সংবাদ এখানে বসবে।</p>' if n.get("note") else ""
    body=phero('<a href="news.html">সর্বশেষ সংবাদ</a><span aria-hidden="true">/</span><span>সংবাদ</span>', n["title"])+f'''
<article class="post"><div class="wrap">
 <div class="meta"><span class="chip-cat">{n.get("category","সংবাদ")}</span><time datetime="{n["date"]}">{bdate(n["date"])}</time><span>{n.get("author","")}</span></div>
 <figure><img src="img/{n["image_file"]}" alt="{n["alt"]}" width="795" height="497"><figcaption>{n.get("caption") or n.get("place","")}</figcaption></figure>
 {ev}
 <div class="body">{"".join(f"<p>{p}</p>" for p in n["body"])}</div>
 {gal}{note}
 <a class="back" href="news.html">← সব সংবাদ</a>
</div></article>'''
    return POST_CSS, body
