# Design concept

- `home-concept.html`, `objectives.html`, `join.html`, `site.css`: static design reference for rebuilding in Divi.
- Generated from `src/` (illustrations are SVG built in `src/art.py`). Rebuild from the repo root:

```bash
python3 src/build.py design content/objectives.md content/membership-policy.md
```
(run as `python3 design/src/build.py design content/objectives.md content/membership-policy.md`)
