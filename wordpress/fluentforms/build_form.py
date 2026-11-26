"""Builds Fluent Forms import files for the BMPC membership application.
Run from repo root: python3 wordpress/fluentforms/build_form.py
Outputs bmpc-join-form.json (free Fluent Forms, no uploads) and bmpc-join-form-pro.json (Fluent Forms Pro, with
photo and document uploads). bmpc.bd runs the Pro version."""
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
def email(name, label, ph="", required=False, help_=""):
    r = req("ইমেইল দিন") if required else opt(); r["email"] = {"value": True, "message": "সঠিক ইমেইল দিন"}
    return {"index": 2, "element": "input_email", "attributes": {"type": "email", "name": name, "value": "", "id": "", "class": "", "placeholder": ph},
            "settings": {**BASE(label, r, help_), "is_unique": "no", "unique_validation_message": ""},
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
def radio(name, label, items, required=True, default=""):
    return {"index": 5, "element": "input_radio", "attributes": {"type": "radio", "name": name, "value": default},
            "settings": {**BASE(label, req("একটি বাছাই করুন") if required else opt()), "display_type": "", "layout_class": "ff_list_inline", "advanced_options": options(items),
                         "calc_value_status": False, "enable_image_input": False, "randomize_options": "no"},
            "editor_options": {"title": "Radio Field", "icon_class": "ff-edit-radio", "element": "input-radio", "template": "inputCheckable"}, "uniqElKey": key()}
def textarea(name, label, ph=""):
    return {"index": 6, "element": "textarea", "attributes": {"name": name, "value": "", "id": "", "class": "", "placeholder": ph, "rows": 3, "cols": 2, "maxlength": ""},
            "settings": BASE(label, req()), "editor_options": {"title": "Text Area", "icon_class": "ff-edit-textarea", "template": "inputTextarea"}, "uniqElKey": key()}
def upload(name, label, help_, required=True):
    r = req("ফাইলটি যুক্ত করুন") if required else opt()
    r.update({"max_file_size": {"value": 10 * 1024 * 1024, "_valueFrom": "MB", "message": "ফাইলের আকার সর্বোচ্চ ১০ MB হতে পারবে"},
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
    return f'<details class="bmpc-policy"><summary>সংগঠনের নিয়মাবলি পড়ুন</summary><div class="bmpc-policy-body">{out}</div></details>'

DIVS = ["ঢাকা", "চট্টগ্রাম", "রাজশাহী", "খুলনা", "বরিশাল", "সিলেট", "রংপুর", "ময়মনসিংহ"]
BLOOD = ["এ+ (A+)", "এ− (A−)", "বি+ (B+)", "বি− (B−)", "এবি+ (AB+)", "এবি− (AB−)", "ও+ (O+)", "ও− (O−)"]
HOME, ABROAD = "বাংলাদেশে", "প্রবাসে (দেশের বাইরে)"

def when(field, value):
    """Fluent Forms conditional logic: show only when field == value."""
    return {"status": True, "type": "all", "conditions": [{"field": field, "value": value, "operator": "="}]}
def shown_if(el, field, value):
    el["settings"]["conditional_logics"] = when(field, value)
    return el

def image_upload(name, label, help_, required=True):
    el = upload(name, label, help_, required=required)
    el["settings"]["validation_rules"]["allowed_file_types"] = {"value": ["jpg|jpeg|gif|png|bmp"], "message": "শুধু ছবি (JPG/PNG) দিন"}
    el["settings"]["validation_rules"]["max_file_count"] = {"value": 1, "message": "একটি ছবি দিন"}
    return el

def fields(with_uploads=True):
    # Sections and wording follow the council's brief (ক–ঙ). Section titles are "<letter>. <title>";
    # assets/js/bmpc.js turns the letter into the numbered badge and wraps each section in a card.
    f = [
        section("ক. ব্যক্তিগত তথ্য"),
        cols([text("name_bn", "পূর্ণ নাম (বাংলায়)", "যেমন: মোঃ রফিকুল ইসলাম", help_="এনআইডি বা পাসপোর্ট অনুযায়ী")],
             [text("name_en", "পূর্ণ নাম (ইংরেজিতে)", "e.g. Md. Rafiqul Islam", help_="এনআইডি বা পাসপোর্ট অনুযায়ী")]),
        cols([date("dob", "জন্ম তারিখ")], [text("job", "পেশা ও পদবি", "যেমন: শিক্ষক, সহকারী প্রধান শিক্ষক", required=False)]),
        cols([radio("gender", "লিঙ্গ", ["পুরুষ", "নারী", "অন্যান্য"], required=False)],
             [select("blood", "রক্তের গ্রুপ", BLOOD)]),
        text("workplace", "কর্মস্থল / প্রতিষ্ঠান", "প্রতিষ্ঠানের নাম", required=False),
        radio("location", "বর্তমান অবস্থান", [HOME, ABROAD], default=HOME),
    ]
    if with_uploads:
        f.append(image_upload("photo", "পাসপোর্ট সাইজ ছবি", "পরিচয়পত্র ও সদস্য তালিকার জন্য। JPG বা PNG, সর্বোচ্চ ১০ MB।", required=False))
    f += [
        section("খ. বীর মুক্তিযোদ্ধা পিতা বা মাতার তথ্য"),
        cols([radio("relation", "সম্পর্ক", ["বীর মুক্তিযোদ্ধা পিতা", "বীর মুক্তিযোদ্ধা মাতা"])],
             [radio("ff_status", "বীর মুক্তিযোদ্ধার বর্তমান অবস্থা", ["জীবিত", "প্রয়াত"])]),
        cols([text("ff_name", "বীর মুক্তিযোদ্ধার পূর্ণ নাম", "পূর্ণ নাম")],
             [text("gazette", "বীর মুক্তিযোদ্ধা সনদ নম্বর / গেজেট নম্বর", "সনদ বা গেজেটের নম্বর", help_="মূল সনদ বা গেজেট অনুযায়ী নির্ভুল নম্বর")]),
    ]
    if with_uploads:
        f.append(upload("doc_cert", "বীর মুক্তিযোদ্ধা সনদ / গেজেট / পরিচয়পত্রের কপি", "PDF বা JPG, প্রতিটি ফাইল সর্বোচ্চ ১০ MB।"))
    f += [
        section("গ. জাতীয় পরিচয় ও যোগাযোগের তথ্য"),
        cols([radio("id_type", "পরিচয়পত্রের ধরন", ["জাতীয় পরিচয়পত্র (NID)", "পাসপোর্ট", "জন্ম নিবন্ধন"])],
             [text("nid", "পরিচয়পত্রের নম্বর", "নম্বরটি লিখুন", help_="প্রবাসে থাকলে এবং NID না থাকলে পাসপোর্ট বা জন্ম নিবন্ধন নম্বর দিন")]),
    ]
    if with_uploads:
        f.append(upload("doc_nid", "NID / পাসপোর্টের কপি", "পরিচয় নিশ্চিত করার জন্য। PDF বা JPG, সর্বোচ্চ ১০ MB।"))
    f += [
        cols([text("phone", "মোবাইল / হোয়াটসঅ্যাপ নম্বর", "+8801XXXXXXXXX", typ="tel", msg="কান্ট্রি কোডসহ সঠিক নম্বর দিন",
                   help_="কান্ট্রি কোডসহ লিখুন (যেমন: +880…), প্রবাসে থাকলে সে দেশের কোড দিন")],
             [email("email", "ইমেইল অ্যাড্রেস", "name@example.com", required=True, help_="আপডেট ও কনফার্মেশন পাঠানোর জন্য")]),
        section("ঘ. ঠিকানা"),
        html('<p class="bmpc-sub">স্থায়ী ঠিকানা (বাংলাদেশ)</p>'),
        cols([select("division", "বিভাগ", DIVS)], [text("district", "জেলা", "জেলার নাম")], [text("upazila", "উপজেলা / থানা", "উপজেলা বা থানা")]),
        cols([text("village", "গ্রাম / মহল্লা", "গ্রাম বা মহল্লার নাম")], [text("postcode", "পোস্ট কোড", "যেমন: ৩৫০০")]),
        html('<p class="bmpc-sub">বর্তমান ঠিকানা</p>'),
        shown_if(textarea("address", "বাড়ি, রাস্তা ও এলাকা", "উপজেলা ও জেলাসহ লিখুন"), "location", HOME),
        shown_if(cols([text("abroad_city", "শহর", "শহরের নাম")], [text("abroad_country", "দেশ", "দেশের নাম")]), "location", ABROAD),
        section("ঙ. ঘোষণা ও সম্মতি"),
        terms("agree_truth", "আমি এই মর্মে ঘোষণা করছি যে, প্রদত্ত সকল তথ্য সঠিক ও সত্য। তথ্য মিথ্যা প্রমাণিত হলে আমার সদস্যপদ বাতিল বলে গণ্য হবে।"),
        html(policy_html()),
        terms("agree_policy", "আমি সংগঠনের নিয়মাবলি ও গোপনীয়তা নীতিমালায় সম্মতি দিচ্ছি।"),
    ]
    return f

SUBMIT = {"uniqElKey": "el_bmpc_submit", "element": "button", "attributes": {"type": "submit", "class": ""},
          "settings": {"align": "left", "button_style": "default", "container_class": "", "help_message": "", "background_color": "#0B5B3E",
                       "button_size": "lg", "color": "#ffffff", "button_ui": {"type": "default", "text": "আবেদন জমা দিন", "img_url": ""}},
          "editor_options": {"title": "Submit Button"}}
CONFIRM = ('<h3>ধন্যবাদ, আপনার আবেদন জমা হয়েছে।</h3><p>অ্যাডমিন আপনার তথ্য ও কাগজপত্র যাচাই করে মোবাইল বা হোয়াটসঅ্যাপ নম্বরে যোগাযোগ করবেন। '
           'যাচাই সম্পন্ন হলে আপনাকে সদস্য হিসেবে অন্তর্ভুক্ত করা হবে।</p>')
SETTINGS = {"confirmation": {"redirectTo": "samePage", "messageToShow": CONFIRM, "customPage": None, "samePageFormBehavior": "hide_form", "customUrl": None},
            "restrictions": {"limitNumberOfEntries": {"enabled": False, "numberOfEntries": None, "period": "total", "limitReachedMsg": ""},
                             "scheduleForm": {"enabled": False, "start": None, "end": None, "pendingMsg": "", "expiredMsg": ""},
                             "requireLogin": {"enabled": False, "requireLoginMsg": ""},
                             "denyEmptySubmission": {"enabled": True, "message": "ফর্মটি খালি জমা দেওয়া যাবে না।"}},
            "layout": {"labelPlacement": "top", "helpMessagePlacement": "under_input", "errorMessagePlacement": "inline",
                       "cssClassName": "bmpc-form", "asteriskPlacement": "asterisk-right"}}

for variant, uploads in (("free", False), ("pro", True)):
    _k = itertools.count(1)
    form = {"id": "1", "title": "সদস্য আবেদন ফর্ম" + (" (ফাইল আপলোড সহ)" if uploads else ""), "status": "published",
            "type": "form", "has_payment": "0", "appearance_settings": None, "conditions": None,
            "form_fields": {"fields": fields(uploads), "submitButton": SUBMIT},
            "metas": [{"meta_key": "formSettings", "value": json.dumps(SETTINGS, ensure_ascii=False)},
                      {"meta_key": "template_name", "value": "blank_form"}]}
    path = os.path.join(HERE, "bmpc-join-form.json" if variant == "free" else "bmpc-join-form-pro.json")
    with open(path, "w", encoding="utf-8") as fh: json.dump([form], fh, ensure_ascii=False, indent=1)
    print("wrote", os.path.relpath(path, ROOT))
