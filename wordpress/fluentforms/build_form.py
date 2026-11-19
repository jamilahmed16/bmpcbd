"""Builds Fluent Forms import files for the BMPC membership application.
Run from repo root: python3 wordpress/fluentforms/build_form.py
Outputs bmpc-join-form-pro.json (with file uploads) and bmpc-join-form-free.json (no uploads)."""
import json, os, re, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
BN = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
_k = itertools.count(1)
def key(): return f"el_bmpc{next(_k):03d}"
def req(msg="এই তথ্যটি দিন"): return {"required": {"value": True, "message": msg}}
def opt(): return {"required": {"value": False, "message": "এই তথ্যটি দিন"}}
BASE = lambda label, rules, help_="": {"container_class": "", "label": label, "admin_field_label": "", "label_placement": "",
    "help_message": help_, "validation_rules": rules, "conditional_logics": []}

def text(name, label, ph="", required=True, msg="এই তথ্যটি দিন", typ="text", help_=""):
    return {"index": 1, "element": "input_text", "attributes": {"type": typ, "name": name, "value": "", "class": "", "placeholder": ph, "maxlength": ""},
            "settings": {**BASE(label, req(msg) if required else opt(), help_), "prefix_label": "", "suffix_label": "", "is_unique": "no", "unique_validation_message": ""},
            "editor_options": {"title": "Simple Text", "icon_class": "ff-edit-text", "template": "inputText"}, "uniqElKey": key()}
def email(name, label, ph=""):
    r = opt(); r["email"] = {"value": True, "message": "সঠিক ইমেইল দিন"}
    return {"index": 2, "element": "input_email", "attributes": {"type": "email", "name": name, "value": "", "id": "", "class": "", "placeholder": ph},
            "settings": {**BASE(label, r), "is_unique": "no", "unique_validation_message": ""},
            "editor_options": {"title": "Email Address", "icon_class": "ff-edit-email", "template": "inputText"}, "uniqElKey": key()}
def date(name, label):
    return {"index": 3, "element": "input_date", "attributes": {"type": "text", "name": name, "value": "", "id": "", "class": "", "placeholder": "দিন/মাস/বছর"},
            "settings": {**BASE(label, req()), "date_format": "d/m/Y", "date_config": ""},
            "editor_options": {"title": "Time & Date", "icon_class": "ff-edit-date", "template": "inputText"}, "uniqElKey": key()}
def options(items): return [{"label": x, "value": x, "calc_value": ""} for x in items]
def select(name, label, items, required=True, msg="একটি বাছাই করুন"):
    return {"index": 4, "element": "select", "attributes": {"name": name, "value": "", "id": "", "class": ""},
            "settings": {**BASE(label, req(msg) if required else opt()), "placeholder": "বাছাই করুন", "advanced_options": options(items),
                         "calc_value_status": False, "enable_image_input": False, "randomize_options": "no", "enable_select_2": "no"},
            "editor_options": {"title": "Dropdown", "icon_class": "ff-edit-dropdown", "element": "select", "template": "select"}, "uniqElKey": key()}
def radio(name, label, items):
    return {"index": 5, "element": "input_radio", "attributes": {"type": "radio", "name": name, "value": ""},
            "settings": {**BASE(label, req("একটি বাছাই করুন")), "display_type": "", "layout_class": "ff_list_inline", "advanced_options": options(items),
                         "calc_value_status": False, "enable_image_input": False, "randomize_options": "no"},
            "editor_options": {"title": "Radio Field", "icon_class": "ff-edit-radio", "element": "input-radio", "template": "inputCheckable"}, "uniqElKey": key()}
def textarea(name, label, ph=""):
    return {"index": 6, "element": "textarea", "attributes": {"name": name, "value": "", "id": "", "class": "", "placeholder": ph, "rows": 3, "cols": 2, "maxlength": ""},
            "settings": BASE(label, req()), "editor_options": {"title": "Text Area", "icon_class": "ff-edit-textarea", "template": "inputTextarea"}, "uniqElKey": key()}
def upload(name, label, help_, required=True):
    r = req("ফাইলটি যুক্ত করুন") if required else opt()
    r.update({"max_file_size": {"value": 5, "_valueFrom": "MB", "message": "ফাইলের আকার সর্বোচ্চ ৫ MB হতে পারবে"},
              "max_file_count": {"value": 2, "message": "সর্বোচ্চ ২টি ফাইল যুক্ত করা যাবে"},
              "allowed_file_types": {"value": ["jpg|jpeg|gif|png|bmp", "pdf"], "message": "শুধু ছবি (JPG/PNG) অথবা PDF ফাইল দিন"}})
    return {"index": 7, "element": "input_file", "attributes": {"type": "file", "name": name, "value": "", "id": "", "class": ""},
            "settings": {**BASE(label, r, help_), "btn_text": "ফাইল বাছাই করুন", "upload_file_location": "default", "file_location_type": "follow_global_settings"},
            "editor_options": {"title": "File Upload", "icon_class": "ff-edit-files", "template": "inputFile"}, "uniqElKey": key()}
def section(label, desc=""):
    return {"index": 8, "element": "section_break", "attributes": {"id": "", "class": "bmpc-step"},
            "settings": {"label": label, "description": desc, "align": "left", "conditional_logics": []},
            "editor_options": {"title": "Section Break", "icon_class": "ff-edit-section-break", "template": "sectionBreak"}, "uniqElKey": key()}
def html(code, cls=""):
    return {"index": 9, "element": "custom_html", "attributes": {},
            "settings": {"html_codes": code, "conditional_logics": [], "container_class": cls},
            "editor_options": {"title": "Custom HTML", "icon_class": "ff-edit-html", "template": "customHTML"}, "uniqElKey": key()}
def terms(name, text_html):
    return {"index": 10, "element": "terms_and_condition", "attributes": {"type": "checkbox", "name": name, "value": False, "class": ""},
            "settings": {"tnc_html": text_html, "has_checkbox": True, "admin_field_label": "", "container_class": "",
                         "validation_rules": req("সম্মতি দিন"), "conditional_logics": []},
            "editor_options": {"title": "Terms & Conditions", "icon_class": "ff-edit-terms-condition", "template": "termsCheckbox"}, "uniqElKey": key()}
def cols(*groups):
    n = len(groups); w = round(100 / n, 2)
    return {"index": 11, "element": "container", "attributes": {}, "settings": {"container_class": "", "conditional_logics": [], "container_width": ""},
            "columns": [{"width": w, "fields": list(g)} for g in groups],
            "editor_options": {"title": "Two Column Container" if n == 2 else "Three Column Container", "icon_class": "ff-edit-column-2" if n == 2 else "ff-edit-column-3"},
            "uniqElKey": key()}

def policy_html():
    md = open(os.path.join(ROOT, "content", "membership-policy.md"), encoding="utf-8").read()
    out = ""
    for h, body in re.findall(r"## (.*?)\n(.*?)(?=\n## |\Z)", md, re.S):
        lis = "".join(f"<li>{l[2:].strip()}</li>" for l in body.strip().split("\n") if l.startswith("- "))
        out += f"<h4>{h}</h4><ul>{lis}</ul>"
    return f'<details class="bmpc-policy"><summary>সদস্য হওয়ার নীতিমালা পড়ুন</summary><div class="bmpc-policy-body">{out}</div></details>'

DIVS = ["ঢাকা", "চট্টগ্রাম", "রাজশাহী", "খুলনা", "বরিশাল", "সিলেট", "রংপুর", "ময়মনসিংহ"]
SECTORS = ["অজানা"] + [f"সেক্টর {str(i).translate(BN)}" for i in range(1, 12)]

def fields(with_uploads):
    f = [
        section("১. আবেদনকারীর তথ্য"),
        cols([text("name_bn", "পূর্ণ নাম (বাংলায়)", "যেমন: মোঃ রফিকুল ইসলাম")], [text("name_en", "পূর্ণ নাম (ইংরেজিতে)", "e.g. Md. Rafiqul Islam")]),
        cols([date("dob", "জন্ম তারিখ")], [radio("gender", "লিঙ্গ", ["পুরুষ", "নারী", "অন্যান্য"])]),
        cols([text("nid", "জাতীয় পরিচয়পত্র / জন্ম নিবন্ধন নম্বর", "১০, ১৩ বা ১৭ সংখ্যার নম্বর")],
             [text("phone", "মোবাইল নম্বর", "01XXXXXXXXX", typ="tel", msg="সঠিক মোবাইল নম্বর দিন")]),
        cols([email("email", "ইমেইল (ঐচ্ছিক)", "name@example.com")], [text("job", "পেশা (ঐচ্ছিক)", "যেমন: শিক্ষক, ব্যবসায়ী, শিক্ষার্থী", required=False)]),
        section("২. বীর মুক্তিযোদ্ধার তথ্য", "যে বীর মুক্তিযোদ্ধার প্রজন্ম হিসেবে আবেদন করছেন, তাঁর তথ্য দিন।"),
        text("ff_name", "বীর মুক্তিযোদ্ধার নাম", "পূর্ণ নাম"),
        cols([select("relation", "আপনার সম্পর্ক", ["সন্তান (পুত্র)", "সন্তান (কন্যা)", "নাতি / নাতনী", "অন্যান্য প্রজন্ম"])],
             [radio("ff_status", "বর্তমান অবস্থা", ["জীবিত", "প্রয়াত"])]),
        cols([text("gazette", "গেজেট নম্বর", "মুক্তিযোদ্ধা গেজেটের নম্বর")], [text("cert", "মুক্তিযোদ্ধা সনদ নম্বর (ঐচ্ছিক)", "যদি থাকে", required=False)]),
        cols([select("sector", "যুদ্ধকালীন সেক্টর (ঐচ্ছিক)", SECTORS, required=False)], [text("ff_district", "বীর মুক্তিযোদ্ধার নিজ জেলা", "যেমন: কুমিল্লা")]),
        section("৩. ঠিকানা"),
        cols([select("division", "বিভাগ", DIVS)], [text("district", "জেলা", "জেলার নাম")], [text("upazila", "উপজেলা / থানা", "উপজেলা বা থানা")]),
        textarea("address", "বর্তমান ঠিকানা", "বাড়ি নম্বর, রাস্তা, এলাকা"),
    ]
    if with_uploads:
        f += [section("৪. প্রমাণপত্র", "ছবি (JPG/PNG) অথবা PDF, প্রতিটি ফাইল সর্বোচ্চ ৫ MB। আপনার ব্যক্তিগত তথ্য গোপন রাখা হবে।"),
              cols([upload("doc_cert", "মুক্তিযোদ্ধা সনদ / গেজেটের কপি", "সনদ অথবা গেজেটের পাতা")], [upload("doc_nid", "আবেদনকারীর NID / জন্ম নিবন্ধন", "উভয় পাশ")]),
              cols([upload("doc_photo", "আবেদনকারীর ছবি", "পাসপোর্ট সাইজ")], [upload("doc_rel", "সম্পর্কের প্রমাণ (ঐচ্ছিক)", "যেমন: ওয়ারিশ সনদ বা জন্ম নিবন্ধন", required=False)])]
        n = "৫"
    else:
        n = "৪"
    f += [section(f"{n}. অঙ্গীকার"), html(policy_html()),
          terms("agree_policy", "আমি সদস্য হওয়ার নীতিমালা পড়েছি এবং তা মেনে চলব।"),
          terms("agree_truth", "আমি নিশ্চিত করছি যে উপরের সকল তথ্য সত্য এবং আমি একজন বীর মুক্তিযোদ্ধার সন্তান বা প্রজন্ম।")]
    return f

SUBMIT = {"uniqElKey": "el_bmpc_submit", "element": "button", "attributes": {"type": "submit", "class": ""},
          "settings": {"align": "left", "button_style": "default", "container_class": "", "help_message": "", "background_color": "#0B5B3E",
                       "button_size": "lg", "color": "#ffffff", "button_ui": {"type": "default", "text": "আবেদন জমা দিন", "img_url": ""}},
          "editor_options": {"title": "Submit Button"}}
CONFIRM = ('<h3>ধন্যবাদ, আপনার আবেদন জমা হয়েছে।</h3><p>অ্যাডমিন আপনার তথ্য যাচাই করে মোবাইল নম্বরে যোগাযোগ করবেন। '
           'যাচাই সম্পন্ন হলে আপনাকে সদস্য হিসেবে অন্তর্ভুক্ত করা হবে।</p>')
SETTINGS = {"confirmation": {"redirectTo": "samePage", "messageToShow": CONFIRM, "customPage": None, "samePageFormBehavior": "hide_form", "customUrl": None},
            "restrictions": {"limitNumberOfEntries": {"enabled": False, "numberOfEntries": None, "period": "total", "limitReachedMsg": ""},
                             "scheduleForm": {"enabled": False, "start": None, "end": None, "pendingMsg": "", "expiredMsg": ""},
                             "requireLogin": {"enabled": False, "requireLoginMsg": ""},
                             "denyEmptySubmission": {"enabled": True, "message": "ফর্মটি খালি জমা দেওয়া যাবে না।"}},
            "layout": {"labelPlacement": "top", "helpMessagePlacement": "with_label", "errorMessagePlacement": "inline",
                       "cssClassName": "bmpc-form", "asteriskPlacement": "asterisk-right"}}

for variant, uploads in (("pro", True), ("free", False)):
    _k = itertools.count(1)
    form = {"id": "1", "title": "সদস্য আবেদন ফর্ম" + (" (ফাইল আপলোড সহ)" if uploads else ""), "status": "published",
            "type": "form", "has_payment": "0", "appearance_settings": None, "conditions": None,
            "form_fields": {"fields": fields(uploads), "submitButton": SUBMIT},
            "metas": [{"meta_key": "formSettings", "value": json.dumps(SETTINGS, ensure_ascii=False)},
                      {"meta_key": "template_name", "value": "blank_form"}]}
    path = os.path.join(HERE, f"bmpc-join-form-{variant}.json")
    with open(path, "w", encoding="utf-8") as fh: json.dump([form], fh, ensure_ascii=False, indent=1)
    print("wrote", os.path.relpath(path, ROOT))
