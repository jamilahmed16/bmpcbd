# BMPC website — project brief

**Organisation:** বাংলাদেশ মুক্তিযোদ্ধা প্রজন্ম কাউন্সিল (Bangladesh Muktijoddha Projonmo Council, BMPC)
**Live site:** https://bmpc.bd/
**Nature:** Non-political organisation of the children and descendants of Bir Muktijoddhas (1971 Liberation War freedom fighters). Mission: preserve and teach the true history of the Liberation War and inspire the new generation with patriotism.

## Stack
- WordPress, Divi Pro (licensed) as theme/builder
- Novamira — connects Claude Code to the WordPress install
- Impeccable — design-quality guidance for the front end
- Claude Code for building and editing
- Fluent Forms for all forms (join form: `wordpress/fluentforms/`, see SETUP.md there)
- Divi child theme: `wordpress/divi/` (build with `python3 wordpress/divi/build_theme.py`, launch steps in INSTALL.md). Design source of truth is `design/src/`.

## Content rules
- Primary language: Bangla (bn-BD). Keep the client's wording; don't rewrite meaning.
- Source content lives in `content/` as Markdown, one file per page. Treat it as the source of truth before pushing to WordPress.
- Use Bangla numerals in Bangla copy (১, ২, ৩…).
- Tone: respectful, dignified, historical. No party-political language.

## Design direction (to confirm)
- Bangla-first typography (e.g. Hind Siliguri / Noto Sans Bengali / Noto Serif Bengali / Tiro Bangla).
- Palette rooted in the national flag: **bottle green is the primary colour** (header, hero, large bands); red is the accent (sun, numerals, highlights); warm newsprint neutral. Avoid looking like a party or government site.
- Illustration style: 1971 linocut poster, SVG, generated in `design/src/art.py`.
