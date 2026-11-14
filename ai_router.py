"""
ai_router.py - Multilingual Farmer AI Intent Router & Knowledge Engine
Designed specifically for Maharashtra farmers (Smart India Hackathon SIH 2026).
- 100% Offline Reliable Rule & Live-Data Response Engine reading in-memory farm state.
- Optional Google Gemini API integration when GEMINI_API_KEY environment variable is present.
- Detects query language (Marathi vs English) and responds in the EXACT matching language.
- Recommends direct one-click navigation links to relevant KrishiVaani modules.
- STRICTLY ZERO DATABASE required.
"""

import os
import re
import datetime


def is_marathi_text(text: str) -> bool:
    """Checks if text contains Devanagari Unicode characters (U+0900 to U+097F)."""
    return bool(re.search(r"[\u0900-\u097F]", text))


def route_farmer_query(query: str, farmer: dict, live_context: dict, lang: str = None) -> dict:
    """
    Intelligent bilingual query router.
    
    Parameters:
    - query: User query string in Marathi or English
    - farmer: Active farmer profile dictionary from in-memory session
    - live_context: Dictionary with current in-memory stats (expenses, livestock, crops, services, marketplace)
    - lang: Active session language ('mr' or 'en')
    
    Returns:
    {
        "response_text": str,
        "recommended_module": {
            "title": str,
            "url": str,
            "icon": str
        } or None,
        "intent": str
    }
    """
    cleaned_query = (query or "").strip()
    if not cleaned_query:
        msg_en = "Please ask a question regarding your farm, crops, livestock, services, or expenses."
        msg_mr = "कृपया आपले शेत, पिके, पशुधन, स्थानिक सेवा किंवा खर्चाविषयी प्रश्न विचारा."
        return {
            "response_text": msg_mr if (lang == "mr" or is_marathi_text(cleaned_query)) else msg_en,
            "recommended_module": None,
            "intent": "empty"
        }

    # Detect language of the query
    detected_lang = "mr" if is_marathi_text(cleaned_query) else (lang if lang in ("mr", "en") else "en")
    q_lower = cleaned_query.lower()

    # Extract live context numbers
    exp_ctx = live_context.get("expenses", {})
    cur_month_spend = exp_ctx.get("current_month_spend", 12450)
    total_spend = exp_ctx.get("total_spend", 35550)
    top_cat_en = exp_ctx.get("top_category_en", "Fertilizers & Nutrients")
    top_cat_mr = exp_ctx.get("top_category_mr", "खते व पोषण")

    ls_ctx = live_context.get("livestock", {})
    total_animals = ls_ctx.get("total_animals", 7)
    daily_milk = ls_ctx.get("daily_milk", 39.5)
    overdue_count = ls_ctx.get("overdue_count", 1)
    overdue_details = ls_ctx.get("overdue_details", "Gauri (Gir Cow) - FMD")

    crop_ctx = live_context.get("crops", {})
    active_crops_en = crop_ctx.get("crops_en", "Grapes, Onion, Soybean")
    active_crops_mr = crop_ctx.get("crops_mr", "द्राक्ष, कांदा, सोयाबीन")
    pending_tasks_count = crop_ctx.get("pending_tasks", 5)

    srv_ctx = live_context.get("services", {})
    srv_count = srv_ctx.get("total_services", 4)
    srv_sample_en = srv_ctx.get("sample_en", "Dr. Deshmukh Vet Clinic & Kisan Krishi Seva Kendra")
    srv_sample_mr = srv_ctx.get("sample_mr", "डॉ. देशमुख पशुवैद्यक क्लिनिक व किसान कृषी सेवा केंद्र")

    mkt_ctx = live_context.get("marketplace", {})
    mkt_count = mkt_ctx.get("total_listings", 6)

    # -------------------------------------------------------------
    # 1. OPTIONAL GEMINI API CALL (If user configured GEMINI_API_KEY)
    # -------------------------------------------------------------
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if gemini_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            prompt = f"""
You are KrishiVaani Agro Assistant, a polite and practical agricultural copilot for Maharashtra farmers.
Farmer Name: {farmer.get('name', {}).get(detected_lang, 'Ramesh Patil')}
Location: Niphad, Nashik, Maharashtra
Live Farm Data:
- Active Crops: {active_crops_en if detected_lang == 'en' else active_crops_mr}
- November 2026 Monthly Spend: ₹{cur_month_spend:,} (Total: ₹{total_spend:,})
- Top Expense Category: {top_cat_en if detected_lang == 'en' else top_cat_mr}
- Livestock: {total_animals} animals, Daily Milk: {daily_milk} L, Overdue Vaccines: {overdue_count} ({overdue_details})
- Regional Agro Services: {srv_count} stores/clinics in Niphad

Answer this farmer's query in 2-3 concise, helpful sentences in { 'pure Marathi (मराठी)' if detected_lang == 'mr' else 'pure English' }:
Query: "{cleaned_query}"
"""
            gemini_resp = model.generate_content(prompt)
            if gemini_resp and gemini_resp.text:
                # Classify intent for module button
                rec_module = _detect_recommended_module(q_lower, detected_lang)
                return {
                    "response_text": gemini_resp.text.strip(),
                    "recommended_module": rec_module,
                    "intent": "gemini_generated"
                }
        except Exception:
            # Seamless fallback to offline deterministic engine
            pass

    # -------------------------------------------------------------
    # 2. OFFLINE 100% DETERMINISTIC BILINGUAL INTENT & LIVE DATA ENGINE
    # -------------------------------------------------------------

    # Intent A: EXPENSE & BUDGET INQUIRY
    expense_keywords = [
        "खर्च", "पैसा", "पैसे", "बिल", "खर्चा", "हिशोब", "बजेट", "रुपये",
        "expense", "spend", "cost", "budget", "money", "ledger", "spent"
    ]
    if any(k in q_lower for k in expense_keywords):
        if detected_lang == "mr":
            response = (
                f"आपला चालू महिन्यातील (नोव्हेंबर २०२६) शेतखर्च ₹{cur_month_spend:,} इतका झाला आहे. "
                f"हंगामातील एकूण नोंदवलेला खर्च ₹{total_spend:,} असून, सर्वाधिक गुंतवणूक '{top_cat_mr}' "
                f"या प्रकारात झाली आहे. सविस्तर हिशोब व चार्ट पाहण्यासाठी खालील बटणावर क्लिक करा."
            )
            module = {
                "title": "विभाग ७: शेतखर्च नोंदवही उघडा",
                "url": "/expenses",
                "icon": "receipt"
            }
        else:
            response = (
                f"Your farm expenditure for the active month (November 2026) is ₹{cur_month_spend:,}. "
                f"Your total recorded spend across 12 agro categories is ₹{total_spend:,}, with the highest "
                f"share invested in '{top_cat_en}'. Click below to inspect your seasonal cash-flow ledger."
            )
            module = {
                "title": "Open Module 7: Farm Expense Tracker",
                "url": "/expenses",
                "icon": "receipt"
            }
        return {"response_text": response, "recommended_module": module, "intent": "expenses"}

    # Intent B: CROP ADVISORY & TASKS
    crop_keywords = [
        "पीक", "पिके", "शेतात", "काम", "द्राक्ष", "कांदा", "सोयाबीन", "फवारणी", "हंगाम", "खत", "छाटणी", "रोग", "भुरी", "पाणी", "सापळे",
        "crop", "grape", "onion", "soybean", "spray", "harvest", "pruning", "task", "work", "farm", "fertilizer dose", "mildew"
    ]
    if any(k in q_lower for k in crop_keywords):
        if detected_lang == "mr":
            response = (
                f"आपल्या शेतात सध्या {active_crops_mr} ही मुख्य पिके नोंदणीकृत आहेत. "
                f"द्राक्षासाठी सध्या गोडी छाटणीनंतर टप्पा ३ (फुलधारणा व मणी सेटिंग) सुरू असून ०:५२:३४ खताचा डोस आणि भुरी प्रतिबंधक सल्फर फवारणी शिफारस केलेली आहे. "
                f"आपल्याकडे {pending_tasks_count} आगामी शेतकामे नियोजित आहेत."
            )
            module = {
                "title": "विभाग २: पीक सल्ला व कामे पहा",
                "url": "/crop-helper",
                "icon": "sprout"
            }
        else:
            response = (
                f"Your farm currently has active plots of {active_crops_en}. "
                f"Your Thomson Seedless grapes are in Stage 3 (Flowering & Berry Setting), requiring 0:52:34 MKP foliar nutrition and powdery mildew prophylaxis. "
                f"You currently have {pending_tasks_count} pending field tasks scheduled."
            )
            module = {
                "title": "Open Module 2: Crop & Farming Helper",
                "url": "/crop-helper",
                "icon": "sprout"
            }
        return {"response_text": response, "recommended_module": module, "intent": "crops"}

    # Intent C: NEARBY SERVICES & INPUT SHOPS
    service_keywords = [
        "दुकान", "दुकानदार", "डॉक्टर", "दवाखाना", "पशुवैद्यक", "अवजारे", "भाडे", "सेवा", "जवळ", "खते दुकान", "बियाणे", "ट्रॅक्टर", "क्लिनिक",
        "service", "shop", "store", "vet", "doctor", "clinic", "machinery", "tractor", "near", "fertilizer shop", "seed shop", "rental"
    ]
    if any(k in q_lower for k in service_keywords):
        if detected_lang == "mr":
            response = (
                f"निफाड व पिंपळगाव बसवंत तालुक्यात {srv_count} प्रमाणित कृषी सेवा केंद्र उपलब्ध आहेत. "
                f"यामध्ये {srv_sample_mr} यांचा समावेश आहे. "
                f"आपण थेट फोन किंवा व्हॉट्सॲपवरून संपर्क साधू शकता."
            )
            module = {
                "title": "विभाग ४: जवळची कृषी सेवा केंद्र पहा",
                "url": "/nearby-services",
                "icon": "map-pin"
            }
        else:
            response = (
                f"There are {srv_count} verified agricultural service providers registered in Niphad & Pimpalgaon Baswant. "
                f"Key verified centres include {srv_sample_en}. "
                f"You can call or WhatsApp them directly from the directory."
            )
            module = {
                "title": "Open Module 4: Nearby Agricultural Services",
                "url": "/nearby-services",
                "icon": "map-pin"
            }
        return {"response_text": response, "recommended_module": module, "intent": "services"}

    # Intent D: LIVESTOCK & VACCINATIONS
    livestock_keywords = [
        "जनावर", "जनावरे", "गाय", "म्हैस", "शेळी", "लस", "लसीकरण", "दूध", "आजारी", "खुरखूत", "पशुधन", "गीर", "गोठा",
        "livestock", "cow", "cattle", "buffalo", "goat", "vaccine", "vaccination", "overdue", "milk", "fmd", "health", "gir"
    ]
    if any(k in q_lower for k in livestock_keywords):
        if detected_lang == "mr":
            if overdue_count > 0:
                response = (
                    f"आपल्या गोठ्यात एकूण {total_animals} जनावरे नोंदणीकृत असून सरासरी दैनिक दूध उत्पादन {daily_milk} लिटर आहे. "
                    f"लक्ष द्या: 'गौरी' (गीर गाय) ची लाळ्या खुरखूत (FMD) लस मुदतबाह्य (Overdue) झाली आहे. "
                    f"तातडीने लसीकरण नोंदवण्यासाठी खालील विभाग उघडा."
                )
            else:
                response = (
                    f"आपल्या गोठ्यात एकूण {total_animals} जनावरे नोंदणीकृत असून दैनिक दूध {daily_milk} लिटर आहे. "
                    f"सर्व जनावरांचे लसीकरण वेळेवर पूर्ण आहे."
                )
            module = {
                "title": "विभाग ६: पशुधन नोंदवही व लसीकरण उघडा",
                "url": "/livestock",
                "icon": "heart-pulse"
            }
        else:
            if overdue_count > 0:
                response = (
                    f"Your livestock holding comprises {total_animals} registered animals producing {daily_milk} L/day. "
                    f"Alert: {overdue_details} vaccination is currently overdue past its scheduled date. "
                    f"Click below to review cattle health records and log the completed vaccine dose."
                )
            else:
                response = (
                    f"Your livestock registry contains {total_animals} healthy animals yielding {daily_milk} L of milk daily. "
                    f"All scheduled vaccines are currently up-to-date."
                )
            module = {
                "title": "Open Module 6: Livestock Records & Reminders",
                "url": "/livestock",
                "icon": "heart-pulse"
            }
        return {"response_text": response, "recommended_module": module, "intent": "livestock"}

    # Intent E: MARKETPLACE & HARVEST LOTS
    market_keywords = [
        "बाजार", "बाजारभाव", "विक्री", "भाव", "खरेदी", "व्यापारी", "विकणे", "क्विंटल", "कांदा भाव", "द्राक्ष भाव", "माल",
        "market", "marketplace", "sell", "buyer", "price", "rate", "harvest", "mandi", "quintal", "listing"
    ]
    if any(k in q_lower for k in market_keywords):
        if detected_lang == "mr":
            response = (
                f"कृषीवाणी शेतकरी बाजारपेठेत सध्या {mkt_count} थेट शेतीमाल विक्री नोंदी उपलब्ध आहेत. "
                f"कांदा (₹१,९५०/क्विंटल), द्राक्ष (₹६,२००/क्विंटल) व सोयाबीनसाठी व्यापारी चौकशी करू शकतात. "
                f"आपला स्वतःचा शेतीमाल नोंदवण्यासाठी किंवा खरेदीदारांशी थेट संपर्क साधण्यासाठी खालील विभाग उघडा."
            )
            module = {
                "title": "विभाग ५: शेतकरी बाजारपेठ उघडा",
                "url": "/marketplace",
                "icon": "store"
            }
        else:
            response = (
                f"The KrishiVaani Marketplace currently has {mkt_count} active harvest lots listed by local farmers, "
                f"including Gavran Red Onion (₹1,950/qtl), Export Grapes (₹6,200/qtl), and JS 335 Soybean. "
                f"You can contact buyers directly without broker fees or post your own produce lot."
            )
            module = {
                "title": "Open Module 5: Farmer-to-Buyer Marketplace",
                "url": "/marketplace",
                "icon": "store"
            }
        return {"response_text": response, "recommended_module": module, "intent": "marketplace"}

    # Intent F: GOVERNMENT SCHEMES & SUBSIDIES
    scheme_keywords = [
        "योजना", "अनुदान", "सबसिडी", "महाडीबीटी", "पीएम किसान", "विमा", "सेंद्रिय", "जीवामृत", "दशपर्णी",
        "scheme", "subsidy", "pm-kisan", "mahadbt", "insurance", "organic", "jeevamrut", "subsidy portal"
    ]
    if any(k in q_lower for k in scheme_keywords):
        if detected_lang == "mr":
            response = (
                "महाराष्ट्रातील शेतकऱ्यांसाठी महाडीबीटी (MahaDBT) पोर्टलवर ठिबक सिंचनासाठी ५५% ते ७५% अनुदान उपलब्ध आहे. "
                "तसेच पीएम-किसान योजनेचा पुढील हप्ता व पीक विमा (PMFBY) अर्ज जवळच्या सीएससी केंद्रावर किंवा महाडीबीटीवर करता येतात. "
                "सेंद्रिय शेतीसाठी २०० लिटर पाण्यात १० किलो शेण, १० लिटर गोमूत्र व गूळ मिसळून जीवामृत तयार करा."
            )
            module = {
                "title": "विभाग २: सेंद्रिय व कृषी सल्ला पहा",
                "url": "/crop-helper",
                "icon": "sprout"
            }
        else:
            response = (
                "For Maharashtra farmers, MahaDBT offers 55% to 75% subsidies for micro-irrigation (drip and sprinkler) and farm ponds. "
                "PM-KISAN ₹2,000 seasonal installments and PMFBY crop insurance can be verified on the official MahaDBT and pmkisan.gov.in portals. "
                "For natural pest management, prepare Dashparni Ark or Jeevamrut using native cow dung and urine."
            )
            module = {
                "title": "Open Module 2: Crop Advisory & Organic Tips",
                "url": "/crop-helper",
                "icon": "sprout"
            }
        return {"response_text": response, "recommended_module": module, "intent": "schemes"}

    # Intent G: GREETING & GENERAL POLITE INQUIRY
    greeting_keywords = [
        "नमस्कार", "राम राम", "हाय", "हॅलो", "कसा", "मदत", "नाव",
        "namaskar", "hello", "hi", "hey", "help", "who are you", "what can you do"
    ]
    if any(k in q_lower for k in greeting_keywords):
        if detected_lang == "mr":
            response = (
                f"नमस्कार {farmer.get('name', {}).get('mr', 'शेतकरी दादा')}! मी आपला कृषीवाणी AI शेती सहाय्यक आहे. "
                "मी आपल्या चालू पिकांचे मार्गदर्शन, जनावरांचे लसीकरण, जवळची खत दुकाने आणि शेतखर्चाचा थेट हिशोब देऊ शकतो. "
                "आपण वरील कोणत्याही प्रश्नावर १-क्लिक करून विचारू शकता किंवा स्वतःचा प्रश्न टाईप करू शकता."
            )
            module = {
                "title": "विभाग १: मुख्य शेत डॅशबोर्ड",
                "url": "/dashboard",
                "icon": "layout-dashboard"
            }
        else:
            response = (
                f"Namaskar {farmer.get('name', {}).get('en', 'Farmer')}! I am your KrishiVaani Agro Copilot. "
                "I have real-time access to your active crops, livestock health records, local agro stores, and expense ledgers. "
                "Click any sample question above or type your agricultural inquiry."
            )
            module = {
                "title": "Module 1: Farm Dashboard",
                "url": "/dashboard",
                "icon": "layout-dashboard"
            }
        return {"response_text": response, "recommended_module": module, "intent": "greeting"}

    # Intent H: DEFAULT FALLBACK
    if detected_lang == "mr":
        response = (
            f"आपला प्रश्न समजला: '{cleaned_query}'. कृषीवाणी सह-मार्गदर्शक म्हणून मी ५ मुख्य विषयांवर मार्गदर्शन करतो: "
            "१) पीक सल्ला व फवारणी (विभाग २), २) जवळची खत व पशुवैद्यक दुकाने (विभाग ४), "
            "३) जनावरांचे लसीकरण (विभाग ६), ४) शेतखर्च विश्लेषण (विभाग ७), आणि ५) शेतीमाल विक्री बाजारपेठ (विभाग ५). "
            "कृपया यापैकी एका विषयाशी संबंधित प्रश्न विचारा."
        )
        module = {
            "title": "विभाग १: मुख्य डॅशबोर्ड",
            "url": "/dashboard",
            "icon": "layout-dashboard"
        }
    else:
        response = (
            f"Understood your inquiry: '{cleaned_query}'. As your KrishiVaani Copilot, I specialize in 5 practical areas: "
            "1) Stage-by-stage crop nutrition & pests, 2) Regional verified farm services, "
            "3) Cattle vaccination overdue tracking, 4) Farm financial ledger analytics, and 5) Direct harvest trade. "
            "Please ask a query related to one of these modules for targeted guidance."
        )
        module = {
            "title": "Module 1: Main Dashboard",
            "url": "/dashboard",
            "icon": "layout-dashboard"
        }
    return {"response_text": response, "recommended_module": module, "intent": "fallback"}


def _detect_recommended_module(q_lower: str, lang: str):
    """Helper to pick module button when Gemini responds."""
    if any(k in q_lower for k in ["खर्च", "पैसा", "expense", "spend", "cost"]):
        return {
            "title": "विभाग ७: शेतखर्च नोंदवही" if lang == "mr" else "Module 7: Farm Expense Tracker",
            "url": "/expenses",
            "icon": "receipt"
        }
    elif any(k in q_lower for k in ["पीक", "काम", "crop", "spray", "task"]):
        return {
            "title": "विभाग २: पीक सल्ला" if lang == "mr" else "Module 2: Crop & Farming Helper",
            "url": "/crop-helper",
            "icon": "sprout"
        }
    elif any(k in q_lower for k in ["दुकान", "डॉक्टर", "service", "vet", "shop"]):
        return {
            "title": "विभाग ४: कृषी सेवा केंद्र" if lang == "mr" else "Module 4: Nearby Agricultural Services",
            "url": "/nearby-services",
            "icon": "map-pin"
        }
    elif any(k in q_lower for k in ["जनावर", "लस", "livestock", "cow", "vaccine"]):
        return {
            "title": "विभाग ६: पशुधन व्यवस्थापन" if lang == "mr" else "Module 6: Livestock Records & Reminders",
            "url": "/livestock",
            "icon": "heart-pulse"
        }
    elif any(k in q_lower for k in ["बाजार", "विक्री", "market", "sell", "buyer"]):
        return {
            "title": "विभाग ५: शेतकरी बाजारपेठ" if lang == "mr" else "Module 5: Farmer Marketplace",
            "url": "/marketplace",
            "icon": "store"
        }
    return {
        "title": "मुख्य डॅशबोर्ड" if lang == "mr" else "Main Dashboard",
        "url": "/dashboard",
        "icon": "layout-dashboard"
    }
