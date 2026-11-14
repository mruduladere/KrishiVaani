"""
app.py - Main Flask Web Application Controller for KrishiVaani (Voice of Agriculture)
Unified Python digital platform for Indian farmers built with Flask, Tailwind CSS, and Lucide Icons.
Strictly NO external database (uses Python in-memory state + flask.session).
Bilingual English & Marathi support via translations.py.
"""

import copy
import datetime
import urllib.parse
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
from translations import t, TRANSLATIONS

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
# JINJA TEMPLATE CONTEXT INJECTION (BILINGUAL SUPPORT)
# ---------------------------------------------------------
@app.context_processor
def inject_template_globals():
    """
    Injects active language ('mr' or 'en') and the translation function t(key)
    into all Jinja2 templates automatically.
    """
    active_lang = session.get("lang", "mr")
    
    def translate(key):
        return t(key, lang=active_lang)

    return {
        "t": translate,
        "lang": active_lang
    }


def get_current_farmer():
    """Retrieves active farmer profile from in-memory database."""
    phone = session.get("phone")
    if phone and phone in FARMERS_DB:
        return FARMERS_DB[phone]
    return FARMERS_DB.get("9822012345", SAMPLE_FARMER)


def normalize_phone(phone_str):
    """Normalizes phone string by stripping whitespace and dashes."""
    if not phone_str:
        return ""
    cleaned = "".join(c for c in phone_str if c.isdigit())
    if len(cleaned) > 10 and cleaned.startswith("91"):
        cleaned = cleaned[2:]
    return cleaned


def detect_crop_key(crop_name):
    """Maps farmer crop profile strings to standardized CROP_GUIDES keys."""
    crop_lower = crop_name.lower()
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
    return "Grapes"


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
    flash(t("reg_success"), "success")
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    """Clears user session and redirects to login card."""
    session.pop("is_authenticated", None)
    session.pop("phone", None)
    session.pop("farmer_name", None)
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

    stats = {
        "nov_expenses": nov_expenses,
        "total_livestock": total_livestock,
        "active_crops_count": len(farmer.get("crops_grown", [])),
        "total_tasks": len(TASKS_DB)
    }

    return render_template(
        "dashboard.html",
        farmer=farmer,
        stats=stats,
        tasks=TASKS_DB,
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
        farmer["crops_grown"] = [c.strip() for c in crops_raw.split(",") if c.strip()]

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
    farmer_crop_keys = [detect_crop_key(c) for c in farmer.get("crops_grown", [])]

    # Selected crop from query parameter or default to first farmer crop
    requested_crop = request.args.get("crop")
    if requested_crop and requested_crop in CROP_GUIDES:
        active_crop = requested_crop
    elif farmer_crop_keys and farmer_crop_keys[0] in CROP_GUIDES:
        active_crop = farmer_crop_keys[0]
    else:
        active_crop = "Grapes"

    current_guide = CROP_GUIDES.get(active_crop, CROP_GUIDES["Grapes"])
    crop_tasks = [tsk for tsk in TASKS_DB if tsk.get("crop") == active_crop]

    return render_template(
        "crop_helper.html",
        farmer=farmer,
        active_crop=active_crop,
        current_guide=current_guide,
        all_crops=CROP_GUIDES,
        farmer_crops_keys=farmer_crop_keys,
        crop_tasks=crop_tasks,
        active_nav="crop_helper"
    )


@app.route("/toggle-task/<task_id>", methods=["POST"])
def toggle_task(task_id):
    """Toggles task completed status in in-memory TASKS_DB."""
    for task in TASKS_DB:
        if task.get("id") == task_id:
            task["status"] = not task.get("status", False)
            break

    redirect_to = request.form.get("redirect") or request.referrer or url_for("dashboard")
    return redirect(redirect_to)


@app.route("/add-task", methods=["POST"])
def add_task():
    """Appends a new farming reminder task to in-memory TASKS_DB."""
    title = request.form.get("title", "").strip()
    crop = request.form.get("crop", "Grapes").strip()
    due_date = request.form.get("due_date", "Pending").strip()
    priority = request.form.get("priority", "Medium").strip()
    current_crop = request.form.get("current_crop", crop)

    if title:
        new_id = f"TSK-{len(TASKS_DB) + 1:02d}"
        TASKS_DB.append({
            "id": new_id,
            "crop": crop,
            "title": title,
            "stage": "Custom Reminder",
            "due_date": due_date,
            "priority": priority,
            "status": False
        })
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

    # Unique categories and talukas for filter controls
    all_categories = sorted(list(set(srv.get("category") for srv in SERVICES_DB)))
    all_talukas = sorted(list(set(srv.get("taluka") for srv in SERVICES_DB)))

    # Filter logic
    filtered = []
    for srv in SERVICES_DB:
        if selected_category and srv.get("category") != selected_category:
            continue
        if selected_taluka and srv.get("taluka") != selected_taluka:
            continue
        if search_query:
            searchable_text = f"{srv.get('name', '')} {srv.get('speciality', '')} {srv.get('location', '')}".lower()
            if search_query not in searchable_text:
                continue
        filtered.append(srv)

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
# ROADMAP PLACEHOLDER MODULES (MODULES 3, 5, 6, 7)
# ---------------------------------------------------------
@app.route("/ai-assistant")
def ai_assistant():
    """Module 3 placeholder."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))
    info = {
        "title": "Module 3: Multilingual Farmer AI Assistant",
        "marathi_subtitle": "मराठी व इंग्रजी AI शेती सहाय्यक",
        "step": "Step 3",
        "icon": "bot",
        "scope": "Text-based Marathi and English intent router providing instant answers to farming queries, crop diseases, government subsidies, and soil management without speech-to-text latency.",
        "planned": [
            "Fast intent classification for Marathi and English text queries",
            "Instant guidance on PM-KISAN, MahaDBT schemes, and crop insurance",
            "Organic farming tips and natural pesticide formulations (Jeevamrut, Dashparni)",
            "Interactive question-answering for common agronomy doubts"
        ]
    }
    return render_template("placeholder.html", farmer=get_current_farmer(), info=info, active_nav="ai_assistant")


@app.route("/marketplace")
def marketplace():
    """Module 5 placeholder."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))
    info = {
        "title": "Module 5: Simple Farmer-to-Buyer Marketplace",
        "marathi_subtitle": "थेट शेतकरी ते खरेदीदार बाजारपेठ",
        "step": "Step 5",
        "icon": "store",
        "scope": "Direct farmer-to-buyer listing portal eliminating middleman commissions. Enables farmers to post harvest lots and connect directly with wholesale buyers.",
        "planned": [
            "Farmer harvest posting form (crop, variety, quantity in quintals, price/quintal)",
            "Buyer enquiry contact generator via direct phone and WhatsApp connection",
            "Active regional commodity listings with quality specifications",
            "Zero online payment or logistics complications (direct peer-to-peer enquiry)"
        ]
    }
    return render_template("placeholder.html", farmer=get_current_farmer(), info=info, active_nav="marketplace")


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
    
    total_animals = len(LIVESTOCK_DB)
    total_milk = sum(float(a.get("daily_milk_yield_litres", 0)) for a in LIVESTOCK_DB)
    
    overdue_count = 0
    upcoming_count = 0
    
    processed_animals = []
    for animal in LIVESTOCK_DB:
        animal_copy = copy.deepcopy(animal)
        processed_vaccines = []
        has_overdue = False
        has_upcoming = False
        
        for v in animal.get("vaccination_history", []):
            v_copy = copy.deepcopy(v)
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
                badge_label = v.get("status", "Logged")
                badge_icon = "check"

            v_copy["days_diff"] = days_diff
            v_copy["status_code"] = status_code
            v_copy["badge_class"] = badge_class
            v_copy["badge_label"] = badge_label
            v_copy["badge_icon"] = badge_icon
            processed_vaccines.append(v_copy)
            
        if has_overdue:
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
    vaccine_name = request.form.get("vaccine_name", "").strip()
    today = datetime.date.today()

    for animal in LIVESTOCK_DB:
        if animal.get("tag_id") == animal_id:
            for v in animal.get("vaccination_history", []):
                if v.get("vaccine") == vaccine_name:
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
    
    total_spend = sum(float(e.get("amount", 0)) for e in EXPENSES_DB)
    total_entries = len(EXPENSES_DB)
    
    current_month_spend = sum(
        float(e.get("amount", 0))
        for e in EXPENSES_DB
        if "Nov" in e.get("month", "") or "11" in e.get("date", "")
    )

    # 1. Category aggregation
    cat_map = {}
    for e in EXPENSES_DB:
        cat = e.get("category", "Other")
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

    top_cat = category_stats[0] if category_stats else {"name": "None", "amount": 0, "share": 0}

    # 2. Crop aggregation
    crop_map = {}
    for e in EXPENSES_DB:
        c = e.get("crop", "General Farm")
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

    # 3. Monthly aggregation
    month_map = {}
    for e in EXPENSES_DB:
        m = e.get("month", "Recent")
        amt = float(e.get("amount", 0))
        month_map[m] = month_map.get(m, 0) + amt

    month_order = ["September 2026", "October 2026", "November 2026"]
    sorted_months = sorted(month_map.keys(), key=lambda x: month_order.index(x) if x in month_order else 99)

    # 4. Seasonal aggregation
    season_map = {}
    for e in EXPENSES_DB:
        s = e.get("season", "Rabi 2026-27")
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

    # Prepare Chart.js datasets
    chart_cat_labels = [c["name"].split("(")[0].strip() for c in category_stats]
    chart_cat_data = [c["amount"] for c in category_stats]

    chart_month_labels = [m.split(" ")[0] for m in sorted_months]
    chart_month_data = [int(month_map[m]) for m in sorted_months]

    return render_template(
        "expenses.html",
        farmer=farmer,
        expenses=sorted(EXPENSES_DB, key=lambda x: x.get("date", ""), reverse=True),
        all_categories=EXPENSE_CATEGORIES,
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


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
