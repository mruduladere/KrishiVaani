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
├── form_digitizer.py           # Flagship Smart Form Digitizer & auto-filler engine
├── smart_dispatcher.py         # Multi-module natural language & voice intent dispatcher
├── sarvam_client.py            # Official Sarvam AI SDK integration (105b, saaras:v3 STT, bulbul:v3 TTS)
├── ai_router.py                # Module 3: Multilingual intent router & live farm state copilot
├── sample_data.py              # Pre-loaded Maharashtra farming datasets & knowledge base
├── translations.py             # Complete bilingual dictionaries (English & Marathi) + t() helper
├── ARCHITECTURE.md             # Technical documentation & SIH defense guide
├── INSTRUCTIONS.md             # Hackathon project rules & constraints
├── .gitignore                  # Ignores __pycache__ and bytecode
│
├── templates/                  # Dribbble-grade HTML + Tailwind templates
│   ├── base.html               # Main AgFarm shell (fixed sidebar, topbar, user profile card)
│   ├── login.html              # Minimalist split-screen login card with botanical sprout animation
│   ├── dashboard.html          # Module 1: 4 KPI metric cards, crop stage cards & task reminders
│   ├── crop_helper.html        # Module 2: Crop tabs, 4-stage agronomy cards & task checklist
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

The **Smart Form Digitizer & Auto-Filler** eliminates the primary friction point for rural farmers applying for central and state agricultural schemes (PM-KISAN, Pradhan Mantri Fasal Bima Yojana, Magel Tyala Shettale).

### Architecture & Data Pipeline
1. **Document Intake (Upload or 1-Click Sample Form):**
   - Farmers or CSC operators upload a phone photo/scan of any paper application sheet (PNG, JPG) or trigger the **1-Click Sample Form** button pre-loaded with an authentic Maharashtra PM-KISAN / Crop Insurance application.
2. **Sarvam AI Vision OCR & Document Intelligence:**
   - Evaluates the document structure via Sarvam AI's Document Intelligence / Vision APIs and `sarvam-105b` to parse scheme headers, field boxes, and normalized positional coordinates (`x_pct`, `y_pct`).
   - If offline or operating without external internet, it automatically falls back to our internal Maharashtra scheme schema.
3. **Smart Profile Auto-Fill Mapping:**
   - Pre-populates all known farmer data directly from `session['farmer_profile']` (Applicant Name, Phone Number, Village, Taluka, District, Land Holding, and Crops Cultivated), tagging them with an emerald `"Auto-filled from Profile"` badge so the farmer only types missing transaction fields (e.g., Bank Account, IFSC, Survey/Gat number).
4. **Interactive Digital Form Editor:**
   - Provides a side-by-side verification interface where the uploaded paper image is displayed alongside accessible digital web inputs in the active language (`English` or `मराठी`).
5. **Dual-Mode Completed Document Generator:**
   - **Annotated Form Overlay View:** Uses a responsive container (`position: relative`) placing crisp digital values at exact coordinates (`x_pct`, `y_pct`) on top of the original form image, complete with a digital signature stamp.
   - **Clean Official A4 Print-Ready Application Sheet:** Formats a government-standard bordered application table containing applicant details, land data, DBT bank accounts, and signature blocks.
6. **Print & Standalone Download:**
   - `@media print` CSS cleanly strips navigation bars and sidebars, outputting an official single-page A4 application.
   - The **Download Filled Form** endpoint delivers a standalone printable HTML/PDF file with auto-print triggers.

---

## 10. How to Run KrishiVaani

```bash
# 1. Install Flask and requirements
pip install flask pillow sarvamai python-dotenv

# 2. Run the application
python app.py

# 3. Open your browser
http://127.0.0.1:5000
```
