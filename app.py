"""
app.py - Main Flask Web Application Controller for KrishiVaani (Voice of Agriculture)
Unified Python digital platform for Indian farmers built with Flask, Tailwind CSS, and Lucide Icons.
Strictly NO external database (uses Python in-memory state + flask.session).
Bilingual English & Marathi support via translations.py.
"""

import copy
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
    CROP_GUIDES
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


@app.route("/livestock")
def livestock():
    """Module 6 placeholder."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))
    info = {
        "title": "Module 6: Livestock Records & Reminders",
        "marathi_subtitle": "पशुधन व्यवस्थापन व लसीकरण वेळापत्रक",
        "step": "Step 6",
        "icon": "heart-pulse",
        "scope": "Digital registry for farm cattle and goats with automated vaccination schedules and overdue alert calculations.",
        "planned": [
            "Individual animal profiles with Ear Tag ID, breed, age, and lactation cycle",
            "Daily milk yield tracker with monthly production trends",
            "Vaccination calendar with automated overdue date math for FMD, HS, BQ",
            "Veterinary checkup and deworming reminder flags"
        ]
    }
    return render_template("placeholder.html", farmer=get_current_farmer(), info=info, active_nav="livestock")


@app.route("/expenses")
def expenses():
    """Module 7 placeholder."""
    if not session.get("is_authenticated"):
        return redirect(url_for("index"))
    info = {
        "title": "Module 7: Farm Expense Tracker",
        "marathi_subtitle": "शेतखर्च नोंदवही व नफा विश्लेषण",
        "step": "Step 7",
        "icon": "receipt",
        "scope": "Systematic accounting of input investments and labor expenses with automated monthly, seasonal, crop-wise, and category-wise totals.",
        "planned": [
            "Quick expense logging form (seeds, fertilizer, pesticide, labor, diesel/machinery)",
            "Monthly expenditure breakdown (e.g. October vs November 2026)",
            "Crop-wise cost allocation (Grapes vs Onion vs Soybean)",
            "Category-wise breakdown for input cost optimization"
        ]
    }
    return render_template("placeholder.html", farmer=get_current_farmer(), info=info, active_nav="expense_tracker")


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
