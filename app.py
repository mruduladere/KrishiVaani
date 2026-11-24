"""
app.py - Main Flask Web Application Controller for KrishiVaani (Voice of Agriculture)
Unified Python digital platform for Indian farmers built with Flask, Tailwind CSS, and Lucide Icons.
Strictly NO external database (uses Python in-memory state + flask.session).
Bilingual English & Marathi support via translations.py.
"""

import re
import copy
import datetime
import urllib.parse
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, session, flash
from sample_data import (
    SAMPLE_FARMER,
    SAMPLE_REGISTERED_FARMERS,
    SAMPLE_SERVICES,
    SAMPLE_CROP_TASKS,
    SAMPLE_LIVESTOCK,
    SAMPLE_MARKETPLACE,
    SAMPLE_EXPENSES,
    CROP_GUIDES,
    EXPENSE_CATEGORIES
)
from translations import t, pick, TRANSLATIONS
from ai_router import route_farmer_query
from smart_dispatcher import extract_and_dispatch
from form_digitizer import digitize_form

app = Flask(__name__)
app.secret_key = "krishivaani-secret-key-sih2026-pure-python"

# ---------------------------------------------------------
# IN-MEMORY RUNTIME DATA STORE (STRICTLY NO DATABASE)
# ---------------------------------------------------------
# Global mutable Python dictionaries pre-populated with realistic
# Maharashtra farming records. Updated during runtime session without SQL.
FARMERS_DB = copy.deepcopy(SAMPLE_REGISTERED_FARMERS)
SERVICES_DB = copy.deepcopy(SAMPLE_SERVICES)
TASKS_DB = copy.deepcopy(SAMPLE_CROP_TASKS)
LIVESTOCK_DB = copy.deepcopy(SAMPLE_LIVESTOCK)
MARKETPLACE_DB = copy.deepcopy(SAMPLE_MARKETPLACE)
EXPENSES_DB = copy.deepcopy(SAMPLE_EXPENSES)


# ---------------------------------------------------------
# JINJA TEMPLATE CONTEXT INJECTION & FILTERS (BILINGUAL SUPPORT)
# ---------------------------------------------------------
@app.context_processor
def inject_template_globals():
    """
    Injects active language ('mr' or 'en'), t(key), and pick(val)
    into all Jinja2 templates automatically.
    """
    active_lang = session.get("lang", "mr")
    
    def translate(key):
        return t(key, lang=active_lang)

    def pick_lang(val):
        return pick(val, lang=active_lang)

    return {
        "t": translate,
        "pick": pick_lang,
        "lang": active_lang
    }


@app.template_filter("pick")
def pick_filter(val):
    """Jinja filter: {{ value | pick }} returns pure active language string."""
    active_lang = session.get("lang", "mr")
    return pick(val, lang=active_lang)


def get_current_farmer():
    """Retrieves active farmer profile from session or in-memory database."""
    if session.get("farmer_profile"):
        return session["farmer_profile"]
    phone = session.get("phone")
    if phone and phone in FARMERS_DB:
        session["farmer_profile"] = copy.deepcopy(FARMERS_DB[phone])
        return session["farmer_profile"]
    sample = copy.deepcopy(FARMERS_DB.get("9822012345", SAMPLE_FARMER))
    session["farmer_profile"] = sample
    return sample


def normalize_phone(phone_str):
    """Normalizes phone string by stripping whitespace and dashes."""
    if not phone_str:
        return ""
    cleaned = "".join(c for c in phone_str if c.isdigit())
    if len(cleaned) > 10 and cleaned.startswith("91"):
        cleaned = cleaned[2:]
    return cleaned


def detect_crop_key(crop_name):
    """Maps farmer crop profile strings or dicts to standardized CROP_GUIDES keys or None if unknown."""
    if isinstance(crop_name, dict):
        if "key" in crop_name:
            return crop_name["key"]
        crop_name = crop_name.get("en", "") or crop_name.get("mr", "")
    crop_lower = str(crop_name).lower()
    if "grape" in crop_lower or "द्राक्ष" in crop_lower:
        return "Grapes"
    elif "onion" in crop_lower or "कांदा" in crop_lower:
        return "Onion"
    elif "soybean" in crop_lower or "सोयाबीन" in crop_lower:
        return "Soybean"
    elif "cotton" in crop_lower or "कापूस" in crop_lower:
        return "Cotton"
    elif "sugarcane" in crop_lower or "ऊस" in crop_lower:
        return "Sugarcane"
    elif "wheat" in crop_lower or "गहू" in crop_lower:
        return "Wheat"
    return None


def get_crop_slug(crop_name):
    """Generates a clean URL slug / dictionary key from any crop string or dict."""
    if isinstance(crop_name, dict):
        name_str = crop_name.get("en") or crop_name.get("key") or crop_name.get("mr") or "Crop"
    else:
        name_str = str(crop_name).strip()
    # Normalize
    slug = re.sub(r"[^a-zA-Z0-9_\u0900-\u097F]+", "_", name_str).strip("_")
    return slug if slug else "Crop"


def generate_custom_crop_guide(crop_name):
    """
    Dynamically generates a realistic 4-stage general agronomy guide
    for custom crops (e.g. Wheat, Tomato, Cotton, Pomegranate).
    """
    if isinstance(crop_name, dict):
        name_en = crop_name.get("en", "Crop")
        name_mr = crop_name.get("mr", "पीक")
    else:
        name_str = str(crop_name).strip()
        # Heuristic translation/display
        marathi_crop_map = {
            "wheat": ("Wheat", "गहू"),
            "tomato": ("Tomato", "टोमॅटो"),
            "cotton": ("Cotton", "कापूस"),
            "sugarcane": ("Sugarcane", "ऊस"),
            "pomegranate": ("Pomegranate", "डाळिंब"),
            "turmeric": ("Turmeric", "हळद"),
            "maize": ("Maize", "मका"),
            "chilli": ("Chilli", "मिरची"),
            "gram": ("Bengal Gram", "हरभरा"),
            "bajra": ("Pearl Millet (Bajra)", "बाजरी"),
            "rice": ("Paddy / Rice", "भात / तांदूळ"),
        }
        lower = name_str.lower()
        matched = False
        for k, (en_val, mr_val) in marathi_crop_map.items():
            if k in lower:
                name_en, name_mr = en_val, mr_val
                matched = True
                break
        if not matched:
            name_en = name_str
            name_mr = name_str

    return {
        "display_name": {
            "en": name_en,
            "mr": name_mr
        },
        "season": {
            "en": "Current Season (Maharashtra Agro-Climatic Zone)",
            "mr": "चालू हंगाम (महाराष्ट्र कृषी हवामान विभाग)"
        },
        "recommended_soil": {
            "en": "Well-drained fertile black to medium loam soil with good aeration",
            "mr": "उत्तम निचरा होणारी कसदार मध्यम ते काळी पोयट्याची जमीन"
        },
        "stages": [
            {
                "stage_name": {
                    "en": f"Stage 1: Land Prep, Seed Treatment & Sowing",
                    "mr": f"टप्पा १: जमीन पूर्वमशागत, बीजप्रक्रिया व पेरणी"
                },
                "duration": {
                    "en": "Day 1 to 20",
                    "mr": "दिवस १ ते २०"
                },
                "fertilizer": {
                    "en": f"Basal application of well-rotted FYM (5 tons/acre) + balanced DAP/SSP & Potash. Apply Trichoderma for root health in {name_en}.",
                    "mr": f"पायाभूत खत: एकरी ५ टन चांगले कुजलेले शेणखत + डीएपी/सुपर फॉस्फेट आणि पोटॅश. {name_mr} पिकासाठी ट्रायकोडर्मा बुरशीनाशक प्रक्रिया करा."
                },
                "irrigation": {
                    "en": "Ensure field capacity moisture before planting; provide light first irrigation after seed emergence.",
                    "mr": "वाफसा आल्यावर पेरणी/लागवड करा; रोपे/दाणे रुजल्यानंतर लगेच हलके पाणी द्या."
                },
                "pest_disease": {
                    "en": "Seed treatment with biological or chemical fungicide to shield early seedlings from damping-off and soil pathogens.",
                    "mr": "मर रोग व बुरशी प्रतिबंधासाठी बीजप्रक्रिया किंवा मुळे बुडवून पुनर्लागवड करा."
                },
                "pro_tip": {
                    "en": f"Maintain recommended row-to-row spacing to enable unhindered canopy aeration and sunlight penetration for {name_en}.",
                    "mr": f"{name_mr} पिकाच्या निरोगी वाढीसाठी योग्य ओळीतील व रोपांमधील अंतर ठेवा, ज्यामुळे पुरेसा सूर्यप्रकाश व हवा खेळती राहते."
                }
            },
            {
                "stage_name": {
                    "en": f"Stage 2: Vegetative Canopy & Tillering / Branching",
                    "mr": f"टप्पा २: शाकीय वाढ व फुटवे फुटणे"
                },
                "duration": {
                    "en": "Day 21 to 50",
                    "mr": "दिवस २१ ते ५०"
                },
                "fertilizer": {
                    "en": f"Top dress with Urea/Nitrogen in split doses. Foliar spray of 19:19:19 (5 g/L) + micronutrients for lush foliage.",
                    "mr": f"युरिया/नत्र खताचा हप्ता विभागून द्या. १९:१९:१९ विद्राव्य खत (५ ग्रॅम/लिटर) व सूक्ष्मअन्नद्रव्यांची फवारणी करा."
                },
                "irrigation": {
                    "en": "Maintain consistent drip/furrow irrigation intervals. Avoid waterlogging around root zones.",
                    "mr": "ठिबक किंवा पाटाने नियमित पाणी द्या. मुळांपाशी पाणी साचू देऊ नका."
                },
                "pest_disease": {
                    "en": "Inspect under-surfaces of leaves for sucking pests (Aphids, Thrips, Mites). Install yellow/blue sticky traps.",
                    "mr": "पानांच्या खालच्या बाजूस मावा, तुडतुडे व फुलकिड्यांचे निरीक्षण करा. एकरी १५ चिकट सापळे लावा."
                },
                "pro_tip": {
                    "en": "Timely weeding within first 35 days prevents nutrition theft and creates natural soil mulch.",
                    "mr": "पहिल्या ३५ दिवसांत खुरपणी करून शेत तणमुक्त ठेवा; त्यामुळे पिकाला संपूर्ण खते मिळतात."
                }
            },
            {
                "stage_name": {
                    "en": f"Stage 3: Flowering, Setting & Grain/Fruit Development",
                    "mr": f"टप्पा ३: फुलधारणा व दाणे / फळ फुगवण"
                },
                "duration": {
                    "en": "Day 51 to 85",
                    "mr": "दिवस ५१ ते ८५"
                },
                "fertilizer": {
                    "en": "Supply 0:52:34 MKP + 13:00:45 or Calcium Boron to maximize flower retention and grain/fruit weight.",
                    "mr": "०:५२:३४ व १३:००:४५ पोटॅशियम नायट्रेट + बोरॉन फवारणी द्या, ज्यामुळे फुलगळ थांबते व वजन वाढते."
                },
                "irrigation": {
                    "en": "Critical moisture period. Strictly avoid severe water stress during flowering and grain fill.",
                    "mr": "हा संवेदनशील काळ आहे. फुलोरा व दाणे भरण्याच्या टप्प्यात पाण्याचा ताण अजिबात पडू देऊ नका."
                },
                "pest_disease": {
                    "en": "Spray preventive bio-fungicide or contact-systemic spray against blight, powdery mildew, and fruit/pod borers.",
                    "mr": "करपा, भुरी व अळीच्या नियंत्रणासाठी वेळेवर प्रतिबंधक बुरशीनाशक व कीटकनाशक फवारणी करा."
                },
                "pro_tip": {
                    "en": "Never spray strong chemical insecticides during peak morning pollinator hours (8 AM - 11 AM).",
                    "mr": "सकाळी ८ ते ११ दरम्यान मधमाश्यांच्या परागीभवनाच्या काळात कोणतीही विषारी कीटकनाशक फवारणी टाळा."
                }
            },
            {
                "stage_name": {
                    "en": f"Stage 4: Maturation, Harvesting & Safe Storage",
                    "mr": f"टप्पा ४: पक्वता, काढणी व साठवणूक"
                },
                "duration": {
                    "en": "Day 86 to 120",
                    "mr": "दिवस ८६ ते १२०"
                },
                "fertilizer": {
                    "en": "Withhold all chemical nitrogen fertilizer; permit natural translocation of reserves.",
                    "mr": "रासायनिक खते पूर्णपणे बंद करा; पिकातील अन्नघटक नैसर्गिकरीत्या फळांत/दाण्यांत भरू द्या."
                },
                "irrigation": {
                    "en": "Taper off irrigation 8-12 days before final harvest to boost keeping quality and prevent rot.",
                    "mr": "काढणीच्या ८-१२ दिवस आधी पाणी बंद करा, जेणेकरून साठवणूक क्षमता सुधारते व सड टळते."
                },
                "pest_disease": {
                    "en": "Protect harvested produce from dew or unseasonal showers. Ensure storage humidity under 12-14%.",
                    "mr": "कापणी केलेला शेतमाल कोरड्या जागी ठेवा. ओलावा १२% पेक्षा कमी झाल्यावरच साठवणूक करा."
                },
                "pro_tip": {
                    "en": f"Grade and sort {name_en} according to APMC standards to secure premium price discovery on KrishiVaani Marketplace.",
                    "mr": f"{name_mr} शेतमालाची गुणवत्ता प्रतवारी करा जेणेकरून कृषीवाणी बाजारपेठेत उत्तम बाजारभाव मिळेल."
                }
            }
        ]
    }


def generate_starter_tasks_for_crops(crops_list):
    """Generates starter tasks checklist matching the farmer's specific active crops."""
    matched_tasks = []
    task_idx = 1
    
    # 1. First search in existing SAMPLE_CROP_TASKS
    for crop_item in crops_list:
        c_key = detect_crop_key(crop_item)
        c_name = pick(crop_item, lang="en") if isinstance(crop_item, dict) else str(crop_item).strip()
        c_name_mr = pick(crop_item, lang="mr") if isinstance(crop_item, dict) else str(crop_item).strip()

        found_existing = False
        if c_key:
            for tsk in SAMPLE_CROP_TASKS:
                tsk_crop_key = detect_crop_key(tsk.get("crop"))
                if tsk_crop_key == c_key:
                    task_copy = copy.deepcopy(tsk)
                    task_copy["id"] = f"TSK-{task_idx:02d}"
                    matched_tasks.append(task_copy)
                    task_idx += 1
                    found_existing = True
        
        # 2. If no pre-existing tasks found for this custom crop, generate clean custom starter tasks
        if not found_existing:
            matched_tasks.append({
                "id": f"TSK-{task_idx:02d}",
                "crop": {"en": c_name, "mr": c_name_mr},
                "title": {
                    "en": f"Apply basal dose FYM and NPK fertilizer for {c_name}",
                    "mr": f"{c_name_mr} पिकासाठी शेणखत व एनपीके खताचा पायाभूत डोस देणे"
                },
                "stage": {"en": "Land Prep", "mr": "पूर्वमशागत"},
                "due_date": {"en": "Immediate", "mr": "तातडीने"},
                "priority": {"en": "High", "mr": "उच्च"},
                "status": True
            })
            task_idx += 1
            matched_tasks.append({
                "id": f"TSK-{task_idx:02d}",
                "crop": {"en": c_name, "mr": c_name_mr},
                "title": {
                    "en": f"Foliar spray of 19:19:19 + micronutrients for {c_name} vegetative vigor",
                    "mr": f"{c_name_mr} पिकाच्या शाकीय वाढीसाठी १९:१९:१९ व सूक्ष्मअन्नद्रव्य फवारणी"
                },
                "stage": {"en": "Vegetative Growth", "mr": "शाकीय वाढ"},
                "due_date": {"en": "Next 3 Days", "mr": "पुढील ३ दिवसांत"},
                "priority": {"en": "Medium", "mr": "मध्यम"},
                "status": False
            })
            task_idx += 1
            matched_tasks.append({
                "id": f"TSK-{task_idx:02d}",
                "crop": {"en": c_name, "mr": c_name_mr},
                "title": {
                    "en": f"Install 15 yellow sticky traps per acre for pest prevention in {c_name}",
                    "mr": f"{c_name_mr} पिकात कीड नियंत्रणासाठी एकरी १५ पिवळे चिकट सापळे लावणे"
                },
                "stage": {"en": "Crop Protection", "mr": "पीक संरक्षण"},
                "due_date": {"en": "This Week", "mr": "या आठवड्यात"},
                "priority": {"en": "Medium", "mr": "मध्यम"},
                "status": False
            })
            task_idx += 1

    return matched_tasks


# ---------------------------------------------------------
# AUTHENTICATION & SESSION ROUTES
# ---------------------------------------------------------
@app.route("/")
def index():
    """Root route: Redirects to dashboard if logged in, else renders split-screen login card."""
    if session.get("is_authenticated"):
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    """Validates mobile number and 4-digit PIN against in-memory registered accounts."""
    phone_input = request.form.get("phone", "").strip()
    pin_input = request.form.get("pin", "").strip()

    cleaned_phone = normalize_phone(phone_input)

    # Search in registered farmers in-memory dictionary
    matched_farmer = None
    for reg_phone, profile in FARMERS_DB.items():
        if normalize_phone(reg_phone) == cleaned_phone:
            if profile.get("pin") == pin_input:
                matched_farmer = profile
                break

    if matched_farmer:
        session["is_authenticated"] = True
        session["phone"] = cleaned_phone
        session["farmer_name"] = matched_farmer.get("name", "Farmer")
        session["farmer_profile"] = copy.deepcopy(matched_farmer)
        session["crop_tasks"] = generate_starter_tasks_for_crops(matched_farmer.get("crops_grown", []))
        flash(t("login_success"), "success")
        return redirect(url_for("dashboard"))

    flash(t("login_failed"), "error")
    return redirect(url_for("index"))


@app.route("/demo-login")
def demo_login():
    """1-Click Demo Login bypass for Smart India Hackathon evaluators."""
    session["is_authenticated"] = True
    session["phone"] = "9822012345"
    session["farmer_name"] = SAMPLE_FARMER["name"]
    session["farmer_profile"] = copy.deepcopy(SAMPLE_FARMER)
    session["crop_tasks"] = generate_starter_tasks_for_crops(SAMPLE_FARMER.get("crops_grown", []))
    flash("Welcome to KrishiVaani Demo Account (Ramesh Patil)", "success")
    return redirect(url_for("dashboard"))


@app.route("/register", methods=["POST"])
def register():
    """Registers a new farmer account in-memory and signs them in immediately."""
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    pin = request.form.get("pin", "").strip()
    village = request.form.get("village", "Pimpalgaon Baswant").strip()
    taluka = request.form.get("taluka", "Niphad").strip()
    district = request.form.get("district", "Nashik").strip()
    land_size = float(request.form.get("land_size", 3.0))
    crops_raw = request.form.get("crops", "Grapes, Onion").strip()

    crops_list = [c.strip() for c in crops_raw.split(",") if c.strip()]
    cleaned_phone = normalize_phone(phone)

    if not name or not cleaned_phone or not pin:
        flash(t("reg_validation_error"), "error")
        return redirect(url_for("index"))

    new_farmer = {
        "name": name,
        "phone": phone,
        "pin": pin,
        "email": f"{cleaned_phone}@krishivaani.in",
        "village": village,
        "taluka": taluka,
        "district": district,
        "state": "Maharashtra",
        "pincode": "422001",
        "land_size_acres": land_size,
        "soil_type": "Medium Black Soil (काळी मध्यम जमीन)",
        "irrigation_type": "Drip Irrigation (ठिबक सिंचन)",
        "primary_language": "Marathi & English",
        "crops_grown": crops_list if crops_list else ["Grapes", "Onion"],
        "livestock_summary": {
            "gir_cows": 1,
            "murrah_buffaloes": 1,
            "goats": 2,
            "total_animals": 4,
            "daily_milk_litres": 14.0
        }
    }

    # Save to in-memory store
    FARMERS_DB[cleaned_phone] = new_farmer

    # Set session
    session["is_authenticated"] = True
    session["phone"] = cleaned_phone
    session["farmer_name"] = name
    session["farmer_profile"] = copy.deepcopy(new_farmer)
    session["crop_tasks"] = generate_starter_tasks_for_crops(new_farmer["crops_grown"])
    flash(t("reg_success"), "success")
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    """Clears user session and redirects to login card."""
    session.pop("is_authenticated", None)
    session.pop("phone", None)
    session.pop("farmer_name", None)
    session.pop("farmer_profile", None)
    session.pop("crop_tasks", None)
    return redirect(url_for("index"))


@app.route("/set-lang/<lang_code>")
def set_language(lang_code):
    """Switches active session language ('mr' or 'en') and redirects back to previous page."""
    if lang_code in ["mr", "en"]:
        session["lang"] = lang_code
    return redirect(request.referrer or url_for("dashboard"))


# ---------------------------------------------------------
# MODULE 1: FARMER PROFILE & DASHBOARD
# ---------------------------------------------------------
@app.route("/dashboard")
def dashboard():
    """Farmer home dashboard displaying KPIs, active crop stages, and tasks."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))

    farmer = get_current_farmer()
    active_lang = session.get("lang", "mr")

    # Dynamic calculation of stats
    nov_expenses = sum(
        item.get("amount", 0)
        for item in EXPENSES_DB
        if "Nov" in item.get("month", "") or "11" in item.get("date", "")
    )

    livestock = farmer.get("livestock_summary", {})
    total_livestock = (
        livestock.get("gir_cows", 0)
        + livestock.get("murrah_buffaloes", 0)
        + livestock.get("goats", 0)
    )

    # Use session['crop_tasks'] if present, else fallback
    current_tasks = session.get("crop_tasks")
    if current_tasks is None:
        current_tasks = generate_starter_tasks_for_crops(farmer.get("crops_grown", []))
        session["crop_tasks"] = current_tasks

    stats = {
        "nov_expenses": nov_expenses,
        "total_livestock": total_livestock,
        "active_crops_count": len(farmer.get("crops_grown", [])),
        "total_tasks": len(current_tasks)
    }

    # Dynamically resolve crop overview cards matching farmer's current crops
    crop_cards = []
    for raw_crop in farmer.get("crops_grown", []):
        crop_name = pick(raw_crop, lang=active_lang) if isinstance(raw_crop, dict) else str(raw_crop).strip()
        matched_key = detect_crop_key(raw_crop)

        if matched_key and matched_key in CROP_GUIDES:
            guide = CROP_GUIDES[matched_key]
            disp_name = pick(guide.get("display_name", crop_name), lang=active_lang)
            # Pick representative stage (Stage 3 for Grapes, Stage 2 for Onion, Stage 4 for Soybean)
            stages = guide.get("stages", [])
            stage_idx = 2 if matched_key == "Grapes" else (1 if matched_key == "Onion" else (3 if len(stages) > 3 else 0))
            if stage_idx >= len(stages):
                stage_idx = 0
            stage_data = stages[stage_idx] if stages else {}

            crop_cards.append({
                "crop_key": matched_key,
                "display_name": disp_name,
                "stage_badge": {"en": f"Stage {stage_idx + 1}", "mr": f"टप्पा {stage_idx + 1}"},
                "stage_title": stage_data.get("stage_name", {}),
                "stage_duration": stage_data.get("duration", {}),
                "summary": stage_data.get("fertilizer", stage_data.get("pro_tip", {})),
                "footer_tag": {"en": f"{matched_key} Advisory Plan", "mr": f"{disp_name} कृषी सल्ला"},
                "has_guide": True,
                "guide_url": url_for("crop_helper", crop=matched_key)
            })
        else:
            # Custom crop entered by farmer (e.g. "Tomato", "Wheat", "Sugarcane")
            custom_guide = generate_custom_crop_guide(raw_crop)
            disp_name = pick(custom_guide["display_name"], lang=active_lang)
            first_stage = custom_guide["stages"][1] if len(custom_guide["stages"]) > 1 else custom_guide["stages"][0]
            crop_cards.append({
                "crop_key": get_crop_slug(raw_crop),
                "display_name": disp_name,
                "stage_badge": {"en": "Stage 2", "mr": "टप्पा २"},
                "stage_title": first_stage.get("stage_name", {}),
                "stage_duration": first_stage.get("duration", {}),
                "summary": first_stage.get("fertilizer", {}),
                "footer_tag": {"en": "General Agronomy Guidance", "mr": "सर्वसाधारण पीक सल्ला"},
                "has_guide": True,
                "guide_url": url_for("crop_helper", crop=get_crop_slug(raw_crop))
            })

    return render_template(
        "dashboard.html",
        farmer=farmer,
        stats=stats,
        tasks=current_tasks,
        crop_cards=crop_cards,
        active_nav="dashboard"
    )


@app.route("/update-profile", methods=["POST"])
def update_profile():
    """Updates the active farmer profile directly in memory."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))

    farmer = get_current_farmer()
    farmer["name"] = request.form.get("name", farmer["name"])
    farmer["land_size_acres"] = float(request.form.get("land_size", farmer["land_size_acres"]))
    farmer["soil_type"] = request.form.get("soil_type", farmer["soil_type"])
    farmer["village"] = request.form.get("village", farmer["village"])
    farmer["taluka"] = request.form.get("taluka", farmer["taluka"])
    farmer["district"] = request.form.get("district", farmer["district"])
    farmer["irrigation_type"] = request.form.get("irrigation_type", farmer["irrigation_type"])
    
    crops_raw = request.form.get("crops", "")
    if crops_raw:
        new_crops = [c.strip() for c in crops_raw.split(",") if c.strip()]
        farmer["crops_grown"] = new_crops
        # Update session copy and regenerate synchronized crop tasks
        session["farmer_profile"] = farmer
        session["crop_tasks"] = generate_starter_tasks_for_crops(new_crops)
    else:
        session["farmer_profile"] = farmer

    # Also sync back into FARMERS_DB if phone is registered
    phone = session.get("phone")
    if phone:
        FARMERS_DB[phone] = copy.deepcopy(farmer)

    flash(t("profile_updated_success"), "success")
    return redirect(url_for("dashboard"))


@app.route("/reset-defaults")
def reset_defaults():
    """Resets runtime in-memory database to original sample data."""
    global FARMERS_DB, SERVICES_DB, TASKS_DB, LIVESTOCK_DB, MARKETPLACE_DB, EXPENSES_DB
    FARMERS_DB = copy.deepcopy(SAMPLE_REGISTERED_FARMERS)
    SERVICES_DB = copy.deepcopy(SAMPLE_SERVICES)
    TASKS_DB = copy.deepcopy(SAMPLE_CROP_TASKS)
    LIVESTOCK_DB = copy.deepcopy(SAMPLE_LIVESTOCK)
    MARKETPLACE_DB = copy.deepcopy(SAMPLE_MARKETPLACE)
    EXPENSES_DB = copy.deepcopy(SAMPLE_EXPENSES)

    session["farmer_profile"] = copy.deepcopy(SAMPLE_FARMER)
    session["crop_tasks"] = generate_starter_tasks_for_crops(SAMPLE_FARMER.get("crops_grown", []))

    flash(t("reset_success"), "success")
    return redirect(url_for("dashboard"))


# ---------------------------------------------------------
# MODULE 2: CROP & FARMING HELPER
# ---------------------------------------------------------
@app.route("/crop-helper")
def crop_helper():
    """Crop lifecycle advisory covering nutrition, irrigation, pests, and tasks."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))

    farmer = get_current_farmer()
    active_lang = session.get("lang", "mr")

    # 1. Build dynamically resolved crops knowledge base matching the farmer's active crops
    # farmer['crops_grown'] is the single source of truth!
    farmer_crops = farmer.get("crops_grown", [])
    if not farmer_crops:
        farmer_crops = ["Grapes", "Onion"]

    # Build crop guides dictionary for all farmer crops
    farmer_crop_tabs = {}
    for crop_item in farmer_crops:
        matched_key = detect_crop_key(crop_item)
        slug = get_crop_slug(crop_item)

        if matched_key and matched_key in CROP_GUIDES:
            guide = copy.deepcopy(CROP_GUIDES[matched_key])
            tab_key = matched_key
        else:
            guide = generate_custom_crop_guide(crop_item)
            tab_key = slug

        # Resolve display name for the selector tab
        guide["display_name"] = pick(guide.get("display_name", tab_key), lang=active_lang)
        farmer_crop_tabs[tab_key] = guide

    # Determine active crop
    requested_crop = request.args.get("crop")
    if requested_crop and requested_crop in farmer_crop_tabs:
        active_crop = requested_crop
    else:
        # Default to first crop in farmer's active list
        active_crop = list(farmer_crop_tabs.keys())[0]

    raw_guide = farmer_crop_tabs[active_crop]

    # Resolve bilingual fields in current active guide
    current_guide = copy.deepcopy(raw_guide)
    current_guide["season"] = pick(raw_guide.get("season", ""), lang=active_lang)
    current_guide["recommended_soil"] = pick(raw_guide.get("recommended_soil", ""), lang=active_lang)
    resolved_stages = []
    for stage in raw_guide.get("stages", []):
        rs = copy.deepcopy(stage)
        rs["stage_name"] = pick(stage.get("stage_name", ""), lang=active_lang)
        rs["duration"] = pick(stage.get("duration", ""), lang=active_lang)
        rs["fertilizer"] = pick(stage.get("fertilizer", ""), lang=active_lang)
        rs["irrigation"] = pick(stage.get("irrigation", ""), lang=active_lang)
        rs["pest_disease"] = pick(stage.get("pest_disease", ""), lang=active_lang)
        rs["pro_tip"] = pick(stage.get("pro_tip", ""), lang=active_lang)
        resolved_stages.append(rs)
    current_guide["stages"] = resolved_stages

    # 2. Filter tasks strictly matching the currently logged-in farmer's active crops
    current_tasks = session.get("crop_tasks")
    if current_tasks is None:
        current_tasks = generate_starter_tasks_for_crops(farmer_crops)
        session["crop_tasks"] = current_tasks

    # Filter tasks for active_crop tab (or all farmer crop tasks)
    # A task matches if its crop matches active_crop (by key or name)
    active_crop_display = current_guide["display_name"]
    filtered_tasks = []
    for tsk in current_tasks:
        tsk_crop_val = tsk.get("crop", "")
        tsk_key = detect_crop_key(tsk_crop_val)
        tsk_slug = get_crop_slug(tsk_crop_val)
        
        # Match against active crop tab
        if (active_crop == tsk_key) or (active_crop == tsk_slug) or (active_crop.lower() in str(tsk_crop_val).lower()):
            rt = copy.deepcopy(tsk)
            rt["title"] = pick(tsk.get("title", ""), lang=active_lang)
            rt["crop"] = pick(tsk.get("crop", ""), lang=active_lang)
            rt["stage"] = pick(tsk.get("stage", ""), lang=active_lang)
            rt["due_date"] = pick(tsk.get("due_date", ""), lang=active_lang)
            rt["priority"] = pick(tsk.get("priority", ""), lang=active_lang)
            filtered_tasks.append(rt)

    # If no tasks match this specific crop tab, show all tasks for farmer's active crops
    if not filtered_tasks:
        for tsk in current_tasks:
            rt = copy.deepcopy(tsk)
            rt["title"] = pick(tsk.get("title", ""), lang=active_lang)
            rt["crop"] = pick(tsk.get("crop", ""), lang=active_lang)
            rt["stage"] = pick(tsk.get("stage", ""), lang=active_lang)
            rt["due_date"] = pick(tsk.get("due_date", ""), lang=active_lang)
            rt["priority"] = pick(tsk.get("priority", ""), lang=active_lang)
            filtered_tasks.append(rt)

    return render_template(
        "crop_helper.html",
        farmer=farmer,
        active_crop=active_crop,
        active_crop_label=active_crop_display,
        current_guide=current_guide,
        all_crops=farmer_crop_tabs,
        farmer_crops_keys=list(farmer_crop_tabs.keys()),
        crop_tasks=filtered_tasks,
        active_nav="crop_helper"
    )


@app.route("/toggle-task/<task_id>", methods=["POST"])
def toggle_task(task_id):
    """Toggles task completed status in session['crop_tasks'] and TASKS_DB."""
    # 1. Update in session['crop_tasks']
    tasks_list = session.get("crop_tasks", [])
    for task in tasks_list:
        if task.get("id") == task_id:
            task["status"] = not task.get("status", False)
            break
    session["crop_tasks"] = tasks_list

    # 2. Also update global TASKS_DB if present
    for task in TASKS_DB:
        if task.get("id") == task_id:
            task["status"] = not task.get("status", False)
            break

    redirect_to = request.form.get("redirect") or request.referrer or url_for("dashboard")
    return redirect(redirect_to)


@app.route("/add-task", methods=["POST"])
def add_task():
    """Appends a new farming reminder task to session['crop_tasks'] and TASKS_DB."""
    title = request.form.get("title", "").strip()
    crop = request.form.get("crop", "Grapes").strip()
    due_date = request.form.get("due_date", "Pending").strip()
    priority = request.form.get("priority", "Medium").strip()
    current_crop = request.form.get("current_crop", crop)

    if title:
        tasks_list = session.get("crop_tasks")
        if tasks_list is None:
            farmer = get_current_farmer()
            tasks_list = generate_starter_tasks_for_crops(farmer.get("crops_grown", []))

        new_id = f"TSK-{len(tasks_list) + 1:02d}"
        new_task = {
            "id": new_id,
            "crop": crop,
            "title": title,
            "stage": "Custom Reminder",
            "due_date": due_date,
            "priority": priority,
            "status": False
        }
        tasks_list.insert(0, new_task)
        session["crop_tasks"] = tasks_list
        TASKS_DB.insert(0, new_task)
        flash(t("task_saved_success"), "success")

    return redirect(url_for("crop_helper", crop=current_crop))


# ---------------------------------------------------------
# MODULE 4: NEARBY AGRICULTURAL SERVICES
# ---------------------------------------------------------
@app.route("/nearby-services")
def nearby_services():
    """Local agricultural services directory with category and taluka filters."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))

    farmer = get_current_farmer()

    # Extract filter parameters
    selected_category = request.args.get("cat", "").strip()
    selected_taluka = request.args.get("taluka", "").strip()
    search_query = request.args.get("q", "").strip().lower()
    active_lang = session.get("lang", "mr")

    # Build resolved (string) versions for filtering and display
    resolved_services = []
    for srv in SERVICES_DB:
        resolved = copy.deepcopy(srv)
        resolved["name"] = pick(srv.get("name", ""), lang=active_lang)
        resolved["category"] = pick(srv.get("category", ""), lang=active_lang)
        resolved["taluka"] = pick(srv.get("taluka", ""), lang=active_lang)
        resolved["district"] = pick(srv.get("district", ""), lang=active_lang)
        resolved["location"] = pick(srv.get("location", ""), lang=active_lang)
        resolved["timings"] = pick(srv.get("timings", ""), lang=active_lang)
        resolved["speciality"] = pick(srv.get("speciality", ""), lang=active_lang)
        resolved_services.append(resolved)

    # Unique categories and talukas for filter controls (resolved strings)
    all_categories = sorted(list(set(r["category"] for r in resolved_services)))
    all_talukas = sorted(list(set(r["taluka"] for r in resolved_services)))

    # Filter logic (on resolved strings)
    filtered = []
    for resolved in resolved_services:
        if selected_category and resolved["category"] != selected_category:
            continue
        if selected_taluka and resolved["taluka"] != selected_taluka:
            continue
        if search_query:
            searchable_text = f"{resolved['name']} {resolved['speciality']} {resolved['location']}".lower()
            if search_query not in searchable_text:
                continue
        filtered.append(resolved)

    return render_template(
        "nearby_services.html",
        farmer=farmer,
        services=filtered,
        categories=all_categories,
        talukas=all_talukas,
        selected_category=selected_category,
        selected_taluka=selected_taluka,
        search_query=search_query,
        active_nav="nearby_services"
    )


@app.route("/add-service", methods=["POST"])
def add_service():
    """Registers a new service provider directly into in-memory SERVICES_DB."""
    name = request.form.get("name", "").strip()
    category = request.form.get("category", "").strip()
    taluka = request.form.get("taluka", "Niphad").strip()
    location = request.form.get("location", "").strip()
    phone = request.form.get("phone", "").strip()
    timings = request.form.get("timings", "9:00 AM - 6:00 PM").strip()
    speciality = request.form.get("speciality", "").strip()

    if name and phone:
        new_id = f"SRV-{len(SERVICES_DB) + 1:02d}"
        SERVICES_DB.append({
            "id": new_id,
            "name": name,
            "category": category,
            "taluka": taluka,
            "district": "Nashik",
            "location": location,
            "phone": phone,
            "timings": timings,
            "speciality": speciality,
            "rating": 5.0,
            "verified": True
        })
        flash(t("service_saved_success"), "success")

    return redirect(url_for("nearby_services"))


# ---------------------------------------------------------
# MODULE 3: MULTILINGUAL FARMER AI ASSISTANT
# ---------------------------------------------------------
@app.route("/ai-assistant")
def ai_assistant():
    """Module 3: Multilingual Farmer AI Assistant with Live Farm Data Context."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))

    farmer = get_current_farmer()
    chat_history = session.get("chat_history", [])
    return render_template(
        "ai_assistant.html",
        farmer=farmer,
        chat_history=chat_history,
        active_nav="ai_assistant"
    )


@app.route("/ai-assistant/ask", methods=["POST"])
def ai_assistant_ask():
    """Processes farmer's query and routes to the appropriate knowledge domain or module."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))

    query = request.form.get("query", "").strip()
    if not query:
        return redirect(url_for("ai_assistant"))

    farmer = get_current_farmer()
    active_lang = session.get("lang", "mr")

    # Compute live farm context figures
    current_month_spend = sum(
        float(e.get("amount", 0))
        for e in EXPENSES_DB
        if "11" in str(e.get("date", ""))[:7]
    )
    total_spend = sum(float(e.get("amount", 0)) for e in EXPENSES_DB)

    # Compute top category
    cat_counts = {}
    for e in EXPENSES_DB:
        c_en = pick(e.get("category", ""), lang="en")
        c_mr = pick(e.get("category", ""), lang="mr")
        amt = float(e.get("amount", 0))
        cat_counts[(c_en, c_mr)] = cat_counts.get((c_en, c_mr), 0) + amt
    top_cat = max(cat_counts.items(), key=lambda x: x[1])[0] if cat_counts else ("Fertilizers & Nutrients", "खते व पोषण")

    # Livestock overdue calculations
    today = datetime.date.today()
    overdue_count = 0
    overdue_names = []
    for a in LIVESTOCK_DB:
        for v in a.get("vaccination_history", []):
            try:
                due = datetime.datetime.strptime(v.get("due_date", ""), "%Y-%m-%d").date()
                if (due - today).days < 0:
                    overdue_count += 1
                    a_name = pick(a.get("name", ""), lang=active_lang)
                    v_name = pick(v.get("vaccine", ""), lang=active_lang)
                    overdue_names.append(f"{a_name} ({v_name})")
            except Exception:
                pass

    farmer_crops = farmer.get("crops_grown", [])
    crops_en = ", ".join(pick(c, lang="en") for c in farmer_crops)
    crops_mr = ", ".join(pick(c, lang="mr") for c in farmer_crops)
    pending_tasks = len([t for t in TASKS_DB if not t.get("status", False)])

    live_context = {
        "expenses": {
            "current_month_spend": int(current_month_spend),
            "total_spend": int(total_spend),
            "top_category_en": top_cat[0],
            "top_category_mr": top_cat[1]
        },
        "livestock": {
            "total_animals": len(LIVESTOCK_DB),
            "daily_milk": round(sum(float(a.get("daily_milk_yield_litres", 0)) for a in LIVESTOCK_DB), 1),
            "overdue_count": overdue_count,
            "overdue_details": ", ".join(overdue_names) if overdue_names else "None"
        },
        "crops": {
            "crops_en": crops_en,
            "crops_mr": crops_mr,
            "pending_tasks": pending_tasks
        },
        "services": {
            "total_services": len(SERVICES_DB),
            "sample_en": "Dr. Deshmukh Vet Clinic & Kisan Krishi Seva Kendra",
            "sample_mr": "डॉ. देशमुख पशुवैद्यक क्लिनिक व किसान कृषी सेवा केंद्र"
        },
        "marketplace": {
            "total_listings": len(MARKETPLACE_DB)
        }
    }

    result = route_farmer_query(query, farmer, live_context, lang=active_lang)

    # Save to session chat history
    chat_history = session.get("chat_history", [])
    chat_history.append({"role": "user", "text": query})
    chat_history.append({
        "role": "assistant",
        "text": result.get("response_text", ""),
        "recommended_module": result.get("recommended_module"),
        "intent": result.get("intent", "")
    })
    session["chat_history"] = chat_history
    session.modified = True

    return redirect(url_for("ai_assistant"))


@app.route("/ai-assistant/clear", methods=["POST"])
def ai_assistant_clear():
    """Clears assistant chat history from session."""
    session.pop("chat_history", None)
    session.modified = True
    return redirect(url_for("ai_assistant"))


# ---------------------------------------------------------
# MODULE 5: FARMER-TO-BUYER MARKETPLACE
# ---------------------------------------------------------
@app.route("/marketplace")
def marketplace():
    """Module 5: Direct Farmer-to-Buyer Produce Marketplace."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))

    farmer = get_current_farmer()
    active_lang = session.get("lang", "mr")

    selected_category = request.args.get("cat", "").strip()
    search_query = request.args.get("q", "").strip().lower()

    # Resolve all listings to active language
    resolved_listings = []
    for item in MARKETPLACE_DB:
        ri = copy.deepcopy(item)
        ri["crop_name"] = pick(item.get("crop_name", ""), lang=active_lang)
        ri["category"] = pick(item.get("category", ""), lang=active_lang)
        ri["variety"] = pick(item.get("variety", ""), lang=active_lang)
        ri["quality_grade"] = pick(item.get("quality_grade", ""), lang=active_lang)
        ri["seller_name"] = pick(item.get("seller_name", ""), lang=active_lang)
        ri["village"] = pick(item.get("village", ""), lang=active_lang)
        ri["taluka"] = pick(item.get("taluka", ""), lang=active_lang)
        ri["district"] = pick(item.get("district", ""), lang=active_lang)
        ri["status"] = pick(item.get("status", ""), lang=active_lang)
        ri["notes"] = pick(item.get("notes", ""), lang=active_lang)

        # Category matching: check both en and mr versions of category
        raw_cat_en = pick(item.get("category", ""), lang="en")
        raw_cat_mr = pick(item.get("category", ""), lang="mr")
        if selected_category and (selected_category not in (raw_cat_en, raw_cat_mr, ri["category"])):
            continue

        # Search matching: crop_name, village, taluka, variety
        if search_query:
            searchable = f"{ri['crop_name']} {ri['variety']} {ri['village']} {ri['taluka']} {ri['quality_grade']}".lower()
            if search_query not in searchable:
                continue

        resolved_listings.append(ri)

    # Compute overall statistics
    total_volume = sum(int(i.get("quantity_quintals", 0)) for i in MARKETPLACE_DB)
    avg_price = int(sum(float(i.get("expected_price_per_quintal", 0)) for i in MARKETPLACE_DB) / len(MARKETPLACE_DB)) if MARKETPLACE_DB else 0

    return render_template(
        "marketplace.html",
        farmer=farmer,
        listings=resolved_listings,
        selected_category=selected_category,
        search_query=request.args.get("q", "").strip(),
        total_volume=total_volume,
        avg_price=avg_price,
        active_nav="marketplace"
    )


@app.route("/marketplace/add", methods=["POST"])
def add_marketplace_listing():
    """Adds a new produce harvest lot to in-memory MARKETPLACE_DB."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))

    farmer = get_current_farmer()
    crop_name = request.form.get("crop_name", "").strip()
    category = request.form.get("category", "Vegetables").strip()
    variety = request.form.get("variety", "").strip()
    qty_str = request.form.get("quantity_quintals", "10").strip()
    price_str = request.form.get("expected_price", "2000").strip()
    quality_grade = request.form.get("quality_grade", "Grade A").strip()
    seller_phone = request.form.get("seller_phone", farmer.get("phone", "")).strip()
    notes = request.form.get("notes", "").strip()

    try:
        qty = int(qty_str)
    except ValueError:
        qty = 10

    try:
        price = float(price_str)
    except ValueError:
        price = 2000.0

    today = datetime.date.today().strftime("%Y-%m-%d")
    new_id = f"MKT-{len(MARKETPLACE_DB) + 101}"

    new_listing = {
        "id": new_id,
        "crop_name": {"en": crop_name, "mr": crop_name},
        "category": {"en": category, "mr": pick(category, lang="mr")},
        "variety": {"en": variety, "mr": variety},
        "quality_grade": {"en": quality_grade, "mr": quality_grade},
        "quantity_quintals": qty,
        "expected_price_per_quintal": price,
        "seller_name": farmer.get("name", {"en": "Farmer", "mr": "शेतकरी"}),
        "seller_phone": seller_phone,
        "village": farmer.get("village", {"en": "Niphad", "mr": "निफाड"}),
        "taluka": farmer.get("taluka", {"en": "Niphad", "mr": "निफाड"}),
        "district": farmer.get("district", {"en": "Nashik", "mr": "नाशिक"}),
        "location": {"en": "Niphad, Nashik", "mr": "निफाड, नाशिक"},
        "harvest_date": today,
        "status": {"en": "Available", "mr": "उपलब्ध"},
        "notes": {"en": notes, "mr": notes}
    }

    MARKETPLACE_DB.insert(0, new_listing)
    flash(t("mkt_added_success"), "success")
    return redirect(url_for("marketplace"))


# ---------------------------------------------------------
# MODULE 6: LIVESTOCK RECORDS & VACCINES
# ---------------------------------------------------------
@app.route("/livestock")
def livestock():
    """Digital registry for farm cattle and goats with automated vaccination schedules."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))

    farmer = get_current_farmer()
    today = datetime.date.today()
    active_lang = session.get("lang", "mr")

    total_animals = len(LIVESTOCK_DB)
    total_milk = sum(float(a.get("daily_milk_yield_litres", 0)) for a in LIVESTOCK_DB)
    
    overdue_count = 0
    upcoming_count = 0
    
    processed_animals = []
    for animal in LIVESTOCK_DB:
        animal_copy = copy.deepcopy(animal)
        # Resolve bilingual string fields
        animal_copy["name"] = pick(animal.get("name", ""), lang=active_lang)
        animal_copy["type"] = pick(animal.get("type", ""), lang=active_lang)
        animal_copy["breed"] = pick(animal.get("breed", ""), lang=active_lang)
        animal_copy["health_status"] = pick(animal.get("health_status", ""), lang=active_lang)

        processed_vaccines = []
        has_overdue = False
        has_upcoming = False
        
        for v in animal.get("vaccination_history", []):
            v_copy = copy.deepcopy(v)
            # Resolve vaccine name bilingually
            v_copy["vaccine"] = pick(v.get("vaccine", ""), lang=active_lang)
            # For form submission we still need the en key for route matching
            v_copy["vaccine_key"] = pick(v.get("vaccine", ""), lang="en")

            due_str = v.get("due_date", "")
            days_diff = None
            status_code = "uptodate"
            
            try:
                due_date = datetime.datetime.strptime(due_str, "%Y-%m-%d").date()
                days_diff = (due_date - today).days
                if days_diff < 0:
                    status_code = "overdue"
                    has_overdue = True
                    overdue_count += 1
                    badge_class = "bg-red-50 text-red-700 border-red-200"
                    badge_label = t("status_overdue_badge")
                    badge_icon = "alert-circle"
                elif days_diff <= 14:
                    status_code = "upcoming"
                    has_upcoming = True
                    upcoming_count += 1
                    badge_class = "bg-amber-50 text-amber-700 border-amber-200"
                    badge_label = t("status_upcoming_badge")
                    badge_icon = "clock"
                else:
                    status_code = "uptodate"
                    badge_class = "bg-emerald-50 text-emerald-700 border-emerald-200"
                    badge_label = t("status_uptodate_badge")
                    badge_icon = "check-circle"
            except Exception:
                badge_class = "bg-slate-100 text-slate-600 border-slate-200"
                badge_label = t("status_uptodate_badge")
                badge_icon = "check"

            v_copy["days_diff"] = days_diff
            v_copy["status_code"] = status_code
            v_copy["badge_class"] = badge_class
            v_copy["badge_label"] = badge_label
            v_copy["badge_icon"] = badge_icon
            processed_vaccines.append(v_copy)
            
        if animal.get("registration_status") == "Registration pending":
            animal_copy["overall_badge_class"] = "bg-amber-100 text-amber-800 border-amber-300"
            animal_copy["overall_status_text"] = t("status_reg_pending")
            animal_copy["overall_icon"] = "clock"
            animal_copy["is_pending"] = True
        elif has_overdue:
            animal_copy["overall_badge_class"] = "bg-red-50 text-red-700 border-red-200"
            animal_copy["overall_status_text"] = t("health_attention")
            animal_copy["overall_icon"] = "alert-triangle"
        elif has_upcoming:
            animal_copy["overall_badge_class"] = "bg-amber-50 text-amber-700 border-amber-200"
            animal_copy["overall_status_text"] = t("status_upcoming_badge")
            animal_copy["overall_icon"] = "clock"
        else:
            animal_copy["overall_badge_class"] = "bg-emerald-50 text-emerald-700 border-emerald-200"
            animal_copy["overall_status_text"] = t("health_healthy")
            animal_copy["overall_icon"] = "check-circle"
            
        animal_copy["processed_vaccines"] = processed_vaccines
        processed_animals.append(animal_copy)

    return render_template(
        "livestock.html",
        farmer=farmer,
        animals=processed_animals,
        total_animals=total_animals,
        total_milk=total_milk,
        overdue_count=overdue_count,
        upcoming_count=upcoming_count,
        today_str=today.strftime("%Y-%m-%d"),
        active_nav="livestock"
    )


@app.route("/livestock/vaccinate", methods=["POST"])
def vaccinate_animal():
    """Marks a vaccine completed and updates the next due date using datetime math."""
    animal_id = request.form.get("animal_id", "").strip()
    vaccine_name = request.form.get("vaccine_name", "").strip()  # always en key
    today = datetime.date.today()

    for animal in LIVESTOCK_DB:
        if animal.get("tag_id") == animal_id:
            for v in animal.get("vaccination_history", []):
                # vaccine field may be a dict or a plain string — resolve to en for comparison
                v_en = pick(v.get("vaccine", ""), lang="en")
                if v_en == vaccine_name or v.get("vaccine") == vaccine_name:
                    v["date_given"] = today.strftime("%Y-%m-%d")
                    # Biannual (180 days) for FMD/BQ/HS, 365 days for Brucellosis/others
                    name_lower = vaccine_name.lower()
                    if "fmd" in name_lower or "bq" in name_lower or "hs" in name_lower:
                        next_due = today + datetime.timedelta(days=180)
                    else:
                        next_due = today + datetime.timedelta(days=365)
                    v["due_date"] = next_due.strftime("%Y-%m-%d")
                    v["status"] = "Up-to-Date"
                    break
            break

    flash(t("vaccine_updated_success"), "success")
    return redirect(url_for("livestock"))


@app.route("/livestock/add", methods=["POST"])
def add_animal():
    """Adds a new animal to the in-memory livestock registry."""
    tag_id = request.form.get("tag_id", "").strip()
    name = request.form.get("name", "").strip()
    animal_type = request.form.get("type", "Cow").strip()
    breed = request.form.get("breed", "Gir").strip()
    age_years = float(request.form.get("age_years", 3.0))
    daily_milk = float(request.form.get("daily_milk", 8.0))
    initial_vaccine = request.form.get("initial_vaccine", "FMD").strip()
    
    today = datetime.date.today()
    if not tag_id:
        tag_id = f"MH-NSK-0{len(LIVESTOCK_DB) + 1:02d}"

    vaccine_labels = {
        "FMD": "Foot & Mouth Disease (FMD)",
        "HS": "Hemorrhagic Septicemia (HS)",
        "BQ": "Black Quarter (BQ)",
        "Brucellosis": "Brucellosis"
    }
    v_name = vaccine_labels.get(initial_vaccine, "Foot & Mouth Disease (FMD)")
    due_date = today + datetime.timedelta(days=180)

    new_animal = {
        "tag_id": tag_id,
        "name": name if name else f"Animal {tag_id}",
        "type": animal_type,
        "breed": breed,
        "age_years": age_years,
        "daily_milk_yield_litres": daily_milk,
        "health_status": "Healthy",
        "vaccination_history": [
            {
                "vaccine": v_name,
                "date_given": today.strftime("%Y-%m-%d"),
                "due_date": due_date.strftime("%Y-%m-%d"),
                "status": "Up-to-Date"
            }
        ]
    }
    
    LIVESTOCK_DB.append(new_animal)

    # Sync with farmer profile livestock summary
    farmer = get_current_farmer()
    livestock_sum = farmer.setdefault("livestock_summary", {})
    livestock_sum["total_animals"] = len(LIVESTOCK_DB)
    livestock_sum["daily_milk_litres"] = sum(float(a.get("daily_milk_yield_litres", 0)) for a in LIVESTOCK_DB)

    flash(t("animal_added_success"), "success")
    return redirect(url_for("livestock"))


@app.route("/livestock/complete-pending", methods=["POST"])
def complete_pending_livestock():
    """Updates pending livestock record with official tag and agronomic details."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))

    animal_id = request.form.get("animal_id", "").strip()
    official_tag = request.form.get("official_tag", "").strip()
    breed = request.form.get("breed", "").strip()
    age_str = request.form.get("age_years", "").strip()
    milk_str = request.form.get("daily_milk", "").strip()
    vax_name = request.form.get("vaccine_name", "").strip()
    vax_date = request.form.get("vaccine_date", "").strip()

    today = datetime.date.today()
    updated = False
    for animal in LIVESTOCK_DB:
        if animal.get("tag_id") == animal_id:
            if official_tag:
                animal["tag_id"] = official_tag
                animal["registration_status"] = "Registered"
                animal["health_status"] = {"en": "Registered & Active", "mr": "नोंदणीकृत व सक्रिय"}
            if breed:
                animal["breed"] = {"en": breed, "mr": breed}
            if age_str:
                try:
                    animal["age_years"] = float(age_str)
                except ValueError:
                    pass
            if milk_str:
                try:
                    animal["daily_milk_yield_litres"] = float(milk_str)
                except ValueError:
                    pass
            if vax_name:
                animal["vaccination_history"] = [{
                    "vaccine": {"en": vax_name, "mr": vax_name},
                    "date_given": vax_date or today.strftime("%Y-%m-%d"),
                    "due_date": (today + datetime.timedelta(days=180)).strftime("%Y-%m-%d"),
                    "status": "Up-to-Date"
                }]
            updated = True
            flash(t("animal_added_success"), "success")
            break

    if not updated:
        flash("Could not find the animal record to update.", "error")

    return redirect(url_for("livestock"))


# ---------------------------------------------------------
# MODULE 7: FARM EXPENSE TRACKER & ANALYTICS
# ---------------------------------------------------------
@app.route("/expenses")
def expenses():
    """Farm expense tracker with multi-dimensional reports and Chart.js analytics."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))

    farmer = get_current_farmer()
    today = datetime.date.today()
    active_lang = session.get("lang", "mr")

    # Resolve all bilingual fields in expenses to pure active-language strings
    resolved_expenses = []
    for e in EXPENSES_DB:
        re = copy.deepcopy(e)
        re["category"] = pick(e.get("category", ""), lang=active_lang)
        re["crop"] = pick(e.get("crop", ""), lang=active_lang)
        re["month"] = pick(e.get("month", ""), lang=active_lang)
        re["season"] = pick(e.get("season", ""), lang=active_lang)
        re["description"] = pick(e.get("description", ""), lang=active_lang)
        re["payment_mode"] = pick(e.get("payment_mode", ""), lang=active_lang)
        resolved_expenses.append(re)

    total_spend = sum(float(e.get("amount", 0)) for e in EXPENSES_DB)
    total_entries = len(EXPENSES_DB)

    # Current month detection (November = month 11)
    current_month_spend = sum(
        float(e.get("amount", 0))
        for e in EXPENSES_DB
        if "11" in str(e.get("date", ""))[:7]
    )

    # 1. Category aggregation (use resolved strings as keys)
    cat_map = {}
    for idx, e in enumerate(EXPENSES_DB):
        cat = resolved_expenses[idx]["category"]
        amt = float(e.get("amount", 0))
        if cat not in cat_map:
            cat_map[cat] = {"amount": 0, "count": 0}
        cat_map[cat]["amount"] += amt
        cat_map[cat]["count"] += 1

    category_stats = []
    for cat_name, data in sorted(cat_map.items(), key=lambda x: x[1]["amount"], reverse=True):
        share = round((data["amount"] / total_spend * 100), 1) if total_spend > 0 else 0
        category_stats.append({
            "name": cat_name,
            "amount": int(data["amount"]),
            "count": data["count"],
            "share": share
        })

    top_cat = category_stats[0] if category_stats else {"name": t("none_label") if t("none_label") != "none_label" else "None", "amount": 0, "share": 0}

    # 2. Crop aggregation (use resolved strings)
    crop_map = {}
    for idx, e in enumerate(EXPENSES_DB):
        c = resolved_expenses[idx]["crop"]
        amt = float(e.get("amount", 0))
        if c not in crop_map:
            crop_map[c] = {"amount": 0, "count": 0}
        crop_map[c]["amount"] += amt
        crop_map[c]["count"] += 1

    crop_stats = []
    for crop_name, data in sorted(crop_map.items(), key=lambda x: x[1]["amount"], reverse=True):
        share = round((data["amount"] / total_spend * 100), 1) if total_spend > 0 else 0
        crop_stats.append({
            "name": crop_name,
            "amount": int(data["amount"]),
            "count": data["count"],
            "share": share
        })

    top_crop = crop_stats[0] if crop_stats else {"name": "None", "amount": 0, "share": 0}

    # 3. Monthly aggregation (resolved month labels)
    month_map = {}
    month_order_en = ["September 2026", "October 2026", "November 2026"]
    month_order_mr = ["सप्टेंबर २०२६", "ऑक्टोबर २०२६", "नोव्हेंबर २०२६"]
    month_order = month_order_mr if active_lang == "mr" else month_order_en

    for idx, e in enumerate(EXPENSES_DB):
        m = resolved_expenses[idx]["month"]
        amt = float(e.get("amount", 0))
        month_map[m] = month_map.get(m, 0) + amt

    sorted_months = sorted(month_map.keys(), key=lambda x: month_order.index(x) if x in month_order else 99)

    # 4. Seasonal aggregation (resolved season labels)
    season_map = {}
    for idx, e in enumerate(EXPENSES_DB):
        s = resolved_expenses[idx]["season"]
        amt = float(e.get("amount", 0))
        if s not in season_map:
            season_map[s] = {"amount": 0, "count": 0}
        season_map[s]["amount"] += amt
        season_map[s]["count"] += 1

    season_stats = []
    for s_name, data in sorted(season_map.items(), key=lambda x: x[1]["amount"], reverse=True):
        share = round((data["amount"] / total_spend * 100), 1) if total_spend > 0 else 0
        season_stats.append({
            "name": s_name,
            "amount": int(data["amount"]),
            "count": data["count"],
            "share": share
        })

    # Prepare Chart.js datasets (pure active-language labels)
    chart_cat_labels = [c["name"] for c in category_stats]
    chart_cat_data = [c["amount"] for c in category_stats]

    # Chart month labels: use short month name only (e.g. "September" → "Sep" or "सप्टेंबर")
    chart_month_labels = [m.split(" ")[0] for m in sorted_months]
    chart_month_data = [int(month_map[m]) for m in sorted_months]

    # Resolve EXPENSE_CATEGORIES for the Add modal dropdown
    resolved_categories = [pick(cat, lang=active_lang) for cat in EXPENSE_CATEGORIES]

    # Sort expenses by date desc, with resolved bilingual fields
    sorted_expenses = sorted(resolved_expenses, key=lambda x: x.get("date", ""), reverse=True)

    return render_template(
        "expenses.html",
        farmer=farmer,
        expenses=sorted_expenses,
        all_categories=resolved_categories,
        total_spend=int(total_spend),
        total_entries=total_entries,
        current_month_spend=int(current_month_spend),
        top_category_name=top_cat["name"],
        top_category_amount=top_cat["amount"],
        top_category_share=top_cat["share"],
        top_crop_name=top_crop["name"],
        top_crop_amount=top_crop["amount"],
        top_crop_share=top_crop["share"],
        category_stats=category_stats,
        crop_stats=crop_stats,
        season_stats=season_stats,
        chart_category_labels=chart_cat_labels,
        chart_category_data=chart_cat_data,
        chart_monthly_labels=chart_month_labels,
        chart_monthly_data=chart_month_data,
        today_str=today.strftime("%Y-%m-%d"),
        active_nav="expense_tracker"
    )


@app.route("/expenses/add", methods=["POST"])
def add_expense():
    """Logs a new farm expenditure directly to in-memory EXPENSES_DB."""
    amount_str = request.form.get("amount", "0").strip()
    date_str = request.form.get("date", "").strip()
    category = request.form.get("category", "Fertilizers & Nutrients").strip()
    season = request.form.get("season", "Rabi 2026-27").strip()
    crop = request.form.get("crop", "Grapes").strip()
    payment_mode = request.form.get("payment_mode", "UPI").strip()
    description = request.form.get("description", "").strip()

    try:
        amount = float(amount_str)
    except ValueError:
        amount = 0.0

    today = datetime.date.today()
    if not date_str:
        date_str = today.strftime("%Y-%m-%d")

    try:
        month_str = datetime.datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %Y")
    except Exception:
        month_str = today.strftime("%B %Y")

    new_id = f"EXP-{len(EXPENSES_DB) + 1:03d}"
    new_expense = {
        "id": new_id,
        "date": date_str,
        "month": month_str,
        "season": season,
        "crop": crop,
        "category": category,
        "description": description if description else f"{category.split('(')[0]} for {crop}",
        "amount": amount,
        "payment_mode": payment_mode
    }
    
    EXPENSES_DB.insert(0, new_expense)
    flash(t("expense_added_success"), "success")
    return redirect(url_for("expenses"))


@app.route("/expenses/delete/<expense_id>", methods=["POST"])
def delete_expense(expense_id):
    """Removes an expense record from in-memory EXPENSES_DB."""
    global EXPENSES_DB
    EXPENSES_DB = [e for e in EXPENSES_DB if e.get("id") != expense_id]
    flash(t("expense_deleted_success"), "success")
    return redirect(url_for("expenses"))


# ---------------------------------------------------------
# SARVAM AI FEATURES: 1-LINE SMART EXPENSE & TEXT-TO-SPEECH
# ---------------------------------------------------------
@app.route("/expenses/smart-add", methods=["POST"])
def smart_add_expense():
    """Parses 1-line natural language text via Sarvam AI and logs to EXPENSES_DB."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))

    raw_text = request.form.get("smart_text", "").strip()
    if not raw_text:
        return redirect(url_for("expenses"))

    active_lang = session.get("lang", "mr")
    from sarvam_client import parse_smart_expense
    parsed = parse_smart_expense(raw_text, active_lang=active_lang)

    if parsed and parsed.get("amount", 0) > 0:
        today = datetime.date.today()
        month_str = today.strftime("%B %Y")
        new_id = f"EXP-{len(EXPENSES_DB) + 1:03d}"
        new_expense = {
            "id": new_id,
            "date": today.strftime("%Y-%m-%d"),
            "month": month_str,
            "season": parsed.get("season", "Rabi 2026-27"),
            "crop": parsed.get("crop", "General Farm"),
            "category": parsed.get("category", "Fertilizers & Nutrients"),
            "description": parsed.get("description", {}),
            "amount": float(parsed.get("amount", 0)),
            "payment_mode": parsed.get("payment_mode", "Cash")
        }
        EXPENSES_DB.insert(0, new_expense)
        flash(t("expense_added_success"), "success")
    else:
        flash("Could not parse expense text. Please try again or use standard form.", "error")

    return redirect(url_for("expenses"))


@app.route("/smart-log", methods=["GET"])
def smart_log():
    """Renders Universal Smart Voice & Text Log page."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))

    farmer = get_current_farmer()
    result = session.pop("smart_log_result", None)

    return render_template(
        "smart_log.html",
        farmer=farmer,
        active_nav="smart_log",
        result=result
    )


@app.route("/smart-log/submit", methods=["POST"])
def smart_log_submit():
    """Processes natural language input across multiple modules."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))

    raw_text = request.form.get("raw_text", "").strip()
    if not raw_text:
        flash("Please enter or speak a log statement.", "error")
        return redirect(url_for("smart_log"))

    farmer = get_current_farmer()
    active_lang = session.get("lang", "mr")

    in_memory_dbs = {
        "livestock": LIVESTOCK_DB,
        "expenses": EXPENSES_DB,
        "marketplace": MARKETPLACE_DB,
        "tasks": TASKS_DB
    }

    result = extract_and_dispatch(raw_text, farmer, in_memory_dbs, active_lang=active_lang)
    session["smart_log_result"] = result

    if result.get("success"):
        flash(t("smart_log_result_success"), "success")
        if result.get("has_pending_cattle"):
            flash(t("smart_log_cattle_pending_alert"), "warning")
    else:
        flash(t("smart_log_empty_prompt"), "error")

    return redirect(url_for("smart_log"))


# Global in-memory storage for active digitized form sessions: { phone_or_session_id: form_dict }
FORM_SESSIONS = {}


# ---------------------------------------------------------
# FLAGSHIP MODULE: SMART FORM DIGITIZER & AUTO-FILLER
# ---------------------------------------------------------
@app.route("/form-filler", methods=["GET"])
def form_filler():
    """Renders the Smart Form Digitizer & Auto-Filler interface."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))

    user_id = session.get("phone", "demo_user")

    # Explicit reset query param handler
    if request.args.get("reset") == "1":
        FORM_SESSIONS.pop(user_id, None)
        session.pop("has_form", None)
        session.pop("form_is_generated", None)
        session.modified = True
        return redirect(url_for("form_filler"))

    # Explicit edit query param handler
    if request.args.get("edit") == "1":
        session["form_is_generated"] = False
        session.modified = True

    farmer = get_current_farmer()
    
    # Retrieve form data primarily from lightweight in-memory dictionary
    form_data = FORM_SESSIONS.get(user_id)
    is_generated = session.get("form_is_generated", False)

    # Dictionary of field values for quick template lookups
    form_dict = {}
    if form_data and "fields" in form_data:
        for f in form_data["fields"]:
            form_dict[f["field_id"]] = f.get("value", "")

    today_str = datetime.date.today().strftime("%d / %m / %Y")

    return render_template(
        "form_filler.html",
        farmer=farmer,
        active_nav="form_filler",
        form_data=form_data,
        form_dict=form_dict,
        is_generated=is_generated,
        current_date=today_str
    )


@app.route("/form-filler/reset", methods=["GET", "POST"])
def form_filler_reset():
    """Resets active form session in server memory and session, returning to Step 1 upload screen."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))

    user_id = session.get("phone", "demo_user")
    FORM_SESSIONS.pop(user_id, None)
    session.pop("has_form", None)
    session.pop("form_is_generated", None)
    session.modified = True
    flash(t("form_filler_reset_success"), "info")
    return redirect(url_for("form_filler"))


@app.route("/form-filler/edit", methods=["GET", "POST"])
def form_filler_edit():
    """Switches view back to Step 2 digital form editor while preserving all entered values."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))

    session["form_is_generated"] = False
    session.modified = True
    return redirect(url_for("form_filler"))


@app.route("/form-filler/sample", methods=["GET", "POST"])
def form_filler_sample():
    """Direct route for 1-click PM-KISAN / Pik Vima Sample Form testing."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))

    farmer = get_current_farmer()
    active_lang = session.get("lang", "mr")
    user_id = session.get("phone", "demo_user")

    # Digitize sample form immediately into server memory
    parsed_form = digitize_form("sample_pmkisan_form.png", farmer, active_lang=active_lang, is_sample=True)
    FORM_SESSIONS[user_id] = parsed_form
    session["has_form"] = True
    session["form_is_generated"] = False
    session.modified = True
    flash(t("form_filler_success"), "success")

    return redirect(url_for("form_filler"))


@app.route("/form-filler/scan", methods=["POST"])
def form_filler_scan():
    """Handles upload of form photo or 1-click sample form scan."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))

    farmer = get_current_farmer()
    active_lang = session.get("lang", "mr")
    user_id = session.get("phone", "demo_user")
    use_sample = request.form.get("use_sample") == "true" or request.args.get("sample") == "1"

    uploads_dir = Path(__file__).parent / "static" / "uploads"
    try:
        uploads_dir.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

    if use_sample or "form_image" not in request.files or not request.files["form_image"].filename:
        # Use sample pre-generated PM-KISAN form
        target_path = uploads_dir / "sample_pmkisan_form.png"
    else:
        file = request.files["form_image"]
        safe_filename = f"upload_{int(datetime.datetime.now().timestamp())}_{file.filename}"
        target_path = uploads_dir / safe_filename
        try:
            file.save(str(target_path))
        except Exception:
            target_path = uploads_dir / "sample_pmkisan_form.png"

    # Parse and auto-fill from farmer profile into server memory
    parsed_form = digitize_form(str(target_path), farmer, active_lang=active_lang, is_sample=use_sample)
    FORM_SESSIONS[user_id] = parsed_form
    session["has_form"] = True
    session["form_is_generated"] = False
    session.modified = True
    flash(t("form_filler_success"), "success")

    return redirect(url_for("form_filler"))


@app.route("/form-filler/generate", methods=["POST"])
def form_filler_generate():
    """Collects reviewed/edited digital form inputs and locks completed document state."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))

    user_id = session.get("phone", "demo_user")
    form_data = FORM_SESSIONS.get(user_id)
    if not form_data:
        return redirect(url_for("form_filler"))

    # Update field values with farmer's edits in server memory
    for field in form_data.get("fields", []):
        field_id = field.get("field_id")
        ftype = field.get("field_type")
        if ftype == "checkbox":
            posted_val = request.form.get(f"field_{field_id}")
            field["value"] = "checked" if posted_val else ""
        else:
            posted_val = request.form.get(f"field_{field_id}", "").strip()
            if posted_val:
                field["value"] = posted_val

    FORM_SESSIONS[user_id] = form_data
    session["form_is_generated"] = True
    session.modified = True
    flash("Application Form finalized and ready for Print / Download!", "success")

    return redirect(url_for("form_filler"))


@app.route("/form-filler/download")
def form_filler_download():
    """Generates and serves a standalone printable HTML document for download."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))

    user_id = session.get("phone", "demo_user")
    form_data = FORM_SESSIONS.get(user_id)
    farmer = get_current_farmer()
    active_lang = session.get("lang", "mr")

    if not form_data:
        return redirect(url_for("form_filler"))

    form_dict = {f["field_id"]: f.get("value", "") for f in form_data.get("fields", [])}
    today_str = datetime.date.today().strftime("%d-%m-%Y")

    scheme_title = (
        form_data.get("scheme_name", {}).get(active_lang)
        or form_data.get("scheme_name", {}).get("en")
        or "PM-KISAN Samman Nidhi & Pik Vima Application"
    )
    scheme_code = form_data.get("scheme_code", "MH-AGRI-2026")
    applicant_name = (
        form_dict.get("farmer_name")
        or form_dict.get("full_name")
        or form_dict.get("name")
        or pick(farmer.get("name", ""), lang=active_lang)
    )
    taluka_val = form_dict.get("taluka") or pick(farmer.get("taluka", ""), lang=active_lang)
    district_val = form_dict.get("district") or pick(farmer.get("district", ""), lang=active_lang)

    table_rows = ""
    for field in form_data.get("fields", []):
        lbl = (
            field.get("label", {}).get(active_lang)
            or field.get("label", {}).get("en")
            or field.get("field_id", "")
        )
        val = field.get("value", "")
        table_rows += f"<tr><td width='40%'><strong>{lbl}:</strong></td><td>{val}</td></tr>\n"

    html_content = f"""<!DOCTYPE html>
<html lang="{active_lang}">
<head>
<meta charset="UTF-8">
<title>Completed_Application_{applicant_name.replace(' ', '_')}_{today_str}</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #fff; margin: 20px; color: #111; }}
.container {{ max-width: 800px; margin: 0 auto; border: 2px solid #047857; padding: 24px; border-radius: 8px; }}
h2 {{ text-align: center; color: #064E3B; margin: 0 0 4px; }}
h3 {{ text-align: center; color: #047857; margin: 0 0 16px; font-size: 14px; text-transform: uppercase; }}
table {{ width: 100%; border-collapse: collapse; margin-top: 16px; font-size: 13px; }}
th, td {{ border: 1px solid #111; padding: 8px 12px; text-align: left; }}
th {{ background: #ECFDF5; color: #064E3B; font-weight: bold; }}
.sig-block {{ margin-top: 40px; display: flex; justify-content: space-between; }}
@media print {{ body {{ margin: 0; }} .container {{ border: none; }} }}
</style>
</head>
<body onload="window.print()">
<div class="container">
<h2>GOVERNMENT OF MAHARASHTRA • DEPARTMENT OF AGRICULTURE</h2>
<h3>{scheme_title} ({scheme_code})</h3>
<table>
<tr><th colspan="2">DIGITIZED APPLICATION DETAILS / अर्जाचा तपशील</th></tr>
{table_rows}
</table>
<div class="sig-block" style="display:flex; justify-content:space-between; margin-top:40px;">
<div><p>Place: {taluka_val}, {district_val}</p><p>Date: {today_str}</p></div>
<div style="text-align:center;"><p style="font-family:cursive; font-size:16px; margin:0;">{applicant_name}</p><p style="border-top:1px solid #000; padding-top:4px; margin:0;">Applicant Farmer Signature</p></div>
</div>
</div>
</body>
</html>"""

    from flask import Response
    return Response(
        html_content,
        mimetype="text/html",
        headers={"Content-Disposition": f"attachment;filename=Filled_Application_{today_str}.html"}
    )


@app.route("/api/stt", methods=["POST"])
def api_speech_to_text():
    """Speech-to-text endpoint powered by Sarvam AI saaras:v3."""
    if "audio" not in request.files:
        return {"status": "error", "message": "No audio file provided"}, 400

    audio_file = request.files["audio"]
    language_code = request.form.get("language_code", "mr-IN")

    from sarvam_client import speech_to_text
    audio_bytes = audio_file.read()
    transcript = speech_to_text(audio_bytes, language_code=language_code, model="saaras:v3")

    if transcript:
        return {"status": "ok", "transcript": transcript}
    return {"status": "error", "message": "STT conversion failed or offline"}, 500


@app.route("/api/tts", methods=["POST"])
def api_text_to_speech():
    """Generates speech via Sarvam AI bulbul:v3 with fallback notification."""
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    language_code = (data.get("language_code") or "mr-IN").strip()

    if not text:
        return {"status": "error", "message": "Text is required", "fallback": True}, 400

    from sarvam_client import text_to_speech
    audio_base64 = text_to_speech(text, language_code=language_code, speaker="ritu", model="bulbul:v3")

    if audio_base64:
        return {"status": "ok", "audio_base64": audio_base64, "fallback": False}
    return {"status": "fallback", "fallback": True}


# ---------------------------------------------------------
# FLAGSHIP MODULE: AI CROP & NUTRIENT DOCTOR
# ---------------------------------------------------------
@app.route("/disease-scanner", methods=["GET"])
def disease_scanner():
    """Renders the AI Crop & Nutrient Doctor interface."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))

    farmer = get_current_farmer()
    return render_template(
        "disease_scanner.html",
        farmer=farmer,
        active_nav="disease_scanner"
    )


@app.route("/api/analyze-plant", methods=["POST"])
def api_analyze_plant():
    """
    Analyzes leaf photo via Two-Stage Sarvam AI Vision + Maharashtra Agronomy Engine.
    Handles missing, null, or whitespace optional fields consistently.
    """
    if not session.get("is_authenticated"):
        return {"success": False, "message": "Unauthorized"}, 401

    data = request.get_json(silent=True) or {}
    image_base64 = (data.get("image_base64") or "").strip()
    triage_crop = (data.get("triage_crop") or "").strip()
    triage_leaf_age = (data.get("triage_leaf_age") or "").strip()
    triage_pattern = (data.get("triage_pattern") or "").strip()
    shc_note = (data.get("shc_note") or "").strip()
    active_lang = session.get("lang", "mr")

    from plant_doctor import analyze_plant_leaf
    farmer = get_current_farmer()

    result = analyze_plant_leaf(
        image_base64=image_base64,
        farmer_profile=farmer,
        triage_crop=triage_crop,
        triage_leaf_age=triage_leaf_age,
        triage_pattern=triage_pattern,
        shc_note=shc_note,
        active_lang=active_lang
    )

    return result


# ---------------------------------------------------------
# MODULE 11: REAL-TIME WEATHER & AGRONOMIC ADVISORY
# ---------------------------------------------------------
@app.route("/weather-advisory", methods=["GET"])
def weather_advisory_page():
    """Renders the real-time location-specific weather & agronomic advisory page."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))

    farmer = get_current_farmer()
    active_lang = session.get("lang", "mr")

    # Import weather advisory engine
    import weather_advisory

    # Determine location: check URL params, then fallback to farmer profile
    req_lat = request.args.get("lat")
    req_lon = request.args.get("lon")
    name_en = request.args.get("name_en")
    name_mr = request.args.get("name_mr")
    dist_param = request.args.get("district")
    tal_param = request.args.get("taluka")

    # If coordinates are provided in query
    if req_lat and req_lon:
        try:
            lat = float(req_lat)
            lon = float(req_lon)
            disp_en = name_en or f"Location ({lat:.4f}, {lon:.4f})"
            disp_mr = name_mr or f"स्थान ({lat:.4f}, {lon:.4f})"
            selected_loc = {
                "display_name": disp_mr if active_lang == "mr" else disp_en,
                "display_name_en": disp_en,
                "display_name_mr": disp_mr,
                "district_en": dist_param or "Maharashtra",
                "district_mr": dist_param or "महाराष्ट्र",
                "taluka_en": tal_param or "",
                "taluka_mr": tal_param or "",
                "lat": round(lat, 4),
                "lon": round(lon, 4)
            }
        except (ValueError, TypeError):
            req_lat, req_lon = None, None

    if not req_lat or not req_lon:
        # Fallback to farmer's profile village/taluka/district
        farmer_dist = pick(farmer.get("district", "Nashik"), lang="en")
        farmer_tal = pick(farmer.get("taluka", "Niphad"), lang="en")
        farmer_vil = pick(farmer.get("village", "Pimpalgaon Baswant"), lang="en")

        # Lookup coordinates in location database
        resolved_coords = None
        dist_entry = weather_advisory.MAHARASHTRA_LOCATIONS.get(farmer_dist) or weather_advisory.MAHARASHTRA_LOCATIONS.get("Nashik")
        if dist_entry:
            tal_entry = dist_entry.get("talukas", {}).get(farmer_tal)
            if tal_entry:
                for vil in tal_entry.get("villages", []):
                    if farmer_vil.lower() in vil.get("en", "").lower():
                        resolved_coords = (vil["lat"], vil["lon"])
                        break
                if not resolved_coords:
                    resolved_coords = (tal_entry["lat"], tal_entry["lon"])
            if not resolved_coords:
                resolved_coords = (dist_entry["lat"], dist_entry["lon"])

        if not resolved_coords:
            resolved_coords = (20.0764, 74.1086)  # Niphad, Nashik default

        selected_loc = {
            "display_name": f"{pick(farmer.get('village'), lang=active_lang)}, {pick(farmer.get('taluka'), lang=active_lang)}",
            "display_name_en": f"{pick(farmer.get('village'), lang='en')}, {pick(farmer.get('taluka'), lang='en')}",
            "display_name_mr": f"{pick(farmer.get('village'), lang='mr')}, {pick(farmer.get('taluka'), lang='mr')}",
            "district_en": farmer_dist,
            "district_mr": pick(farmer.get("district"), lang="mr"),
            "taluka_en": farmer_tal,
            "taluka_mr": pick(farmer.get("taluka"), lang="mr"),
            "lat": resolved_coords[0],
            "lon": resolved_coords[1]
        }

    # Fetch real-time weather from Open-Meteo
    try:
        raw_weather, fetched_at_str, _ = weather_advisory.fetch_open_meteo_raw(
            selected_loc["lat"],
            selected_loc["lon"]
        )
    except Exception as e:
        flash(f"Open-Meteo Weather Service is momentarily slow or unreachable: {str(e)}", "warning")
        raw_weather = {
            "current": {"temperature_2m": 24.5, "relative_humidity_2m": 58, "precipitation": 0.0, "wind_speed_10m": 8.5, "wind_gusts_10m": 12.0, "weather_code": 1, "cloud_cover": 25},
            "hourly": {"time": [], "temperature_2m": [], "precipitation": [], "wind_speed_10m": [], "relative_humidity_2m": [], "weather_code": []},
            "daily": {"time": [], "temperature_2m_max": [], "temperature_2m_min": [], "precipitation_sum": [], "wind_speed_10m_max": [], "wind_gusts_10m_max": [], "weather_code": []}
        }
        fetched_at_str = "Recent Estimate"

    # Generate full advisory & rule calculations
    advisory = weather_advisory.generate_weather_analysis_and_advisories(
        raw_weather,
        farmer,
        selected_loc
    )

    return render_template(
        "weather_advisory.html",
        farmer=farmer,
        selected_location=selected_loc,
        advisory=advisory,
        fetched_at_str=fetched_at_str,
        active_nav="weather_advisory"
    )


@app.route("/api/weather/locations", methods=["GET"])
def api_weather_locations():
    """Returns the full 36-district Maharashtra location hierarchy for cascading dropdowns."""
    import weather_advisory
    return weather_advisory.MAHARASHTRA_LOCATIONS


@app.route("/api/weather/search-locations", methods=["GET"])
def api_weather_search_locations():
    """Searches Maharashtra locations by text query and returns matching lat/lon."""
    query = request.args.get("q", "").strip()
    import weather_advisory
    results = weather_advisory.search_locations_in_db(query, max_results=8)
    return {"results": results}


@app.route("/api/weather/forecast", methods=["GET"])
def api_weather_forecast():
    """JSON API endpoint returning real-time Open-Meteo forecast and agronomic advisories."""
    if not session.get("is_authenticated"):
        return {"success": False, "message": "Unauthorized"}, 401

    farmer = get_current_farmer()
    active_lang = session.get("lang", "mr")
    lat_str = request.args.get("lat")
    lon_str = request.args.get("lon")

    if not lat_str or not lon_str:
        return {"success": False, "error": "lat and lon parameters are required"}, 400

    try:
        lat = float(lat_str)
        lon = float(lon_str)
    except ValueError:
        return {"success": False, "error": "Invalid coordinates"}, 400

    import weather_advisory
    try:
        raw_weather, fetched_at_str, is_fresh = weather_advisory.fetch_open_meteo_raw(lat, lon)
        selected_loc = {
            "lat": lat,
            "lon": lon,
            "display_name": f"{lat:.4f}, {lon:.4f}"
        }
        advisory = weather_advisory.generate_weather_analysis_and_advisories(raw_weather, farmer, selected_loc)
        return {
            "success": True,
            "fetched_at": fetched_at_str,
            "is_fresh": is_fresh,
            "advisory": advisory
        }
    except Exception as e:
        return {"success": False, "error": str(e)}, 500


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
