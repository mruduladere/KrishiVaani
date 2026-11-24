# KrishiVaani (Voice of Agriculture) — Architecture Documentation

KrishiVaani is a unified, pure-Python digital platform designed for Indian farmers, tailored specifically to the agro-climatic context of Maharashtra (starting with the Niphad/Nashik belt).

This document serves as the project's living architectural manual, written in plain English for developers and Smart India Hackathon (SIH) evaluators.

---

## 1. System Overview & Technical Guidelines

| Dimension | Specification | Rationale |
| :--- | :--- | :--- |
| **Backend Framework** | **Flask 3.1 (Pure Python)** | Ultra-lightweight, beginner-friendly web server. Clean RESTful routing without Streamlit layout constraints or unexpected re-execution bugs. |
| **Frontend Framework** | **HTML5 + Tailwind CSS (via CDN)** | Clean, modern, Dribbble-grade SaaS aesthetics with zero compilation overhead. Full control over padding, shadows, responsiveness, and viewport height. |
| **Data Visualizations** | **Chart.js (via CDN)** | High-performance canvas-based charting for multi-dimensional expense analytics (category doughnut & monthly spend bar charts). |
| **Iconography** | **Lucide Icons (via CDN)** | Crisp, professional SVG line icons (`data-lucide="..."`) replacing inconsistent platform emojis. |
| **Typography** | **Inter & Noto Sans Devanagari** | Professional dual-language font stack rendering English and Marathi Devanagari with crisp legibility. |
| **Database** | **STRICTLY ZERO DATABASE** | Core project constraint. Runtime state is maintained entirely in Python memory (`FARMERS_DB`, `SERVICES_DB`, `TASKS_DB`, `LIVESTOCK_DB`, `EXPENSES_DB`) and `flask.session`. Zero SQL/NoSQL setup required. |
| **Persistence** | In-Memory Global Dictionaries + Session Cookie | Boots immediately with rich pre-loaded Maharashtra farming datasets. Edits, vaccinations, new animals, and expense logs persist during the server lifecycle. |
| **Bilingual Architecture** | First-Class Pure English & Pure Marathi (100% Separation) | Managed via `translations.py` dictionary lookups, `pick()` resolver, and `@app.template_filter('pick')`. Backend routes resolve dynamic bilingual dictionaries before rendering. Zero mixed parentheses like `"Seeds (बियाणे)"` or cross-language leakage. |

---

## 2. Directory Structure

```text
KrishiVaani/
│
├── app.py                      # Flask application controller & route handlers
├── plant_doctor.py             # Flagship AI Crop & Nutrient Doctor engine (Vision + Agronomy)
├── form_digitizer.py           # Flagship Smart Form Digitizer & auto-filler engine
├── smart_dispatcher.py         # Multi-module natural language & voice intent dispatcher
├── sarvam_client.py            # Official Sarvam AI SDK integration (105b, saaras:v3 STT, bulbul:v3 TTS)
├── ai_router.py                # Module 3: Multilingual intent router & live farm state copilot
├── sample_data.py              # Pre-loaded Maharashtra farming datasets & knowledge base
├── translations.py             # Complete bilingual dictionaries (English & Marathi) + t() helper
├── maharashtra_agronomy_kb.md  # Verified Maharashtra agronomy knowledge base (CROPSAP/MPKV/HORTSAP)
├── ARCHITECTURE.md             # Technical documentation & SIH defense guide
├── INSTRUCTIONS.md             # Hackathon project rules & constraints
├── .gitignore                  # Ignores __pycache__ and bytecode
│
├── templates/                  # Dribbble-grade HTML + Tailwind templates
│   ├── base.html               # Main AgFarm shell (fixed sidebar, topbar, user profile card)
│   ├── login.html              # Minimalist split-screen login card with botanical sprout animation
│   ├── dashboard.html          # Module 1: 4 KPI metric cards, crop stage cards & task reminders
│   ├── crop_helper.html        # Module 2: Crop tabs, 4-stage agronomy cards & task checklist
│   ├── disease_scanner.html    # Flagship AI Crop & Nutrient Doctor (live camera, triage, TTS audio)
│   ├── ai_assistant.html       # Module 3: Multilingual AI assistant chat & 1-click prompt router
│   ├── nearby_services.html    # Module 4: Filterable directory with click-to-call & WhatsApp
│   ├── marketplace.html        # Module 5: Direct farmer-to-buyer produce marketplace & lots
│   ├── livestock.html          # Module 6: Cattle health registry, milk tracker & vaccine calendar
│   ├── expenses.html           # Module 7: Multi-dimensional expense ledger & Chart.js reports
│   ├── smart_log.html          # Universal Smart Voice & Text Log with multi-module allocation
│   └── form_filler.html        # Flagship Smart Form Digitizer, auto-filler & A4 print generator
│
└── modules/                    # Legacy/modular reference components
    ├── auth.py
    ├── dashboard.py
    ├── crop_helper.py
    └── nearby_services.py
```

---

## 3. Core Modules & Step-by-Step Implementation

### A. Authentication & Session Gate (`templates/login.html` + `app.py`)
- Centered `max-w-4xl` split-screen card with rounded-3xl corners and soft drop shadow.
- Left panel displays botanical crop sprout SVG breathing gently via CSS keyframes (`gentleBreath`).
- Right panel provides 1-Click Demo Login (`9822012345`), standard 4-digit PIN form, and interactive registration toggle.

### B. Base Application Shell (`templates/base.html`)
- Fixed left sidebar (`w-64`) with active page highlight and bottom user profile snapshot.
- Topbar (`h-16`) with dynamic bilingual greeting, season indicator, and language mode switcher (`मराठी | English`).

### C. Module 1: Farmer Profile & Dashboard (`templates/dashboard.html`)
- 4 dynamic KPI cards: Land Size, Active Crops, Livestock Holding, and Monthly Spend.
- Active crop lifecycle summary for Grapes, Onion, and Soybean.
- Interactive farm task checklist with 1-click status toggling (`POST /toggle-task/<id>`).
- In-memory profile editor modal (`POST /update-profile`) and sample data reset (`GET /reset-defaults`).

### D. Module 2: Crop & Farming Helper (`templates/crop_helper.html`)
- Pill tabs for Grapes, Onion, Soybean, Cotton, Sugarcane, and Wheat.
- 4 sequential lifecycle stages with fertilizer dosage, irrigation schedule, pest remedies, and expert tips.
- Crop-specific interactive task checklist with add task form.

### E. Module 4: Nearby Agricultural Services (`templates/nearby_services.html`)
- Category filter pills, Taluka dropdown, and keyword search.
- Verified cards with Click-to-Call (`tel:`) and direct WhatsApp inquiries (`https://wa.me/`).
- In-memory provider registration modal (`POST /add-service`).

### F. Module 6: Livestock Records & Reminders (`templates/livestock.html` + `app.py`)
1. **Dynamic `datetime` Vaccination Engine:**
   - Evaluates each animal's vaccination schedule relative to `datetime.date.today()`:
     - `days_diff < 0`: **Overdue** (`bg-red-50 text-red-700 border-red-200`) with alert icon.
     - `0 <= days_diff <= 14`: **Upcoming within 14 days** (`bg-amber-50 text-amber-700 border-amber-200`) with clock icon.
     - `days_diff > 14`: **Up-to-Date** (`bg-emerald-50 text-emerald-700 border-emerald-200`) with checkmark icon.
   - Computes overall health condition: flags cattle as "Attention Needed" if any vaccine is overdue, or "Healthy & Productive" if all are current.
2. **"Mark Completed" Action (`POST /livestock/vaccinate`):**
   - Automatically sets `date_given = today.strftime("%Y-%m-%d")`.
   - Computes next `due_date`: 180 days (6 months) in the future for FMD, HS, and BQ, or 365 days (1 year) for annual vaccines like Brucellosis.
   - Updates status to "Up-to-Date" in memory without database latency.
3. **Add New Animal Form (`POST /livestock/add`):**
   - Collects Tag ID, Name, Species (Cow/Buffalo/Goat), Breed, Age, Daily Milk Yield, and Initial Vaccine schedule.
   - Automatically synchronizes with `farmer["livestock_summary"]` so total cattle count and daily milk yield in Dashboard KPIs immediately reflect the new animal.

### G. Module 7: Farm Expense Tracker & Analytics (`templates/expenses.html` + `app.py`)
1. **12 Problem Statement Categories:**
   - *Seeds, Fertilizers, Pesticides, Labour, Irrigation, Machinery, Transport, Fodder, Veterinary, Vaccination, Fuel/Electricity, and Repairs*.
2. **Multi-Dimensional Backend Aggregation:**
   - **Category-wise:** Aggregates total spend, transaction count, and percentage share per category; sorts descending to identify the highest spending category.
   - **Crop-wise:** Computes cost allocation for Grapes, Onion, Soybean, Livestock, and General Farm.
   - **Monthly Trend:** Groups expenditures chronologically (e.g. September, October, November 2026).
   - **Seasonal Breakdown:** Compares Kharif vs Rabi season investments.
3. **Chart.js Interactive Visualizations:**
   - **Category Doughnut Chart:** Color-coded breakdown of input expenses with percentage shares.
   - **Monthly Spend Bar Chart:** Visualizes cash flow peaks (e.g. forward pruning & basal fertilization surges).
4. **Structured Comparison Tables:**
   - Tab 1: Recent Transactions Ledger with inline delete action (`POST /expenses/delete/<id>`).
   - Tab 2: Category Summary Table with animated progress share bars.
   - Tab 3: Crop-wise Allocation Table.
   - Tab 4: Seasonal Comparison Table.
5. **Add Expense Form (`POST /expenses/add`):**
   - Logs Amount (₹), Date, Category, Season, Crop, Payment Mode (UPI, Cash, Bank, Credit), and Description directly into memory.

### H. Module 3: Multilingual Farmer AI Assistant (`templates/ai_assistant.html` + `ai_router.py` + `sarvam_client.py`)
1. **Official Sarvam AI Integration (`sarvam-105b-conversations`):**
   - Natural language conversations supporting Marathi, Hindi, and English (including colloquial rural terms and Marathinglish).
   - Injects farmer's live in-memory metrics (active crops, November expenses of ₹12,450, overdue FMD vaccines, local Niphad stores) directly into prompts.
   - Generates an actionable one-click navigation button (`Open Recommended Module →`) inside the assistant bubble.
2. **Text-to-Speech Voice Playback (`bulbul:v3`):**
   - Every AI reply bubble and Crop Helper stage card features an **"🔊 ऐका / Listen"** button.
   - Backend endpoint `/api/tts` calls Sarvam's `bulbul:v3` model (`mr-IN` / `en-IN`, speaker: `"ritu"`).
   - Seamlessly falls back to browser `window.speechSynthesis` if offline or if the API key is not configured.
3. **Dual Offline & Online Architecture:**
   - 100% reliable offline deterministic engine requiring zero external dependencies or internet connection.
   - Leverages Sarvam AI as primary LLM (and optional Google Gemini 1.5 Flash as secondary).
4. **1-Click Quick Prompts:**
   - Sample prompts in Marathi and English directly above the input box allow instant evaluation during hackathon demos without typing.

### I. Module 5: Simple Farmer-to-Buyer Marketplace (`templates/marketplace.html` + `app.py`)
1. **Peer-to-Peer Harvest Trade (0% Brokerage):**
   - Eliminates commission intermediaries by connecting farmers directly with wholesale buyers, food processors, and FPOs.
   - Explicit active-language policy badge: *"Direct Farmer-to-Buyer Enquiry • No Online Payments or Logistics"*.
2. **Filterable Commodity Directory:**
   - Categorized by Fruits, Vegetables, and Grains & Pulses with live keyword search.
   - Each card displays crop variety, available volume (Quintals), farmer-quoted farm gate price (₹/qtl), quality grade, and seller location.
3. **Direct Contact Generator:**
   - 1-Click Call (`tel:`) and pre-filled WhatsApp inquiry links (`https://wa.me/`) enable direct phone negotiation without app escrow.
4. **In-Memory Produce Listing (`POST /marketplace/add`):**
   - Instant produce lot submission persisting in `MARKETPLACE_DB` during runtime.

### J. Strict 100% Pure-Language Separation Architecture
1. **Zero Cross-Language Leakage & No Mixed Parentheses:**
   - When Marathi (`lang == 'mr'`) is active, zero raw English strings or parenthesized combinations (e.g., `"Seeds (बियाणे)"`) appear anywhere—including in dynamic tables, KPI cards, badges, and Chart.js tooltips/labels.
   - When English (`lang == 'en'`) is active, 100% pure English text appears with zero Devanagari characters.
2. **Backend Pre-Resolution Pattern:**
   - Backend Flask routes (`/crop-helper`, `/nearby-services`, `/livestock`, `/expenses`, `/marketplace`) deep-copy and resolve all bilingual dictionaries (`{"en": "...", "mr": "..."}`) into pure strings using `pick(field, lang=active_lang)` before passing datasets to Jinja2 templates.
   - Multi-dimensional aggregations (categories, crops, months, seasons) operate directly on resolved active-language strings.
3. **Bilingual Utility Suite (`translations.py`):**
   - `t(key, lang)`: UI string translator with language fallback.
   - `pick(val, lang)`: Universal language selector handling bilingual dicts, reverse lookup for submitted strings, and regex-based stripping of legacy parenthetical text.
   - `@app.template_filter('pick')`: Enables `{{ val | pick }}` in Jinja2 templates for raw farmer profile dictionaries.

---

## 4. Why Flask + Tailwind CSS Was Chosen Over Alternatives (SIH Defense)

1. **Freedom from Streamlit's Rigid Box-in-Box Layout:**
   - Streamlit automatically wraps forms and containers in nested gray borders, forcing vertical scrolling and preventing clean split-screen layouts.
   - Flask + Tailwind CSS allows precise CSS grid, single-viewport fit (`min-h-screen`), and full visual polish matching top SaaS products (Apple, Notion, AgFarm).
2. **Professional Line Icons Over Emojis:**
   - Streamlit relies heavily on Unicode emojis which render inconsistently across Windows, Android, and iOS.
   - Lucide Icons provide uniform, crisp vector line icons that convey modern engineering quality to hackathon judges.
3. **Strict Compliance with "NO DATABASE" Constraint:**
   - Flask works seamlessly with pure Python in-memory dictionaries (`FARMERS_DB`, `SERVICES_DB`, `TASKS_DB`, `LIVESTOCK_DB`, `EXPENSES_DB`).
   - Session cookies (`flask.session`) maintain authentication and language selection across page requests without writing to any SQL or disk database.
4. **Instant Startup & Zero Build Steps:**
   - Tailwind CSS, Lucide Icons, and Chart.js load directly via CDN. No `npm`, `webpack`, or Node.js toolchains are needed.
   - Evaluators only need Python to launch: `pip install flask && python app.py`.

---

## 5. Key Edge Cases Handled

1. **Vaccine Overdue Math:** Python's `datetime` module accurately calculates past-due negative day offsets and highlights overdue records in red, avoiding timezone or client-side calculation bugs.
2. **Zero-Division Protection:** In expense and milk statistics, percentage and average calculations check for `total_spend > 0` and `total_animals > 0` to prevent `ZeroDivisionError`.
3. **Phone Number Formatting:** `normalize_phone()` strips spaces, hyphens, and `+91` prefixes so farmers can type `9822012345` or `+91 98220 12345` interchangeably.
4. **Bilingual Fallback:** In `translations.py`, `t(key)` resolves against the active language (`mr` or `en`), falling back gracefully to English and then to the raw key if a translation is missing.
5. **In-Memory Mutations Without Persistence Loss:** Global dictionaries allow immediate reactivity during testing; a 1-click "Restore Defaults" button lets evaluators reset the demonstration state anytime.

---

## 6. Smart India Hackathon (SIH) Evaluator Defense Q&A

### Q1: Why text-based instead of voice for the Multilingual AI Assistant (Module 3)?
- **Answer:** Real-world rural connectivity in Maharashtra is often low-bandwidth (2G/3G in remote fields). Voice input introduces speech-to-text latency (3–6 seconds per query), high API failure rates with rural Marathi accents/dialects (Ahirani, Khandeshi), and heavy browser audio permissions. A text-based assistant with pre-populated 1-click quick prompt pills guarantees instantaneous (<50ms) intent routing and zero network failure during live evaluations.

### Q2: How does the AI Assistant avoid hallucinations when discussing farmer finances or cattle health?
- **Answer:** Rather than passing unbounded free-form prompts to a distant LLM, KrishiVaani’s `ai_router.py` engine directly queries the active in-memory state (`EXPENSES_DB`, `LIVESTOCK_DB`, `TASKS_DB`). It injects ground-truth figures—such as the exact November spend of ₹12,450 or the overdue FMD vaccine for "Gauri"—directly into the response template before providing a direct link to the corresponding module.

### Q3: Why is the Marketplace (Module 5) strictly peer-to-peer enquiry without online payments or delivery?
- **Answer:** Agricultural wholesale trading in India does not operate like consumer e-commerce. Produce lots (such as 55 quintals of onion or 30 quintals of grapes) require physical moisture and quality grading before payment settlement. Introducing digital payment gateways would impose 2% transaction charges on farmers and require escrow banking licenses. Direct Click-to-Call and WhatsApp integration mirrors how APMC traders and FPOs actually do business, keeping the prototype legal, realistic, and instantly functional.

---

## 8. Universal Smart Log ("बोलून किंवा लिहून नोंदवा") Architecture

The **Universal Smart Log** provides unified multi-module natural language data entry for farmers via voice or text.

### Data Flow Pipeline
1. **Farmer Input:** A single Marathi or English utterance (e.g. *"मी गौरी नावाची नवीन गीर गाय ४५,००० रुपयांना खरेदी केली, वय ३ वर्षे, लाळ्या खुरकूत लस दिली आहे"*).
2. **Audio Transcription:** Browser Web Speech API (`mr-IN` / `en-IN`) captures realtime speech, with a backend `/api/stt` endpoint powered by Sarvam AI `saaras:v3`.
3. **Structured Intent Extraction:** Sent to `smart_dispatcher.py`, which prompts `sarvam-105b` returning strict JSON schema actions.
4. **Deterministic Fallback:** If internet is down or API fails, an offline Marathi/English regex & keyword parser takes over with 100% deterministic accuracy.
5. **Multi-Module Dispatch:** Automatically mutates `LIVESTOCK_DB` (new cow + tag ID), `EXPENSES_DB` (₹45,000 veterinary/livestock entry), `MARKETPLACE_DB`, and `TASKS_DB` in memory.
6. **Instant UI Confirmation:** Visual confirmation cards display extracted detail pills and 1-click navigation buttons directly to the updated modules.

---

## 9. Flagship Smart Form Digitizer & Auto-Filler ("स्मार्ट अर्ज भरणे")

The **Smart Form Digitizer & Auto-Filler** eliminates the primary friction point for rural farmers applying for central and state agricultural schemes (PM-KISAN, Pradhan Mantri Fasal Bima Yojana, Magel Tyala Shettale, and State Farmer Registration Portals).

### Architecture & Data Pipeline
1. **Document Intake (Upload or 1-Click Sample Form):**
   - **Custom Uploads (`is_sample=False`):** Farmers or CSC operators upload a phone photo or scan of ANY paper application sheet or digital registration portal form (PNG, JPG).
   - **1-Click Sample Form (`is_sample=True`):** Provides instant evaluation capability using an authentic Maharashtra PM-KISAN & Crop Insurance form (with embedded vector SVG fallback if offline).
2. **Dynamic Vision OCR & Field Extraction Pipeline (`form_digitizer.py`):**
   - **Two-Stage Real Image Reader:**
     - **Stage A (Visual OCR & Bounding Box Extraction):** Integrates Sarvam Document Intelligence (`doc_ai.parse`) with an offline pure-Python local OCR fallback powered by `rapidocr-onnxruntime` (`onnxruntime` + `pyclipper` + `shapely`). RapidOCR extracts exact text lines, line order, and normalized bounding box coordinates (`[x_min, y_min, x_max, y_max]`) directly from the image with zero external binary dependencies.
     - **Stage B (Structured Field Synthesis via `sarvam-105b`):** Feeds the exact OCR text lines and spatial coordinates to **`sarvam-105b`** (with a fallback to a spatial deterministic line parser) using a strict prompt to extract ONLY fillable elements (`field_id`, bilingual `label_en`/`label_mr`, `field_type`, `x_pct`, `y_pct`, `yes_coords`, `no_coords`) genuinely present in the document. Real uploads never fall back to hardcoded dummy questions.
   - **Sample Form:** Strictly adheres to the official PM-KISAN & Pik Vima schema with verified baseline coordinates.
3. **Smart Profile Auto-Fill Matching (`_match_and_autofill_profile`):**
   - Performs flexible keyword matching across `field_id`, English labels, and Marathi labels against `session['farmer_profile']` (Farmer Name, Phone, Email, Village, Taluka, District, State, Farm Size, Crops Cultivated, Livestock Holding, Irrigation Type).
   - **Strict Pre-Fill Boundary:** Pre-fills **ONLY** fields that genuinely appear on the uploaded form, tagging them with an emerald `"Auto-filled from Profile"` (`प्रोफाइलमधून भरले`) badge, while leaving form-specific blanks (DOB, Gender, Annual Yield, Bank Account) for farmer review.
4. **Lightweight In-Memory State Architecture (No Cookie Overflow):**
   - To strictly obey Flask's 4KB cookie threshold without a persistent database, all parsed forms, extracted fields, and coordinate maps are stored in a server-side Python dictionary: `FORM_SESSIONS = { user_phone: parsed_form_dict }`.
   - The user's cookie session stores only lightweight boolean flags (`has_form`, `form_is_generated`), preventing silent browser cookie drops.
5. **Interactive Digital Form Editor & Pixel-Accurate Coordinate Overlay:**
   - **Interactive Elements:** Renders clean radio buttons for `yes_no` fields (`Yes`/`No` or `होय`/`नाही`) and toggles for `checkbox` fields in pure English or pure Marathi.
   - **Pixel-Accurate Text Alignment:** Anchors digitized text with `transform: translateY(-85%)` so that values sit **directly on top of printed underlines (`____`)** and inside table cells rather than floating above them.
   - **Precise Checkmark Rendering:** Places bold checkmarks (`✓`) centered at normalized `yes_coords`, `no_coords`, or checkbox square coordinates (`translate(-50%, -50%)`) when selected.
6. **Robust Workflow State Machine & Navigation (`/form-filler/reset` & `/form-filler/edit`):**
   - **Upload Another Form / Reset:** Dedicated `/form-filler/reset` route clears `FORM_SESSIONS[user_id]` and resets session state back to Step 1 (Upload screen).
   - **Edit Values Navigation:** Dedicated `/form-filler/edit` route toggles completed state back to Step 2 while preserving all user-modified text, radio choices, and checkbox states in server memory.
7. **Dynamic Print & Standalone Download (`/form-filler/download`):**
   - Generates a standalone, print-optimized (`@media print`) HTML document dynamically constructed from all extracted fields in the active language, complete with an official bordered application table, applicant signature block, and auto-print triggers.

---

## 10. Flagship AI Crop & Nutrient Doctor ("पीक रोग व पोषण तपासणी")

The **AI Crop & Nutrient Doctor** provides instant, vision-guided disease and nutrient deficiency diagnosis for Maharashtra farmers. Grounded strictly in `maharashtra_agronomy_kb.md`, it prevents catastrophic agricultural misdiagnoses (such as spraying toxic systemic insecticides when a leaf is simply starving for Potassium or Zinc).

### Architecture & Two-Stage Vision Pipeline
1. **Multimodal Leaf Capture & Triage Intake (`templates/disease_scanner.html`):**
   - **Live HTML5 Camera Viewfinder:** Uses `navigator.mediaDevices.getUserMedia` with rear-camera preference (`facingMode: "environment"`), reticle overlay, and instant frame grab to canvas.
   - **Field Photo Upload:** Supports high-resolution JPG/PNG leaf uploads with drag-and-drop.
   - **1-Click Demo Evaluation Samples:** Pre-loaded with 4 verified Maharashtra field cases (*Vidarbha Bt Cotton Potassium Scorch, Western Maharashtra Grapes Downy Mildew, Marathwada Soybean Zinc Chlorosis, Nashik Onion Purple Blotch*) with embedded SVG vector leaf illustrations.
   - **Field Context & Triage Chips:** Accepts Crop selection, Affected Leaf Position (*Older/Lower* vs. *Younger/Top* vs. *Whole Canopy*), Symptom Pattern (*Burnt Margins*, *Interveinal Chlorosis*, *Spots/Powder*, *Curling*), and optional Soil Health Card / pH notes.
2. **Two-Stage Sarvam AI Vision & Agronomy Pipeline (`plant_doctor.py`):**
   - **Stage A (Vision Model Analysis & Validation):** Validates uploaded base64 image data using Pillow (verifying format, dimensions >= 20px, and image integrity). Submits the image to Sarvam AI or chat completion via `sarvam-105b` guided by the system prompt loaded with `maharashtra_agronomy_kb.md`.
   - **Stage B (Grounded Maharashtra Agronomy Synthesis):** Synthesizes visual observations against state research authority rules:
     - **Strict Crop Isolation (Zero Cross-Crop Leakage):** Enforces strict crop boundaries so that Tomato leaves never receive Cotton advice (or vice-versa). Unspecified crops trigger a clear prompt to specify the crop before chemical advice is provided.
     - **Accurate Disease & Pathogen Taxonomy:** Prevents erroneous conflation of distinct diseases. Correctly distinguishes Bacterial Spot (*Xanthomonas vesicatoria / X. perforans* - foliar/fruit surface spot) from Bacterial Canker (*Clavibacter michiganensis* - systemic vascular wilt with bird's-eye fruit spots) and Early Blight (*Alternaria solani* - concentric target rings).
     - **Honest Diagnostic Certainty (Anti-Fabrication):** Eliminates uncalibrated, fabricated percentage scores (e.g. fake 85% or 94%). Uses honest qualitative certainty tiers (Low, Moderate, High) explicitly labeled as *"Preliminary Visual Estimate (Field Confirmation Required)"*.
     - **Plausible Alternatives & Field Confirmatory Checklist:** When photographic evidence is non-definitive, lists 2-3 plausible alternative conditions and actionable field checks (e.g., inspecting spot undersides for water-soaking, slicing stems for vascular discoloration, inspecting fruit).
     - **Safe Chemical Prescription Guardrail:** Refuses to recommend synthetic chemical pesticides from an unconfirmed photograph alone. Mandates physical field inspection and local Taluka Krishi Adhikari / KVK consultation before purchasing chemicals.
     - **Verified State Dosages:** Integrates verified packages of practices from MPKV Rahuri, Dr. PDKV Akola, VNMKV Parbhani, Dr. BSKKV Dapoli, and ICAR-NRCG Pune.
     - **ETL & Predator Safety:** Checks Economic Threshold Levels and warns against spraying when beneficial insects (ladybird beetles, chrysoperla) are present.
     - **Soil Health Card Priority:** Overrides generic baseline fertilizer charts whenever the farmer supplies specific soil test parameters (pH, available N/P/K, Zinc, Organic Carbon).
     - **Universal Anti-Hallucination Disclaimer:** Strictly outputs *"Confirm exact dosage locally with Taluka Krishi Adhikari / KVK"* instead of guessing unverified chemical doses.
3. **Voice Accessibility via Sarvam Bulbul TTS (`/api/tts`):**
   - Renders a 1-click **🔊 ऐका / Listen Advisory** button powered by Sarvam AI `bulbul:v3` (`ritu` speaker), synthesizing the complete diagnosis and dosage directly into Marathi or Indian English audio with automatic browser audio fallback.
4. **Agro Services Handoff:**
   - Directly links to Module 4 (`/nearby-services`) allowing farmers to locate nearby Krishi Seva Kendras, testing labs, and fertilizer centers to purchase the prescribed remedies.

---

## 11. Module 11: Real-Time Weather & Agronomic Advisory (`/weather-advisory`)

### Architectural Purpose
Provides a real-time, location-specific agro-meteorological advisory engine powered by the official Open-Meteo Weather API (`https://api.open-meteo.com/v1/forecast`, `Asia/Kolkata` timezone). Seamlessly translates live atmospheric observations into actionable farming advisories based on the logged-in farmer's existing profile without prompting for re-entry.

### Key Capabilities & Engineering Standards:
1. **Zero-Database Location Engine & 36-District Database (`build_locations.py` / `static/maharashtra_locations.json`):**
   - Comprehensive coverage of all 36 Maharashtra districts, major agricultural talukas, and prominent farming villages/APMCs (including Pimpalgaon Baswant, Lasalgaon, Baramati KVK, Rahuri MPKV, Narayangaon, etc.).
   - Provides 3 location selection pathways:
     - Cascading 3-tier dropdown: State → District → Taluka → Village.
     - Live debounced autocomplete search across all locations.
     - Browser GPS Geolocation (`navigator.geolocation`) with one-click permission.
   - Instantly recalculates latitude and longitude, updates Open-Meteo coordinates, and reruns the advisory engine without refreshing unrelated state.
2. **Automated Farmer Profile Integration:**
   - Automatically reads crop (`crops_grown`), variety, current growth stage, soil type, irrigation method, and Soil Health Card notes directly from `flask.session['farmer_profile']`.
   - Never prompts the farmer to re-select crop or growth stage.
3. **Open-Meteo Weather Pipeline & 15-Minute In-Memory Cache:**
   - Queries live Open-Meteo endpoints for temperature, relative humidity, precipitation, wind speed & gusts, cloud cover, soil moisture (3–9 cm depth), and FAO ET0 evapotranspiration.
   - Features in-memory caching (`WEATHER_CACHE`, TTL = 15 minutes) to minimize external network requests and prevent rate-limiting.
4. **Colour-Coded Warning & Advisory Engines (`weather_advisory.py`):**
   - **Warning Alerts (Green/Yellow/Orange/Red):** Real-time hazard triggers for rain within 6 hours, heavy rain within 24 hours, thunderstorm/lightning risks, squall winds, heat stress, frost, and high-humidity foliar disease danger.
   - **Irrigation Advisor:** Compares forecasted rainfall, current soil moisture, and evapotranspiration against crop growth stage to advise whether to irrigate, hold, or open drainage trenches.
   - **Spraying Safety Advisor:** Evaluates rain probability within 6 hours, wind speeds (>16 km/h), temperatures (>36°C), and thunderstorms to identify safe spraying windows or mandate postponement.
   - **Sowing & Transplanting Outlook:** Assesses soil temperature and moisture conditions for germination and seedling safety.
   - **Profile Crop Advisory & Action Checklist:** Tailors advice directly to the active crop (e.g. Grapes downy mildew / berry splitting in wet conditions, Soybean pod filling in dry conditions) accompanied by a 4-point "आज काय करावे?" checklist.
5. **Bilingual Presentation (100% Pure Marathi & Pure English):**
   - Fully symmetric translations in `translations.py` ensuring zero language mixing or awkward bracket formatting.

---

## 12. How to Run KrishiVaani

```bash
# 1. Install Flask and requirements
pip install flask pillow sarvamai python-dotenv rapidocr-onnxruntime requests

# 2. Run the application
python app.py

# 3. Open your browser
http://127.0.0.1:5000
```
