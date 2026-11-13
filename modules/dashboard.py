"""
modules/dashboard.py - Module 1: Farmer Profile & Dashboard
KrishiVaani (Voice of Agriculture)

Provides:
1. Quick-access agricultural personal hub with dynamic summary cards.
2. Farmer profile view & interactive in-memory editor (strictly NO database).
3. Navigation shortcuts & preview cards for Modules 2–7.
4. Pure English & Marathi mode rendering via translations.py.
"""

import streamlit as st
from sample_data import reset_to_defaults
from translations import t, get_lang


def calculate_quick_stats(profile, expenses, livestock, marketplace):
    """
    Computes real-time dynamic statistics from in-memory session data.
    Ensures calculations update immediately when profile or expenses change.
    """
    nov_expenses = sum(
        item.get("amount", 0)
        for item in expenses
        if "Nov" in item.get("month", "") or "11" in item.get("date", "")
    )
    
    total_livestock = (
        profile.get("livestock_summary", {}).get("gir_cows", 0)
        + profile.get("livestock_summary", {}).get("murrah_buffaloes", 0)
        + profile.get("livestock_summary", {}).get("goats", 0)
    )
    
    active_crops_count = len(profile.get("crops_grown", []))
    active_listings_count = len(marketplace)

    return {
        "nov_expenses": nov_expenses,
        "total_livestock": total_livestock,
        "active_crops_count": active_crops_count,
        "active_listings_count": active_listings_count,
    }


def render_profile_view(profile):
    """Renders the farmer profile in a clean, informative read-only view."""
    st.markdown(f"### 👨‍🌾 {t('profile_heading')}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**{t('full_name')}:** {profile.get('name', 'N/A')}")
        st.markdown(f"**{t('contact_phone')}:** `{profile.get('phone', 'N/A')}`")
        st.markdown(f"**{t('contact_email')}:** {profile.get('email', 'N/A')}")
        st.markdown(f"**{t('pref_language')}:** {profile.get('primary_language', 'Marathi & English')}")
        
        taluka_prefix = "ता. " if get_lang() == "mr" else "Tal. "
        dist_prefix = "जि. " if get_lang() == "mr" else "Dist. "
        st.markdown(
            f"**{t('address_label')}:** {profile.get('village', '')}, "
            f"{taluka_prefix}{profile.get('taluka', '')}, {dist_prefix}{profile.get('district', '')} - {profile.get('pincode', '')}"
        )

    with col2:
        unit_acres = "एकर (Acres)" if get_lang() == "mr" else "Acres"
        st.markdown(f"**{t('land_size_label')}:** `{profile.get('land_size_acres', 0)} {unit_acres}`")
        st.markdown(f"**{t('soil_type_label')}:** {profile.get('soil_type', 'N/A')}")
        st.markdown(f"**{t('irrigation_label')}:** {profile.get('irrigation_type', 'N/A')}")
        
        livestock = profile.get("livestock_summary", {})
        if get_lang() == "mr":
            livestock_text = (
                f"{livestock.get('gir_cows', 0)} गीर गायी, "
                f"{livestock.get('murrah_buffaloes', 0)} मुऱ्हा म्हैस, "
                f"{livestock.get('goats', 0)} शेळ्या"
            )
            milk_unit = "लिटर/दिवस"
        else:
            livestock_text = (
                f"{livestock.get('gir_cows', 0)} Gir Cows, "
                f"{livestock.get('murrah_buffaloes', 0)} Murrah Buffalo, "
                f"{livestock.get('goats', 0)} Goats"
            )
            milk_unit = "Litres/day"

        st.markdown(f"**{t('livestock_summary_label')}:** {livestock_text}")
        st.markdown(f"**{t('daily_milk_label')}:** `{livestock.get('daily_milk_litres', 0)} {milk_unit}`")

    st.markdown("---")
    st.markdown(f"**{t('crops_cultivated_label')}:**")
    crops = profile.get("crops_grown", [])
    if crops:
        crop_cols = st.columns(len(crops))
        for idx, crop in enumerate(crops):
            with crop_cols[idx]:
                st.info(f"🌱 {crop}")
    else:
        st.caption("No crops listed.")


def render_profile_edit(profile):
    """Renders the profile editing form that saves changes directly into st.session_state."""
    st.markdown(f"### ✏️ {t('btn_edit_profile')}")

    with st.form("edit_farmer_profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name_input = st.text_input(t("full_name"), value=profile.get("name", ""))
            phone_input = st.text_input(t("contact_phone"), value=profile.get("phone", ""))
            email_input = st.text_input(t("contact_email"), value=profile.get("email", ""))
            village_input = st.text_input("गाव / Village", value=profile.get("village", ""))
            taluka_input = st.text_input("तालुका / Taluka", value=profile.get("taluka", ""))
            district_input = st.text_input("जिल्हा / District", value=profile.get("district", "Nashik"))
            pincode_input = st.text_input("पिनकोड / Pincode", value=profile.get("pincode", "422209"))
            
        with col2:
            land_size_input = st.number_input(
                t("land_size_label"),
                min_value=0.1,
                max_value=500.0,
                value=float(profile.get("land_size_acres", 4.5)),
                step=0.5
            )
            
            soil_options = [
                "Medium Black Soil (काळी मध्यम जमीन)",
                "Deep Black Cotton Soil (भारी काळी कापशी जमीन)",
                "Red Loamy Soil (तांबडी पोयट्याची जमीन)",
                "Sandy Loam Soil (हलकी वालुकामय जमीन)"
            ]
            current_soil = profile.get("soil_type", soil_options[0])
            soil_index = soil_options.index(current_soil) if current_soil in soil_options else 0
            soil_input = st.selectbox(t("soil_type_label"), options=soil_options, index=soil_index)
            
            irrigation_options = [
                "Drip Irrigation & Farm Pond (ठिबक सिंचन व शेततळे)",
                "Well & Sprinkler System (विहीर व तुषार सिंचन)",
                "Canal Flood Irrigation (कालवा पाटपाणी)",
                "Borewell & Direct Pipeline (बोअरवेल व पाईपलाईन)"
            ]
            current_irr = profile.get("irrigation_type", irrigation_options[0])
            irr_index = irrigation_options.index(current_irr) if current_irr in irrigation_options else 0
            irrigation_input = st.selectbox(t("irrigation_label"), options=irrigation_options, index=irr_index)

            st.markdown(f"**{t('livestock_summary_label')}:**")
            l_col1, l_col2, l_col3 = st.columns(3)
            with l_col1:
                gir_cows = st.number_input("गायी (Cows)", min_value=0, max_value=100, value=int(profile.get("livestock_summary", {}).get("gir_cows", 2)))
            with l_col2:
                buffaloes = st.number_input("म्हशी (Buffaloes)", min_value=0, max_value=100, value=int(profile.get("livestock_summary", {}).get("murrah_buffaloes", 1)))
            with l_col3:
                goats = st.number_input("शेळ्या (Goats)", min_value=0, max_value=100, value=int(profile.get("livestock_summary", {}).get("goats", 4)))

            daily_milk = st.number_input(
                t("daily_milk_label"),
                min_value=0.0,
                max_value=1000.0,
                value=float(profile.get("livestock_summary", {}).get("daily_milk_litres", 22.0)),
                step=1.0
            )

        crops_raw = st.text_area(
            t("crops_cultivated_label"),
            value=", ".join(profile.get("crops_grown", []))
        )

        submitted = st.form_submit_button(t("btn_save_profile"), use_container_width=True)

        if submitted:
            parsed_crops = [c.strip() for c in crops_raw.replace("\n", ",").split(",") if c.strip()]
            
            st.session_state.farmer_profile["name"] = name_input.strip() or profile.get("name")
            st.session_state.farmer_profile["phone"] = phone_input.strip() or profile.get("phone")
            st.session_state.farmer_profile["email"] = email_input.strip()
            st.session_state.farmer_profile["village"] = village_input.strip()
            st.session_state.farmer_profile["taluka"] = taluka_input.strip()
            st.session_state.farmer_profile["district"] = district_input.strip()
            st.session_state.farmer_profile["pincode"] = pincode_input.strip()
            st.session_state.farmer_profile["land_size_acres"] = land_size_input
            st.session_state.farmer_profile["soil_type"] = soil_input
            st.session_state.farmer_profile["irrigation_type"] = irrigation_input
            st.session_state.farmer_profile["crops_grown"] = parsed_crops
            st.session_state.farmer_profile["livestock_summary"] = {
                "gir_cows": gir_cows,
                "murrah_buffaloes": buffaloes,
                "goats": goats,
                "total_animals": gir_cows + buffaloes + goats,
                "daily_milk_litres": daily_milk
            }
            
            st.session_state.editing_profile = False
            st.success(t("profile_updated_success"))
            st.rerun()


def render_module_placeholders():
    """
    Renders clean, descriptive cards and navigation shortcuts for Modules 2 to 7.
    Adapts text dynamically to active English or Marathi mode.
    """
    st.markdown(f"### 🚀 {t('services_hub_title')}")
    st.caption(t("services_hub_caption"))

    is_mr = get_lang() == "mr"
    status_live = "🟢 उपलब्ध (Live)" if is_mr else "🟢 Live"
    status_dev = "🚧 विकासाधीन" if is_mr else "🚧 In Progress"

    modules_info = [
        {
            "id": "crop_helper",
            "icon": "🌱",
            "title": "पीक सल्लागार व मार्गदर्शन" if is_mr else "Crop & Farming Helper",
            "desc": "पिकांचे टप्प्याटप्प्याने खत व पाणी व्यवस्थापन, रोग नियंत्रण व दैनंदिन शेतकाम चेकलिस्ट." if is_mr else "Stage-wise fertilizer doses, irrigation schedules, pest alerts, and interactive crop action checklists.",
            "status": status_live
        },
        {
            "id": "ai_assistant",
            "icon": "🤖",
            "title": "मराठी व इंग्रजी AI सहाय्यक" if is_mr else "Multilingual Farmer AI Assistant",
            "desc": "शासकीय योजना, खते, रोग आणि अनुदानाबाबत त्वरित प्रश्नोत्तरे व सल्लागार." if is_mr else "Text-based Marathi & English intent router for farming FAQs, government schemes, and instant crop solutions.",
            "status": status_dev
        },
        {
            "id": "nearby_services",
            "icon": "📍",
            "title": "जवळपासची कृषी सेवा केंद्र" if is_mr else "Nearby Agricultural Services",
            "desc": "स्थानिक पशुवैद्यकीय डॉक्टर, बियाणे-खत दुकाने, कृषी अवजारे भाडे केंद्र व माती परीक्षण लॅब." if is_mr else "Directory of vetted local vets, Krishi Seva Kendra seed shops, soil labs, and machinery rental centres.",
            "status": status_live
        },
        {
            "id": "marketplace",
            "icon": "🛒",
            "title": "शेतकरी थेट बाजारपेठ" if is_mr else "Farmer-to-Buyer Marketplace",
            "desc": "कांदा, द्राक्षे व शेतमालाची थेट खरेदीदारांशी जोडणी, दलाली विरहित फोन व व्हॉट्सॲप चौकशी." if is_mr else "Post farm produce listings (Onions, Grapes, Soybeans) and receive direct phone enquiries from wholesale buyers.",
            "status": status_dev
        },
        {
            "id": "livestock",
            "icon": "🐄",
            "title": "पशुधन नोंदी व लसीकरण" if is_mr else "Livestock Records & Reminders",
            "desc": "गाय-म्हशींच्या टॅग नोंदी, दैनंदिन दूध उत्पादन आणि लाळ-खुरकत (FMD) लसीकरण स्मरणपत्रे." if is_mr else "Tag-based cattle profiles, milk yield tracking, and automated overdue vaccination deadline alerts.",
            "status": status_dev
        },
        {
            "id": "expense_tracker",
            "icon": "💰",
            "title": "शेतखर्च ट्रॅकर व नफा" if is_mr else "Farm Expense Tracker",
            "desc": "बियाणे, खते व मजुरी खर्चाची मासिक विभागणी आणि पीकनिहाय नफा-तोटा विश्लेषण." if is_mr else "Categorize input costs (seeds, fertilizer, labor), calculate monthly totals, and view crop-wise ROI comparisons.",
            "status": status_dev
        }
    ]

    cols = st.columns(3)
    for index, mod in enumerate(modules_info):
        col = cols[index % 3]
        with col:
            with st.container(border=True):
                st.markdown(f"#### {mod['icon']} {mod['title']}")
                st.markdown(f"`{mod['status']}`")
                st.write(mod["desc"])
                
                btn_text = f"{t('btn_open_module')} {mod['icon']}" if "Live" in mod["status"] or "उपलब्ध" in mod["status"] else f"{t('btn_view_info')} {mod['icon']}"
                if st.button(btn_text, key=f"nav_btn_{mod['id']}", use_container_width=True):
                    st.session_state.active_nav = mod["id"]
                    st.rerun()


def render_dashboard():
    """
    Main entry point for Module 1: Farmer Profile & Dashboard.
    Bilingual, reactive, and completely in-memory.
    """
    profile = st.session_state.farmer_profile
    expenses = st.session_state.farm_expenses
    livestock = st.session_state.livestock_records
    marketplace = st.session_state.marketplace_listings

    stats = calculate_quick_stats(profile, expenses, livestock, marketplace)
    is_mr = get_lang() == "mr"

    # 1. Welcome Greeting Banner
    greet_title = f"🌾 {t('greeting_welcome')}, {profile.get('name', 'Farmer')}!"
    sub_land = f"{profile.get('land_size_acres', 0)} " + ("एकर" if is_mr else "Acres")
    
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #1e522f 0%, #2e7d32 100%);
                    padding: 22px 26px; border-radius: 12px; color: white; margin-bottom: 20px;">
            <h2 style="margin: 0; color: white;">{greet_title}</h2>
            <p style="margin: 6px 0 0 0; font-size: 15px; opacity: 0.92;">
                📍 <b>{profile.get('village', '')}, {profile.get('district', '')}</b> | 
                {t('greeting_season')} | 
                {t('greeting_land')}: <b>{sub_land}</b>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. Quick-Access Personal Hub Summary Cards
    st.markdown(f"### 📊 {t('quick_overview')}")
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.metric(
            label=f"🚜 {t('metric_land')}",
            value=f"{profile.get('land_size_acres', 0)} Acres",
            delta=profile.get("soil_type", "").split("(")[0].strip()
        )
    with m2:
        crops_delta = "द्राक्ष, कांदा, सोयाबीन" if is_mr else "Grapes, Onion, Soybean"
        st.metric(
            label=f"🌱 {t('metric_crops')}",
            value=f"{stats['active_crops_count']} {t('crops_count_suffix')}",
            delta=crops_delta
        )
    with m3:
        milk_delta = f"दूध: {profile.get('livestock_summary', {}).get('daily_milk_litres', 0)} L/day" if is_mr else f"Milk: {profile.get('livestock_summary', {}).get('daily_milk_litres', 0)} L/day"
        st.metric(
            label=f"🐄 {t('metric_livestock')}",
            value=f"{stats['total_livestock']} {t('animals_count_suffix')}",
            delta=milk_delta
        )
    with m4:
        st.metric(
            label=f"💳 {t('metric_expenses')}",
            value=f"₹{stats['nov_expenses']:,}",
            delta=f"3 {t('logs_suffix')}"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Farmer Profile View & In-Memory Editor
    if "editing_profile" not in st.session_state:
        st.session_state.editing_profile = False

    head_col1, head_col2 = st.columns([3, 1])
    with head_col1:
        st.markdown(f"### 👤 {t('profile_heading')}")
    with head_col2:
        toggle_label = t("btn_view_profile") if st.session_state.editing_profile else t("btn_edit_profile")
        if st.button(toggle_label, use_container_width=True):
            st.session_state.editing_profile = not st.session_state.editing_profile
            st.rerun()

    with st.container(border=True):
        if st.session_state.editing_profile:
            render_profile_edit(profile)
        else:
            render_profile_view(profile)

    # Option to reload default sample data
    with st.expander(f"⚙️ {t('reset_defaults_title')}"):
        st.write(t("reset_defaults_desc"))
        if st.button(t("btn_reset_defaults")):
            reset_to_defaults(st)
            st.session_state.editing_profile = False
            st.success(t("reset_success"))
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Navigation Placeholders for Modules 2–7
    render_module_placeholders()
