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
│   ├── livestock.html          # Module 6: Cattle health registry, milk tracker & vaccine calendar
│   ├── expenses.html           # Module 7: Multi-dimensional expense ledger & Chart.js reports
│   └── placeholder.html        # Roadmap template for Modules 3 and 5
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

### H. Roadmap Placeholders (Modules 3 and 5)
- Standardized `templates/placeholder.html` rendering scope, badge, and planned capabilities for Module 3 (Multilingual AI Assistant) and Module 5 (Direct Marketplace).

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

## 6. How to Run KrishiVaani

```bash
# 1. Install Flask
pip install flask

# 2. Run the application
python app.py

# 3. Open your browser
http://127.0.0.1:5000
```
