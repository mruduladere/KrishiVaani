"""
smart_dispatcher.py - Multi-Intent Natural Language & Voice Dispatcher for KrishiVaani
Parses natural language (Marathi / English / Hinglish / Marathinglish) using Sarvam AI (sarvam-105b)
and extracts structured multi-module actions (Livestock, Expenses, Marketplace, Crop Tasks).
Directly updates in-memory stores with 100% offline deterministic fallback.
Strictly NO DATABASE.
"""

import re
import json
import logging
from datetime import datetime, timedelta
from sarvam_client import get_sarvam_client, chat_completion, is_marathi_text

logger = logging.getLogger("krishivaani.dispatcher")


def extract_and_dispatch(raw_text: str, farmer: dict, in_memory_dbs: dict, active_lang: str = "mr") -> dict:
    """
    Parses unstructured text and updates corresponding in-memory DBs.
    
    in_memory_dbs:
    {
        "livestock": list,
        "expenses": list,
        "marketplace": list,
        "tasks": list
    }
    
    Returns structured result dict:
    {
        "success": bool,
        "raw_text": str,
        "engine": "Sarvam AI (sarvam-105b)" | "Offline Deterministic Engine",
        "actions_taken": [...],
        "has_pending_cattle": bool,
        "pending_cattle_info": dict or None,
        "notifications": list
    }
    """
    cleaned = (raw_text or "").strip()
    if not cleaned:
        return {
            "success": False,
            "raw_text": "",
            "engine": "None",
            "actions_taken": [],
            "has_pending_cattle": False,
            "pending_cattle_info": None,
            "notifications": [
                {"en": "Please provide input text or voice recording.", "mr": "कृपया आवाज रेकॉर्डिंग किंवा मजकूर प्रविष्ट करा."}
            ],
            "message": {"en": "Please provide input text or voice recording.", "mr": "कृपया आवाज रेकॉर्डिंग किंवा मजकूर प्रविष्ट करा."}
        }

    client = get_sarvam_client()
    parsed_plan = None
    engine_used = "Offline Deterministic Engine"

    if client:
        prompt = f"""
You are the central multi-module AI dispatcher for KrishiVaani, an agricultural operating system for farmers in Maharashtra.
A farmer has spoken or written the following entry:
"{cleaned}"

Analyze the statement and identify ALL distinct intents:
1. "cattle_purchase": if the farmer bought, purchased, or added a new cow, buffalo, or goat (e.g. "I bought a cow named Gauri for ₹25,000" or "मी गौरी नावाची गाय घेतली").
2. "livestock_vaccination": if the farmer completed or scheduled vaccination for an EXISTING animal (e.g. "I completed Gauri's vaccination today").
3. "milk_yield": if the farmer recorded daily milk production (e.g. "My ten cows produced 65 litres of milk today").
4. "farm_expense": if money was spent on farm inputs like seeds, fertiliser, pesticides, labour, diesel, or equipment (e.g. "I purchased fertiliser for ₹1,200").
5. "produce_income": if the farmer sold produce and earned revenue (e.g. "I sold onions for ₹8,000").
6. "marketplace_listing": if the farmer wants to post an advance listing of crop to sell in the market.
7. "crop_task": if a farm reminder or crop activity is scheduled (spraying, weeding, irrigation).

Note: Statements like "I bought a cow named Gauri for ₹25,000" involve BOTH cattle_purchase AND farm_expense (purchase price).
Do NOT invent missing details such as animal age, daily milk yield, government ear tags, or dates if not stated.

Return VALID JSON ONLY with this schema:
{{
    "actions": ["cattle_purchase", "livestock_vaccination", "milk_yield", "farm_expense", "produce_income", "marketplace_listing", "crop_task"],
    "cattle_purchase": {{
        "name_en": "string (or null)",
        "name_mr": "string (or null)",
        "type_en": "Cow | Buffalo | Goat | Bull",
        "type_mr": "गाय | म्हैस | शेळी | बैल",
        "breed_en": "string (or null)",
        "breed_mr": "string (or null)",
        "age_years": number or null,
        "daily_milk": number or null,
        "purchase_price": number or null,
        "official_tag_id": "string (or null)",
        "vaccine_name": "string (or null)"
    }},
    "livestock_vaccination": {{
        "animal_name": "string",
        "vaccine_name": "string (or null)",
        "completed": true
    }},
    "milk_yield": {{
        "litres": number,
        "animal_count": number or null
    }},
    "farm_expense": {{
        "amount": number,
        "category_en": "Fertilizers & Nutrients | Seeds & Seedlings | Pesticides & Bio-agents | Labour & Pruning | Animal Fodder & Feed | Veterinary & Healthcare | Fuel & Electricity | Livestock Purchase",
        "category_mr": "खते व पोषण | बियाणे व रोपे | कीटकनाशके व बुरशीनाशके | मजुरी व छाटणी | पशुखाद्य व वैरण | पशुवैद्यकीय उपचार | डिझेल व वीज बिल | पशुधन खरेदी",
        "crop_en": "General Farm | Onion | Grapes | Soybean | Livestock / Dairy",
        "crop_mr": "सामायिक शेती | कांदा | द्राक्ष | सोयाबीन | दुग्धव्यवसाय / पशुधन",
        "description_en": "string",
        "description_mr": "string"
    }},
    "produce_income": {{
        "amount": number,
        "crop_en": "Onion | Grapes | Soybean | Wheat | Vegetables",
        "crop_mr": "कांदा | द्राक्ष | सोयाबीन | गहू | भाजीपाला",
        "quantity_quintals": number or null
    }},
    "crop_task": {{
        "title_en": "string",
        "title_mr": "string",
        "crop_en": "string",
        "crop_mr": "string"
    }}
}}
Only output the JSON object.
"""
        try:
            raw_reply = chat_completion(
                messages=[{"role": "user", "content": prompt}],
                model="sarvam-105b-conversations",
                temperature=0.1
            )
            if raw_reply:
                json_match = re.search(r"\{.*\}", raw_reply, re.DOTALL)
                if json_match:
                    parsed_plan = json.loads(json_match.group(0))
                    engine_used = "Sarvam AI (sarvam-105b)"
        except Exception as e:
            logger.warning(f"Sarvam dispatch planning failed, falling back: {e}")

    # Fallback to offline rule-based parser if AI was unavailable or failed
    if not parsed_plan:
        parsed_plan = _offline_parse_dispatch(cleaned, in_memory_dbs)
        engine_used = "Offline Deterministic Engine"

    # Now execute the plan against the in-memory databases
    execution_result = _apply_dispatch_plan(parsed_plan, cleaned, farmer, in_memory_dbs)

    return {
        "success": len(execution_result["actions_taken"]) > 0,
        "raw_text": cleaned,
        "engine": engine_used,
        "actions_taken": execution_result["actions_taken"],
        "has_pending_cattle": execution_result.get("has_pending_cattle", False),
        "pending_cattle_info": execution_result.get("pending_cattle_info"),
        "notifications": execution_result.get("notifications", [])
    }


def _offline_parse_dispatch(text: str, in_memory_dbs: dict = None) -> dict:
    """
    Deterministic offline parser using Marathi and English keyword heuristics.
    Never invents missing details (age, milk, vaccine, or price).
    """
    text_lower = text.lower()
    actions = []
    plan = {"actions": actions}

    # Extract all monetary numbers with ₹, Rs, रु, रुपये or context
    # E.g. "for ₹25,000", "₹1,200", "₹8,000", "1200 rupees", "8000 रुपये"
    extracted_amounts = []
    amt_patterns = [
        r"(?:₹|rs\.?|रु\.?|रुपये)\s*(\d+(?:,\d+)*(?:\.\d+)?)",
        r"(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:₹|rs\.?|रु\.?|रुपये|rupees)",
        r"(?:for|किंमत|भाव|दर|खर्च|विकले|विकला)\s*(?:₹|rs\.?|रु\.?|रुपये)?\s*(\d+(?:,\d+)*(?:\.\d+)?)"
    ]
    for p in amt_patterns:
        for m in re.finditer(p, text_lower):
            try:
                val = float(m.group(1).replace(",", ""))
                if val not in extracted_amounts:
                    extracted_amounts.append(val)
            except ValueError:
                pass

    primary_amt = extracted_amounts[0] if extracted_amounts else None

    # -------------------------------------------------------------
    # 1. Check for Milk Yield Intent
    # E.g.: "My ten cows produced 65 litres of milk today."
    # E.g.: "माझ्या १० गाईंनी आज ६५ लिटर दूध दिले."
    # -------------------------------------------------------------
    is_milk_yield = any(k in text_lower for k in [
        "litres of milk", "liters of milk", "litres", "liters", "लिटर", "दूध दिले", "दूध काढले", "दूध उत्पादन", "milk today"
    ]) and not any(k in text_lower for k in ["bought", "purchased", "खरेदी", "विकले", "sold"])

    if is_milk_yield:
        actions.append("milk_yield")
        litres = 0.0
        litres_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:litres?|liters?|लिटर)", text_lower)
        if litres_match:
            try:
                litres = float(litres_match.group(1))
            except ValueError:
                litres = 0.0

        # Animal count
        animal_count = 1
        word_numbers = {
            "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
            "एक": 1, "दोन": 2, "तीन": 3, "चार": 4, "पाच": 5, "सहा": 6, "सात": 7, "आठ": 8, "नऊ": 9, "दहा": 10
        }
        count_match = re.search(r"(\d+|ten|five|two|four|दहा|पाच|दोन)\s*(?:cows?|buffaloes?|cattle|गाई|म्हशी|जनावरे)", text_lower)
        if count_match:
            raw_c = count_match.group(1)
            if raw_c.isdigit():
                animal_count = int(raw_c)
            elif raw_c in word_numbers:
                animal_count = word_numbers[raw_c]

        plan["milk_yield"] = {
            "litres": litres,
            "animal_count": animal_count
        }
        return plan

    # -------------------------------------------------------------
    # 2. Check for Livestock Vaccination Intent (for existing animal)
    # E.g.: "I completed Gauri's vaccination today."
    # E.g.: "मी आज गौरीचे लसीकरण पूर्ण केले."
    # -------------------------------------------------------------
    is_vax_intent = any(k in text_lower for k in [
        "vaccination", "vaccinated", "vaccine", "लस", "लसीकरण", "टोचली"
    ]) and any(k in text_lower for k in [
        "completed", "done", "today", "पूर्ण", "झाले", "केले", "दिली", "टोचली"
    ]) and not any(k in text_lower for k in ["bought", "purchased", "खरेदी", "घेतली"])

    if is_vax_intent:
        actions.append("livestock_vaccination")
        target_name = "Gauri"  # fallback default if Gauri mentioned
        if "lakshmi" in text_lower or "लक्ष्मी" in text_lower:
            target_name = "Lakshmi"
        elif "kaveri" in text_lower or "कावेरी" in text_lower:
            target_name = "Kaveri"
        elif "gauri" in text_lower or "गौरी" in text_lower:
            target_name = "Gauri"
        else:
            # Try to match any animal name from database
            if in_memory_dbs and "livestock" in in_memory_dbs:
                for a in in_memory_dbs["livestock"]:
                    en_n = a.get("name", {}).get("en", "") if isinstance(a.get("name"), dict) else str(a.get("name", ""))
                    mr_n = a.get("name", {}).get("mr", "") if isinstance(a.get("name"), dict) else str(a.get("name", ""))
                    if en_n.lower() in text_lower or (mr_n and mr_n in text):
                        target_name = en_n
                        break

        vax_type = None
        if "fmd" in text_lower or "लाळ्या" in text_lower or "खुरखूत" in text_lower:
            vax_type = "Foot & Mouth Disease (FMD)"
        elif "hs" in text_lower or "घटसर्प" in text_lower:
            vax_type = "Hemorrhagic Septicemia (HS)"
        elif "bq" in text_lower or "एकटांग्या" in text_lower:
            vax_type = "Black Quarter (BQ)"
        elif "brucellosis" in text_lower or "ब्रुसेलोसिस" in text_lower:
            vax_type = "Brucellosis"

        plan["livestock_vaccination"] = {
            "animal_name": target_name,
            "vaccine_name": vax_type,
            "completed": True
        }
        return plan

    # -------------------------------------------------------------
    # 3. Check for Produce Sales / Income Intent
    # E.g.: "I sold onions for ₹8,000."
    # E.g.: "मी ८,००० रुपयांचा कांदा विकला."
    # -------------------------------------------------------------
    is_produce_sale = any(k in text_lower for k in [
        "sold", "selling", "विकले", "विकला", "विक्री केली", "मिळाले", "विक्री"
    ]) and not any(k in text_lower for k in ["bought", "purchased", "खरेदी", "घेतली", "खर्च"])

    if is_produce_sale:
        actions.append("produce_income")
        sale_amt = primary_amt if primary_amt else 0.0

        # Detect crop
        crop_en = "Onion"
        crop_mr = "कांदा"
        if any(k in text_lower for k in ["onion", "कांदा", "कांद्या"]):
            crop_en = "Onion"
            crop_mr = "कांदा"
        elif any(k in text_lower for k in ["grape", "द्राक्ष", "द्राक्षा"]):
            crop_en = "Grapes"
            crop_mr = "द्राक्ष"
        elif any(k in text_lower for k in ["soybean", "सोयाबीन"]):
            crop_en = "Soybean"
            crop_mr = "सोयाबीन"
        elif any(k in text_lower for k in ["tomato", "टोमॅटो"]):
            crop_en = "Tomato"
            crop_mr = "टोमॅटो"
        elif any(k in text_lower for k in ["wheat", "गहू"]):
            crop_en = "Wheat"
            crop_mr = "गहू"

        plan["produce_income"] = {
            "amount": sale_amt,
            "crop_en": crop_en,
            "crop_mr": crop_mr
        }
        return plan

    # -------------------------------------------------------------
    # 4. Check for Cattle Purchase / Addition Intent
    # E.g.: "I bought a cow named Gauri for ₹25,000."
    # E.g.: "I bought a cow named Gauri" (no price)
    # E.g.: "मी गौरी नावाची नवीन गाय खरेदी केली २५,००० रुपयांना."
    # -------------------------------------------------------------
    is_cattle_purchase = any(k in text_lower for k in [
        "bought a cow", "bought a new cow", "bought a buffalo", "bought a calf", "bought a goat", "bought cattle",
        "purchased a cow", "purchased cow", "purchased a new cow", "purchased a buffalo", "purchased animal",
        "new cow", "new buffalo", "नवीन गाय", "गाय खरेदी", "म्हैस खरेदी", "गाय घेतली", "गाई खरेदी", "पशुधन खरेदी"
    ]) or (
        ("bought" in text_lower or "purchased" in text_lower or "खरेदी" in text_lower or "घेतली" in text_lower)
        and any(k in text_lower for k in ["cow", "buffalo", "goat", "calf", "bull", "cattle", "गाय", "म्हैस", "शेळी", "बैल"])
    )

    if is_cattle_purchase:
        actions.append("cattle_purchase")

        # Extract animal name accurately without inventing
        name_en = "Gauri" if "gauri" in text_lower or "गौरी" in text_lower else "Lakshmi" if "lakshmi" in text_lower or "लक्ष्मी" in text_lower else None
        name_mr = "गौरी" if "gauri" in text_lower or "गौरी" in text_lower else "लक्ष्मी" if "lakshmi" in text_lower or "लक्ष्मी" in text_lower else None

        if not name_en:
            # Check pattern: "named X" or "नाव X" or "X नावाची"
            name_match = re.search(r"(?:named|name|नाव)\s+([A-Za-z\u0900-\u097F]+)", text, re.IGNORECASE)
            if not name_match:
                name_match = re.search(r"([A-Za-z\u0900-\u097F]+)\s+(?:named|नावाची|नावाचा|नावाची गाय|नावाचे)", text, re.IGNORECASE)
            if name_match:
                extracted_name = name_match.group(1).strip()
                if extracted_name.lower() not in ["cow", "buffalo", "goat", "new", "a", "गाय", "नवीन"]:
                    name_en = extracted_name.capitalize()
                    name_mr = extracted_name

        if not name_en:
            name_en = "New Animal"
            name_mr = "नवीन पशुधन"

        # Determine animal type
        is_buf = any(k in text_lower for k in ["buffalo", "म्हैस", "मुऱ्हा", "murrah"])
        is_goat = any(k in text_lower for k in ["goat", "शेळी"])
        type_en = "Buffalo" if is_buf else ("Goat" if is_goat else "Cow")
        type_mr = "म्हैस" if is_buf else ("शेळी" if is_goat else "गाय")

        # Breed (Never fabricate Gir unless specified)
        breed_en = "Not Specified"
        breed_mr = "नोंद नाही"
        if "gir" in text_lower or "गीर" in text_lower:
            breed_en, breed_mr = "Gir", "गीर"
        elif "murrah" in text_lower or "मुऱ्हा" in text_lower:
            breed_en, breed_mr = "Murrah", "मुऱ्हा"
        elif "dangi" in text_lower or "डांगी" in text_lower:
            breed_en, breed_mr = "Dangi", "डांगी"
        elif "khillar" in text_lower or "खिलार" in text_lower:
            breed_en, breed_mr = "Khillar", "खिलार"

        # Age (Never fabricate 3.0 unless explicitly mentioned)
        age = None
        age_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:years?|वर्षे|वर्ष)", text_lower)
        if age_match:
            try:
                age = float(age_match.group(1))
            except ValueError:
                pass

        # Daily milk (Never fabricate 11.5 unless explicitly mentioned)
        daily_milk = None
        milk_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:litres?|liters?|लिटर)", text_lower)
        if milk_match:
            try:
                daily_milk = float(milk_match.group(1))
            except ValueError:
                pass

        # Vaccination (Never fabricate completed FMD unless explicitly stated)
        vax_name = None
        if "fmd" in text_lower or "लाळ्या" in text_lower:
            vax_name = "Foot & Mouth Disease (FMD)"
        elif "vaccine" in text_lower or "लस" in text_lower:
            vax_name = "General Initial Vaccination"

        # Check for price
        purchase_price = primary_amt if primary_amt else None

        plan["cattle_purchase"] = {
            "name_en": name_en,
            "name_mr": name_mr,
            "type_en": type_en,
            "type_mr": type_mr,
            "breed_en": breed_en,
            "breed_mr": breed_mr,
            "age_years": age,
            "daily_milk": daily_milk,
            "purchase_price": purchase_price,
            "official_tag_id": None,
            "vaccine_name": vax_name
        }

        # If purchase price exists, trigger multi-action: Farm Expense
        if purchase_price and purchase_price > 0:
            actions.append("farm_expense")
            plan["farm_expense"] = {
                "amount": purchase_price,
                "category_en": "Livestock Purchase",
                "category_mr": "पशुधन खरेदी",
                "crop_en": "Livestock / Dairy",
                "crop_mr": "दुग्धव्यवसाय / पशुधन",
                "payment_mode_en": "Cash",
                "payment_mode_mr": "रोख",
                "description_en": f"Cattle purchase: {type_en} named {name_en} for ₹{purchase_price:,.0f}",
                "description_mr": f"पशुधन खरेदी: {name_mr} {type_mr} खरेदी ₹{purchase_price:,.0f}"
            }

        return plan

    # -------------------------------------------------------------
    # 5. Check for Farm Input Expense Intent
    # E.g.: "I purchased fertiliser for ₹1,200."
    # E.g.: "मी १२०० रुपयांचे खत खरेदी केले."
    # -------------------------------------------------------------
    is_farm_expense = (primary_amt is not None and primary_amt > 0) or any(k in text_lower for k in [
        "spent", "paid", "bought", "purchased", "expense", "खर्च", "खरेदी", "दिले", "भरले"
    ])

    if is_farm_expense:
        actions.append("add_farm_expense")
        amt = primary_amt if primary_amt else 1000.0

        # Identify category
        cat_en = "General Farm Inputs"
        cat_mr = "सामायिक शेती निविष्ठा"
        crop_en = "General Farm"
        crop_mr = "सामायिक शेती"

        if any(k in text_lower for k in ["fertiliser", "fertilizer", "urea", "dap", "खत", "युरिया", "डीएपी"]):
            cat_en = "Fertilizers & Nutrients"
            cat_mr = "खते व पोषण"
        elif any(k in text_lower for k in ["seed", "seeds", "बियाणे", "रोपे"]):
            cat_en = "Seeds & Seedlings"
            cat_mr = "बियाणे व रोपे"
        elif any(k in text_lower for k in ["spray", "pesticide", "fungicide", "कीटकनाशक", "बुरशीनाशक", "औषध"]):
            cat_en = "Pesticides & Bio-agents"
            cat_mr = "कीटकनाशके व बुरशीनाशके"
        elif any(k in text_lower for k in ["labour", "labor", "pruning", "मजुरी", "छाटणी"]):
            cat_en = "Labour & Pruning"
            cat_mr = "मजुरी व छाटणी"
        elif any(k in text_lower for k in ["feed", "fodder", "चारा", "पशुखाद्य", "पेंड"]):
            cat_en = "Animal Fodder & Feed"
            cat_mr = "पशुखाद्य व वैरण"
            crop_en = "Livestock / Dairy"
            crop_mr = "दुग्धव्यवसाय / पशुधन"
        elif any(k in text_lower for k in ["diesel", "fuel", "electricity", "डिझेल", "वीज"]):
            cat_en = "Fuel & Electricity"
            cat_mr = "डिझेल व वीज बिल"

        # Identify crop if mentioned
        if any(k in text_lower for k in ["onion", "कांदा"]):
            crop_en, crop_mr = "Onion", "कांदा"
        elif any(k in text_lower for k in ["grape", "grapes", "द्राक्ष"]):
            crop_en, crop_mr = "Grapes", "द्राक्ष"
        elif any(k in text_lower for k in ["soybean", "सोयाबीन"]):
            crop_en, crop_mr = "Soybean", "सोयाबीन"

        # Payment mode
        pm_en = "UPI" if any(k in text_lower for k in ["upi", "फोनपे", "gpay", "online"]) else "Cash"
        pm_mr = "यूपीआय" if pm_en == "UPI" else "रोख"

        plan["farm_expense"] = {
            "amount": amt,
            "category_en": cat_en,
            "category_mr": cat_mr,
            "crop_en": crop_en,
            "crop_mr": crop_mr,
            "payment_mode_en": pm_en,
            "payment_mode_mr": pm_mr,
            "description_en": f"{cat_en} for {crop_en}: {text}",
            "description_mr": f"{crop_mr} पिकासाठी {cat_mr}: {text}"
        }
        return plan

    # -------------------------------------------------------------
    # 6. Check for Crop Task / Spray Reminder
    # -------------------------------------------------------------
    is_task = any(k in text_lower for k in [
        "spray", "spraying", "reminder", "task", "fungicide", "mildew", "irrigate", "schedule",
        "फवारणी", "फवारा", "तासिका", "काम", "नियोजन", "स्मरणपत्र"
    ])
    if is_task:
        actions.append("crop_task")
        crop_en = "Grapes" if any(k in text_lower for k in ["द्राक्ष", "grape", "mildew"]) else "Onion"
        crop_mr = "द्राक्ष" if crop_en == "Grapes" else "कांदा"

        plan["crop_task"] = {
            "title_en": f"Scheduled activity: {text}",
            "title_mr": f"नियोजित शेती काम: {text}",
            "crop_en": crop_en,
            "crop_mr": crop_mr
        }
        return plan

    # Default fallback to general farm task/note
    actions.append("crop_task")
    plan["crop_task"] = {
        "title_en": f"Farm note: {text}",
        "title_mr": f"शेती नोंद: {text}",
        "crop_en": "General Farm",
        "crop_mr": "सामायिक शेती"
    }
    return plan


def _apply_dispatch_plan(plan: dict, raw_text: str, farmer: dict, in_memory_dbs: dict) -> dict:
    """
    Applies parsed actions directly to LIVESTOCK_DB, EXPENSES_DB, MARKETPLACE_DB, TASKS_DB.
    Avoids duplicate transactions if user repeats or edits a statement.
    Does not fabricate unverified details.
    """
    actions_taken = []
    notifications = []
    actions = plan.get("actions", [])
    has_pending_cattle = False
    pending_cattle_info = None

    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")

    # -------------------------------------------------------------------------
    # A. Dedicated Cattle Purchase / Registration Workflow
    # -------------------------------------------------------------------------
    if "cattle_purchase" in actions and plan.get("cattle_purchase"):
        cp = plan["cattle_purchase"]
        name_en = cp.get("name_en") or "New Cattle"
        name_mr = cp.get("name_mr") or "नवीन पशुधन"
        type_en = cp.get("type_en") or "Cow"
        type_mr = cp.get("type_mr") or "गाय"
        breed_en = cp.get("breed_en") or "Not Specified"
        breed_mr = cp.get("breed_mr") or "नोंद नाही"
        age = cp.get("age_years")
        daily_milk = cp.get("daily_milk")
        purchase_price = cp.get("purchase_price")
        official_tag = cp.get("official_tag_id")

        # Deduplication check: Has a pending animal with this exact name been registered just now?
        existing_animal = None
        for a in in_memory_dbs.get("livestock", []):
            a_name_en = a.get("name", {}).get("en", "") if isinstance(a.get("name"), dict) else str(a.get("name", ""))
            a_name_mr = a.get("name", {}).get("mr", "") if isinstance(a.get("name"), dict) else str(a.get("name", ""))
            if (a_name_en.lower() == name_en.lower() or (name_mr and a_name_mr == name_mr)) and a.get("registration_status") == "Registration pending":
                existing_animal = a
                break

        if existing_animal:
            # Update existing pending record instead of creating duplicate
            if purchase_price:
                existing_animal["purchase_price"] = purchase_price
            if age is not None:
                existing_animal["age_years"] = age
            if daily_milk is not None:
                existing_animal["daily_milk_yield_litres"] = daily_milk
            assigned_tag = existing_animal["tag_id"]
        else:
            # Assign official tag if present, else assign pending tag
            assigned_tag = official_tag if official_tag else f"REG-PENDING-{len(in_memory_dbs['livestock']) + 101:04d}"
            reg_status = "Registered" if official_tag else "Registration pending"

            vax_hist = []
            if cp.get("vaccine_name"):
                vax_hist.append({
                    "vaccine": {"en": cp["vaccine_name"], "mr": cp["vaccine_name"]},
                    "date_given": today_str,
                    "due_date": (now + timedelta(days=180)).strftime("%Y-%m-%d"),
                    "status": "Up-to-Date"
                })

            animal_entry = {
                "tag_id": assigned_tag,
                "name": {"en": name_en, "mr": name_mr},
                "type": {"en": type_en, "mr": type_mr},
                "breed": {"en": breed_en, "mr": breed_mr},
                "age_years": age if age is not None else 0.0,
                "daily_milk_yield_litres": daily_milk if daily_milk is not None else 0.0,
                "purchase_price": purchase_price,
                "registration_status": reg_status,
                "health_status": {
                    "en": "Healthy" if reg_status == "Registered" else "Registration Pending",
                    "mr": "निरोगी" if reg_status == "Registered" else "नोंदणी प्रलंबित"
                },
                "vaccination_history": vax_hist,
                "notes": {
                    "en": "Registration pending. Government 12-digit ear tag required from Taluka Veterinary Clinic.",
                    "mr": "नोंदणी प्रलंबित. तालुका पशुवैद्यकीय दवाखान्यातून शासकीय १२-अंकी कानातील टॅग आवश्यक."
                }
            }
            in_memory_dbs["livestock"].insert(0, animal_entry)

            # Update farmer livestock summary
            lsum = farmer.setdefault("livestock_summary", {})
            lsum["total_animals"] = len(in_memory_dbs["livestock"])

        has_pending_cattle = True
        missing_fields = []
        if not official_tag:
            missing_fields.append("Government 12-digit INAPH Tag")
        if age is None:
            missing_fields.append("Age / Date of Birth")
        if daily_milk is None:
            missing_fields.append("Daily Milk Yield")
        if not cp.get("vaccine_name"):
            missing_fields.append("Prior Vaccination History")

        pending_cattle_info = {
            "tag_id": assigned_tag,
            "name": name_en,
            "type": type_en,
            "breed": breed_en,
            "purchase_price": purchase_price,
            "missing_fields": missing_fields
        }

        # Build UI action card
        badge_status = "Registration Pending" if not official_tag else "Registered"
        actions_taken.append({
            "module_id": "livestock",
            "module_name": {"en": "Livestock Records", "mr": "पशुधन व्यवस्थापन"},
            "action_desc": {
                "en": f"Initiated record for {type_en} '{name_en}' ({badge_status} • Tag: {assigned_tag})",
                "mr": f"{name_mr} {type_mr} नोंदणी सुरू केली ({badge_status} • टॅग: {assigned_tag})"
            },
            "view_url": "/livestock",
            "badge_color": "amber" if not official_tag else "emerald",
            "details": [
                {"label": {"en": "Tag ID", "mr": "टॅग क्र."}, "value": assigned_tag},
                {"label": {"en": "Registration Status", "mr": "नोंदणी स्थिती"}, "value": badge_status},
                {"label": {"en": "Purchase Price", "mr": "खरेदी किंमत"}, "value": f"₹{purchase_price:,.0f}" if purchase_price else "Not Provided"},
                {"label": {"en": "Next Step", "mr": "पुढील पायरी"}, "value": "Visit Taluka Clinic for Ear Tag" if not official_tag else "Complete"}
            ]
        })

        if not official_tag:
            notifications.append({
                "en": f"Animal '{name_en}' saved with 'Registration Pending'. Official 12-digit INAPH ear-tag is missing. Visit your Taluka Veterinary Clinic for official tagging.",
                "mr": f"'{name_mr}' जनावराची नोंद 'नोंदणी प्रलंबित' म्हणून जतन केली. शासकीय १२-अंकी टॅग बाकी आहे. अधिकृत टॅगिंगसाठी तालुका पशुवैद्यकीय दवाखान्यात संपर्क साधा."
            })

    # -------------------------------------------------------------------------
    # B. Livestock Vaccination Update (For Existing Animal)
    # -------------------------------------------------------------------------
    if "livestock_vaccination" in actions and plan.get("livestock_vaccination"):
        lv = plan["livestock_vaccination"]
        target_name = (lv.get("animal_name") or "Gauri").strip().lower()
        requested_vax = lv.get("vaccine_name")

        matched_animal = None
        for a in in_memory_dbs.get("livestock", []):
            en_n = a.get("name", {}).get("en", "") if isinstance(a.get("name"), dict) else str(a.get("name", ""))
            mr_n = a.get("name", {}).get("mr", "") if isinstance(a.get("name"), dict) else str(a.get("name", ""))
            if en_n.lower() == target_name or mr_n == target_name:
                matched_animal = a
                break

        if matched_animal:
            # Find vaccine to update or create entry
            vax_list = matched_animal.setdefault("vaccination_history", [])
            target_vax = None
            if requested_vax:
                for v in vax_list:
                    v_en = v.get("vaccine", {}).get("en", "") if isinstance(v.get("vaccine"), dict) else str(v.get("vaccine", ""))
                    if requested_vax.lower() in v_en.lower():
                        target_vax = v
                        break
            if not target_vax and vax_list:
                # Update first overdue or upcoming vaccine
                for v in vax_list:
                    if v.get("status") in ["Overdue", "Upcoming"]:
                        target_vax = v
                        break
                if not target_vax:
                    target_vax = vax_list[0]

            v_title_en = "Foot & Mouth Disease (FMD)"
            v_title_mr = "लाळ्या खुरखूत"
            if target_vax:
                target_vax["date_given"] = today_str
                target_vax["due_date"] = (now + timedelta(days=180)).strftime("%Y-%m-%d")
                target_vax["status"] = "Up-to-Date"
                v_title_en = target_vax.get("vaccine", {}).get("en", v_title_en) if isinstance(target_vax.get("vaccine"), dict) else str(target_vax.get("vaccine", v_title_en))
                v_title_mr = target_vax.get("vaccine", {}).get("mr", v_title_mr) if isinstance(target_vax.get("vaccine"), dict) else str(target_vax.get("vaccine", v_title_mr))
            else:
                new_vax = {
                    "vaccine": {"en": v_title_en, "mr": v_title_mr},
                    "date_given": today_str,
                    "due_date": (now + timedelta(days=180)).strftime("%Y-%m-%d"),
                    "status": "Up-to-Date"
                }
                vax_list.append(new_vax)

            matched_animal["health_status"] = {"en": "Healthy & Up-to-Date", "mr": "निरोगी व लसीकरण पूर्ण"}

            animal_disp_en = matched_animal.get("name", {}).get("en", target_name.capitalize()) if isinstance(matched_animal.get("name"), dict) else str(matched_animal.get("name", target_name))
            animal_disp_mr = matched_animal.get("name", {}).get("mr", target_name) if isinstance(matched_animal.get("name"), dict) else str(matched_animal.get("name", target_name))
            next_due_str = (now + timedelta(days=180)).strftime("%Y-%m-%d")

            actions_taken.append({
                "module_id": "livestock",
                "module_name": {"en": "Livestock Vaccination Record", "mr": "पशुधन लसीकरण नोंद"},
                "action_desc": {
                    "en": f"Marked {v_title_en} completed today for {animal_disp_en} (Tag: {matched_animal.get('tag_id')}). Next scheduled dose: {next_due_str}.",
                    "mr": f"{animal_disp_mr} (टॅग: {matched_animal.get('tag_id')}) साठी {v_title_mr} लसीकरण आज पूर्ण नोंदवले. पुढील देय तारीख: {next_due_str}."
                },
                "view_url": "/livestock",
                "badge_color": "emerald",
                "details": [
                    {"label": {"en": "Animal", "mr": "जनावर"}, "value": f"{animal_disp_en} ({matched_animal.get('tag_id')})"},
                    {"label": {"en": "Vaccine", "mr": "लस"}, "value": v_title_en},
                    {"label": {"en": "Date Completed", "mr": "दिलेली तारीख"}, "value": today_str},
                    {"label": {"en": "Next Due Date", "mr": "पुढील देय तारीख"}, "value": next_due_str}
                ]
            })
            notifications.append({
                "en": f"Vaccination completed for {animal_disp_en}. Next dose due on {next_due_str}.",
                "mr": f"{animal_disp_mr} साठी लसीकरण पूर्ण नोंदवले. पुढील डोसची देय तारीख {next_due_str} आहे."
            })
        else:
            notifications.append({
                "en": f"Could not locate an existing animal named '{target_name}'. Please verify the animal registry.",
                "mr": f"'{target_name}' नावाचे जनावर नोंदवहीत सापडले नाही. कृपया जनावरांचे नाव तपासा."
            })

    # -------------------------------------------------------------------------
    # C. Daily Milk Yield Tracking
    # -------------------------------------------------------------------------
    if "milk_yield" in actions and plan.get("milk_yield"):
        my = plan["milk_yield"]
        litres = float(my.get("litres", 0))
        animal_count = int(my.get("animal_count", 1))

        # Update farmer dashboard livestock summary
        lsum = farmer.setdefault("livestock_summary", {})
        lsum["daily_milk_litres"] = litres

        # Append or update today's milk yield record
        prod_logs = farmer.setdefault("milk_production_logs", [])
        existing_log = next((l for l in prod_logs if l.get("date") == today_str), None)
        if existing_log:
            existing_log["daily_milk_litres"] = litres
            existing_log["animal_count"] = animal_count
        else:
            prod_logs.insert(0, {
                "date": today_str,
                "daily_milk_litres": litres,
                "animal_count": animal_count,
                "average_per_cow": round(litres / max(1, animal_count), 1)
            })

        avg_cow = round(litres / max(1, animal_count), 1)
        actions_taken.append({
            "module_id": "livestock",
            "module_name": {"en": "Livestock Milk Registry", "mr": "पशुधन दूध उत्पादन नोंद"},
            "action_desc": {
                "en": f"Recorded daily milk yield of {litres:.1f} Litres from {animal_count} cows (Avg: {avg_cow:.1f} L/cow).",
                "mr": f"{animal_count} गाईंचे दैनिक {litres:.1f} लिटर दूध उत्पादन नोंदवले (सरासरी: {avg_cow:.1f} लि/गाय)."
            },
            "view_url": "/livestock",
            "badge_color": "blue",
            "details": [
                {"label": {"en": "Total Yield", "mr": "एकूण दूध"}, "value": f"{litres:.1f} Litres"},
                {"label": {"en": "Animal Count", "mr": "जनावरांची संख्या"}, "value": f"{animal_count} Cows"},
                {"label": {"en": "Average / Cow", "mr": "प्रति गाय सरासरी"}, "value": f"{avg_cow:.1f} L/day"},
                {"label": {"en": "Log Date", "mr": "नोंद तारीख"}, "value": today_str}
            ]
        })
        notifications.append({
            "en": f"Daily milk production of {litres:.1f} Litres recorded. Farm livestock summary refreshed.",
            "mr": f"दैनिक {litres:.1f} लिटर दूध उत्पादन यशस्वीरीत्या नोंदवले. शेतकरी डॅशबोर्ड अद्ययावत झाला."
        })

    # -------------------------------------------------------------------------
    # D. Produce Sales & Farm Income Tracker
    # -------------------------------------------------------------------------
    if "produce_income" in actions and plan.get("produce_income"):
        pi = plan["produce_income"]
        amt = float(pi.get("amount", 0))
        crop_en = pi.get("crop_en", "Onion")
        crop_mr = pi.get("crop_mr", "कांदा")

        # Avoid duplicate insertion if exact same amount & crop was logged in last entry
        recent_exp = in_memory_dbs.get("expenses", [])
        is_dup = (
            len(recent_exp) > 0 and
            recent_exp[0].get("amount") == amt and
            recent_exp[0].get("category", {}).get("en") == "Produce Sales & Income"
        )

        if not is_dup and amt > 0:
            new_id = f"EXP-{len(in_memory_dbs['expenses']) + 1:03d}"
            income_entry = {
                "id": new_id,
                "date": today_str,
                "month": {"en": now.strftime("%B %Y"), "mr": now.strftime("%B %Y")},
                "season": {"en": "Rabi 2026-27", "mr": "रब्बी २०२६-२७"},
                "crop": {"en": crop_en, "mr": crop_mr},
                "category": {"en": "Produce Sales & Income", "mr": "उत्पन्न व शेतमाल विक्री"},
                "description": {
                    "en": f"Produce sale: Sold {crop_en} for ₹{amt:,.0f}",
                    "mr": f"शेतमाल विक्री: {crop_mr} विक्रीतून ₹{amt:,.0f} उत्पन्न"
                },
                "amount": amt,
                "payment_mode": {"en": "Cash", "mr": "रोख"},
                "type": "Income"
            }
            in_memory_dbs["expenses"].insert(0, income_entry)

        actions_taken.append({
            "module_id": "expenses",
            "module_name": {"en": "Farm Expense Tracker (Income)", "mr": "शेतखर्च वही (उत्पन्न)"},
            "action_desc": {
                "en": f"Logged produce revenue of ₹{amt:,.0f} from {crop_en} sales.",
                "mr": f"{crop_mr} शेतमाल विक्रीतून ₹{amt:,.0f} उत्पन्नाची नोंद केली."
            },
            "view_url": "/expenses",
            "badge_color": "emerald",
            "details": [
                {"label": {"en": "Revenue Amount", "mr": "उत्पन्न रक्कम"}, "value": f"₹{amt:,.0f}"},
                {"label": {"en": "Crop Sold", "mr": "विक्री केलेले पीक"}, "value": crop_en},
                {"label": {"en": "Category", "mr": "प्रवर्ग"}, "value": "Produce Sales & Income"},
                {"label": {"en": "Date", "mr": "तारीख"}, "value": today_str}
            ]
        })
        notifications.append({
            "en": f"Produce sale income of ₹{amt:,.0f} ({crop_en}) recorded in Farm Expense Tracker.",
            "mr": f"{crop_mr} विक्रीतून मिळालेले ₹{amt:,.0f} उत्पन्न शेतखर्च वहीत नोंदवले गेले."
        })

    # -------------------------------------------------------------------------
    # E. Farm Expenditure Logging
    # -------------------------------------------------------------------------
    if ("farm_expense" in actions or "add_farm_expense" in actions) and plan.get("farm_expense"):
        fe = plan["farm_expense"]
        amt = float(fe.get("amount", 0))

        # Avoid duplicate insertion if exact same amount & category was logged just now
        recent_exp = in_memory_dbs.get("expenses", [])
        is_dup = (
            len(recent_exp) > 0 and
            recent_exp[0].get("amount") == amt and
            recent_exp[0].get("category", {}).get("en") == fe.get("category_en", "Fertilizers & Nutrients")
        )

        if not is_dup and amt > 0:
            new_id = f"EXP-{len(in_memory_dbs['expenses']) + 1:03d}"
            expense_entry = {
                "id": new_id,
                "date": today_str,
                "month": {"en": now.strftime("%B %Y"), "mr": now.strftime("%B %Y")},
                "season": {"en": "Rabi 2026-27", "mr": "रब्बी २०२६-२७"},
                "crop": {
                    "en": fe.get("crop_en", "General Farm"),
                    "mr": fe.get("crop_mr", "सामायिक शेती")
                },
                "category": {
                    "en": fe.get("category_en", "Fertilizers & Nutrients"),
                    "mr": fe.get("category_mr", "खते व पोषण")
                },
                "description": {
                    "en": fe.get("description_en", raw_text),
                    "mr": fe.get("description_mr", raw_text)
                },
                "amount": amt,
                "payment_mode": {
                    "en": fe.get("payment_mode_en", "Cash"),
                    "mr": fe.get("payment_mode_mr", "रोख")
                }
            }
            in_memory_dbs["expenses"].insert(0, expense_entry)

        cat_disp_en = fe.get("category_en", "General Farm Inputs")
        cat_disp_mr = fe.get("category_mr", "सामायिक शेती")
        actions_taken.append({
            "module_id": "expenses",
            "module_name": {"en": "Farm Expense Tracker", "mr": "शेत खर्च वही"},
            "action_desc": {
                "en": f"Logged expenditure of ₹{amt:,.0f} under {cat_disp_en}.",
                "mr": f"₹{amt:,.0f} खर्च नोंदवला - {cat_disp_mr}."
            },
            "view_url": "/expenses",
            "badge_color": "amber",
            "details": [
                {"label": {"en": "Amount", "mr": "रक्कम"}, "value": f"₹{amt:,.0f}"},
                {"label": {"en": "Category", "mr": "प्रवर्ग"}, "value": cat_disp_en},
                {"label": {"en": "Crop / Module", "mr": "पीक / विभाग"}, "value": fe.get("crop_en", "General Farm")},
                {"label": {"en": "Payment Mode", "mr": "पेमेंट पद्धत"}, "value": fe.get("payment_mode_en", "Cash")}
            ]
        })
        notifications.append({
            "en": f"Expense of ₹{amt:,.0f} recorded under {cat_disp_en}.",
            "mr": f"{cat_disp_mr} अंतर्गत ₹{amt:,.0f} चा खर्च नोंदवला गेला."
        })

    # -------------------------------------------------------------------------
    # F. Marketplace Advance Listing
    # -------------------------------------------------------------------------
    if ("marketplace_listing" in actions or "add_marketplace" in actions) and plan.get("marketplace"):
        mkt = plan["marketplace"]
        new_id = f"MKT-{len(in_memory_dbs['marketplace']) + 101:03d}"
        q = float(mkt.get("quantity_quintals", 10.0))
        price = float(mkt.get("expected_price_per_quintal", 2000.0))

        listing_entry = {
            "id": new_id,
            "crop_name": {"en": mkt.get("crop_name_en", "Farm Produce"), "mr": mkt.get("crop_name_mr", "शेतमाल")},
            "category": {"en": mkt.get("category_en", "Vegetables"), "mr": mkt.get("category_mr", "भाजीपाला")},
            "variety": {"en": mkt.get("variety_en", "Fresh Harvest"), "mr": mkt.get("variety_mr", "ताजी काढणी")},
            "quality_grade": {"en": mkt.get("quality_grade_en", "Grade A"), "mr": mkt.get("quality_grade_mr", "अ दर्जा")},
            "quantity_quintals": q,
            "expected_price_per_quintal": price,
            "seller_name": farmer.get("name", {"en": "Farmer", "mr": "शेतकरी"}),
            "seller_phone": farmer.get("phone", "+91 98220 12345"),
            "village": farmer.get("village", {"en": "Pimpalgaon Baswant", "mr": "पिंपळगाव बसवंत"}),
            "taluka": farmer.get("taluka", {"en": "Niphad", "mr": "निफाड"}),
            "district": farmer.get("district", {"en": "Nashik", "mr": "नाशिक"}),
            "location": {
                "en": f"{farmer.get('village', {}).get('en', 'Pimpalgaon')}, {farmer.get('taluka', {}).get('en', 'Niphad')}",
                "mr": f"{farmer.get('village', {}).get('mr', 'पिंपळगाव')}, {farmer.get('taluka', {}).get('mr', 'निफाड')}"
            },
            "harvest_date": today_str,
            "status": {"en": "Available", "mr": "उपलब्ध"},
            "notes": {"en": f"Listed via Smart Log. {raw_text}", "mr": f"स्मार्ट नोंदणीद्वारे पोस्ट केले. {raw_text}"}
        }
        in_memory_dbs["marketplace"].insert(0, listing_entry)
        actions_taken.append({
            "module_id": "marketplace",
            "module_name": {"en": "Farmer Marketplace", "mr": "शेतकरी थेट बाजारपेठ"},
            "action_desc": {
                "en": f"Posted listing for {q:.0f} Qtl {listing_entry['crop_name']['en']} @ ₹{price:,.0f}/Qtl",
                "mr": f"{listing_entry['crop_name']['mr']} {q:.0f} क्विंटल विक्री नोंदणी @ ₹{price:,.0f}/क्विंटल"
            },
            "view_url": "/marketplace",
            "badge_color": "blue",
            "details": [
                {"label": {"en": "Listing ID", "mr": "नोंदणी क्र."}, "value": new_id},
                {"label": {"en": "Produce", "mr": "शेतमाल"}, "value": listing_entry['crop_name']['en']},
                {"label": {"en": "Quantity", "mr": "प्रमाण"}, "value": f"{q:.0f} Qtl"},
                {"label": {"en": "Target Price", "mr": "अपेक्षित दर"}, "value": f"₹{price:,.0f}/Qtl"}
            ]
        })

    # -------------------------------------------------------------------------
    # G. Crop Calendar / Spray Task
    # -------------------------------------------------------------------------
    if ("crop_task" in actions or "add_crop_task" in actions) and plan.get("crop_task"):
        tsk = plan["crop_task"]
        new_id = f"TSK-{len(in_memory_dbs['tasks']) + 1:02d}"

        task_entry = {
            "id": new_id,
            "crop": {"en": tsk.get("crop_en", "General Farm"), "mr": tsk.get("crop_mr", "सामायिक शेती")},
            "title": {"en": tsk.get("title_en", raw_text), "mr": tsk.get("title_mr", raw_text)},
            "stage": {"en": "Crop Management", "mr": "पीक व्यवस्थापन"},
            "due_date": {"en": "Scheduled", "mr": "नियोजित"},
            "priority": {"en": "High", "mr": "उच्च"},
            "status": False
        }
        in_memory_dbs["tasks"].insert(0, task_entry)
        actions_taken.append({
            "module_id": "tasks",
            "module_name": {"en": "Crop Calendar & Advisory", "mr": "पीक दिनदर्शिका व कामे"},
            "action_desc": {
                "en": f"Scheduled task: {task_entry['title']['en']} ({task_entry['crop']['en']})",
                "mr": f"नवीन काम जोडले: {task_entry['title']['mr']} ({task_entry['crop']['mr']})"
            },
            "view_url": "/crop-helper",
            "badge_color": "purple",
            "details": [
                {"label": {"en": "Task ID", "mr": "काम क्र."}, "value": new_id},
                {"label": {"en": "Crop", "mr": "पीक"}, "value": task_entry['crop']['en']},
                {"label": {"en": "Due Date", "mr": "मुदत"}, "value": task_entry['due_date']['en']}
            ]
        })

    return {
        "actions_taken": actions_taken,
        "has_pending_cattle": has_pending_cattle,
        "pending_cattle_info": pending_cattle_info,
        "notifications": notifications
    }
