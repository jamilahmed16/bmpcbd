import sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import art
from art import bn
import pages2, seo
OUT = sys.argv[1]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
 '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anek+Bangla:wdth,wght@75..100,400..800&family=Galada&family=Hind+Siliguri:wght@400;500;600&display=swap">'
 '<link rel="stylesheet" href="site.css"><script src="motion.js" defer></script>')
LOGO = '<img class="logo" src="img/logo.png" width="68" height="68" alt="">'

NAV=[("index.html","হোম","home",None),
     (None,"আমাদের সম্পর্কে","about",[("about.html","পরিচিতি ও নীতিমালা"),("manifesto.html","ঘোষণাপত্র"),("constitution.html","গঠনতন্ত্র"),("objectives.html","লক্ষ্য ও উদ্দেশ্য")]),
     (None,"বাণী","msg",[("chairman.html","চেয়ারম্যানের বাণী"),("secretary.html","মহাসচিবের বাণী")]),
     ("news.html","সর্বশেষ সংবাদ","news",None),("#footer","যোগাযোগ","contact",None)]
GROUP={"about":"about","manifesto":"about","constitution":"about","objectives":"about","chairman":"msg","secretary":"msg","news":"news","home":"home"}
def header(cur):
    g=GROUP.get(cur,cur); nav=""; drop=""
    for href,t,k,sub in NAV:
        cc=' aria-current="page"' if k==g else ''
        if sub:
            items="".join(f'<a href="{h}">{x}</a>' for h,x in sub)
            nav+=f'<div class="dd"><button type="button" class="dd-btn"{cc} aria-haspopup="true">{t}<span class="chev" aria-hidden="true"></span></button><div class="dd-menu">{items}</div></div>'
            drop+=f'<span class="drop-h">{t}</span>'+"".join(f'<a class="sub" href="{h}">{x}</a>' for h,x in sub)
        else:
            nav+=f'<a href="{href}"{cc}>{t}</a>'; drop+=f'<a href="{href}">{t}</a>'
    drop+='<a href="join.html">সদস্য হোন</a>'
    return f"""<header class="top"><div class="wrap">
<a class="brand" href="index.html" aria-label="বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিল, হোম">{LOGO}<span><b>বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিল</b></span></a>
<nav class="nav" aria-label="প্রধান মেনু">{nav}</nav>
<a class="btn btn-paper" href="join.html">সদস্য হোন</a>
<details class="menu"><summary>মেনু</summary><nav class="drop" aria-label="মোবাইল মেনু">{drop}</nav></details>
</div></header>"""

SOCIAL = ('<div class="social" aria-label="সামাজিক যোগাযোগ">'
  '<a href="#" aria-label="Facebook"><svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M14 8h3V4h-3c-2.8 0-4 1.7-4 4.2V10H7v4h3v8h4v-8h3l1-4h-4V8.6c0-.4.3-.6.6-.6z"/></svg></a>'
  '<a href="#" aria-label="X"><svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M17.7 3h3.1l-6.8 7.8L22 21h-6.3l-4.9-6.4L5.2 21H2.1l7.3-8.3L1.8 3h6.4l4.4 5.9zm-1.1 16.2h1.7L7.5 4.7H5.7z"/></svg></a>'
  '<a href="#" aria-label="Instagram"><svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M12 7.3A4.7 4.7 0 1 0 12 16.7 4.7 4.7 0 0 0 12 7.3zm0 7.7a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm4.9-8.9a1.1 1.1 0 1 1 0 2.2 1.1 1.1 0 0 1 0-2.2zM12 2.5c-2.6 0-2.9 0-3.9.1C4.6 2.7 2.7 4.6 2.6 8.1c-.1 1-.1 1.3-.1 3.9s0 2.9.1 3.9c.1 3.5 2 5.4 5.5 5.5 1 .1 1.3.1 3.9.1s2.9 0 3.9-.1c3.5-.1 5.4-2 5.5-5.5.1-1 .1-1.3.1-3.9s0-2.9-.1-3.9c-.1-3.5-2-5.4-5.5-5.5-1-.1-1.3-.1-3.9-.1zm0 1.7c2.5 0 2.8 0 3.8.1 2.5.1 3.7 1.3 3.8 3.8.1 1 .1 1.3.1 3.8s0 2.8-.1 3.8c-.1 2.5-1.3 3.7-3.8 3.8-1 .1-1.3.1-3.8.1s-2.8 0-3.8-.1c-2.5-.1-3.7-1.3-3.8-3.8-.1-1-.1-1.3-.1-3.8s0-2.8.1-3.8C4.5 5.6 5.7 4.4 8.2 4.3c1-.1 1.3-.1 3.8-.1z"/></svg></a>'
  '<a href="https://www.youtube.com/channel/UC3pXvRvIoVYgEGwdkNx3Gfw" aria-label="YouTube" rel="noopener" target="_blank"><svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12a31 31 0 0 0 .5 4.8 3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .5-4.8 31 31 0 0 0-.5-4.8zM9.7 15V9l5.8 3z"/></svg></a>'
  '<a href="news.html" aria-label="সংবাদ (RSS)"><svg viewBox="0 0 24 24" width="20" height="20"><path fill="currentColor" d="M5 17a2 2 0 1 1 0 4 2 2 0 0 1 0-4zM3 10v3a8 8 0 0 1 8 8h3A11 11 0 0 0 3 10zm0-6v3a14 14 0 0 1 14 14h3A17 17 0 0 0 3 4z"/></svg></a></div>')

FOOTER = f'''<footer id="footer"><div class="wrap"><div class="cols">
<div><a class="brand" href="index.html">{LOGO}<span><b>বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিল</b></span></a>
<p class="about-f">মুক্তিযুদ্ধের চেতনা ধারণকারী অরাজনৈতিক সংগঠন। বীর মুক্তিযোদ্ধার সন্তান ও প্রজন্মের ঐক্যবদ্ধ প্ল্যাটফর্ম।</p>{SOCIAL}</div>
<div><h2 class="fh">সংগঠন</h2><ul><li><a href="about.html">আমাদের সম্পর্কে</a></li><li><a href="manifesto.html">ঘোষণাপত্র</a></li><li><a href="constitution.html">গঠনতন্ত্র</a></li><li><a href="objectives.html">লক্ষ্য ও উদ্দেশ্য</a></li></ul></div>
<div><h2 class="fh">অংশ নিন</h2><ul><li><a href="join.html">সদস্য হোন</a></li><li><a href="chairman.html">চেয়ারম্যানের বাণী</a></li><li><a href="secretary.html">মহাসচিবের বাণী</a></li><li><a href="news.html">সর্বশেষ সংবাদ</a></li></ul></div>
</div><div class="emergency" aria-label="জরুরি হটলাইন"><b>জরুরি নম্বর</b><span><strong>৯৯৯</strong> জাতীয় জরুরি সেবা (পুলিশ, ফায়ার সার্ভিস, অ্যাম্বুলেন্স)</span><span><strong>৩৩৩</strong> সরকারি তথ্য ও সেবা</span><span><strong>১০২</strong> ফায়ার সার্ভিস</span><span><strong>১০৯ / ১০৯২১</strong> নারী ও শিশু নির্যাতন প্রতিরোধ</span><span><strong>১৬২৬৩</strong> স্বাস্থ্য বাতায়ন</span><span><strong>১৬৪৩০</strong> আইনগত সহায়তা</span></div><div class="legal"><span>© ২০২৬ বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিল</span><span>Developed by Rank On Fire LLC</span></div></div></footer>'''

def page(title, css, body, full, script="", fname=None, news=None):
    if fname and full: title = seo.PAGES[fname][1]
    meta = ("\n" + seo.head(fname, news)) if fname else ""
    head = f'<title>{title}</title>\n<meta name="claude:viewport-fit-sides" content="cover">{meta}\n{FONTS}\n<style>{css}</style>\n'
    content = head + body + (f"<script>{script}</script>" if script else "")
    if full:
        return ('<!doctype html><html lang="bn"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
                + head + '</head><body>' + body + (f"<script>{script}</script>" if script else "") + '</body></html>')
    return content

# ---------------- content
md = open(sys.argv[2]).read()
def section(md, h):
    m = re.search(r'## '+h+r'\n(.*?)(?=\n## |\Z)', md, re.S); return m.group(1)
def items(txt):
    return [re.sub(r'^[০-৯]+\.\s*','',l.strip()) for l in txt.split('\n\n') if re.match(r'^[০-৯]+\.',l.strip())]
goals = items(section(md,'আমাদের লক্ষ্য'))
short = items(section(md,'স্বল্পমেয়াদী উদ্দেশ্য'))
long_ = items(section(md,'দীর্ঘমেয়াদী উদ্দেশ্য'))
assert (len(goals),len(short),len(long_))==(8,6,23), (len(goals),len(short),len(long_))
closing = "এই লক্ষ্যগুলির মাধ্যমে কাউন্সিল মুক্তিযুদ্ধের আদর্শ ও ইতিহাসকে বর্তমান এবং ভবিষ্যৎ প্রজন্মের কাছে সঠিকভাবে পৌঁছে দিতে সক্ষম হবে।"

CATS = {"edu":"শিক্ষা ও সংস্কৃতি","welfare":"কল্যাণ ও স্বাস্থ্য","work":"কর্মসংস্থান ও অর্থনীতি","rights":"অধিকার ও সুরক্ষা","heritage":"ঐতিহ্য ও সংগঠন"}
LCAT = {1:"edu",2:"rights",3:"edu",4:"work",5:"welfare",6:"work",7:"work",8:"rights",9:"welfare",10:"work",11:"work",12:"heritage",
        13:"rights",14:"rights",15:"welfare",16:"welfare",17:"heritage",18:"heritage",19:"rights",20:"work",21:"work",22:"welfare",23:"work"}

# ---------------- HOME
HOME_CSS = '''
.hero .wrap{display:grid;grid-template-columns:minmax(0,.95fr) minmax(0,1.2fr);gap:20px;align-items:end;padding-block:56px 0}
.hero h1{font-size:clamp(46px,6.6vw,90px);font-weight:800;font-stretch:76%;letter-spacing:-.01em;margin:18px 0 22px;line-height:1.03}
.hero h1 em{font-style:normal;text-decoration:underline 7px var(--sun);text-underline-offset:10px;text-decoration-skip-ink:none}
.hero .lede{font-size:19px;max-width:32em;opacity:.95}
.cta-row{display:flex;flex-wrap:wrap;gap:12px;margin:30px 0 64px}
.hero-art{margin-right:calc(-1 * max(16px,env(safe-area-inset-right,0px)))}
.hero-art svg{display:block;width:100%;height:auto}
@media (max-width:880px){.hero .wrap{grid-template-columns:1fr;padding-top:36px}.cta-row{margin-bottom:12px}.hero-art{margin-left:calc(-1 * max(16px,env(safe-area-inset-left,0px)))}}
.about .wrap{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:64px;align-items:center}
.about .big{font:800 clamp(110px,16vw,220px)/.85 var(--f-display);font-stretch:75%;color:transparent;-webkit-text-stroke:2px var(--red);letter-spacing:-.02em}
.about .big span{color:var(--red);-webkit-text-stroke:0}
.about .tag{display:block;margin-top:20px;font:500 16px/1.6 var(--f-body);color:var(--ink-soft);max-width:22em;border-left:3px solid var(--red);padding-left:14px}
.about p.body{font-size:20px;line-height:1.9;margin-bottom:24px}
.about p.body strong{color:var(--red);font-weight:600}
.pill-row{display:flex;flex-wrap:wrap;gap:10px}
.pill{font:600 14px/1 var(--f-body);padding:10px 14px;border:1.5px solid var(--ink);border-radius:999px}
@media (max-width:880px){.about .wrap{grid-template-columns:1fr;gap:28px}}
.goals{background:var(--green-deep);color:var(--on-red);position:relative;overflow:hidden}
.goals::before{content:"";position:absolute;inset:0;background:repeating-conic-gradient(from 0deg at 100% 0%,rgba(0,0,0,.16) 0 4deg,transparent 4deg 8deg);pointer-events:none}
.goals .wrap{position:relative}
.goals .script{color:#FFC9C4}
.goals ol{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:56px}
.goals li{display:grid;grid-template-columns:clamp(38px,9vw,60px) minmax(0,1fr);gap:16px;padding:22px 0;border-top:1px solid rgba(251,243,230,.22)}
.goals .n{font:800 46px/1 var(--f-display);font-stretch:75%}
.goals li p{font-size:16.5px;line-height:1.8;opacity:.93}
.goals .foot{display:flex;flex-wrap:wrap;gap:20px 40px;align-items:center;justify-content:space-between;margin-top:40px}
.goals .closing{font:600 20px/1.6 var(--f-display);max-width:40em;border-left:4px solid var(--on-red);padding-left:18px}
@media (max-width:880px){.goals ol{grid-template-columns:1fr}}
.leaders .lgrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px}
.lcard{display:grid;grid-template-columns:190px minmax(0,1fr);text-decoration:none;border:2px solid var(--ink);background:var(--field);box-shadow:8px 8px 0 var(--green)}
.lcard img{width:100%;height:100%;object-fit:cover;object-position:top;display:block;border-right:2px solid var(--ink);min-height:240px}
.lcard div{padding:24px;display:grid;gap:8px;align-content:start}
.lcard q{font:600 17px/1.7 var(--f-display);quotes:"“" "”";margin-bottom:6px}
.lcard b{font:800 22px/1.2 var(--f-display)}
.lcard span{font-size:14.5px;color:var(--ink-soft)}
.lcard em{font:700 15px/1 var(--f-display);font-style:normal;color:var(--green);margin-top:8px}
.lcard:hover em{text-decoration:underline}
@media (max-width:980px){.leaders .lgrid{grid-template-columns:1fr}}
@media (max-width:520px){.lcard{grid-template-columns:120px minmax(0,1fr)}.lcard div{padding:16px}.lcard q{font-size:15.5px}}
.row-head{display:flex;flex-wrap:wrap;gap:16px;align-items:end;justify-content:space-between;max-width:none}
.hnews{padding-top:0}
.nstory{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);text-decoration:none;border:2px solid var(--ink);background:var(--field)}
.nstory img{width:100%;height:100%;object-fit:cover;display:block;min-height:240px}
.nstory div{padding:30px clamp(20px,3vw,40px);display:grid;gap:12px;align-content:center;border-left:2px solid var(--ink)}
.ndate{font:600 14px/1.3 var(--f-body);color:var(--red)}
.nstory h3{font-size:clamp(24px,2.6vw,32px);font-weight:800;font-stretch:84%}
.nstory:hover h3{text-decoration:underline;text-underline-offset:6px}
@media (max-width:820px){.nstory{grid-template-columns:1fr}.nstory div{border-left:0;border-top:2px solid var(--ink)}}
.plans .grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px}
.plan{border:2px solid var(--ink);padding:32px;display:grid;gap:14px;align-content:start;background:var(--field);box-shadow:8px 8px 0 var(--green)}
.plan .count{font:800 76px/1 var(--f-display);font-stretch:75%;color:var(--red)}
.plan h3{font-size:28px;font-weight:700}
.plan ul{margin:0;padding-left:20px;color:var(--ink-soft)}
.plan li{margin:6px 0}
.plan a{font:700 16px/1 var(--f-display);color:var(--red);text-underline-offset:6px;margin-top:6px}
@media (max-width:760px){.plans .grid{grid-template-columns:1fr}}
.days{background:var(--paper-2);border-block:1px solid var(--rule)}
.day-row{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px}
.day{display:grid;gap:12px;align-content:start}
.day svg{width:100%;height:auto;display:block;background:#EFE8DA;border:2px solid var(--ink)}
.day .date{font:800 32px/1.1 var(--f-display);font-stretch:80%;color:var(--red)}
.day .date small{display:block;font:500 15px/1.4 var(--f-body);color:var(--ink-soft);margin-top:6px}
.acts{margin-top:52px;display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.acts strong{font:700 18px/1 var(--f-display);margin-right:8px}
.acts span{font:500 15px/1 var(--f-body);padding:11px 14px;background:var(--field);border:1px solid var(--rule)}
@media (max-width:760px){.day-row{grid-template-columns:1fr}}
.join{background:#167452;color:#FBF3E6;position:relative;overflow:hidden}
.join::after{content:"";position:absolute;width:440px;height:440px;border-radius:50%;background:#E8362E;right:-150px;bottom:-200px;opacity:.95;
  -webkit-mask:repeating-linear-gradient(180deg,#000 0 16px,transparent 16px 22px);mask:repeating-linear-gradient(180deg,#000 0 16px,transparent 16px 22px)}
.join .wrap{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:56px;align-items:center;position:relative;z-index:1}
.join h2{font-size:clamp(36px,4.6vw,58px);font-weight:800;font-stretch:80%}
.join p.lead{font-size:19px;margin-top:16px;opacity:.95}
.join .script{color:#FFC9C4}
.steps{list-style:none;margin:0;padding:0;display:grid;gap:14px}
.steps li{display:grid;grid-template-columns:52px minmax(0,1fr);gap:16px;align-items:center;background:rgba(0,0,0,.2);padding:16px 18px;border-left:4px solid #E8362E}
.steps b{font:800 34px/1 var(--f-display);font-stretch:75%}
.join .btn{margin-top:28px}
@media (max-width:880px){.join .wrap{grid-template-columns:1fr;gap:32px}}
'''
goal_li = "".join(f'<li><span class="n">{bn(i+1)}</span><p>{g}</p></li>' for i,g in enumerate(goals))
HOME = header("home") + f'''
<main>
<section class="hero"><div class="wrap">
 <div>
  <span class="eyebrow">অরাজনৈতিক · মুক্তিযুদ্ধের চেতনায়</span>
  <h1>রক্তে কেনা স্বাধীনতা, <em>প্রজন্মের</em> অঙ্গীকার</h1>
  <p class="lede">নতুন প্রজন্মকে মুক্তিযুদ্ধের সত্যিকার ইতিহাস জানানো এবং দেশপ্রেমে উদ্বুদ্ধ করা আমাদের মূল লক্ষ্য। বীর মুক্তিযোদ্ধার সন্তান ও প্রজন্মের ঐক্যবদ্ধ প্ল্যাটফর্ম।</p>
  <div class="cta-row"><a class="btn btn-paper" href="join.html">সদস্য হোন</a><a class="btn btn-ghost" href="objectives.html">আমাদের লক্ষ্য</a></div>
 </div>
 <div class="hero-art poster">{art.hero_svg()}</div>
</div></section>
<div class="ribbon" aria-label="মুক্তিযুদ্ধ এক নজরে"><div class="wrap">
 <div><b>২৬ মার্চ</b><span>স্বাধীনতার ঘোষণা, ১৯৭১</span></div><div><b>২৬৬ দিন</b><span>নয় মাসের রক্তক্ষয়ী যুদ্ধ</span></div>
 <div><b>১১টি</b><span>রণাঙ্গনের সেক্টর</span></div><div><b class="r">১৬ ডিসেম্বর</b><span>মহান বিজয়, ১৯৭১</span></div>
</div></div>
<section class="about" id="about"><div class="wrap">
 <div><div class="big" aria-hidden="true">১৯<span>৭১</span></div>
  <span class="tag">যে ইতিহাস আমাদের পিতা ও পিতামহরা লিখেছেন, তা পৌঁছে দিতে হবে পরের প্রজন্মের হাতে।</span></div>
 <div><div class="sec-head" style="margin-bottom:24px"><h2>মুক্তিযুদ্ধের চেতনা ধারণকারী অরাজনৈতিক সংগঠন</h2></div>
  <p class="body">আমাদের সংগঠন <strong>অরাজনৈতিক</strong> এবং মুক্তিযুদ্ধের চেতনা ধারণ করে। এখানে আমরা বাংলাদেশের মহান মুক্তিযুদ্ধের ইতিহাস, গৌরবগাঁথা এবং মুক্তিযোদ্ধাদের অবদান সম্পর্কে আলোচনা করে থাকি। নতুন প্রজন্মকে মুক্তিযুদ্ধের <strong>সত্যিকার ইতিহাস</strong> জানানো এবং দেশপ্রেমে উদ্বুদ্ধ করা আমাদের মূল লক্ষ্য।</p>
  <div class="pill-row"><a class="pill" href="about.html" style="text-decoration:none;background:var(--green);color:#fff;border-color:var(--green)">বিস্তারিত পরিচিতি →</a><span class="pill">ঐক্য ও সংহতি</span><span class="pill">সঠিক ইতিহাস</span><span class="pill">মুক্তিযোদ্ধা পরিবারের কল্যাণ</span><span class="pill">দুর্নীতিমুক্ত সমাজ</span></div></div>
</div></section>
<section class="goals" id="goals"><div class="wrap">
 <div class="sec-head"><h2>আটটি অঙ্গীকার</h2></div>
 <ol>{goal_li}</ol>
 <div class="foot"><p class="closing">{closing}</p><a class="btn btn-paper" href="objectives.html">সব উদ্দেশ্য দেখুন</a></div>
</div></section>
<section class="leaders"><div class="wrap">
 <div class="sec-head"><h2>শেকড় সন্ধানী এক আন্দোলন</h2></div>
 <div class="lgrid">
  <a class="lcard" href="chairman.html"><img src="img/chairman.jpg" alt="রহিমুল ফারুক বাবু" width="375" height="666"><div><q>আমাদের এই ওয়েবসাইটটি হবে আমাদের মিলনকেন্দ্র—যেখানে আমরা ইতিহাসের সঠিক চর্চা করব, আমাদের সামাজিক দায়বদ্ধতা পালন করব এবং একে অপরের পাশে দাঁড়াব।</q><b>রহিমুল ফারুক বাবু</b><span>চেয়ারম্যান, কেন্দ্রীয় কাউন্সিল</span><em>চেয়ারম্যানের বাণী পড়ুন →</em></div></a>
  <a class="lcard" href="secretary.html"><img src="img/secretary.jpg" alt="মোঃ আল আমিন" width="480" height="458"><div><q>মহাসচিব হিসেবে আমার অঙ্গীকার হলো—সংগঠনের প্রতিটি স্তরে প্রশাসনিক স্বচ্ছতা বজায় রাখা।</q><b>মোঃ আল আমিন</b><span>মহাসচিব, কেন্দ্রীয় কাউন্সিল</span><em>মহাসচিবের বাণী পড়ুন →</em></div></a>
 </div>
</div></section>
<section class="plans"><div class="wrap">
 <div class="sec-head"><h2>আজকের কাজ, আগামীর বাংলাদেশ</h2></div>
 <div class="grid">
  <article class="plan"><span class="count">৬</span><h3>স্বল্পমেয়াদী উদ্দেশ্য</h3><ul>
   <li>সকল বীর মুক্তিযোদ্ধা, সন্তান ও প্রজন্মকে ডাটাবেজে অন্তর্ভুক্ত করে প্রত্যয়ন পত্র ও আইডি কার্ড প্রদান</li>
   <li>জীবিত বীর মুক্তিযোদ্ধাদের যুদ্ধকালীন ইতিহাস অনলাইনে প্রচার ও সংরক্ষণ</li>
   <li>অসচ্ছল মুক্তিযোদ্ধা পরিবারের সহায়তায় ফাউন্ডেশন গঠন</li></ul>
   <a href="objectives.html#short">স্বল্পমেয়াদী উদ্দেশ্য পড়ুন →</a></article>
  <article class="plan"><span class="count">২৩</span><h3>দীর্ঘমেয়াদী উদ্দেশ্য</h3><ul>
   <li>স্কুল-কলেজে বিতর্ক, কুইজ, খেলাধুলা ও সাংস্কৃতিক কর্মশালা</li>
   <li>বধ্যভূমি, কবরস্থান ও মুক্তিযুদ্ধের স্মৃতি জড়িত স্থাপনা সংরক্ষণ</li>
   <li>নারী ও শিশু অধিকার প্রতিষ্ঠা এবং বাল্য বিবাহ রোধে প্রকল্প</li></ul>
   <a href="objectives.html#long">দীর্ঘমেয়াদী উদ্দেশ্য পড়ুন →</a></article>
 </div>
</div></section>
<section class="hnews"><div class="wrap">
 <div class="sec-head row-head"><div><h2>মাঠের কর্মসূচি</h2></div><a class="btn btn-green" href="news.html">সব সংবাদ</a></div>
 {pages2.home_news(os.path.dirname(sys.argv[2]))}
</div></section>
<section class="days" id="days"><div class="wrap">
 <div class="sec-head"><h2>যে দিনগুলো আমরা প্রতি বছর পালন করি</h2></div>
 <div class="day-row">
  <article class="day poster">{art.minar_svg()}<p class="date">২১ ফেব্রুয়ারি<small>শহীদ দিবস ও আন্তর্জাতিক মাতৃভাষা দিবস</small></p></article>
  <article class="day poster">{art.sunrise_svg()}<p class="date">২৬ মার্চ<small>স্বাধীনতা দিবস ও সংগঠনের প্রতিষ্ঠা বার্ষিকী</small></p></article>
  <article class="day poster">{art.flag_svg()}<p class="date">১৬ ডিসেম্বর<small>মহান বিজয় দিবস</small></p></article>
 </div>
 <div class="acts"><strong>সারা বছর:</strong><span>বিতর্ক ও কুইজ</span><span>স্বেচ্ছায় রক্তদান</span><span>ত্রাণ বিতরণ</span><span>দুর্নীতি ও মাদকবিরোধী মানববন্ধন</span><span>ঈদ পুনর্মিলনী</span><span>বিনামূল্যে তথ্য সেবা</span></div>
</div></section>
<section class="join" id="join"><div class="wrap">
 <div><h2>আপনি কি বীর মুক্তিযোদ্ধার সন্তান বা প্রজন্ম?</h2>
  <p class="lead">শুধুমাত্র বীর মুক্তিযোদ্ধার সন্তান ও প্রজন্ম এই কাউন্সিলের সদস্য হতে পারবেন। আসুন, একসাথে ইতিহাসের দায়িত্ব নিই।</p>
  <a class="btn btn-paper" href="join.html">অনলাইন ফর্ম পূরণ করুন</a></div>
 <ol class="steps"><li><b>১</b><span>প্রকৃত পরিচয়ে অ্যাকাউন্ট তৈরি করুন</span></li><li><b>২</b><span>অনলাইন সদস্য ফর্ম পূরণ করুন</span></li><li><b>৩</b><span>সদস্য নীতিমালা ও পারস্পরিক শ্রদ্ধা মেনে চলুন</span></li></ol>
</div></section>
</main>''' + FOOTER

# ---------------- OBJECTIVES
OBJ_CSS = '''
.hero .wrap{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,.8fr);gap:32px;align-items:center;padding-block:48px}
.hero h1{font-size:clamp(46px,7vw,96px);font-weight:800;font-stretch:76%;margin:16px 0 18px;line-height:1.02}
.hero .lede{font-size:19px;max-width:34em;opacity:.95}
.jump{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:32px;max-width:640px}
.jump a{display:grid;gap:2px;text-decoration:none;border:2px solid var(--on-red);padding:14px 16px;transition:background .15s}
.jump a:hover{background:var(--on-red);color:var(--green-deep)}
.jump b{font:800 40px/1 var(--f-display);font-stretch:75%}
.jump span{font:600 15px/1.3 var(--f-body)}
.hero-art svg{display:block;width:100%;max-width:380px;margin-left:auto;height:auto;border-radius:50%}
@media (max-width:820px){.hero .wrap{grid-template-columns:1fr}.hero-art{order:-1}.hero-art svg{max-width:200px;margin:0}}
@media (max-width:460px){.jump b{font-size:32px}.jump span{font-size:13px}.jump a{padding:12px}}
.mission ol{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 56px}
.mission li{display:grid;grid-template-columns:clamp(40px,10vw,72px) minmax(0,1fr);gap:clamp(10px,3vw,18px);padding:26px 0;border-top:2px solid var(--ink)}
.mission .n{font:800 clamp(40px,9vw,58px)/.9 var(--f-display);font-stretch:75%;color:var(--red)}
.mission li p{font-size:17px;line-height:1.85}
.mission .closing{margin-top:40px;background:var(--green);color:var(--on-red);padding:28px 32px;font:600 21px/1.6 var(--f-display);box-shadow:8px 8px 0 #1A1514}
@media (max-width:820px){.mission ol{grid-template-columns:1fr}}
.short{background:var(--green-deep);color:var(--on-red);position:relative;overflow:hidden}
.short::before{content:"";position:absolute;inset:0;background:repeating-conic-gradient(from 0deg at 0% 100%,rgba(0,0,0,.18) 0 4deg,transparent 4deg 8deg);pointer-events:none}
.short .wrap{position:relative}
.short .script{color:#FFC9C4}
.short .intro{font-size:18px;opacity:.9;max-width:44em}
.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.card{background:#EFE8DA;color:#1A1514;padding:26px 24px 28px;display:grid;gap:14px;align-content:start;border-top:8px solid #E8362E}
.card .n{font:800 44px/1 var(--f-display);font-stretch:75%;color:#C8171E}
.card p{font-size:16px;line-height:1.8}
@media (max-width:980px){.cards{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:620px){.cards{grid-template-columns:1fr}}
.chips{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:28px}
.chip{font:600 15px/1 var(--f-body);padding:11px 16px;border:2px solid var(--ink);background:transparent;color:var(--ink);cursor:pointer;border-radius:999px;display:inline-flex;gap:8px;align-items:center}
.chip i{font-style:normal;font-family:var(--f-display);font-weight:700;opacity:.7}
.chip[aria-pressed="true"]{background:var(--green);border-color:var(--green);color:#fff}
.chip[aria-pressed="true"] i{opacity:1}
.long-list{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 48px}
.long-list li{display:grid;grid-template-columns:clamp(36px,9vw,56px) minmax(0,1fr);gap:14px;padding:20px 0;border-top:1px solid var(--rule)}
.long-list .n{font:800 36px/1 var(--f-display);font-stretch:75%;color:var(--red)}
.long-list p{font-size:16px;line-height:1.8}
.long-list .tag{display:inline-block;margin-top:10px;font:600 12.5px/1 var(--f-body);letter-spacing:.03em;padding:6px 10px;background:var(--paper-2);color:var(--ink-soft)}
.long-list li[hidden]{display:none}
.count-line{font:500 15px/1 var(--f-body);color:var(--ink-soft);margin-bottom:8px}
@media (max-width:820px){.long-list{grid-template-columns:1fr}}
.cta{background:#167452;color:#FBF3E6}
.cta .wrap{display:flex;flex-wrap:wrap;gap:24px;align-items:center;justify-content:space-between;padding-block:48px}
.cta h2{font-size:clamp(28px,3.4vw,40px);font-weight:800;font-stretch:80%}
.cta p{opacity:.85;margin-top:6px}
'''
mission_li="".join(f'<li><span class="n">{bn(i+1)}</span><p>{g}</p></li>' for i,g in enumerate(goals))
short_cards="".join(f'<article class="card"><span class="n">{bn(i+1)}</span><p>{g}</p></article>' for i,g in enumerate(short))
long_li="".join(f'<li data-cat="{LCAT[i+1]}"><span class="n">{bn(i+1)}</span><div><p>{g}</p><span class="tag">{CATS[LCAT[i+1]]}</span></div></li>' for i,g in enumerate(long_))
counts={k:sum(1 for v in LCAT.values() if v==k) for k in CATS}
chips='<button class="chip" type="button" data-f="all" aria-pressed="true">সবগুলো <i>২৩</i></button>'+"".join(f'<button class="chip" type="button" data-f="{k}" aria-pressed="false">{v} <i>{bn(counts[k])}</i></button>' for k,v in CATS.items())
OBJ = header("objectives") + f'''
<main>
<section class="hero"><div class="wrap">
 <div><nav class="crumbs" aria-label="অবস্থান"><a href="index.html">হোম</a><span aria-hidden="true">/</span><span>লক্ষ্য ও উদ্দেশ্য</span></nav>
  <h1>লক্ষ্য ও উদ্দেশ্য</h1>
  <p class="lede">{closing}</p>
  <div class="jump"><a href="#mission"><b>৮</b><span>মূল লক্ষ্য</span></a><a href="#short"><b>৬</b><span>স্বল্পমেয়াদী</span></a><a href="#long"><b>২৩</b><span>দীর্ঘমেয়াদী</span></a></div></div>
 <div class="hero-art poster">{art.torch_svg()}</div>
</div></section>
<section class="mission" id="mission"><div class="wrap">
 <div class="sec-head"><h2>আটটি মূল লক্ষ্য</h2></div>
 <ol>{mission_li}</ol>
</div></section>
<section class="short" id="short"><div class="wrap">
 <div class="sec-head"><h2>স্বল্পমেয়াদী উদ্দেশ্য</h2><p class="intro">এ সংগঠনের উদ্দেশ্য বিস্তৃতভাবে বর্ণিত হয়েছে। সংক্ষেপে এ সংগঠনের কয়েকটি মৌলিক লক্ষ্য ও উদ্দেশ্য নিচে বর্ণিত হলো:</p></div>
 <div class="cards">{short_cards}</div>
</div></section>
<section class="long" id="long"><div class="wrap">
 <div class="sec-head"><h2>দীর্ঘমেয়াদী উদ্দেশ্য</h2></div>
 <div class="chips" role="group" aria-label="বিষয় অনুযায়ী দেখুন">{chips}</div>
 <p class="count-line" id="count" aria-live="polite">২৩টি উদ্দেশ্য দেখানো হচ্ছে</p>
 <ol class="long-list">{long_li}</ol>
</div></section>
<section class="cta" style="padding-block:0"><div class="wrap">
 <div><h2>এই অঙ্গীকারে আপনিও যুক্ত হোন</h2><p>বীর মুক্তিযোদ্ধার সন্তান ও প্রজন্মের জন্য সদস্যপদ উন্মুক্ত।</p></div>
 <a class="btn btn-red" href="join.html">সদস্য আবেদন করুন</a>
</div></section>
</main>''' + FOOTER
OBJ_JS = '''
const BN="০১২৩৪৫৬৭৮৯", bn=n=>String(n).replace(/\\d/g,d=>BN[d]);
const chips=[...document.querySelectorAll('.chip')], rows=[...document.querySelectorAll('.long-list li')], count=document.getElementById('count');
chips.forEach(c=>c.addEventListener('click',()=>{
  const f=c.dataset.f; chips.forEach(x=>x.setAttribute('aria-pressed',x===c));
  let n=0; rows.forEach(r=>{const on=f==='all'||r.dataset.cat===f; r.hidden=!on; if(on)n++;});
  count.textContent=bn(n)+'টি উদ্দেশ্য দেখানো হচ্ছে';
}));
'''

# ---------------- JOIN
policy_md=open(sys.argv[3]).read()
pol_html=""
for blk in re.findall(r'## (.*?)\n(.*?)(?=\n## |\Z)', policy_md, re.S):
    lis="".join(f"<li>{l[2:].strip()}</li>" for l in blk[1].strip().split('\n') if l.startswith('- '))
    pol_html+=f"<h4>{blk[0]}</h4><ul>{lis}</ul>"
DIVS=["ঢাকা","চট্টগ্রাম","রাজশাহী","খুলনা","বরিশাল","সিলেট","রংপুর","ময়মনসিংহ"]
JOIN_CSS='''
.hero .wrap{padding-block:44px 52px;display:grid;gap:14px}
.hero h1{font-size:clamp(42px,6vw,80px);font-weight:800;font-stretch:76%;line-height:1.04}
.hero .lede{font-size:19px;max-width:40em;opacity:.95}
.draft{display:inline-flex;gap:10px;align-items:center;margin-top:8px;font:600 14px/1.4 var(--f-body);background:rgba(0,0,0,.2);padding:10px 14px;max-width:max-content}
.draft::before{content:"";width:10px;height:10px;border-radius:50%;background:#FFD35C;flex:none}
.layout{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:48px;align-items:start;padding-block:56px 96px}
@media (max-width:980px){.layout{grid-template-columns:1fr}.aside{order:-1}}
form{display:grid;gap:28px}
fieldset{border:2px solid var(--ink);background:var(--field);padding:28px 28px 32px;margin:0;min-width:0;display:grid;gap:20px;box-shadow:8px 8px 0 var(--green)}
legend{display:flex;align-items:center;gap:12px;padding:0 10px;margin-left:-10px;font:800 26px/1.2 var(--f-display);font-stretch:82%}
legend b{display:inline-grid;place-items:center;width:42px;height:42px;background:var(--green);color:#fff;font-size:26px}
.hint{font-size:15px;color:var(--ink-soft);margin-top:-10px}
.row{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px 20px}
.row.three{grid-template-columns:repeat(3,minmax(0,1fr))}
@media (max-width:640px){.row,.row.three{grid-template-columns:1fr}fieldset{padding:22px 18px 24px;box-shadow:5px 5px 0 var(--green)}}
.f{display:grid;gap:7px;min-width:0}
.f.full{grid-column:1/-1}
label,.lbl{font:600 15.5px/1.3 var(--f-body)}
.req{color:var(--red);margin-left:3px}
.opt{font-weight:400;color:var(--ink-soft);font-size:13.5px;margin-left:6px}
input[type=text],input[type=tel],input[type=email],input[type=date],select,textarea{
  font:400 16px/1.4 var(--f-body);color:var(--ink);background:var(--paper);border:2px solid var(--ink);border-radius:0;padding:12px 14px;width:100%;min-width:0}
textarea{min-height:96px;resize:vertical}
input:focus,select:focus,textarea:focus{outline:none;border-color:var(--red);box-shadow:0 0 0 3px color-mix(in srgb,var(--red) 30%,transparent)}
.f.bad input,.f.bad select{border-color:var(--red)}
.err{display:none;font-size:13.5px;color:var(--red);font-weight:600}
.f.bad .err{display:block}
.seg{display:flex;flex-wrap:wrap;gap:8px}
.seg label{position:relative;font-weight:500}
.seg input{position:absolute;opacity:0;inset:0;cursor:pointer}
.seg span{display:inline-block;padding:11px 16px;border:2px solid var(--ink);background:var(--paper)}
.seg input:checked+span{background:var(--ink);color:var(--paper)}
.seg input:focus-visible+span{outline:3px solid var(--red);outline-offset:2px}
.drop-f{position:relative;border:2px dashed var(--ink);background:var(--paper);padding:18px;display:grid;gap:4px;text-align:center;cursor:pointer}
.drop-f:hover{border-color:var(--red)}
.drop-f input{position:absolute;inset:0;opacity:0;cursor:pointer}
.drop-f b{font:700 16px/1.3 var(--f-display)}
.drop-f small{font-size:13.5px;color:var(--ink-soft)}
.drop-f.has{border-style:solid;border-color:var(--green);background:color-mix(in srgb,var(--green) 10%,var(--paper))}
.drop-f .fname{font-size:14px;color:var(--green);font-weight:600;word-break:break-all}
.fhint{font-size:14px;line-height:1.5;color:var(--ink-soft)}
.sub{font:700 17px/1.3 var(--f-display);color:var(--green);margin:6px 0 -6px}
[data-when][hidden]{display:none}
.check{display:grid;grid-template-columns:24px minmax(0,1fr);gap:12px;align-items:start;font:500 16px/1.6 var(--f-body)}
.check input{width:22px;height:22px;margin:3px 0 0;accent-color:var(--red)}
details.policy{border:2px solid var(--ink);background:var(--paper)}
details.policy summary{cursor:pointer;padding:14px 16px;font:700 17px/1.3 var(--f-display);display:flex;justify-content:space-between;gap:12px}
details.policy summary::after{content:"+";font-size:22px;line-height:1}
details.policy[open] summary::after{content:"−"}
.pol{padding:4px 20px 18px;max-height:380px;overflow:auto;border-top:1px solid var(--rule)}
.pol h4{font-size:17px;margin:16px 0 6px;color:var(--red)}
.pol ul{margin:0;padding-left:20px;font-size:15px;line-height:1.75}
.submit-row{display:flex;flex-wrap:wrap;gap:16px;align-items:center}
.submit-row .btn{font-size:18px;padding:16px 28px}
.submit-row p{font-size:14px;color:var(--ink-soft);max-width:30em}
.aside{display:grid;gap:22px;position:sticky;top:calc(env(safe-area-inset-top,0px) + 92px)}
@media (max-width:980px){.aside{position:static}}
.tree{background:#EFE8DA;border:2px solid var(--ink)}
.tree svg{display:block;width:100%;height:auto}
.box{border:2px solid var(--ink);padding:20px 22px;background:var(--field)}
.box h2{font-size:20px;margin-bottom:12px}
.prog{list-style:none;margin:0;padding:0;display:grid;gap:4px}
.prog li{display:grid;grid-template-columns:30px minmax(0,1fr);gap:10px;align-items:center;font:500 15px/1.4 var(--f-body);padding:6px 0}
.prog i{width:26px;height:26px;display:grid;place-items:center;border:2px solid var(--ink);font:700 14px/1 var(--f-display);font-style:normal}
.prog li.done i{background:var(--green);border-color:var(--green);color:#fff}
.prog li.done i::before{content:"✓"}
.prog li.done i span{display:none}
.prog a{text-decoration:none}.prog a:hover{text-decoration:underline}
.boxnote{font-size:14.5px;color:var(--ink-soft);margin-bottom:8px}
.need{margin:0;padding-left:20px;font-size:15px;line-height:1.8}
@media (max-width:980px){.aside .tree{display:none}}
@media (max-width:640px){.aside{grid-template-columns:1fr}}
.done-panel{border:2px solid var(--ink);background:var(--field);padding:40px 32px;display:grid;gap:16px;justify-items:start;box-shadow:8px 8px 0 var(--green)}
.done-panel h2{font-size:clamp(30px,4vw,44px);font-weight:800;font-stretch:80%;color:var(--green)}
.done-panel .note{background:var(--paper-2);padding:12px 14px;font-size:15px}
'''
def fld(id, label, typ="text", req=True, ph="", full=False, opt=None, err="এই তথ্যটি দিন", extra="", hint=""):
    r = ' required' if req else ''
    lab = f'<label for="{id}">{label}{"<span class=req aria-hidden=true>*</span>" if req else "<span class=opt>(ঐচ্ছিক)</span>"}</label>'
    if typ=="select":
        o='<option value="">বাছাই করুন</option>'+"".join(f'<option>{x}</option>' for x in opt)
        ctl=f'<select id="{id}" name="{id}"{r}>{o}</select>'
    elif typ=="textarea":
        ctl=f'<textarea id="{id}" name="{id}" placeholder="{ph}"{r}></textarea>'
    else:
        ctl=f'<input id="{id}" name="{id}" type="{typ}" autocomplete="{ {"name_bn":"name","name_en":"name","phone":"tel","email":"email","address":"street-address","dob":"bday","job":"organization-title"}.get(id,"off") }" placeholder="{ph}"{r}{extra}>'
    h = f'<span class="fhint">{hint}</span>' if hint else ''
    return f'<div class="f{" full" if full else ""}">{lab}{ctl}{h}<span class="err">{err}</span></div>'
def upload(id,label,hint,req=True):
    return (f'<div class="f"><span class="lbl" id="{id}-l">{label}{"<span class=req aria-hidden=true>*</span>" if req else "<span class=opt>(ঐচ্ছিক)</span>"}</span>'
            f'<label class="drop-f" for="{id}"><input id="{id}" name="{id}" type="file" accept="image/*,.pdf" aria-labelledby="{id}-l"{" required" if req else ""}>'
            f'<b>ফাইল বাছাই করুন</b><small>{hint}</small><span class="fname"></span></label><span class="err">ফাইলটি যুক্ত করুন</span></div>')
BLOOD=["এ+ (A+)","এ− (A−)","বি+ (B+)","বি− (B−)","এবি+ (AB+)","এবি− (AB−)","ও+ (O+)","ও− (O−)"]
def seg(name,label,items,req=True,full=False,default=None):
    star = "<span class=req aria-hidden=true>*</span>" if req else "<span class=opt>(ঐচ্ছিক)</span>"
    opts = "".join(f'<label><input type="radio" name="{name}" value="{x}"{" required" if req and i==0 else ""}{" checked" if x==default else ""}><span>{x}</span></label>' for i,x in enumerate(items))
    return (f'<div class="f{" full" if full else ""}"><span class="lbl" id="{name}-l">{label}{star}</span>'
            f'<div class="seg" role="radiogroup" aria-labelledby="{name}-l">{opts}</div><span class="err">একটি বাছাই করুন</span></div>')
JOIN = header("join") + f'''
<main>
<section class="hero"><div class="wrap">
 <nav class="crumbs" aria-label="অবস্থান"><a href="index.html">হোম</a><span aria-hidden="true">/</span><span>সদস্য হোন</span></nav>
 <h1>সদস্য আবেদন ফর্ম</h1>
 <p class="lede">শুধুমাত্র বীর মুক্তিযোদ্ধার সন্তান ও প্রজন্ম এই কাউন্সিলের সদস্য হতে পারবেন। সকল সদস্যকে তাদের প্রকৃত পরিচয়ে আবেদন করতে হবে।</p>
 <p class="draft">নকশার নমুনা: এই ফর্মটি এখনো কোথাও তথ্য পাঠায় না।</p>
</div></section>
<div class="wrap layout">
 <div>
 <form id="joinForm" novalidate>
  <fieldset id="s1"><legend><b>ক</b>ব্যক্তিগত তথ্য</legend>
   <div class="row">
    {fld("name_bn","পূর্ণ নাম (বাংলায়)",ph="যেমন: মোঃ রফিকুল ইসলাম",hint="এনআইডি বা পাসপোর্ট অনুযায়ী")}
    {fld("name_en","পূর্ণ নাম (ইংরেজিতে)",ph="e.g. Md. Rafiqul Islam",hint="এনআইডি বা পাসপোর্ট অনুযায়ী")}
    {fld("dob","জন্ম তারিখ","date")}
    {fld("job","পেশা ও পদবি",req=False,ph="যেমন: শিক্ষক, সহকারী প্রধান শিক্ষক")}
    {seg("gender","লিঙ্গ",["পুরুষ","নারী","অন্যান্য"],req=False)}
    {fld("blood","রক্তের গ্রুপ","select",opt=BLOOD,err="রক্তের গ্রুপ বাছাই করুন")}
    {fld("workplace","কর্মস্থল / প্রতিষ্ঠান",req=False,ph="প্রতিষ্ঠানের নাম",full=True)}
    {seg("location","বর্তমান অবস্থান",["বাংলাদেশে","প্রবাসে (দেশের বাইরে)"],full=True,default="বাংলাদেশে")}
   </div>
   {upload("photo","পাসপোর্ট সাইজ ছবি","পরিচয়পত্র ও সদস্য তালিকার জন্য। JPG বা PNG, সর্বোচ্চ ১০ MB।",req=False)}
  </fieldset>
  <fieldset id="s2"><legend><b>খ</b>বীর মুক্তিযোদ্ধা পিতা বা মাতার তথ্য</legend>
   <div class="row">
    {seg("relation","সম্পর্ক",["বীর মুক্তিযোদ্ধা পিতা","বীর মুক্তিযোদ্ধা মাতা"])}
    {seg("ff_status","বীর মুক্তিযোদ্ধার বর্তমান অবস্থা",["জীবিত","প্রয়াত"])}
    {fld("ff_name","বীর মুক্তিযোদ্ধার পূর্ণ নাম",ph="পূর্ণ নাম")}
    {fld("gazette","বীর মুক্তিযোদ্ধা সনদ নম্বর / গেজেট নম্বর",ph="সনদ বা গেজেটের নম্বর",hint="মূল সনদ বা গেজেট অনুযায়ী নির্ভুল নম্বর")}
   </div>
   {upload("doc_cert","বীর মুক্তিযোদ্ধা সনদ / গেজেট / পরিচয়পত্রের কপি","PDF বা JPG, প্রতিটি ফাইল সর্বোচ্চ ১০ MB।")}
  </fieldset>
  <fieldset id="s3"><legend><b>গ</b>জাতীয় পরিচয় ও যোগাযোগের তথ্য</legend>
   <div class="row">
    {seg("id_type","পরিচয়পত্রের ধরন",["জাতীয় পরিচয়পত্র (NID)","পাসপোর্ট","জন্ম নিবন্ধন"])}
    {fld("nid","পরিচয়পত্রের নম্বর",ph="নম্বরটি লিখুন",hint="প্রবাসে থাকলে এবং NID না থাকলে পাসপোর্ট বা জন্ম নিবন্ধন নম্বর দিন")}
   </div>
   {upload("doc_nid","NID / পাসপোর্টের কপি","পরিচয় নিশ্চিত করার জন্য। PDF বা JPG, সর্বোচ্চ ১০ MB।")}
   <div class="row">
    {fld("phone","মোবাইল / হোয়াটসঅ্যাপ নম্বর","tel",ph="+8801XXXXXXXXX",extra=' inputmode="tel"',err="কান্ট্রি কোডসহ সঠিক নম্বর দিন",hint="কান্ট্রি কোডসহ লিখুন (যেমন: +880…), প্রবাসে থাকলে সে দেশের কোড দিন")}
    {fld("email","ইমেইল অ্যাড্রেস","email",ph="name@example.com",hint="আপডেট ও কনফার্মেশন পাঠানোর জন্য")}
   </div>
  </fieldset>
  <fieldset id="s4"><legend><b>ঘ</b>ঠিকানা</legend>
   <p class="sub">স্থায়ী ঠিকানা (বাংলাদেশ)</p>
   <div class="row three">
    {fld("division","বিভাগ","select",opt=DIVS,err="বিভাগ বাছাই করুন")}
    {fld("district","জেলা",ph="জেলার নাম")}
    {fld("upazila","উপজেলা / থানা",ph="উপজেলা বা থানা")}
   </div>
   <div class="row">
    {fld("village","গ্রাম / মহল্লা",ph="গ্রাম বা মহল্লার নাম")}
    {fld("postcode","পোস্ট কোড",ph="যেমন: ৩৫০০")}
   </div>
   <p class="sub">বর্তমান ঠিকানা</p>
   <div data-when="বাংলাদেশে">{fld("address","বাড়ি, রাস্তা ও এলাকা","textarea",ph="উপজেলা ও জেলাসহ লিখুন")}</div>
   <div class="row" data-when="প্রবাসে (দেশের বাইরে)" hidden>
    {fld("abroad_city","শহর",ph="শহরের নাম")}
    {fld("abroad_country","দেশ",ph="দেশের নাম")}
   </div>
  </fieldset>
  <fieldset id="s5"><legend><b>ঙ</b>ঘোষণা ও সম্মতি</legend>
   <div class="f"><label class="check"><input type="checkbox" id="agree1" required><span>আমি এই মর্মে ঘোষণা করছি যে, প্রদত্ত সকল তথ্য সঠিক ও সত্য। তথ্য মিথ্যা প্রমাণিত হলে আমার সদস্যপদ বাতিল বলে গণ্য হবে।</span></label><span class="err">ঘোষণায় সম্মতি দিন</span></div>
   <details class="policy" id="policy"><summary>সংগঠনের নিয়মাবলি পড়ুন</summary><div class="pol">{pol_html}</div></details>
   <div class="f"><label class="check"><input type="checkbox" id="agree2" required><span>আমি সংগঠনের নিয়মাবলি ও গোপনীয়তা নীতিমালায় সম্মতি দিচ্ছি।</span></label><span class="err">নিয়মাবলিতে সম্মতি দিন</span></div>
   <div class="submit-row"><button class="btn btn-green" type="submit">আবেদন জমা দিন</button><p>জমা দেওয়ার পর অ্যাডমিন তথ্য যাচাই করে আপনার মোবাইল বা হোয়াটসঅ্যাপ নম্বরে যোগাযোগ করবেন।</p></div>
  </fieldset>
 </form>
 <div class="done-panel" id="done" hidden tabindex="-1">
  <h2>আপনার আবেদন প্রস্তুত</h2>
  <p>সব প্রয়োজনীয় তথ্য সঠিকভাবে পূরণ হয়েছে। চালু সাইটে এই ধাপে আবেদনটি অ্যাডমিনের কাছে যাচাইয়ের জন্য যাবে।</p>
  <p class="note">নকশার নমুনা: কোনো তথ্য কোথাও পাঠানো বা সংরক্ষণ করা হয়নি।</p>
  <button class="btn btn-red" type="button" id="again">ফর্মে ফিরে যান</button>
 </div>
 </div>
 <aside class="aside" aria-label="আবেদনের সহায়িকা">
  <div class="tree poster">{art.banyan_svg()}</div>
  <div class="box"><h2>শুরু করার আগে হাতের কাছে রাখুন</h2><p class="boxnote">ফর্মে এই কাগজগুলোর ছবি বা PDF যুক্ত করতে হবে, প্রতিটি সর্বোচ্চ ১০ MB:</p><ul class="need"><li>আপনার পাসপোর্ট সাইজ ছবি</li><li>বীর মুক্তিযোদ্ধা সনদ, গেজেট বা পরিচয়পত্রের কপি</li><li>আপনার NID বা পাসপোর্টের কপি</li></ul></div>
 </aside>
</div>
</main>''' + FOOTER
JOIN_JS = r'''
const form=document.getElementById('joinForm'), done=document.getElementById('done');
const fs=[...form.querySelectorAll('fieldset')];
function okField(f){if(f.closest('[hidden]')) return true; const els=[...f.querySelectorAll('input,select,textarea')].filter(e=>e.required);
  if(!els.length) return true;
  if(els[0].type==='radio'){return !!f.querySelector('input[type=radio]:checked');}
  return els.every(e=>{ if(e.id==='phone') return /^\+?[০-৯0-9][০-৯0-9 -]{7,16}$/.test(e.value.trim()); return e.type==='checkbox'?e.checked:e.value.trim()!==''; });}
function progress(){}
form.addEventListener('input',e=>{const f=e.target.closest('.f'); if(f&&f.classList.contains('bad')&&okField(f)) f.classList.remove('bad'); progress();});
form.addEventListener('change',e=>{if(e.target.name==='location'){form.querySelectorAll('[data-when]').forEach(w=>{w.hidden=w.dataset.when!==e.target.value;});}
  if(e.target.type==='file'){const d=e.target.closest('.drop-f');const n=e.target.files[0];
  d.classList.toggle('has',!!n); d.querySelector('.fname').textContent=n?n.name:''; d.querySelector('b').textContent=n?'ফাইল যুক্ত হয়েছে':'ফাইল বাছাই করুন';} progress();});
form.addEventListener('submit',e=>{e.preventDefault(); let first=null;
  form.querySelectorAll('.f').forEach(f=>{const ok=okField(f); f.classList.toggle('bad',!ok); if(!ok&&!first) first=f;});
  if(first){first.scrollIntoView({behavior:'smooth',block:'center'}); const c=first.querySelector('input,select,textarea'); c&&c.focus({preventScroll:true}); return;}
  form.hidden=true; done.hidden=false; done.focus(); done.scrollIntoView({behavior:'smooth',block:'start'});});
document.getElementById('again').addEventListener('click',()=>{done.hidden=true;form.hidden=false;form.scrollIntoView({block:'start'});});
'''
open(f"{OUT}/home-concept.html","w").write(page("BMPC Home Concept", HOME_CSS, HOME, False, fname="index.html"))
open(f"{OUT}/objectives.html","w").write(page("লক্ষ্য ও উদ্দেশ্য · BMPC", OBJ_CSS, OBJ, True, OBJ_JS, fname="objectives.html"))
open(f"{OUT}/join.html","w").write(page("সদস্য আবেদন · BMPC", JOIN_CSS, JOIN, True, JOIN_JS, fname="join.html"))
CONTENT=os.path.dirname(sys.argv[2])
for fname,key,title,fn in [("about","about","",lambda:pages2.about(CONTENT)),
  ("manifesto","manifesto","",lambda:pages2.manifesto(CONTENT)),
  ("constitution","constitution","",lambda:pages2.constitution(CONTENT)),
  ("chairman","chairman","",lambda:pages2.message(CONTENT,"message-chairman.md",("message-secretary.md","secretary.html"))),
  ("secretary","secretary","",lambda:pages2.message(CONTENT,"message-secretary.md",("message-chairman.md","chairman.html"))),
  ("news","news","",lambda:pages2.news_list(CONTENT))]:
    css,b=fn(); open(f"{OUT}/{fname}.html","w").write(page(title,css,header(key)+"<main>"+b+"</main>"+FOOTER,True,fname=fname+".html"))
for item in pages2.news_items(CONTENT):
    seo.news_entry(item); css,b=pages2.news_post(item)
    open(f"{OUT}/{item['slug']}","w").write(page("",css,header("news")+"<main>"+b+"</main>"+FOOTER,True,fname=item["slug"],news=item))
latest=pages2.news_items(CONTENT)[0]["slug"]
open(f"{OUT}/news-post.html","w").write(f'<!doctype html><html lang="bn"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0; url={latest}"><link rel="canonical" href="{latest}"><title>সংবাদ</title></head><body><a href="{latest}">সংবাদ পড়ুন</a></body></html>')
import shutil; shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)),"site.css"), f"{OUT}/site.css"); shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)),"motion.js"), f"{OUT}/motion.js")
print("built")
