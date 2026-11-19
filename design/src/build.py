import sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import art
from art import bn
OUT = sys.argv[1]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
 '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anek+Bangla:wdth,wght@75..100,400..800&family=Galada&family=Hind+Siliguri:wght@400;500;600&display=swap">'
 '<link rel="stylesheet" href="site.css">')
LOGO = '<svg width="46" height="46" viewBox="0 0 46 46" aria-hidden="true"><rect x="1" y="1" width="44" height="44" fill="#0B5B3E" stroke="#FBF3E6" stroke-width="2"/><circle cx="20" cy="23" r="11" fill="#E8362E"/><path d="M7 38h32" stroke="#FBF3E6" stroke-width="2"/></svg>'

def header(cur):
    items=[("index.html","প্রথম পাতা","home"),("index.html#about","আমাদের সম্পর্কে","about"),("objectives.html","লক্ষ্য ও উদ্দেশ্য","objectives"),("index.html#days","কার্যক্রম","days"),("#footer","যোগাযোগ","contact")]
    nav="".join(f'<a href="{h}"{" aria-current=\"page\"" if k==cur else ""}>{t}</a>' for h,t,k in items)
    drop="".join(f'<a href="{h}">{t}</a>' for h,t,k in items)+'<a href="join.html">সদস্য হোন</a>'
    return f'''<header class="top"><div class="wrap">
<a class="brand" href="index.html" aria-label="বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিল, প্রথম পাতা">{LOGO}<span><b>মুক্তিযোদ্ধা প্রজন্ম কাউন্সিল</b><small>বাংলাদেশ · BMPC</small></span></a>
<nav class="nav" aria-label="প্রধান মেনু">{nav}</nav>
<a class="btn btn-paper" href="join.html">সদস্য হোন</a>
<details class="menu"><summary>মেনু</summary><nav class="drop" aria-label="মোবাইল মেনু">{drop}</nav></details>
</div></header>'''

FOOTER = f'''<footer id="footer"><div class="wrap"><div class="cols">
<div><a class="brand" href="index.html">{LOGO}<span><b>বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিল</b></span></a>
<p class="about-f">মুক্তিযুদ্ধের চেতনা ধারণকারী অরাজনৈতিক সংগঠন। বীর মুক্তিযোদ্ধার সন্তান ও প্রজন্মের ঐক্যবদ্ধ প্ল্যাটফর্ম।</p></div>
<div><h4>সংগঠন</h4><ul><li><a href="index.html#about">আমাদের সম্পর্কে</a></li><li><a href="objectives.html">লক্ষ্য ও উদ্দেশ্য</a></li><li><a href="join.html#policy">সদস্য নীতিমালা</a></li></ul></div>
<div><h4>অংশ নিন</h4><ul><li><a href="join.html">সদস্য হোন</a></li><li><a href="index.html#days">কার্যক্রম</a></li><li><a href="#footer">যোগাযোগ (শীঘ্রই)</a></li></ul></div>
</div><div class="legal"><span>© ২০২৬ বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিল</span><span>bmpc.bd</span></div></div></footer>'''

def page(title, css, body, full, script=""):
    head = f'<title>{title}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n{FONTS}\n<style>{css}</style>\n'
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
.goals li{display:grid;grid-template-columns:60px minmax(0,1fr);gap:16px;padding:22px 0;border-top:1px solid rgba(251,243,230,.22)}
.goals .n{font:800 46px/1 var(--f-display);font-stretch:75%}
.goals li p{font-size:16.5px;line-height:1.8;opacity:.93}
.goals .foot{display:flex;flex-wrap:wrap;gap:20px 40px;align-items:center;justify-content:space-between;margin-top:40px}
.goals .closing{font:600 20px/1.6 var(--f-display);max-width:40em;border-left:4px solid var(--on-red);padding-left:18px}
@media (max-width:880px){.goals ol{grid-template-columns:1fr}}
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
 <div><div class="sec-head" style="margin-bottom:24px"><span class="script">আমাদের সম্পর্কে</span><h2>মুক্তিযুদ্ধের চেতনা ধারণকারী অরাজনৈতিক সংগঠন</h2></div>
  <p class="body">আমাদের সংগঠন <strong>অরাজনৈতিক</strong> এবং মুক্তিযুদ্ধের চেতনা ধারণ করে। এখানে আমরা বাংলাদেশের মহান মুক্তিযুদ্ধের ইতিহাস, গৌরবগাঁথা এবং মুক্তিযোদ্ধাদের অবদান সম্পর্কে আলোচনা করে থাকি। নতুন প্রজন্মকে মুক্তিযুদ্ধের <strong>সত্যিকার ইতিহাস</strong> জানানো এবং দেশপ্রেমে উদ্বুদ্ধ করা আমাদের মূল লক্ষ্য।</p>
  <div class="pill-row"><span class="pill">ঐক্য ও সংহতি</span><span class="pill">সঠিক ইতিহাস</span><span class="pill">মুক্তিযোদ্ধা পরিবারের কল্যাণ</span><span class="pill">দুর্নীতিমুক্ত সমাজ</span></div></div>
</div></section>
<section class="goals" id="goals"><div class="wrap">
 <div class="sec-head"><span class="script">লক্ষ্য ও উদ্দেশ্য</span><h2>আটটি অঙ্গীকার</h2></div>
 <ol>{goal_li}</ol>
 <div class="foot"><p class="closing">{closing}</p><a class="btn btn-paper" href="objectives.html">সব উদ্দেশ্য দেখুন</a></div>
</div></section>
<section class="plans"><div class="wrap">
 <div class="sec-head"><span class="script">কর্মপরিকল্পনা</span><h2>আজকের কাজ, আগামীর বাংলাদেশ</h2></div>
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
<section class="days" id="days"><div class="wrap">
 <div class="sec-head"><span class="script">কার্যক্রম</span><h2>যে দিনগুলো আমরা প্রতি বছর পালন করি</h2></div>
 <div class="day-row">
  <article class="day poster">{art.minar_svg()}<p class="date">২১ ফেব্রুয়ারি<small>শহীদ দিবস ও আন্তর্জাতিক মাতৃভাষা দিবস</small></p></article>
  <article class="day poster">{art.sunrise_svg()}<p class="date">২৬ মার্চ<small>স্বাধীনতা দিবস ও সংগঠনের প্রতিষ্ঠা বার্ষিকী</small></p></article>
  <article class="day poster">{art.flag_svg()}<p class="date">১৬ ডিসেম্বর<small>মহান বিজয় দিবস</small></p></article>
 </div>
 <div class="acts"><strong>সারা বছর:</strong><span>বিতর্ক ও কুইজ</span><span>স্বেচ্ছায় রক্তদান</span><span>ত্রাণ বিতরণ</span><span>দুর্নীতি ও মাদকবিরোধী মানববন্ধন</span><span>ঈদ পুনর্মিলনী</span><span>বিনামূল্যে তথ্য সেবা</span></div>
</div></section>
<section class="join" id="join"><div class="wrap">
 <div><span class="script">সদস্যপদ</span><h2>আপনি কি বীর মুক্তিযোদ্ধার সন্তান বা প্রজন্ম?</h2>
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
.mission li{display:grid;grid-template-columns:72px minmax(0,1fr);gap:18px;padding:26px 0;border-top:2px solid var(--ink)}
.mission .n{font:800 58px/.9 var(--f-display);font-stretch:75%;color:var(--red)}
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
.long-list li{display:grid;grid-template-columns:56px minmax(0,1fr);gap:14px;padding:20px 0;border-top:1px solid var(--rule)}
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
 <div><nav class="crumbs" aria-label="অবস্থান"><a href="index.html">প্রথম পাতা</a><span aria-hidden="true">/</span><span>লক্ষ্য ও উদ্দেশ্য</span></nav>
  <h1>লক্ষ্য ও উদ্দেশ্য</h1>
  <p class="lede">{closing}</p>
  <div class="jump"><a href="#mission"><b>৮</b><span>মূল লক্ষ্য</span></a><a href="#short"><b>৬</b><span>স্বল্পমেয়াদী</span></a><a href="#long"><b>২৩</b><span>দীর্ঘমেয়াদী</span></a></div></div>
 <div class="hero-art poster">{art.torch_svg()}</div>
</div></section>
<section class="mission" id="mission"><div class="wrap">
 <div class="sec-head"><span class="script">আমাদের লক্ষ্য</span><h2>আটটি মূল লক্ষ্য</h2></div>
 <ol>{mission_li}</ol>
</div></section>
<section class="short" id="short"><div class="wrap">
 <div class="sec-head"><span class="script">স্বল্পমেয়াদী উদ্দেশ্য</span><h2>এখনই যে কাজগুলো শুরু</h2><p class="intro">এ সংগঠনের উদ্দেশ্য বিস্তৃতভাবে বর্ণিত হয়েছে। সংক্ষেপে এ সংগঠনের কয়েকটি মৌলিক লক্ষ্য ও উদ্দেশ্য নিচে বর্ণিত হলো:</p></div>
 <div class="cards">{short_cards}</div>
</div></section>
<section class="long" id="long"><div class="wrap">
 <div class="sec-head"><span class="script">দীর্ঘমেয়াদী উদ্দেশ্য</span><h2>প্রজন্ম ধরে যে কাজ চলবে</h2></div>
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
.box h3{font-size:20px;margin-bottom:12px}
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
def fld(id, label, typ="text", req=True, ph="", full=False, opt=None, err="এই তথ্যটি দিন", extra=""):
    r = ' required' if req else ''
    lab = f'<label for="{id}">{label}{"<span class=req aria-hidden=true>*</span>" if req else "<span class=opt>(ঐচ্ছিক)</span>"}</label>'
    if typ=="select":
        o='<option value="">বাছাই করুন</option>'+"".join(f'<option>{x}</option>' for x in opt)
        ctl=f'<select id="{id}" name="{id}"{r}>{o}</select>'
    elif typ=="textarea":
        ctl=f'<textarea id="{id}" name="{id}" placeholder="{ph}"{r}></textarea>'
    else:
        ctl=f'<input id="{id}" name="{id}" type="{typ}" placeholder="{ph}"{r}{extra}>'
    return f'<div class="f{" full" if full else ""}">{lab}{ctl}<span class="err">{err}</span></div>'
def upload(id,label,hint,req=True):
    return (f'<div class="f"><span class="lbl" id="{id}-l">{label}{"<span class=req aria-hidden=true>*</span>" if req else "<span class=opt>(ঐচ্ছিক)</span>"}</span>'
            f'<label class="drop-f" for="{id}"><input id="{id}" name="{id}" type="file" accept="image/*,.pdf" aria-labelledby="{id}-l"{" required" if req else ""}>'
            f'<b>ফাইল বাছাই করুন</b><small>{hint}</small><span class="fname"></span></label><span class="err">ফাইলটি যুক্ত করুন</span></div>')
SECTORS=["অজানা"]+[f"সেক্টর {bn(i)}" for i in range(1,12)]
JOIN = header("join") + f'''
<main>
<section class="hero"><div class="wrap">
 <nav class="crumbs" aria-label="অবস্থান"><a href="index.html">প্রথম পাতা</a><span aria-hidden="true">/</span><span>সদস্য হোন</span></nav>
 <h1>সদস্য আবেদন ফর্ম</h1>
 <p class="lede">শুধুমাত্র বীর মুক্তিযোদ্ধার সন্তান ও প্রজন্ম এই কাউন্সিলের সদস্য হতে পারবেন। সকল সদস্যকে তাদের প্রকৃত পরিচয়ে আবেদন করতে হবে।</p>
 <p class="draft">নকশার নমুনা: এই ফর্মটি এখনো কোথাও তথ্য পাঠায় না।</p>
</div></section>
<div class="wrap layout">
 <div>
 <form id="joinForm" novalidate>
  <fieldset id="s1"><legend><b>১</b>আবেদনকারীর তথ্য</legend>
   <div class="row">
    {fld("name_bn","পূর্ণ নাম (বাংলায়)",ph="যেমন: মোঃ রফিকুল ইসলাম")}
    {fld("name_en","পূর্ণ নাম (ইংরেজিতে)",ph="e.g. Md. Rafiqul Islam")}
    {fld("dob","জন্ম তারিখ","date")}
    <div class="f"><span class="lbl" id="g-l">লিঙ্গ<span class="req" aria-hidden="true">*</span></span><div class="seg" role="radiogroup" aria-labelledby="g-l">
     <label><input type="radio" name="gender" value="m" required><span>পুরুষ</span></label><label><input type="radio" name="gender" value="f"><span>নারী</span></label><label><input type="radio" name="gender" value="o"><span>অন্যান্য</span></label></div><span class="err">একটি বাছাই করুন</span></div>
    {fld("nid","জাতীয় পরিচয়পত্র / জন্ম নিবন্ধন নম্বর",ph="১০, ১৩ বা ১৭ সংখ্যার নম্বর",extra=' inputmode="numeric"')}
    {fld("phone","মোবাইল নম্বর","tel",ph="০১XXXXXXXXX",extra=' inputmode="tel"',err="সঠিক মোবাইল নম্বর দিন")}
    {fld("email","ইমেইল","email",req=False,ph="name@example.com")}
    {fld("job","পেশা",req=False,ph="যেমন: শিক্ষক, ব্যবসায়ী, শিক্ষার্থী")}
   </div>
  </fieldset>
  <fieldset id="s2"><legend><b>২</b>বীর মুক্তিযোদ্ধার তথ্য</legend>
   <p class="hint">যে বীর মুক্তিযোদ্ধার প্রজন্ম হিসেবে আবেদন করছেন, তাঁর তথ্য দিন।</p>
   <div class="row">
    {fld("ff_name","বীর মুক্তিযোদ্ধার নাম",ph="পূর্ণ নাম",full=True)}
    {fld("relation","আপনার সম্পর্ক","select",opt=["সন্তান (পুত্র)","সন্তান (কন্যা)","নাতি / নাতনী","অন্যান্য প্রজন্ম"],err="সম্পর্ক বাছাই করুন")}
    <div class="f"><span class="lbl" id="st-l">বর্তমান অবস্থা<span class="req" aria-hidden="true">*</span></span><div class="seg" role="radiogroup" aria-labelledby="st-l">
     <label><input type="radio" name="ff_status" value="alive" required><span>জীবিত</span></label><label><input type="radio" name="ff_status" value="late"><span>প্রয়াত</span></label></div><span class="err">একটি বাছাই করুন</span></div>
    {fld("gazette","গেজেট নম্বর",ph="মুক্তিযোদ্ধা গেজেটের নম্বর")}
    {fld("cert","মুক্তিযোদ্ধা সনদ নম্বর",req=False,ph="যদি থাকে")}
    {fld("sector","যুদ্ধকালীন সেক্টর","select",req=False,opt=SECTORS)}
    {fld("ff_dist","বীর মুক্তিযোদ্ধার নিজ জেলা",ph="যেমন: কুমিল্লা")}
   </div>
  </fieldset>
  <fieldset id="s3"><legend><b>৩</b>ঠিকানা</legend>
   <div class="row three">
    {fld("division","বিভাগ","select",opt=DIVS,err="বিভাগ বাছাই করুন")}
    {fld("district","জেলা",ph="জেলার নাম")}
    {fld("upazila","উপজেলা / থানা",ph="উপজেলা বা থানা")}
   </div>
   {fld("address","বর্তমান ঠিকানা","textarea",ph="বাড়ি নম্বর, রাস্তা, এলাকা")}
  </fieldset>
  <fieldset id="s4"><legend><b>৪</b>অঙ্গীকার</legend>
   <details class="policy" id="policy"><summary>সদস্য হওয়ার নীতিমালা পড়ুন</summary><div class="pol">{pol_html}</div></details>
   <div class="f"><label class="check"><input type="checkbox" id="agree1" required><span>আমি সদস্য হওয়ার নীতিমালা পড়েছি এবং তা মেনে চলব।</span></label><span class="err">নীতিমালায় সম্মতি দিন</span></div>
   <div class="f"><label class="check"><input type="checkbox" id="agree2" required><span>আমি নিশ্চিত করছি যে উপরের সকল তথ্য সত্য এবং আমি একজন বীর মুক্তিযোদ্ধার সন্তান বা প্রজন্ম।</span></label><span class="err">তথ্যের সত্যতা নিশ্চিত করুন</span></div>
   <div class="submit-row"><button class="btn btn-green" type="submit">আবেদন জমা দিন</button><p>জমা দেওয়ার পর অ্যাডমিন তথ্য যাচাই করে আপনার মোবাইল নম্বরে যোগাযোগ করবেন।</p></div>
  </fieldset>
 </form>
 <div class="done-panel" id="done" hidden tabindex="-1">
  <span class="script">ধন্যবাদ</span><h2>আপনার আবেদন প্রস্তুত</h2>
  <p>সব প্রয়োজনীয় তথ্য সঠিকভাবে পূরণ হয়েছে। চালু সাইটে এই ধাপে আবেদনটি অ্যাডমিনের কাছে যাচাইয়ের জন্য যাবে।</p>
  <p class="note">নকশার নমুনা: কোনো তথ্য কোথাও পাঠানো বা সংরক্ষণ করা হয়নি।</p>
  <button class="btn btn-red" type="button" id="again">ফর্মে ফিরে যান</button>
 </div>
 </div>
 <aside class="aside" aria-label="আবেদনের সহায়িকা">
  <div class="tree poster">{art.banyan_svg()}</div>
  <div class="box"><h3>যাচাইয়ের সময় যা লাগবে</h3><p class="boxnote">আবেদন জমার পর অ্যাডমিন যোগাযোগ করে নিচের কাগজপত্রের কপি দেখতে চাইবেন:</p><ul class="need"><li>জাতীয় পরিচয়পত্র বা জন্ম নিবন্ধন</li><li>বীর মুক্তিযোদ্ধার গেজেট ও সনদের কপি</li><li>পাসপোর্ট সাইজের ছবি</li><li>সম্পর্কের প্রমাণপত্র (যদি থাকে)</li></ul></div>
 </aside>
</div>
</main>''' + FOOTER
JOIN_JS = r'''
const form=document.getElementById('joinForm'), done=document.getElementById('done');
const fs=[...form.querySelectorAll('fieldset')];
function okField(f){const els=[...f.querySelectorAll('input,select,textarea')].filter(e=>e.required);
  if(!els.length) return true;
  if(els[0].type==='radio'){return !!f.querySelector('input[type=radio]:checked');}
  return els.every(e=>{ if(e.id==='phone') return /^(০|0)(১|1)[০-৯0-9]{9}$/.test(e.value.trim()); return e.type==='checkbox'?e.checked:e.value.trim()!==''; });}
function progress(){}
form.addEventListener('input',e=>{const f=e.target.closest('.f'); if(f&&f.classList.contains('bad')&&okField(f)) f.classList.remove('bad'); progress();});
form.addEventListener('change',e=>{if(e.target.type==='file'){const d=e.target.closest('.drop-f');const n=e.target.files[0];
  d.classList.toggle('has',!!n); d.querySelector('.fname').textContent=n?n.name:''; d.querySelector('b').textContent=n?'ফাইল যুক্ত হয়েছে':'ফাইল বাছাই করুন';} progress();});
form.addEventListener('submit',e=>{e.preventDefault(); let first=null;
  form.querySelectorAll('.f').forEach(f=>{const ok=okField(f); f.classList.toggle('bad',!ok); if(!ok&&!first) first=f;});
  if(first){first.scrollIntoView({behavior:'smooth',block:'center'}); const c=first.querySelector('input,select,textarea'); c&&c.focus({preventScroll:true}); return;}
  form.hidden=true; done.hidden=false; done.focus(); done.scrollIntoView({behavior:'smooth',block:'start'});});
document.getElementById('again').addEventListener('click',()=>{done.hidden=true;form.hidden=false;form.scrollIntoView({block:'start'});});
'''
open(f"{OUT}/home-concept.html","w").write(page("BMPC Home Concept", HOME_CSS, HOME, False))
open(f"{OUT}/objectives.html","w").write(page("লক্ষ্য ও উদ্দেশ্য · BMPC", OBJ_CSS, OBJ, True, OBJ_JS))
open(f"{OUT}/join.html","w").write(page("সদস্য আবেদন · BMPC", JOIN_CSS, JOIN, True, JOIN_JS))
import shutil; shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)),"site.css"), f"{OUT}/site.css")
print("built")
