"""
app.py - Main Application Controller for KrishiVaani (Voice of Agriculture)
Unified Python digital platform for Indian farmers built with Streamlit.
Strictly NO external database (uses Streamlit in-memory session state).
Bilingual English & Marathi support via translations.py.
"""

import streamlit as st
import textwrap
from sample_data import init_session_data
from translations import t, render_language_switcher
from modules.auth import render_auth
from modules.dashboard import render_dashboard
from modules.crop_helper import render_crop_helper
from modules.nearby_services import render_nearby_services

# Configure page layout and visual identity
st.set_page_config(
    page_title="KrishiVaani - Voice of Agriculture",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize all in-memory sample data
init_session_data(st)

# ----------------- GLOBAL THEME & TYPOGRAPHY POLISH -----------------
st.markdown(
    textwrap.dedent("""<style>
/* Google Fonts: Inter & Noto Sans Devanagari */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+Devanagari:wght@400;500;600;700;800&display=swap');

/* Global typography */
html, body, [class*="css"], .stApp, .stMarkdown, .stButton, input, label, select, textarea {
    font-family: 'Inter', 'Noto Sans Devanagari', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
}

/* Hide Streamlit default chrome to present a clean standalone web application */
#MainMenu {visibility: hidden; display: none;}
header {visibility: hidden; display: none;}
footer {visibility: hidden; display: none;}
div[data-testid="stToolbar"] {visibility: hidden; display: none;}
div[data-testid="stDecoration"] {visibility: hidden; display: none;}
div[data-testid="stStatusWidget"] {visibility: hidden; display: none;}

/* Background tone: warm off-white / slate canvas */
.stApp {
    background-color: #F8FAFC;
}

/* Clean Card Container Polish */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 16px !important;
    background-color: #FFFFFF;
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05);
    border: 1px solid #E2E8F0;
}

/* Polished Input Fields */
div[data-testid="stTextInput"] input, 
div[data-testid="stNumberInput"] input, 
div[data-testid="stSelectbox"] select,
div[data-testid="stTextArea"] textarea {
    border-radius: 10px !important;
    border: 1.5px solid #CBD5E1 !important;
    padding: 10px 14px !important;
    font-size: 14.5px !important;
    background-color: #FFFFFF !important;
    transition: all 0.2s ease-in-out !important;
}

div[data-testid="stTextInput"] input:focus, 
div[data-testid="stNumberInput"] input:focus {
    border-color: #15803D !important;
    box-shadow: 0 0 0 3px rgba(21, 128, 61, 0.15) !important;
}

/* Metric Card Polish */
div[data-testid="stMetricValue"] {
    font-size: 26px !important;
    font-weight: 800 !important;
    color: #14532D !important;
    letter-spacing: -0.5px;
}

/* Buttons: Emerald Primary & Pill Styling */
.stButton>button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 9px 18px !important;
    transition: all 0.2s ease-in-out !important;
}

/* Form Submit CTA Highlight */
div[data-testid="stFormSubmitButton"]>button {
    background: #15803D !important;
    color: #FFFFFF !important;
    border: none !important;
    box-shadow: 0 4px 12px rgba(21, 128, 61, 0.25);
}

div[data-testid="stFormSubmitButton"]>button:hover {
    background: #166534 !important;
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(21, 128, 61, 0.35);
}

/* Secondary Outlined Button */
button[kind="secondary"] {
    background-color: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    color: #334155 !important;
}

button[kind="secondary"]:hover {
    border-color: #15803D !important;
    color: #15803D !important;
    background-color: #F0FDF4 !important;
}

/* Sidebar Clean Styling */
section[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    border-right: 1px solid #E2E8F0;
}
</style>"""),
    unsafe_allow_html=True
)

# ----------------- AUTHENTICATION GATE -----------------
# If user is not authenticated, render split-screen SaaS login portal
if not st.session_state.get("is_authenticated", False):
    render_auth()
    st.stop()


# ----------------- AUTHENTICATED FARMER SIDEBAR -----------------
with st.sidebar:
    # 1. Top Language Mode Switcher (English | मराठी)
    st.markdown("##### 🌐 भाषा / Language Mode")
    render_language_switcher(key="sidebar")
    st.markdown("---")

    # 2. App Branding
    st.markdown(f"## 🌾 {t('app_title')}")
    st.caption(f"{t('app_subtitle')} | {t('sih_badge')}")

    # 3. Farmer Profile Snapshot
    profile = st.session_state.get("farmer_profile", {})
    with st.container(border=True):
        st.markdown(f"**{t('farmer_badge')}:** {profile.get('name', 'N/A')}")
        st.caption(f"📍 {profile.get('village', '')}, {profile.get('district', '')}")
        st.caption(f"🚜 {t('land_badge')}: {profile.get('land_size_acres', 0)} Acres")

    st.markdown("---")
    st.markdown(f"### 🧭 {t('nav_header')}")

    nav_options = {
        "dashboard": t("nav_dashboard"),
        "crop_helper": t("nav_crop_helper"),
        "ai_assistant": t("nav_ai_assistant"),
        "nearby_services": t("nav_nearby_services"),
        "marketplace": t("nav_marketplace"),
        "livestock": t("nav_livestock"),
        "expense_tracker": t("nav_expense_tracker")
    }

    # Determine current selection index
    keys_list = list(nav_options.keys())
    current_key = st.session_state.get("active_nav", "dashboard")
    current_index = keys_list.index(current_key) if current_key in keys_list else 0

    selected_label = st.radio(
        label="Select Module:",
        options=list(nav_options.values()),
        index=current_index,
        label_visibility="collapsed"
    )

    # Reverse lookup key from label
    for k, v in nav_options.items():
        if v == selected_label:
            st.session_state.active_nav = k
            break

    st.markdown("---")

    # 4. Logout Button
    if st.button(f"🚪 {t('logout_button')}", use_container_width=True):
        st.session_state.is_authenticated = False
        st.session_state.auth_mode = "login"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="font-size: 11px; color: #6b7280; text-align: center;">
            {t('footer_text')}
        </div>
        """,
        unsafe_allow_html=True
    )


# ----------------- MAIN VIEW ROUTER -----------------
active_module = st.session_state.get("active_nav", "dashboard")

if active_module == "dashboard":
    render_dashboard()

elif active_module == "crop_helper":
    render_crop_helper()

elif active_module == "nearby_services":
    render_nearby_services()

else:
    # Clean, informative placeholder for Modules 3, 5, 6, 7
    placeholders = {
        "ai_assistant": {
            "title": "Module 3: Multilingual Farmer AI Assistant (मराठी व इंग्रजी AI सहाय्यक)",
            "step": "Step 3",
            "scope": "Text-based Marathi and English intent router providing instant answers to farming queries, crop diseases, government subsidies, and soil management without speech-to-text latency.",
            "planned": [
                "Fast intent classification for Marathi and English text queries",
                "Instant guidance on PM-KISAN, MahaDBT schemes, and crop insurance",
                "Organic farming tips and natural pesticide formulations (Jeevamrut, Dashparni)",
                "Interactive question-answering for common agronomy doubts"
            ]
        },
        "marketplace": {
            "title": "Module 5: Simple Farmer-to-Buyer Marketplace (थेट शेतकरी ते खरेदीदार बाजारपेठ)",
            "step": "Step 5",
            "scope": "Direct farmer-to-buyer listing portal eliminating middleman commissions. Enables farmers to post harvest lots and connect with wholesale buyers.",
            "planned": [
                "Farmer harvest posting form (crop, variety, quantity in quintals, price/quintal)",
                "Buyer enquiry contact generator via direct phone/WhatsApp connection",
                "Active regional commodity listings with quality specifications",
                "Zero online payment or logistics complications (direct peer-to-peer enquiry)"
            ]
        },
        "livestock": {
            "title": "Module 6: Livestock Records & Reminders (पशुधन व्यवस्थापन व लसीकरण)",
            "step": "Step 6",
            "scope": "Digital registry for farm cattle and goats with automated vaccination schedules and overdue alert calculations.",
            "planned": [
                "Individual animal profiles with Ear Tag ID, breed, age, and lactation cycle",
                "Daily milk yield tracker with monthly production trends",
                "Vaccination calendar with automated overdue date math for FMD, HS, BQ",
                "Veterinary checkup and deworming reminder flags"
            ]
        },
        "expense_tracker": {
            "title": "Module 7: Farm Expense Tracker (शेतखर्च नोंदवही व नफा विश्लेषण)",
            "step": "Step 7",
            "scope": "Systematic accounting of input investments and labor expenses with automated monthly, seasonal, crop-wise, and category-wise totals.",
            "planned": [
                "Quick expense logging form (seeds, fertilizer, pesticide, labor, diesel/machinery)",
                "Monthly expenditure breakdown (e.g. October vs November 2026)",
                "Crop-wise cost allocation (Grapes vs Onion vs Soybean)",
                "Category-wise pie chart / breakdown for input cost optimization"
            ]
        }
    }

    info = placeholders.get(active_module, {
        "title": "Module Under Development",
        "step": "Upcoming Step",
        "scope": "This module will be built incrementally according to project guidelines.",
        "planned": []
    })

    st.markdown(f"## {info['title']}")
    st.info(f"🚧 **{info['step']} {t('under_dev_badge')}:** {info['scope']}")
    
    st.markdown(f"### 📋 {t('planned_features_heading')}")
    for feature in info["planned"]:
        st.markdown(f"- ✅ {feature}")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(t("back_to_dashboard"), use_container_width=False):
        st.session_state.active_nav = "dashboard"
        st.rerun()
