"""
app.py - Main Application Controller for KrishiVaani (Voice of Agriculture)
Unified Python digital platform for Indian farmers built with Streamlit.
Strictly NO external database (uses Streamlit in-memory session state).
"""

import streamlit as st
from sample_data import init_session_data
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

# Custom agricultural CSS polish
st.markdown(
    """
    <style>
    .main-title {
        color: #1b5e20;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .sub-title {
        color: #4a5568;
        font-size: 14px;
        margin-bottom: 15px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 24px;
        font-weight: 700;
        color: #1e522f;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------- SIDEBAR NAVIGATION -----------------
with st.sidebar:
    st.markdown("## 🌾 कृषीवाणी (KrishiVaani)")
    st.caption("Voice of Agriculture | Smart India Hackathon Prototype")
    
    # Farmer snapshot widget in the sidebar
    profile = st.session_state.farmer_profile
    with st.container(border=True):
        st.markdown(f"**शेतकरी:** {profile.get('name', 'N/A')}")
        st.caption(f"📍 {profile.get('village', '')}, {profile.get('district', '')}")
        st.caption(f"🚜 शेतजमीन: {profile.get('land_size_acres', 0)} एकर (Acres)")

    st.markdown("---")
    st.markdown("### 🧭 मुख्य विभाग (Navigation)")

    nav_options = {
        "dashboard": "🏠 1. प्रोफाइल व डॅशबोर्ड (Profile & Hub)",
        "crop_helper": "🌱 2. पीक सल्लागार (Crop Helper)",
        "ai_assistant": "🤖 3. AI शेती सहाय्यक (AI Assistant)",
        "nearby_services": "📍 4. कृषी सेवा केंद्र (Nearby Services)",
        "marketplace": "🛒 5. शेतकरी बाजारपेठ (Marketplace)",
        "livestock": "🐄 6. पशुधन व लसीकरण (Livestock)",
        "expense_tracker": "💰 7. शेतखर्च ट्रॅकर (Expense Tracker)"
    }

    # Determine current selection index
    keys_list = list(nav_options.keys())
    current_key = st.session_state.get("active_nav", "dashboard")
    current_index = keys_list.index(current_key) if current_key in keys_list else 0

    selected_label = st.radio(
        label="विभाग निवडा (Select Module):",
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
    st.markdown(
        """
        <div style="font-size: 12px; color: #6b7280; text-align: center;">
            🌱 <b>KrishiVaani v1.1 (Step 2)</b><br>
            Modules 1, 2, and 4 Active<br>
            Pure Python • No Database
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
    st.info(f"🚧 **{info['step']} विकासाधीन (Under Development):** {info['scope']}")
    
    st.markdown("### 📋 या विभागात समाविष्ट होणारी मुख्य वैशिष्ट्ये (Planned Features):")
    for feature in info["planned"]:
        st.markdown(f"- ✅ {feature}")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅️ डॅशबोर्डवर परत जा (Back to Farmer Dashboard)", use_container_width=False):
        st.session_state.active_nav = "dashboard"
        st.rerun()
