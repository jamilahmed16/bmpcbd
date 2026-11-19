# Join form in Fluent Forms (free version): setup

| File | What it is |
|---|---|
| `bmpc-join-form.json` | Import file for the membership form (free Fluent Forms) |
| `bmpc-fluentforms.css` | Styling that makes the form match the BMPC design |
| `build_form.py` | Regenerates the JSON (labels, options, policy text) |

**No file uploads.** The free version of Fluent Forms has no upload field, so the form collects details only:
the gazette number, certificate number, NID number and so on. The admin checks the documents (NID or birth
registration, gazette or certificate copy, photo, proof of relationship) when they contact the applicant to
verify them. The thank-you message tells applicants to keep these ready.

> **Not yet test-imported.** The file follows Fluent Forms' export format but was built without a WordPress
> install to test against. After importing, open the form once in the editor and check every field. If the
> import fails, build it by hand from the field list below.

## 1. Import
1. WordPress admin → **Fluent Forms → Tools → Import Forms**.
2. Choose `bmpc-join-form.json`. Leave **"Apply default form style"** unchecked, since our CSS does the styling.
3. Click **Import Forms**, open **সদস্য আবেদন ফর্ম**, and click **Save Form** once.

## 2. Settings to check
- **Settings → Form Settings → Layout:** label placement *Top*, form CSS class `bmpc-form`.
- **Confirmation:** "Same page, hide form" with the Bangla thank-you message (already set).
- **Email Notifications:** add one to the council's admin email. Subject `নতুন সদস্য আবেদন: {inputs.name_bn}`, body `{all_data}`.
- **Spam protection:** Fluent Forms → Global Settings → enable **Cloudflare Turnstile** or **reCAPTCHA** (both free) and keep the honeypot on.

## 3. Approving members
Applications arrive under **Fluent Forms → Entries**. For each one:
1. Call or message the mobile number and check the documents.
2. Mark the entry as read, and add a note: *যাচাই সম্পন্ন* or *বাতিল* with the reason.
3. Add approved members to your member list.

The free version can't create WordPress accounts automatically. Do that by hand under Users → Add New, if members need to log in.

## 4. Put it on the Divi page
1. Create the page **সদস্য হোন** (slug `join`).
2. Rebuild the green hero from `design/join.html` with Divi modules.
3. In the left column, add a **Code** module with `[fluentform id="X"]` (X = the form ID in Fluent Forms → All Forms).
4. In the right column, add the banyan illustration and the box "যাচাইয়ের সময় যা লাগবে".
5. Paste `bmpc-fluentforms.css` into **Divi → Theme Options → General → Custom CSS**.

## Field list (for building by hand)
Required fields are marked *.

**১. আবেদনকারীর তথ্য:** পূর্ণ নাম (বাংলায়)* · পূর্ণ নাম (ইংরেজিতে)* · জন্ম তারিখ* (d/m/Y) · লিঙ্গ* (পুরুষ/নারী/অন্যান্য) · NID / জন্ম নিবন্ধন নম্বর* · মোবাইল নম্বর* · ইমেইল · পেশা

**২. বীর মুক্তিযোদ্ধার তথ্য:** বীর মুক্তিযোদ্ধার নাম* · আপনার সম্পর্ক* (সন্তান (পুত্র) / সন্তান (কন্যা) / নাতি / নাতনী / অন্যান্য প্রজন্ম) · বর্তমান অবস্থা* (জীবিত/প্রয়াত) · গেজেট নম্বর* · সনদ নম্বর · যুদ্ধকালীন সেক্টর (অজানা, সেক্টর ১–১১) · নিজ জেলা*

**৩. ঠিকানা:** বিভাগ* (৮টি বিভাগ) · জেলা* · উপজেলা / থানা* · বর্তমান ঠিকানা*

**৪. অঙ্গীকার:** নীতিমালা (Custom HTML, collapsible) · নীতিমালায় সম্মতি* · তথ্যের সত্যতা নিশ্চিত*

Submit button: **আবেদন জমা দিন** (green).

## If you buy Pro later
Set `WITH_UPLOADS = True` in `build_form.py` and run `python3 wordpress/fluentforms/build_form.py`. That builds
`bmpc-join-form-pro.json` with four upload fields. Also switch the mobile field to Pro's Phone field (country: Bangladesh).
