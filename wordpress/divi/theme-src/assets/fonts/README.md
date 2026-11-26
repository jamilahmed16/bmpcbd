# Fonts

Self-hosted so pages don't wait on two extra connections to Google Fonts.

| File | Family | Source | License |
|---|---|---|---|
| `anek-bangla-*.woff2` | Anek Bangla (variable, trimmed to weight 600–800, width 75–100%) | Google Fonts | SIL Open Font License 1.1 |
| `hind-siliguri-*.woff2` | Hind Siliguri 400 / 500 / 600 (hinting removed) | Google Fonts | SIL Open Font License 1.1 |
| `galada-*.woff2` | Galada (hinting removed) | Google Fonts | SIL Open Font License 1.1 |

Each family comes as a Bengali and a Latin file; `assets/css/fonts.css` uses `unicode-range` so a page only
downloads the files its text needs. Trimmed with fontTools (`varLib.instancer`, `subset`).
