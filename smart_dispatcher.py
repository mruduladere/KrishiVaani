"""
smart_dispatcher.py - Multi-Intent Natural Language & Voice Dispatcher for KrishiVaani
Parses natural language (Marathi / English / Hinglish / Marathinglish) using Sarvam AI (sarvam-105b)
and extracts structured multi-module actions (Livestock, Expenses, Marketplace, Crop Tasks).
Directly updates in-memory stores with 100% offline regex/keyword fallback.
Strictly NO DATABASE.
"""

import re
import json
import logging
from datetime import datetime
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
        "actions_taken": [
            {
                "module_id": "livestock" | "expenses" | "marketplace" | "tasks",
                "module_name": {"en": "...", "mr": "..."},
                "action_desc": {"en": "...", "mr": "..."},
                "view_url": "/livestock" | "/expenses" | "/marketplace" | "/crop-helper",
                "details": [ {"label": {"en": "...", "mr": "..."}, "value": str/num} ]
            }
        ]
    }
    """
    cleaned = (raw_text or "").strip()
    if not cleaned:
        return {
            "success": False,
            "raw_text": "",
            "engine": "None",
            "actions_taken": [],
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

Analyze the statement. A single input may trigger ONE or MULTIPLE modules simultaneously:
1. "add_livestock": if the farmer purchased, registered, or updated an animal (Cow, Buffalo, Goat, Bull, etc.), including breed, age, price, or vaccine.
2. "add_expense": if any money was spent on farm inputs, livestock purchase, feed, seeds, fertilizer, labour, diesel, repairs, or veterinary.
3. "add_marketplace": if the farmer wants to sell produce or post a harvest listing (crop name, quantity in quintals, expected price).
4. "add_crop_task": if the farmer needs a farm reminder/task (e.g. spray fungicide, apply fertilizer, irrigation, weeding, harvest).

Return VALID JSON ONLY with this exact schema:
{{
    "actions": ["add_livestock", "add_expense", "add_marketplace", "add_crop_task"],
    "livestock": {{
        "name_en": "string",
        "name_mr": "string",
        "type_en": "Cow | Buffalo | Goat | Bull",
        "type_mr": "गाय | म्हैस | शेळी | बैल",
        "breed_en": "string (e.g. Gir, Murrah, Osmanabadi)",
        "breed_mr": "string (e.g. गीर, मुऱ्हा, उस्मानाबादी)",
        "age_years": number,
        "daily_milk": number,
        "vaccine_name_en": "string (or empty)",
        "vaccine_name_mr": "string (or empty)",
        "vaccine_date": "YYYY-MM-DD (or empty)"
    }},
    "expense": {{
        "amount": number,
        "category_en": "Seeds & Seedlings | Fertilizers & Nutrients | Pesticides & Bio-agents | Labour & Pruning | Irrigation & Water | Machinery & Rentals | Transport & Mandi Hamali | Animal Fodder & Feed | Veterinary & Healthcare | Animal Vaccination | Fuel & Electricity | Repairs & Maintenance",
        "category_mr": "बियाणे व रोपे | खते व पोषण | कीटकनाशके व बुरशीनाशके | मजुरी व छाटणी | सिंचन व पाणी | यंत्रसामग्री व भाडे | वाहतूक व हमाली | पशुखाद्य व वैरण | पशुवैद्यकीय उपचार | पशुधन लसीकरण | डिझेल व वीज बिल | दुरुस्ती व देखभाल",
        "crop_en": "Grapes | Onion | Soybean | Livestock / Dairy | General Farm",
        "crop_mr": "द्राक्ष | कांदा | सोयाबीन | दुग्धव्यवसाय / पशुधन | सामायिक शेती",
        "season_en": "Rabi 2026-27 | Kharif 2026",
        "season_mr": "रब्बी २०२६-२७ | खरीप २०२६",
        "payment_mode_en": "UPI | Cash | Bank Transfer",
        "payment_mode_mr": "यूपीआय | रोख | बँक ट्रान्सफर",
        "description_en": "string",
        "description_mr": "string"
    }},
    "marketplace": {{
        "crop_name_en": "string",
        "crop_name_mr": "string",
        "category_en": "Vegetables | Fruits | Grains & Pulses",
        "category_mr": "भाजीपाला | फळे | धान्य व कडधान्ये",
        "variety_en": "string",
        "variety_mr": "string",
        "quality_grade_en": "string",
        "quality_grade_mr": "string",
        "quantity_quintals": number,
        "expected_price_per_quintal": number
    }},
    "crop_task": {{
        "title_en": "string",
        "title_mr": "string",
        "crop_en": "Grapes | Onion | Soybean | General Farm",
        "crop_mr": "द्राक्ष | कांदा | सोयाबीन | सामायिक शेती",
        "stage_en": "string",
        "stage_mr": "string",
        "due_date_en": "string",
        "due_date_mr": "string",
        "priority_en": "High | Medium | Low",
        "priority_mr": "उच्च | मध्यम | कमी"
    }}
}}
If a section is not triggered by the input, omit it or set its values to null.
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
        parsed_plan = _offline_parse_dispatch(cleaned)
        engine_used = "Offline Deterministic Engine"

    # Now execute the plan against the in-memory databases
    actions_taken = _apply_dispatch_plan(parsed_plan, cleaned, farmer, in_memory_dbs)

    return {
        "success": len(actions_taken) > 0,
        "raw_text": cleaned,
        "engine": engine_used,
        "actions_taken": actions_taken
    }


def _offline_parse_dispatch(text: str) -> dict:
    """Deterministic offline parser using Marathi and English keyword heuristics."""
    text_lower = text.lower()
    actions = []
    plan = {"actions": actions}

    # 1. Detect Amount (₹, Rs, रु, रुपये)
    amt = 0.0
    amt_match = re.search(r"(?:₹|rs\.?|रु\.?|रुपये)?\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:₹|rs\.?|रु\.?|रुपये)?", text_lower)
    if amt_match:
        try:
            amt = float(amt_match.group(1).replace(",", ""))
        except ValueError:
            amt = 0.0

    # 2. Check for Livestock Purchase / Record
    is_livestock = any(k in text_lower for k in [
        "cow", "buffalo", "goat", "bull", "calf", "gir", "murrah", "gauri", "lakshmi", "animal",
        "गाय", "म्हैस", "शेळी", "बैल", "वासरू", "गीर", "मुऱ्हा", "गौरी", "लक्ष्मी", "पशुधन"
    ])
    
    # 3. Check for Expense
    is_expense = (amt > 0) or any(k in text_lower for k in [
        "spent", "paid", "bought", "purchased", "expense", "cost", "rupees", "rs", "₹",
        "खर्च", "खरेदी", "दिले", "भरले", "रुपये"
    ])

    # 4. Check for Marketplace Listing
    is_marketplace = any(k in text_lower for k in [
        "quintal", "quintals", "sell", "selling", "listing", "rate", "ready to harvest", "available for sale",
        "क्विंटल", "विकायचा", "विकणे", "विकायचे", "बाजार भाव", "विक्री"
    ])

    # 5. Check for Task / Spray Reminder
    is_task = any(k in text_lower for k in [
        "spray", "spraying", "reminder", "task", "fungicide", "mildew", "fertilizer dose", "irrigate", "schedule",
        "फवारणी", "फवारा", "तासिका", "काम", "नियोजन", "स्मरणपत्र", "बुरशीनाशक", "कीटकनाशक"
    ]) and not (is_expense and not any(k in text_lower for k in ["spray", "फवारणी"]))

    # Handle Livestock
    if is_livestock:
        actions.append("add_livestock")
        # Extract breed & name
        name_en = "Gauri" if "gauri" in text_lower or "गौरी" in text_lower else "Lakshmi" if "lakshmi" in text_lower or "लक्ष्मी" in text_lower else "Kamdhenu"
        name_mr = "गौरी" if "gauri" in text_lower or "गौरी" in text_lower else "लक्ष्मी" if "lakshmi" in text_lower or "लक्ष्मी" in text_lower else "कामधेनू"
        
        is_buffalo = "buffalo" in text_lower or "म्हैस" in text_lower or "मुऱ्हा" in text_lower or "murrah" in text_lower
        type_en = "Buffalo" if is_buffalo else "Cow"
        type_mr = "म्हैस" if is_buffalo else "गाय"
        breed_en = "Murrah" if is_buffalo else "Gir"
        breed_mr = "मुऱ्हा" if is_buffalo else "गीर"

        # Check age
        age = 3.0
        age_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:years?|वर्षे|वर्ष)", text_lower)
        if age_match:
            try:
                age = float(age_match.group(1))
            except ValueError:
                pass

        # Vaccine
        vax_en = "Foot & Mouth Disease (FMD)"
        vax_mr = "लाळ्या खुरखूत (FMD)"
        vax_date = datetime.now().strftime("%Y-%m-%d")

        plan["livestock"] = {
            "name_en": name_en,
            "name_mr": name_mr,
            "type_en": type_en,
            "type_mr": type_mr,
            "breed_en": breed_en,
            "breed_mr": breed_mr,
            "age_years": age,
            "daily_milk": 11.5 if type_en == "Cow" else 9.0,
            "vaccine_name_en": vax_en,
            "vaccine_name_mr": vax_mr,
            "vaccine_date": vax_date
        }

    # Handle Expense
    if is_expense:
        actions.append("add_expense")
        # Identify crop
        crop_en = "General Farm"
        crop_mr = "सामायिक शेती"
        if any(k in text_lower for k in ["कांदा", "कांद्या", "onion"]):
            crop_en = "Onion"
            crop_mr = "कांदा"
        elif any(k in text_lower for k in ["द्राक्ष", "द्राक्षा", "grape"]):
            crop_en = "Grapes"
            crop_mr = "द्राक्ष"
        elif any(k in text_lower for k in ["सोयाबीन", "soybean"]):
            crop_en = "Soybean"
            crop_mr = "सोयाबीन"
        elif is_livestock or any(k in text_lower for k in ["feed", "fodder", "चारा", "पशुखाद्य"]):
            crop_en = "Livestock / Dairy"
            crop_mr = "दुग्धव्यवसाय / पशुधन"

        # Identify category
        cat_en = "Fertilizers & Nutrients"
        cat_mr = "खते व पोषण"
        if is_livestock and amt >= 20000:
            cat_en = "Veterinary & Healthcare"
            cat_mr = "पशुवैद्यकीय उपचार"
        elif any(k in text_lower for k in ["युरिया", "खत", "urea", "dap", "fertilizer"]):
            cat_en = "Fertilizers & Nutrients"
            cat_mr = "खते व पोषण"
        elif any(k in text_lower for k in ["चारा", "पेंड", "पशुखाद्य", "feed", "fodder"]):
            cat_en = "Animal Fodder & Feed"
            cat_mr = "पशुखाद्य व वैरण"
        elif any(k in text_lower for k in ["फवारणी", "spray", "बुरशीनाशक", "pesticide"]):
            cat_en = "Pesticides & Bio-agents"
            cat_mr = "कीटकनाशके व बुरशीनाशके"
        elif any(k in text_lower for k in ["मजुरी", "labour", "छाटणी", "pruning"]):
            cat_en = "Labour & Pruning"
            cat_mr = "मजुरी व छाटणी"

        # Payment mode
        pm_en = "UPI" if any(k in text_lower for k in ["upi", "फोनपे", "gpay", "online"]) else "Cash"
        pm_mr = "यूपीआय" if pm_en == "UPI" else "रोख"

        plan["expense"] = {
            "amount": amt if amt > 0 else 1800.0,
            "category_en": cat_en,
            "category_mr": cat_mr,
            "crop_en": crop_en,
            "crop_mr": crop_mr,
            "season_en": "Rabi 2026-27",
            "season_mr": "रब्बी २०२६-२७",
            "payment_mode_en": pm_en,
            "payment_mode_mr": pm_mr,
            "description_en": f"{cat_en} for {crop_en}: {text}",
            "description_mr": f"{crop_mr} पिकासाठी {cat_mr}: {text}"
        }

    # Handle Marketplace
    if is_marketplace:
        actions.append("add_marketplace")
        # Extract quintals
        q = 40
        q_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:quintals?|क्विंटल)", text_lower)
        if q_match:
            try:
                q = float(q_match.group(1))
            except ValueError:
                pass

        # Extract rate / expected price
        rate = 2400
        rate_match = re.search(r"(?:₹|rs\.?|दर|भाव|price)?\s*(\d+(?:,\d+)?)\s*(?:per quintal|रुपये|₹)?", text_lower)
        if rate_match and float(rate_match.group(1).replace(",", "")) > 500:
            rate = float(rate_match.group(1).replace(",", ""))

        crop_en = "Gavran Red Onion"
        crop_mr = "गावरान लाल कांदा"
        cat_en = "Vegetables"
        cat_mr = "भाजीपाला"
        if "grape" in text_lower or "द्राक्ष" in text_lower:
            crop_en = "Thomson Seedless Grapes"
            crop_mr = "थॉमसन सिडलेस द्राक्ष"
            cat_en = "Fruits"
            cat_mr = "फळे"
        elif "soybean" in text_lower or "सोयाबीन" in text_lower:
            crop_en = "JS 335 Soybean"
            crop_mr = "जेएस ३३५ सोयाबीन"
            cat_en = "Grains & Pulses"
            cat_mr = "धान्य व कडधान्ये"

        plan["marketplace"] = {
            "crop_name_en": crop_en,
            "crop_name_mr": crop_mr,
            "category_en": cat_en,
            "category_mr": cat_mr,
            "variety_en": "Standard Farm Grade",
            "variety_mr": "उत्कृष्ट शेतमाल प्रत",
            "quality_grade_en": "Grade A (Clean & Graded)",
            "quality_grade_mr": "अ दर्जा (प्रतवारी केलेले)",
            "quantity_quintals": q,
            "expected_price_per_quintal": rate
        }

    # Handle Crop Task
    if is_task:
        actions.append("add_crop_task")
        crop_en = "Grapes" if any(k in text_lower for k in ["द्राक्ष", "grape", "mildew"]) else "Onion"
        crop_mr = "द्राक्ष" if crop_en == "Grapes" else "कांदा"

        plan["crop_task"] = {
            "title_en": f"Scheduled farm activity: {text}",
            "title_mr": f"नियोजित शेती काम: {text}",
            "crop_en": crop_en,
            "crop_mr": crop_mr,
            "stage_en": "Growth Stage",
            "stage_mr": "वाढ अवस्था",
            "due_date_en": "Next Monday (In 3 Days)",
            "due_date_mr": "पुढील सोमवारी (३ दिवसांत)",
            "priority_en": "High",
            "priority_mr": "उच्च"
        }

    # If no specific action matched, default to Farm Expense entry
    if not actions:
        actions.append("add_expense")
        plan["expense"] = {
            "amount": amt if amt > 0 else 1000.0,
            "category_en": "General Farm Inputs",
            "category_mr": "सामायिक शेती निविष्ठा",
            "crop_en": "General Farm",
            "crop_mr": "सामायिक शेती",
            "season_en": "Rabi 2026-27",
            "season_mr": "रब्बी २०२६-२७",
            "payment_mode_en": "Cash",
            "payment_mode_mr": "रोख",
            "description_en": text,
            "description_mr": text
        }

    return plan


def _apply_dispatch_plan(plan: dict, raw_text: str, farmer: dict, in_memory_dbs: dict) -> list:
    """
    Applies parsed actions directly to LIVESTOCK_DB, EXPENSES_DB, MARKETPLACE_DB, TASKS_DB.
    Returns list of formatted action summary objects for the UI.
    """
    actions_taken = []
    actions = plan.get("actions", [])

    # 1. Livestock Record
    if "add_livestock" in actions and plan.get("livestock"):
        ls = plan["livestock"]
        new_tag = f"MH-NSK-{len(in_memory_dbs['livestock']) + 101:04d}"
        
        vax_hist = []
        if ls.get("vaccine_name_en") or ls.get("vaccine_name_mr"):
            vax_hist.append({
                "vaccine": {
                    "en": ls.get("vaccine_name_en", "Foot & Mouth Disease (FMD)"),
                    "mr": ls.get("vaccine_name_mr", "लाळ्या खुरखूत")
                },
                "date_given": ls.get("vaccine_date") or datetime.now().strftime("%Y-%m-%d"),
                "due_date": "2027-04-15",
                "status": "Up-to-Date"
            })

        animal_entry = {
            "tag_id": new_tag,
            "name": {
                "en": ls.get("name_en", "Gauri"),
                "mr": ls.get("name_mr", "गौरी")
            },
            "type": {
                "en": ls.get("type_en", "Cow"),
                "mr": ls.get("type_mr", "गाय")
            },
            "breed": {
                "en": ls.get("breed_en", "Gir"),
                "mr": ls.get("breed_mr", "गीर")
            },
            "age_years": float(ls.get("age_years", 3.0)),
            "daily_milk_yield_litres": float(ls.get("daily_milk", 10.0)),
            "health_status": {
                "en": "Healthy & Vaccinated",
                "mr": "निरोगी व लसीकरण पूर्ण"
            },
            "vaccination_history": vax_hist
        }
        
        # Prepend to livestock list
        in_memory_dbs["livestock"].insert(0, animal_entry)

        actions_taken.append({
            "module_id": "livestock",
            "module_name": {"en": "Livestock Records", "mr": "पशुधन व्यवस्थापन"},
            "action_desc": {
                "en": f"Registered new {animal_entry['breed']['en']} {animal_entry['type']['en']} '{animal_entry['name']['en']}' (Tag: {new_tag})",
                "mr": f"नवीन {animal_entry['breed']['mr']} {animal_entry['type']['mr']} '{animal_entry['name']['mr']}' (टॅग: {new_tag}) नोंदवली"
            },
            "view_url": "/livestock",
            "badge_color": "emerald",
            "details": [
                {"label": {"en": "Tag ID", "mr": "टॅग क्र."}, "value": new_tag},
                {"label": {"en": "Breed & Type", "mr": "जात व प्रकार"}, "value": f"{animal_entry['breed']['en']} / {animal_entry['type']['en']}"},
                {"label": {"en": "Age", "mr": "वय"}, "value": f"{animal_entry['age_years']} Yrs"},
                {"label": {"en": "Vaccine Status", "mr": "लसीकरण स्थिती"}, "value": "Up-to-Date"}
            ]
        })

    # 2. Expense Entry
    if "add_expense" in actions and plan.get("expense"):
        exp = plan["expense"]
        new_id = f"EXP-{len(in_memory_dbs['expenses']) + 1:03d}"
        now = datetime.now()
        month_en = now.strftime("%B %Y")
        marathi_months = {
            "January": "जानेवारी", "February": "फेब्रुवारी", "March": "मार्च", "April": "एप्रिल",
            "May": "मे", "June": "जून", "July": "जुलै", "August": "ऑगस्ट", "September": "सप्टेंबर",
            "October": "ऑक्टोबर", "November": "नोव्हेंबर", "December": "डिसेंबर"
        }
        eng_m = now.strftime("%B")
        mr_m = marathi_months.get(eng_m, eng_m)
        month_mr = f"{mr_m} {now.year}"

        amt = float(exp.get("amount", 0))
        if amt > 0:
            expense_entry = {
                "id": new_id,
                "date": now.strftime("%Y-%m-%d"),
                "month": {"en": month_en, "mr": month_mr},
                "season": {
                    "en": exp.get("season_en", "Rabi 2026-27"),
                    "mr": exp.get("season_mr", "रब्बी २०२६-२७")
                },
                "crop": {
                    "en": exp.get("crop_en", "General Farm"),
                    "mr": exp.get("crop_mr", "सामायिक शेती")
                },
                "category": {
                    "en": exp.get("category_en", "Fertilizers & Nutrients"),
                    "mr": exp.get("category_mr", "खते व पोषण")
                },
                "description": {
                    "en": exp.get("description_en", raw_text),
                    "mr": exp.get("description_mr", raw_text)
                },
                "amount": amt,
                "payment_mode": {
                    "en": exp.get("payment_mode_en", "Cash"),
                    "mr": exp.get("payment_mode_mr", "रोख")
                }
            }
            # Prepend to expenses list
            in_memory_dbs["expenses"].insert(0, expense_entry)

            actions_taken.append({
                "module_id": "expenses",
                "module_name": {"en": "Farm Expense Tracker", "mr": "शेत खर्च वही"},
                "action_desc": {
                    "en": f"Logged expense of ₹{amt:,.0f} under {expense_entry['category']['en']} ({expense_entry['crop']['en']})",
                    "mr": f"₹{amt:,.0f} खर्च नोंदवला - {expense_entry['category']['mr']} ({expense_entry['crop']['mr']})"
                },
                "view_url": "/expenses",
                "badge_color": "amber",
                "details": [
                    {"label": {"en": "Receipt ID", "mr": "पावती क्र."}, "value": new_id},
                    {"label": {"en": "Amount", "mr": "रक्कम"}, "value": f"₹{amt:,.0f}"},
                    {"label": {"en": "Category", "mr": "प्रवर्ग"}, "value": expense_entry['category']['en']},
                    {"label": {"en": "Payment Mode", "mr": "पेमेंट मोड"}, "value": expense_entry['payment_mode']['en']}
                ]
            })

    # 3. Marketplace Listing
    if "add_marketplace" in actions and plan.get("marketplace"):
        mkt = plan["marketplace"]
        new_id = f"MKT-{len(in_memory_dbs['marketplace']) + 101:03d}"
        q = float(mkt.get("quantity_quintals", 10.0))
        price = float(mkt.get("expected_price_per_quintal", 2000.0))

        listing_entry = {
            "id": new_id,
            "crop_name": {
                "en": mkt.get("crop_name_en", "Farm Produce"),
                "mr": mkt.get("crop_name_mr", "शेतमाल")
            },
            "category": {
                "en": mkt.get("category_en", "Vegetables"),
                "mr": mkt.get("category_mr", "भाजीपाला")
            },
            "variety": {
                "en": mkt.get("variety_en", "Fresh Harvest"),
                "mr": mkt.get("variety_mr", "ताजी काढणी")
            },
            "quality_grade": {
                "en": mkt.get("quality_grade_en", "Grade A (Clean & Graded)"),
                "mr": mkt.get("quality_grade_mr", "अ दर्जा (प्रतवारी केलेले)")
            },
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
            "harvest_date": datetime.now().strftime("%Y-%m-%d"),
            "status": {"en": "Available", "mr": "उपलब्ध"},
            "notes": {
                "en": f"Freshly listed via KrishiVaani Smart Log. {raw_text}",
                "mr": f"कृषीवाणी स्मार्ट नोंदणीद्वारे थेट पोस्ट केलेले. {raw_text}"
            }
        }
        # Prepend to marketplace list
        in_memory_dbs["marketplace"].insert(0, listing_entry)

        actions_taken.append({
            "module_id": "marketplace",
            "module_name": {"en": "Farmer Marketplace", "mr": "शेतकरी थेट बाजारपेठ"},
            "action_desc": {
                "en": f"Posted listing for {q:.0f} quintals of {listing_entry['crop_name']['en']} @ ₹{price:,.0f}/Qtl",
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

    # 4. Crop Task
    if "add_crop_task" in actions and plan.get("crop_task"):
        tsk = plan["crop_task"]
        new_id = f"TSK-{len(in_memory_dbs['tasks']) + 1:02d}"

        task_entry = {
            "id": new_id,
            "crop": {
                "en": tsk.get("crop_en", "General Farm"),
                "mr": tsk.get("crop_mr", "सामायिक शेती")
            },
            "title": {
                "en": tsk.get("title_en", raw_text),
                "mr": tsk.get("title_mr", raw_text)
            },
            "stage": {
                "en": tsk.get("stage_en", "Crop Protection"),
                "mr": tsk.get("stage_mr", "पीक संरक्षण")
            },
            "due_date": {
                "en": tsk.get("due_date_en", "Next Monday"),
                "mr": tsk.get("due_date_mr", "पुढील सोमवारी")
            },
            "priority": {
                "en": tsk.get("priority_en", "High"),
                "mr": tsk.get("priority_mr", "उच्च")
            },
            "status": False
        }
        # Prepend to tasks list
        in_memory_dbs["tasks"].insert(0, task_entry)

        actions_taken.append({
            "module_id": "tasks",
            "module_name": {"en": "Crop Calendar & Advisory", "mr": "पीक दिनदर्शिका व कामे"},
            "action_desc": {
                "en": f"Scheduled task: {task_entry['title']['en']} ({task_entry['crop']['en']})",
                "mr": f"नवीन शेती काम जोडले: {task_entry['title']['mr']} ({task_entry['crop']['mr']})"
            },
            "view_url": "/crop-helper",
            "badge_color": "purple",
            "details": [
                {"label": {"en": "Task ID", "mr": "काम क्र."}, "value": new_id},
                {"label": {"en": "Crop", "mr": "पीक"}, "value": task_entry['crop']['en']},
                {"label": {"en": "Priority", "mr": "प्राधान्य"}, "value": task_entry['priority']['en']},
                {"label": {"en": "Due Date", "mr": "मुदत"}, "value": task_entry['due_date']['en']}
            ]
        })

    return actions_taken
