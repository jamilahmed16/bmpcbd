# Adding news

One Markdown file per news post, named `YYYY-MM-DD-short-english-slug.md`. The newest date shows first.

```
---
title: সংবাদের শিরোনাম
date: 2026-11-15
author: BMPC Editor
category: সর্বশেষ
image: design/img/my-photo.jpg
alt: ছবির বর্ণনা (বাংলায়)
place: স্থান (ঐচ্ছিক)
summary: হোম পাতার জন্য এক লাইনের সারাংশ (ঐচ্ছিক)
event: কর্মসূচি · তারিখ · সময় · স্থান   (optional, shows an info strip)
---

প্রথম অনুচ্ছেদ…

দ্বিতীয় অনুচ্ছেদ…

![ছবির বর্ণনা](design/img/photo-2.jpg)
![ছবির বর্ণনা](design/img/photo-3.jpg)
```

Image lines (`![…](…)`) become a photo gallery at the end of the post. Put the image files in `design/img/`.
