# Launching the BMPC design on bmpc.bd (Divi)

The design is packaged as a **Divi child theme**, `bmpc-child.zip`. It contains:

- **Header and footer**, with the logo, the menu from Appearance → Menus, the mobile menu and the social icons.
- **Design system:** colours, Bangla fonts, the illustrations, the scroll animations, and styling for Fluent Forms.
- **News templates:** the **সর্বশেষ সংবাদ** list (`home.php`) and the single news page (`single.php`). News is written as normal WordPress posts.
- **Appearance → BMPC Setup**, a one-click importer. It creates the 9 pages as Divi Builder pages, the news post, the images in the Media Library, the main menu, the home page setting and the Rank Math titles and descriptions.

Tested on WordPress 6.5 with a stand-in for Divi (Divi itself is licensed, so the real parent theme couldn't be used
in testing). All pages, the menu, the news list, the news post and re-running setup worked, with no PHP errors.
**Test on a staging copy first**, as below.

---

## 0. Before you start
1. **Back up the live site** (files + database). Use your host's backup, or UpdraftPlus.
2. **Use a staging copy.** Most hosts (cPanel, Hostinger, SiteGround and others) have a one-click staging site. Do steps 1–6 there,
   check every page, then repeat on live (or push staging to live).
3. Make sure **Divi is up to date** (Divi → Updates).

## 1. Plugins
- **Fluent Forms** (free): Plugins → Add New → "Fluent Forms" → Install → Activate.
- **Rank Math SEO** (free): install, activate, then run its quick setup wizard.

## 2. Join form
Fluent Forms → Tools → **Import Forms** → choose `wordpress/fluentforms/bmpc-join-form.json` → Import.
Leave "Apply default form style" unticked. The full checklist is in `wordpress/fluentforms/SETUP.md`.

## 3. Install the theme
Appearance → Themes → Add New → **Upload Theme** → choose `bmpc-child.zip` → Install → **Activate**.
Divi must stay installed: it is the parent theme.

## 4. Permalinks
Settings → Permalinks → **Post name** → Save. Pages then get clean addresses such as `/about/`.

## 5. Run BMPC Setup
Appearance → **BMPC Setup** → leave everything ticked → **Run setup**. The log shows each step:

| Creates | Slug |
|---|---|
| হোম (set as the front page) | `/` (`home`) |
| আমাদের সম্পর্কে | `/about/` |
| ঘোষণাপত্র | `/manifesto/` |
| গঠনতন্ত্র | `/constitution/` |
| লক্ষ্য ও উদ্দেশ্য | `/objectives/` |
| চেয়ারম্যানের বাণী | `/chairman-message/` |
| মহাসচিবের বাণী | `/secretary-general-message/` |
| সদস্য হোন (shows the Fluent form) | `/join/` |
| সর্বশেষ সংবাদ (set as the posts page) | `/news/` |
| News: বীর মুক্তিযোদ্ধাদের সম্মান ও অধিকার রক্ষায়… | `/press-club-human-chain/` |
| Menu "BMPC প্রধান মেনু" | assigned to Primary Menu |

**Existing pages are never changed unless you tick "Overwrite".** If bmpc.bd already has a page with one of these
slugs, setup skips it and says so. To replace the old page with the new design, tick Overwrite and run again. The old
version is kept under that page's Revisions.

On the same screen, paste the **Facebook / X / Instagram** links for the footer icons and click **Save social links**.

## 5b. Divi 5: convert the new pages
bmpc.bd runs **Divi 5**. The setup writes the pages in Divi's classic module format, which Divi 5 runs in compatibility mode
(they display correctly, but Divi may show an orange notice in the admin bar). To convert them to native Divi 5:

1. Divi → **Divi 5 Migrator**. Step 1 should now list the new pages under "Modules Ready to be Converted".
2. Click **Migrate to Divi 5**. The migrator keeps a backup of each page's old content and can roll back.
3. Open the home page and one inner page to check, then purge the cache.

## 6. Check Divi settings
- **Divi → Theme Builder:** there must be **no custom Global Header or Footer** assigned. The theme draws its own.
  If one exists, remove it from the Default Website Template.
- **Divi → Theme Options → General:** leave "Static CSS File Generation" on. After any change, clear it with **Divi → Theme Options → Builder → Advanced → Clear**.
- If a caching or speed plugin is installed (LiteSpeed, WP Rocket, Autoptimize and so on), purge its cache after setup.

## 7. Check every page
Open each page on a phone and a computer:
- the header, the menu dropdowns and the mobile menu
- the home banner animation
- the "সর্বশেষ সংবাদ" card on the home page
- the join form: submit a test entry and check that the admin email arrives
- the news list and the news post

## 8. Old pages and links
The old site's pages (for example the old আমাদের সম্পর্কে or ঘোষণাপত্র pages, if they have different slugs) are **not
deleted**. After checking the new pages:
1. Rank Math → **Redirections**: add a 301 redirect from each old page address to the new one.
2. Then move the old pages to Draft or Trash.
3. Remove the old menu from Appearance → Menus if it's no longer used.

## Editing content later
- **Page text:** open the page → **Enable Visual Builder** → each section is a *Code* module. Edit the text inside it and Save.
  You can also drag sections up or down to reorder them.
- **News:** Posts → Add New. Write the text, set a **Featured image**, and choose the category "সর্বশেষ".
  Optional fields under Custom Fields:
  - `bmpc_place`: the place
  - `bmpc_event`: `কর্মসূচি · তারিখ · সময় · স্থান`, shown as an info strip
  - `bmpc_summary`: the one-line text for the home page card

  The newest post appears on the home page automatically.
- **Menu:** Appearance → Menus → "BMPC প্রধান মেনু". Second-level items become dropdowns.
- **Design changes:** made in `design/src/`, rebuilt with `python3 wordpress/divi/build_theme.py`, then the new zip is
  uploaded (Appearance → Themes → Add New → Upload → "Replace current with uploaded"). Page content isn't touched by a
  theme update; re-run BMPC Setup with Overwrite only if the page layouts changed.

## Undo
Switch back to the Divi theme under Appearance → Themes. The new pages stay as normal Divi pages. You can trash them,
and restore Settings → Reading and the old menu.

## Notes
- **Multisite:** on a multisite network, only the Super Admin should run setup. Normal site admins can't save the SVG illustrations.
- **Schema:** Rank Math adds the organisation, page and article schema. The theme adds Person schema on the two message pages.
- **Images:** the leaders' photos, the welcome banner and the news photo were cut from screenshots. Replace them in the
  Media Library with the original files ("Replace media" plugin, or upload and swap) for sharper images.
