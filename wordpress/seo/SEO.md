# SEO setup for bmpc.bd (WordPress + Divi)

This folder holds the SEO built into the design preview, ready to copy to the live site:

| File | What it is |
|---|---|
| `pages.md` | SEO title, meta description, slug and schema type for every page |
| `schema/*.json` | The schema.org JSON-LD graph for each page (Organization, WebSite, WebPage, BreadcrumbList, Person, NewsArticle) |
| `schema/_organization-and-people.json` | The council and its two office-bearers on their own, for site-wide use |

Regenerate after changing `design/src/seo.py` or adding news:
`python3 design/src/wp_seo.py`

## 1. Plugin: Rank Math (free)
Install **Rank Math SEO** (free). It covers what Divi doesn't: titles, descriptions, Open Graph previews for
Facebook and WhatsApp, XML sitemap, breadcrumbs and Article schema for news posts.

- **Titles & Meta → Global:** separator `|`, site title `BMPC`.
- **Titles & Meta → Local SEO / Knowledge Graph:** type **Organization**. Name `বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিল`,
  alternate name `BMPC`, logo = `design/img/logo-full.jpg` (628×628, the clean logo), plus the Facebook, X and Instagram links.
- **Sitemap Settings:** on. Include Pages and Posts. Exclude Media attachments.
- **General → Breadcrumbs:** on.
- **Posts (news):** schema type **News Article**.
- **Settings → Reading:** make sure "Discourage search engines" is **off** on the live site.

## 2. Per page
For each page in `pages.md`: open the page → Rank Math box → **Edit Snippet**, then paste the title and description.
Keep the slugs in the table, or update `PAGES` in `design/src/seo.py` to match the slugs bmpc.bd already uses
(changing live slugs needs 301 redirects, which Rank Math → Redirections can do).

## 3. Leader pages (Person schema)
Rank Math free doesn't create Person schema. On **চেয়ারম্যানের বাণী** and **মহাসচিবের বাণী**, add a Divi **Code** module
at the bottom with the `Person` part of `schema/chairman.json` / `schema/secretary.json` wrapped in
`<script type="application/ld+json"> … </script>`. Don't paste the Organization/WebSite parts: Rank Math already prints those.

## 4. Images
- **Social preview image:** upload `design/img/og-default.jpg` (1200×630) as Rank Math's default social image.
- **News posts:** give every post a featured image of at least 1200 px wide.
- **Alt text:** write alt text in Bangla that describes the photo, for example "জাতীয় প্রেসক্লাবের সামনে কাউন্সিলের মানববন্ধন".
- **File size:** compress before upload (WebP, under 200 KB), or use a plugin such as Converter for Media.
- The image URLs in `schema/*.json` assume `wp-content/uploads/<file>`. Replace them with the real media URLs.

## 5. After launch
- Add bmpc.bd to **Google Search Console**, submit `https://bmpc.bd/sitemap_index.xml`, and request indexing of the home page.
- Test a few pages with Google's **Rich Results Test** and the **Schema Markup Validator**.
- Test a news link in Facebook's **Sharing Debugger** so the preview picture appears.

## What the design preview already does
- One `<h1>` per page and a clean heading order, Bangla `lang="bn"`, and descriptive Bangla alt text on every photo.
- Canonical URL pointing at bmpc.bd, Open Graph and Twitter card tags, theme colour and icon.
- JSON-LD schema on every page, matching `schema/`.
- Responsive layout from 320 px phones up to 2560 px screens. Width, height and lazy loading are set on images to keep layout stable.
- The GitHub Pages preview is set to `noindex` and `robots.txt: Disallow`, so it never competes with bmpc.bd in search.
