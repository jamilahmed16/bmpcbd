"""SEO meta + schema.org JSON-LD for every page. PROD = the live WordPress site, PREVIEW = GitHub Pages."""
import json, html as H
PROD = "https://bmpc.bd/"
PREVIEW = "https://jamilahmed16.github.io/bmpcbd/"
ORG_NAME = "বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিল"
SUFFIX = " | BMPC"
ORG_ID = PROD + "#organization"; SITE_ID = PROD + "#website"

# file -> (production path, title, description, page schema type, preview og image, crumb label)
PAGES = {
 "index.html": ("", "বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিল (BMPC)",
   "বীর মুক্তিযোদ্ধার সন্তান ও প্রজন্মের অরাজনৈতিক সংগঠন। মুক্তিযুদ্ধের সঠিক ইতিহাস সংরক্ষণ, মুক্তিযোদ্ধা পরিবারের কল্যাণ ও নতুন প্রজন্মকে দেশপ্রেমে উদ্বুদ্ধ করা।",
   "WebPage", "img/og-default.jpg", "হোম"),
 "about.html": ("about/", "আমাদের সম্পর্কে ও সদস্য নীতিমালা" + SUFFIX,
   "বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিলের পরিচিতি ও সদস্য হওয়ার নীতিমালা: সদস্যপদ, ব্যবহারবিধি, পোস্টিং, অনুমোদন ও গোপনীয়তার নিয়ম।",
   "AboutPage", "img/welcome-banner.jpg", "আমাদের সম্পর্কে"),
 "manifesto.html": ("manifesto/", "ঘোষণাপত্র" + SUFFIX,
   "মুক্তিযুদ্ধের চেতনা, সাম্য, মানবাধিকার, মুক্তিযোদ্ধা পরিবারের সম্মান ও জাতীয় ঐক্যের পাঁচ দফা অঙ্গীকার: বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিলের ঘোষণাপত্র।",
   "WebPage", "img/og-default.jpg", "ঘোষণাপত্র"),
 "constitution.html": ("constitution/", "গঠনতন্ত্র" + SUFFIX,
   "বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিলের গঠনতন্ত্র: সাংগঠনিক কাঠামো, সদস্যপদ ও পরিচালনার নিয়মাবলী।",
   "WebPage", "img/og-default.jpg", "গঠনতন্ত্র"),
 "objectives.html": ("objectives/", "লক্ষ্য ও উদ্দেশ্য" + SUFFIX,
   "কাউন্সিলের ৮টি মূল লক্ষ্য, ৬টি স্বল্পমেয়াদী ও ২৩টি দীর্ঘমেয়াদী উদ্দেশ্য: মুক্তিযুদ্ধের ইতিহাস সংরক্ষণ, মুক্তিযোদ্ধা পরিবারের কল্যাণ ও প্রজন্মের উন্নয়ন।",
   "WebPage", "img/og-default.jpg", "লক্ষ্য ও উদ্দেশ্য"),
 "chairman.html": ("chairman-message/", "চেয়ারম্যানের বাণী: রহিমুল ফারুক বাবু" + SUFFIX,
   "বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিলের চেয়ারম্যান রহিমুল ফারুক বাবুর বাণী: দেশ ও প্রবাসের সকল বীর মুক্তিযোদ্ধার সন্তান ও প্রজন্মকে একতাবদ্ধ হওয়ার আহ্বান।",
   "ProfilePage", "img/chairman.jpg", "চেয়ারম্যানের বাণী"),
 "secretary.html": ("secretary-general-message/", "মহাসচিবের বাণী: মোঃ আল আমিন" + SUFFIX,
   "বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিলের মহাসচিব মোঃ আল আমিনের বাণী: প্রশাসনিক স্বচ্ছতা ও মাঠ পর্যায়ের সদস্যদের সাথে কেন্দ্রীয় কাউন্সিলের সেতুবন্ধনের অঙ্গীকার।",
   "ProfilePage", "img/secretary.jpg", "মহাসচিবের বাণী"),
 "news.html": ("news/", "সর্বশেষ সংবাদ" + SUFFIX,
   "বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিলের সর্বশেষ সংবাদ: মানববন্ধন, প্রতিবাদ সমাবেশ, দিবস পালন ও সাংগঠনিক কার্যক্রম।",
   "CollectionPage", "img/og-default.jpg", "সর্বশেষ সংবাদ"),
 "join.html": ("join/", "সদস্য আবেদন ফর্ম" + SUFFIX,
   "বীর মুক্তিযোদ্ধার সন্তান ও প্রজন্মের জন্য বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিলের অনলাইন সদস্য আবেদন ফর্ম।",
   "WebPage", "img/og-default.jpg", "সদস্য হোন"),
}
PARENT = {"manifesto.html": "about.html", "constitution.html": "about.html", "objectives.html": "about.html"}

ORG = {"@type": "NGO", "@id": ORG_ID, "name": ORG_NAME,
       "alternateName": ["BMPC", "Bangladesh Muktijoddha Projonmo Council"],
       "url": PROD, "logo": {"@type": "ImageObject", "url": PROD + "wp-content/uploads/bmpc-logo.png"},
       "description": "মুক্তিযুদ্ধের চেতনা ধারণকারী বীর মুক্তিযোদ্ধার সন্তান ও প্রজন্মের অরাজনৈতিক সংগঠন।",
       "areaServed": {"@type": "Country", "name": "Bangladesh"}, "inLanguage": "bn-BD",
       "member": [{"@id": PROD + "#chairman"}, {"@id": PROD + "#secretary-general"}]}
PEOPLE = {
 "chairman.html": {"@type": "Person", "@id": PROD + "#chairman", "name": "রহিমুল ফারুক বাবু", "jobTitle": "চেয়ারম্যান, কেন্দ্রীয় কাউন্সিল",
                   "worksFor": {"@id": ORG_ID}, "image": PROD + "wp-content/uploads/chairman.jpg"},
 "secretary.html": {"@type": "Person", "@id": PROD + "#secretary-general", "name": "মোঃ আল আমিন", "jobTitle": "মহাসচিব, কেন্দ্রীয় কাউন্সিল",
                    "worksFor": {"@id": ORG_ID}, "image": PROD + "wp-content/uploads/secretary.jpg"},
}
WEBSITE = {"@type": "WebSite", "@id": SITE_ID, "url": PROD, "name": ORG_NAME, "inLanguage": "bn-BD", "publisher": {"@id": ORG_ID},
           "potentialAction": {"@type": "SearchAction", "target": PROD + "?s={search_term_string}", "query-input": "required name=search_term_string"}}

def news_entry(item):
    """Register a news post page so it gets SEO + NewsArticle schema."""
    desc = item["body"][0][:150].rstrip("… ") + "…"
    PAGES[item["slug"]] = ("news/" + item["stem"] + "/", item["title"] + SUFFIX, desc, "WebPage", "img/" + item["image_file"], item["title"])
    PARENT[item["slug"]] = "news.html"
    return item

def graph(fname, news=None):
    path, title, desc, typ, img, label = PAGES[fname]
    url = PROD + path
    crumbs = [("হোম", PROD)]
    if fname != "index.html":
        if fname in PARENT: p = PAGES[PARENT[fname]]; crumbs.append((p[5], PROD + p[0]))
        crumbs.append((label, url))
    g = [ORG, WEBSITE,
         {"@type": typ, "@id": url + "#webpage", "url": url, "name": title, "description": desc, "inLanguage": "bn-BD",
          "isPartOf": {"@id": SITE_ID}, "about": {"@id": ORG_ID}, "breadcrumb": {"@id": url + "#breadcrumb"},
          "primaryImageOfPage": {"@type": "ImageObject", "url": PREVIEW + img}}]
    if len(crumbs) > 1:
        g.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb",
                  "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]})
    else:
        g[2].pop("breadcrumb")
    if fname in PEOPLE:
        g.append(PEOPLE[fname]); g[2]["mainEntity"] = {"@id": PEOPLE[fname]["@id"]}
    if news:
        g.append({"@type": "NewsArticle", "@id": url + "#article", "headline": news["title"], "description": desc,
                  "image": [PREVIEW + img], "datePublished": news["date"] + "T16:00:00+06:00", "dateModified": news["date"] + "T16:00:00+06:00",
                  "author": {"@id": ORG_ID}, "publisher": {"@id": ORG_ID}, "mainEntityOfPage": {"@id": url + "#webpage"},
                  "inLanguage": "bn-BD", "articleSection": news.get("category", "সংবাদ")})
    if fname == "news.html" and news is None:
        pass
    return {"@context": "https://schema.org", "@graph": g}

def head(fname, news=None):
    path, title, desc, typ, img, label = PAGES[fname]
    e = H.escape
    og_type = "article" if news else "website"
    tags = [f'<meta name="description" content="{e(desc)}">',
            f'<link rel="canonical" href="{PROD + path}">',
            '<meta name="theme-color" content="#073D2A">',
            '<link rel="icon" href="img/logo.png" type="image/png">',
            '<link rel="apple-touch-icon" href="img/logo.png">',
            f'<meta property="og:type" content="{og_type}">',
            f'<meta property="og:site_name" content="{ORG_NAME}">',
            '<meta property="og:locale" content="bn_BD">',
            f'<meta property="og:title" content="{e(title)}">',
            f'<meta property="og:description" content="{e(desc)}">',
            f'<meta property="og:url" content="{PREVIEW + (fname if fname != "index.html" else "")}">',
            f'<meta property="og:image" content="{PREVIEW + img}">',
            '<meta name="twitter:card" content="summary_large_image">']
    if news: tags.append(f'<meta property="article:published_time" content="{news["date"]}T16:00:00+06:00">')
    tags.append('<script type="application/ld+json">' + json.dumps(graph(fname, news), ensure_ascii=False) + '</script>')
    return "\n".join(tags)
