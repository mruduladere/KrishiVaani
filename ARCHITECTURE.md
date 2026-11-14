# KrishiVaani (Voice of Agriculture) — Architecture Documentation

KrishiVaani is a unified, pure-Python digital platform designed for Indian farmers, tailored specifically to the agro-climatic context of Maharashtra (starting with the Niphad/Nashik belt).

This document serves as the project's living architectural manual, written in plain English for developers and Smart India Hackathon (SIH) evaluators.

---

## 1. System Overview & Technical Guidelines

| Dimension | Specification | Rationale |
| :--- | :--- | :--- |
| **Backend Framework** | **Flask 3.1 (Pure Python)** | Ultra-lightweight, beginner-friendly web server. Clean RESTful routing without Streamlit layout constraints or unexpected re-execution bugs. |
| **Frontend Framework** | **HTML5 + Tailwind CSS (via CDN)** | Clean, modern, Dribbble-grade SaaS aesthetics with zero compilation overhead. Full control over padding, shadows, responsiveness, and viewport height. |
| **Iconography** | **Lucide Icons (via CDN)** | Crisp, professional SVG line icons (`data-lucide="..."`) replacing inconsistent platform emojis. |
| **Typography** | **Inter & Noto Sans Devanagari** | Professional dual-language font stack rendering English and Marathi Devanagari with crisp legibility. |
| **Database** | **STRICTLY ZERO DATABASE** | Core project constraint. Runtime state is maintained entirely in Python memory (`FARMERS_DB`, `SERVICES_DB`, `TASKS_DB`, etc.) and `flask.session`. Zero SQL/NoSQL setup required. |
| **Persistence** | In-Memory Global Dictionaries + Session Cookie | Boots immediately with rich pre-loaded Maharashtra farming datasets. Edits, new tasks, and new services persist during the server lifecycle. |
| **Bilingual Architecture** | First-Class English & Marathi | Managed via `translations.py` dictionary lookups. Jinja2 context processor injects `t(key)` and active `lang` automatically into every template. |

---

## 2. Directory Structure

```text
KrishiVaani/
│
├── app.py                      # Flask application controller & route handlers
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
│   ├── nearby_services.html    # Module 4: Filterable directory with click-to-call & WhatsApp
│   └── placeholder.html        # Roadmap template for Modules 3, 5, 6, 7
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
1. **Design & Visual Layout:**
   - Centered `max-w-4xl` split-screen card with rounded-3xl corners and soft drop shadow.
   - **Left Panel:** Soft sage gradient (`#F2F7F4` to `#E4EFE8`) with a delicate botanical crop sprout SVG breathing gently via CSS keyframes (`gentleBreath`).
   - **Right Panel:** Spacious login panel with language switcher pill, 1-Click Demo Login button (Ramesh Patil), 4-digit PIN form, and interactive registration toggle.
2. **Step-by-Step Data Flow:**
   - When a user visits `/`, `app.py` checks `session.get('is_authenticated')`. If `False`, it renders `login.html`.
   - **1-Click Demo Login:** Clicking `/demo-login` bypasses credentials, signs into Ramesh Patil's pre-loaded account (`9822012345`), sets `session['is_authenticated'] = True`, and redirects to `/dashboard`.
   - **PIN Login:** Entering phone + PIN submits `POST /login`. It cleans the phone number, checks `FARMERS_DB`, validates the PIN, sets session credentials, and redirects.
   - **Registration:** Entering farmer details submits `POST /register`. It creates a new farmer record in memory inside `FARMERS_DB[phone]`, logs the farmer in, and redirects to their new dashboard.
   - **Logout:** Clicking `/logout` clears session data and returns to the login screen.

### B. Base Application Shell (`templates/base.html`)
1. **Fixed Left Sidebar (`w-64`):**
   - Branded header with sprout icon.
   - 7 navigation links with crisp Lucide line icons (Dashboard, Crop Helper, AI Assistant, Nearby Services, Marketplace, Livestock, Expense Tracker). Active route highlighted with emerald tint.
   - Bottom farmer snapshot card with name, village, land size, and logout button.
2. **Sticky Topbar (`h-16`):**
   - Dynamic greeting in active language ("Welcome back, Ramesh / स्वागत आहे, रमेश").
   - Season indicator (`Rabi Season 2026-27`).
   - Dual-language toggle pill (`मराठी | English`) linking to `/set-lang/mr` and `/set-lang/en`.
   - `+ Quick Action` button.

### C. Module 1: Farmer Profile & Dashboard (`templates/dashboard.html`)
1. **4 KPI Summary Cards:**
   - **Land Holding:** 4.5 Acres (Medium Black Soil, Drip Irrigated).
   - **Active Crops:** 3 Crops (Grapes, Onion, Soybean).
   - **Livestock Holding:** 7 Animals (2 Cows, 1 Buffalo, 4 Goats • 22 L daily milk).
   - **Monthly Spend:** ₹18,500 (November 2026 input costs).
2. **Active Crop Stage Cards:**
   - Shows active lifecycle stage for each of the farmer's crops (e.g. Grapes - Stage 3 Flowering & Berry Setting; Onion - Stage 2 Vegetative Canopy).
3. **Task Reminders & Checklist:**
   - Live checklist showing pending agronomy tasks with priority pills (`High`, `Medium`, `Low`).
   - Farmers toggle status with 1 click (`POST /toggle-task/<id>`).
4. **In-Memory Profile Editor:**
   - Clean modal form submitting `POST /update-profile` to modify land size, crops, and soil type in memory.
   - "Restore Defaults" button (`GET /reset-defaults`) restores initial sample records.

### D. Module 2: Crop & Farming Helper (`templates/crop_helper.html`)
1. **Crop Selector Tabs:**
   - Pill tabs for Grapes, Onion, Soybean, Cotton, Sugarcane, Wheat, with a `★ Farm` indicator for crops on the farmer's own land.
2. **4-Stage Agronomy Cards:**
   - 1. Sowing / Forward Pruning
   - 2. Vegetative Canopy & Shoot Growth
   - 3. Flowering & Berry Setting
   - 4. Harvesting, Threshing & Post-Harvest Storage
   - Each stage provides 4 detailed breakdown cards: Fertilizer & Nutrition, Irrigation Schedules, Pest & Disease Protection, and Agronomy Pro-Tips.
3. **Task Management:**
   - Filterable checklist for the active crop.
   - "Add Farm Task" form allows adding custom tasks directly to in-memory state.

### E. Module 4: Nearby Agricultural Services (`templates/nearby_services.html`)
1. **Directory & Multi-Tier Filter:**
   - Category filter pills (Veterinary Doctors, Seed & Fertilizer Shops, Machinery Rental, Fodder, Service Centres).
   - Taluka dropdown (Niphad, Nashik, Dindori, Chandwad, Sinnar, Yeola).
   - Keyword search input.
2. **Provider Cards:**
   - Displays provider name, verified badge, rating (⭐ 4.9), category tag, location, operating hours, and speciality list.
   - **Direct Call:** `tel:` button for immediate phone contact.
   - **WhatsApp Inquiry:** `https://wa.me/...` with pre-filled greeting in the farmer's active language.
3. **Add New Service Provider:**
   - Modal form enabling farmers to register trusted local agri-dealers directly in memory (`POST /add-service`).

### F. Roadmap Placeholders (Modules 3, 5, 6, 7)
- Standardized `templates/placeholder.html` rendering scope, badge, and planned capabilities for upcoming steps.

---

## 4. Why Flask + Tailwind CSS Was Chosen Over Alternatives (SIH Defense)

1. **Freedom from Streamlit's Rigid Box-in-Box Layout:**
   - Streamlit automatically wraps forms and containers in nested gray borders, forcing vertical scrolling and preventing clean split-screen layouts.
   - Flask + Tailwind CSS allows precise CSS grid, single-viewport fit (`min-h-screen`), and full visual polish matching top SaaS products (Apple, Notion, AgFarm).
2. **Professional Line Icons Over Emojis:**
   - Streamlit relies heavily on Unicode emojis which render inconsistently across Windows, Android, and iOS.
   - Lucide Icons provide uniform, crisp vector line icons that convey modern engineering quality to hackathon judges.
3. **Strict Compliance with "NO DATABASE" Constraint:**
   - Flask works seamlessly with pure Python in-memory dictionaries (`FARMERS_DB`, `SERVICES_DB`, `TASKS_DB`).
   - Session cookies (`flask.session`) maintain authentication and language selection across page requests without writing to any SQL or disk database.
4. **Instant Startup & Zero Build Steps:**
   - Tailwind CSS and Lucide Icons load directly via CDN. No `npm`, `webpack`, or Node.js toolchains are needed.
   - Evaluators only need Python to launch: `pip install flask && python app.py`.

---

## 5. Key Edge Cases Handled

1. **Phone Number Formatting:** `normalize_phone()` strips spaces, hyphens, and `+91` prefixes so farmers can type `9822012345` or `+91 98220 12345` interchangeably.
2. **Bilingual Fallback:** In `translations.py`, `t(key)` resolves against the active language (`mr` or `en`), falling back gracefully to English and then to the raw key if a translation is missing.
3. **Crop String Normalization:** `detect_crop_key()` automatically detects the base crop key even if the farmer's profile says `"Grapes - Thomson Seedless (द्राक्ष)"`.
4. **Session Authentication Protection:** All authenticated routes (`/dashboard`, `/crop-helper`, `/nearby-services`, etc.) check `session.get('is_authenticated')` and redirect unauthenticated requests to `/`.
5. **In-Memory Mutations Without Persistence Loss:** Global dictionaries allow immediate reactivity during testing; a 1-click "Restore Defaults" button lets evaluators reset the demonstration state anytime.

---

## 6. How to Run KrishiVaani

```bash
# 1. Install Flask
pip install flask

# 2. Run the application
python app.py

# 3. Open your browser
http://127.0.0.1:5000
```
