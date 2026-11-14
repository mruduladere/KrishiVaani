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
from translations import t, pick, TRANSLATIONS
from ai_router import route_farmer_query

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
    """Maps farmer crop profile strings or dicts to standardized CROP_GUIDES keys."""
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
    active_lang = session.get("lang", "mr")

    # Selected crop from query parameter or default to first farmer crop
    requested_crop = request.args.get("crop")
    if requested_crop and requested_crop in CROP_GUIDES:
        active_crop = requested_crop
    elif farmer_crop_keys and farmer_crop_keys[0] in CROP_GUIDES:
        active_crop = farmer_crop_keys[0]
    else:
        active_crop = "Grapes"

    raw_guide = CROP_GUIDES.get(active_crop, CROP_GUIDES["Grapes"])

    # Resolve bilingual display_name for the selector tabs (all crops)
    resolved_all_crops = {}
    for key, guide in CROP_GUIDES.items():
        g = copy.deepcopy(guide)
        g["display_name"] = pick(guide.get("display_name", key), lang=active_lang)
        resolved_all_crops[key] = g

    # Resolve bilingual fields in the current guide
    current_guide = copy.deepcopy(raw_guide)
    current_guide["display_name"] = pick(raw_guide.get("display_name", active_crop), lang=active_lang)
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

    # Resolve crop tasks
    crop_tasks_raw = [tsk for tsk in TASKS_DB if tsk.get("crop") == active_crop]
    crop_tasks = []
    for tsk in crop_tasks_raw:
        rt = copy.deepcopy(tsk)
        rt["title"] = pick(tsk.get("title", ""), lang=active_lang)
        rt["crop"] = pick(tsk.get("crop", ""), lang=active_lang)
        rt["stage"] = pick(tsk.get("stage", ""), lang=active_lang)
        rt["due_date"] = pick(tsk.get("due_date", ""), lang=active_lang)
        rt["priority"] = pick(tsk.get("priority", ""), lang=active_lang)
        crop_tasks.append(rt)

    # Active crop display label
    active_crop_label = pick(raw_guide.get("display_name", active_crop), lang=active_lang)

    return render_template(
        "crop_helper.html",
        farmer=farmer,
        active_crop=active_crop,
        active_crop_label=active_crop_label,
        current_guide=current_guide,
        all_crops=resolved_all_crops,
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


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
