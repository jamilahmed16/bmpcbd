# Join form in Fluent Forms: setup

Files in this folder:

| File | What it is |
|---|---|
| `bmpc-join-form-pro.json` | Import file **with** document uploads (needs **Fluent Forms Pro**) |
| `bmpc-join-form-free.json` | Import file **without** uploads (works on free Fluent Forms) |
| `bmpc-fluentforms.css` | Styling that makes the form match the BMPC design |
| `build_form.py` | Regenerates both JSON files (labels, options, policy text) |

> **Pro or free?** File upload is a Fluent Forms **Pro** field. The design asks applicants for the
> freedom fighter certificate/gazette copy, NID and photo, so Pro is recommended. With the free version, import
> the `free` file and collect documents during verification instead.

> **Not yet test-imported.** These files follow Fluent Forms' export format but were built without a WordPress
> install to test against. After importing, open the form once in the editor and check every field. If the import
> fails, use the field list below to build it by hand.

## 1. Import
1. WordPress admin → **Fluent Forms → Tools → Import Forms**.
2. Choose `bmpc-join-form-pro.json` (or `-free`). Leave **"Apply default form style"** unchecked, since our CSS does the styling.
3. Click **Import Forms**. Open the new form **সদস্য আবেদন ফর্ম** and click **Save Form** once.

## 2. Form settings to check (Settings & Integrations)
- **Form Settings → Layout:** Label placement *Top*, CSS class `bmpc-form`.
- **Confirmation:** "Same page, hide form" with the Bangla thank-you message (already set).
- **Email Notifications:** add one to the council's admin email: subject `নতুন সদস্য আবেদন: {inputs.name_bn}`, body `{all_data}`.
- **Spam protection:** Fluent Forms → Global Settings → enable **Turnstile** or **reCAPTCHA**, and keep the honeypot on.
- **Mobile number:** the free version can't check the number pattern. In Pro, change `phone` to the **Phone/Mobile** field with country *Bangladesh*.
- **File uploads (Pro):** Global Settings → File Upload Location. Choose **Fluent Forms default (protected)** so NID and certificates aren't public.

## 3. Approving members
- Applications arrive under **Fluent Forms → Entries**. Use the entry status/notes to mark *verified* or *rejected*.
- Optional (Pro): the **User Registration** integration can create a WordPress account for approved members.

## 4. Put it on the Divi page
1. Create page **সদস্য হোন** (slug `join`).
2. Rebuild the green hero from `design/join.html` with Divi modules.
3. Add a **Code** (or Text) module with the shortcode: `[fluentform id="X"]` (X = the new form's ID in the All Forms list).
4. Paste `bmpc-fluentforms.css` into **Divi → Theme Options → General → Custom CSS**.
5. The right-hand helper column (banyan illustration, "যা হাতের কাছে রাখবেন") can be a second Divi column. Fluent Forms' free version has no progress tracker.

## Field list (for building by hand)
Required fields are marked *.

**১. আবেদনকারীর তথ্য:** পূর্ণ নাম (বাংলায়)* · পূর্ণ নাম (ইংরেজিতে)* · জন্ম তারিখ* (d/m/Y) · লিঙ্গ* (পুরুষ/নারী/অন্যান্য) · NID / জন্ম নিবন্ধন নম্বর* · মোবাইল নম্বর* · ইমেইল · পেশা

**২. বীর মুক্তিযোদ্ধার তথ্য:** বীর মুক্তিযোদ্ধার নাম* · আপনার সম্পর্ক* (সন্তান (পুত্র) / সন্তান (কন্যা) / নাতি / নাতনী / অন্যান্য প্রজন্ম) · বর্তমান অবস্থা* (জীবিত/প্রয়াত) · গেজেট নম্বর* · সনদ নম্বর · যুদ্ধকালীন সেক্টর (অজানা, সেক্টর ১–১১) · নিজ জেলা*

**৩. ঠিকানা:** বিভাগ* (৮টি বিভাগ) · জেলা* · উপজেলা / থানা* · বর্তমান ঠিকানা*

**৪. প্রমাণপত্র (Pro):** সনদ / গেজেটের কপি* · NID / জন্ম নিবন্ধন* · ছবি* · সম্পর্কের প্রমাণ. JPG/PNG/PDF, max 5 MB, up to 2 files each.

**অঙ্গীকার:** নীতিমালা (Custom HTML, collapsible) · নীতিমালায় সম্মতি* · তথ্যের সত্যতা নিশ্চিত*

Submit button: **আবেদন জমা দিন** (green).
