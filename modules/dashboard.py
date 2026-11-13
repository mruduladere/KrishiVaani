"""
modules/dashboard.py - Module 1: Farmer Profile & Dashboard
KrishiVaani (Voice of Agriculture)

Provides:
1. Quick-access agricultural personal hub with dynamic summary cards.
2. Farmer profile view & interactive in-memory editor (strictly NO database).
3. Navigation shortcuts & preview cards for Modules 2–7.
"""

import streamlit as st
from sample_data import reset_to_defaults


def calculate_quick_stats(profile, expenses, livestock, marketplace):
    """
    Computes real-time dynamic statistics from in-memory session data.
    Ensures calculations update immediately when profile or expenses change.
    """
    # Sum up November 2026 expenses as the active current month
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
    st.markdown("### 👨‍🌾 शेतकरी माहिती (Farmer Profile Details)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**नाव (Full Name):** {profile.get('name', 'N/A')}")
        st.markdown(f"**संपर्क क्रमांक (Phone):** `{profile.get('phone', 'N/A')}`")
        st.markdown(f"**ईमेल (Email):** {profile.get('email', 'N/A')}")
        st.markdown(f"**भाषा (Preferred Language):** {profile.get('primary_language', 'Marathi & English')}")
        st.markdown(
            f"**पत्ता (Location):** {profile.get('village', '')}, "
            f"ता. {profile.get('taluka', '')}, जि. {profile.get('district', '')} - {profile.get('pincode', '')}"
        )

    with col2:
        st.markdown(f"**जमीन धारणा (Land Size):** `{profile.get('land_size_acres', 0)} Acres`")
        st.markdown(f"**मातीचा प्रकार (Soil Type):** {profile.get('soil_type', 'N/A')}")
        st.markdown(f"**सिंचन सुविधा (Irrigation):** {profile.get('irrigation_type', 'N/A')}")
        
        livestock = profile.get("livestock_summary", {})
        livestock_text = (
            f"{livestock.get('gir_cows', 0)} गीर गायी (Gir Cows), "
            f"{livestock.get('murrah_buffaloes', 0)} मुऱ्हा म्हैस (Murrah Buffalo), "
            f"{livestock.get('goats', 0)} शेळ्या (Goats)"
        )
        st.markdown(f"**पशुधन (Livestock):** {livestock_text}")
        st.markdown(f"**दैनंदिन दूध उत्पादन (Daily Milk):** `{livestock.get('daily_milk_litres', 0)} Litres/day`")

    st.markdown("---")
    st.markdown("**सध्याची पिके (Crops Currently Cultivated):**")
    crops = profile.get("crops_grown", [])
    if crops:
        crop_cols = st.columns(len(crops))
        for idx, crop in enumerate(crops):
            with crop_cols[idx]:
                st.info(f"🌱 {crop}")
    else:
        st.caption("No crops currently listed.")


def render_profile_edit(profile):
    """Renders the profile editing form that saves changes directly into st.session_state."""
    st.markdown("### ✏️ प्रोफाइल संपादन (Edit Farmer Profile)")
    st.caption("सर्व बदल थेट ॲप मेमरीमध्ये सेव्ह होतात (All edits update instantly in memory).")

    with st.form("edit_farmer_profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name_input = st.text_input("पूर्ण नाव (Full Name)", value=profile.get("name", ""))
            phone_input = st.text_input("मोबाईल क्रमांक (Phone Number)", value=profile.get("phone", ""))
            email_input = st.text_input("ईमेल (Email Address)", value=profile.get("email", ""))
            village_input = st.text_input("गाव (Village)", value=profile.get("village", ""))
            taluka_input = st.text_input("तालुका (Taluka)", value=profile.get("taluka", ""))
            district_input = st.text_input("जिल्हा (District)", value=profile.get("district", "Nashik"))
            pincode_input = st.text_input("पिनकोड (Pincode)", value=profile.get("pincode", "422209"))
            
        with col2:
            land_size_input = st.number_input(
                "एकूण शेतजमीन (Land Size in Acres)",
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
            soil_input = st.selectbox("मातीचा प्रकार (Soil Type)", options=soil_options, index=soil_index)
            
            irrigation_options = [
                "Drip Irrigation & Farm Pond (ठिबक सिंचन व शेततळे)",
                "Well & Sprinkler System (विहीर व तुषार सिंचन)",
                "Canal Flood Irrigation (कालवा पाटपाणी)",
                "Borewell & Direct Pipeline (बोअरवेल व पाईपलाईन)"
            ]
            current_irr = profile.get("irrigation_type", irrigation_options[0])
            irr_index = irrigation_options.index(current_irr) if current_irr in irrigation_options else 0
            irrigation_input = st.selectbox("सिंचन पद्धत (Irrigation Method)", options=irrigation_options, index=irr_index)

            st.markdown("**पशुधन संख्या (Livestock Count):**")
            l_col1, l_col2, l_col3 = st.columns(3)
            with l_col1:
                gir_cows = st.number_input("गायी (Gir Cows)", min_value=0, max_value=100, value=int(profile.get("livestock_summary", {}).get("gir_cows", 2)))
            with l_col2:
                buffaloes = st.number_input("म्हशी (Buffaloes)", min_value=0, max_value=100, value=int(profile.get("livestock_summary", {}).get("murrah_buffaloes", 1)))
            with l_col3:
                goats = st.number_input("शेळ्या (Goats)", min_value=0, max_value=100, value=int(profile.get("livestock_summary", {}).get("goats", 4)))

            daily_milk = st.number_input(
                "दैनंदिन दूध उत्पादन (Daily Milk in Litres)",
                min_value=0.0,
                max_value=1000.0,
                value=float(profile.get("livestock_summary", {}).get("daily_milk_litres", 22.0)),
                step=1.0
            )

        crops_raw = st.text_area(
            "पिके (Crops Cultivated - एक ओळीत एक किंवा स्वल्पविरामाने वेगळे करा)",
            value=", ".join(profile.get("crops_grown", []))
        )

        submitted = st.form_submit_button("💾 प्रोफाइल जतन करा (Save Profile Changes)", use_container_width=True)

        if submitted:
            # Clean and parse crops input
            parsed_crops = [c.strip() for c in crops_raw.replace("\n", ",").split(",") if c.strip()]
            
            # Update session state profile in place
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
            st.success("✅ प्रोफाइल यशस्वीरीत्या जतन केले! (Profile updated successfully!)")
            st.rerun()


def render_module_placeholders():
    """
    Renders clean, descriptive cards and navigation placeholders for Modules 2 to 7.
    Allows the farmer to jump to any module or preview upcoming capabilities.
    """
    st.markdown("### 🚀 कृषीवाणी सेवा केंद्र (Platform Services & Modules)")
    st.caption("खालील सेवांवर क्लिक करून थेट त्या विभागात जा (Click on any module to navigate).")

    modules_info = [
        {
            "id": "crop_helper",
            "icon": "🌱",
            "title": "Module 2: Crop & Farming Helper",
            "marathi_title": "पीक सल्लागार व मार्गदर्शन",
            "desc": "Stage-wise fertilizer doses, irrigation schedules, pest alerts, and interactive crop action checklists.",
            "status": "🟢 उपलब्ध (Live)"
        },
        {
            "id": "ai_assistant",
            "icon": "🤖",
            "title": "Module 3: Multilingual Farmer AI Assistant",
            "marathi_title": "मराठी व इंग्रजी AI सहाय्यक",
            "desc": "Text-based Marathi & English intent router for farming FAQs, government schemes, and instant crop solutions.",
            "status": "🚧 Step 3"
        },
        {
            "id": "nearby_services",
            "icon": "📍",
            "title": "Module 4: Nearby Agricultural Services",
            "marathi_title": "जवळपासची कृषी सेवा केंद्र",
            "desc": "Directory of vetted local vets, Krishi Seva Kendra seed shops, soil labs, and machinery rental centres.",
            "status": "🟢 उपलब्ध (Live)"
        },
        {
            "id": "marketplace",
            "icon": "🛒",
            "title": "Module 5: Farmer-to-Buyer Marketplace",
            "marathi_title": "थेट शेतकरी ते खरेदीदार बाजारपेठ",
            "desc": "Post farm produce listings (Onions, Grapes, Soybeans) and receive direct phone enquiries from wholesale buyers.",
            "status": "🚧 Step 5"
        },
        {
            "id": "livestock",
            "icon": "🐄",
            "title": "Module 6: Livestock Records & Reminders",
            "marathi_title": "पशुधन व्यवस्थापन व लसीकरण",
            "desc": "Tag-based cattle profiles, milk yield tracking, and automated overdue vaccination deadline alerts.",
            "status": "🚧 Step 6"
        },
        {
            "id": "expense_tracker",
            "icon": "💰",
            "title": "Module 7: Farm Expense Tracker",
            "marathi_title": "शेतखर्च नोंदवही व नफा विश्लेषण",
            "desc": "Categorize input costs (seeds, fertilizer, labor), calculate monthly totals, and view crop-wise ROI comparisons.",
            "status": "🚧 Step 7"
        }
    ]

    cols = st.columns(3)
    for index, mod in enumerate(modules_info):
        col = cols[index % 3]
        with col:
            with st.container(border=True):
                st.markdown(f"#### {mod['icon']} {mod['title']}")
                st.markdown(f"`{mod['status']}` &nbsp;|&nbsp; **{mod['marathi_title']}**")
                st.write(mod["desc"])
                
                # Navigation button that switches the active module
                btn_text = f"उघडा (Open {mod['icon']})" if "Live" in mod["status"] else f"माहिती (View {mod['icon']})"
                if st.button(btn_text, key=f"nav_btn_{mod['id']}", use_container_width=True):
                    st.session_state.active_nav = mod["id"]
                    st.rerun()


def render_dashboard():
    """
    Main entry point for Module 1.
    Renders welcome banner, quick-access metrics, farmer profile management,
    and navigation placeholders for subsequent modules.
    """
    profile = st.session_state.farmer_profile
    expenses = st.session_state.farm_expenses
    livestock = st.session_state.livestock_records
    marketplace = st.session_state.marketplace_listings

    stats = calculate_quick_stats(profile, expenses, livestock, marketplace)

    # 1. Welcome Greeting Banner
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #1e522f 0%, #2e7d32 100%);
                    padding: 22px 26px; border-radius: 12px; color: white; margin-bottom: 20px;">
            <h2 style="margin: 0; color: white;">🌾 नमस्कार, {profile.get('name', 'शेतकरी मित्र')}!</h2>
            <p style="margin: 6px 0 0 0; font-size: 15px; opacity: 0.92;">
                📍 <b>{profile.get('village', '')}, {profile.get('district', '')}</b> | 
                हंगाम: <b>रब्बी २०२६-२७ (Rabi Season)</b> | 
                जमीन: <b>{profile.get('land_size_acres', 0)} एकर</b>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. Quick-Access Personal Hub Summary Cards
    st.markdown("### 📊 शेती सारांश (Quick Farm Overview)")
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.metric(
            label="🚜 एकूण शेतजमीन (Land)",
            value=f"{profile.get('land_size_acres', 0)} Acres",
            delta=profile.get("soil_type", "").split("(")[0].strip()
        )
    with m2:
        st.metric(
            label="🌱 सक्रिय पिके (Active Crops)",
            value=f"{stats['active_crops_count']} पिके",
            delta="द्राक्ष, कांदा, सोयाबीन"
        )
    with m3:
        st.metric(
            label="🐄 एकूण पशुधन (Livestock)",
            value=f"{stats['total_livestock']} जनावरे",
            delta=f"दूध: {profile.get('livestock_summary', {}).get('daily_milk_litres', 0)} L/day"
        )
    with m4:
        st.metric(
            label="💳 चालू महिना खर्च (Nov Expense)",
            value=f"₹{stats['nov_expenses']:,}",
            delta="3 नोंदी (3 logs)"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Farmer Profile View & In-Memory Editor
    if "editing_profile" not in st.session_state:
        st.session_state.editing_profile = False

    head_col1, head_col2 = st.columns([3, 1])
    with head_col1:
        st.markdown("### 👤 शेतकरी प्रोफाइल व्यवस्थापन (Farmer Profile & Farm Details)")
    with head_col2:
        toggle_label = "👁️ पहा (View)" if st.session_state.editing_profile else "✏️ संपादन करा (Edit Profile)"
        if st.button(toggle_label, use_container_width=True):
            st.session_state.editing_profile = not st.session_state.editing_profile
            st.rerun()

    with st.container(border=True):
        if st.session_state.editing_profile:
            render_profile_edit(profile)
        else:
            render_profile_view(profile)

    # Option to reload default sample data
    with st.expander("⚙️ नमुना डेटा रिसेट करा (Reset to Default Sample Data)"):
        st.write("जर तुम्ही डेटा बदलला असेल आणि पुन्हा मूळ नमुना डेटा आणायचा असेल, तर खालील बटण दाबा.")
        if st.button("🔄 मूळ नमुना डेटा पुनर्स्थापित करा (Restore Sample Defaults)"):
            reset_to_defaults(st)
            st.session_state.editing_profile = False
            st.success("✅ मूळ नमुना डेटा पूर्ववत करण्यात आला! (Reset to default sample data)")
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Navigation Placeholders for Modules 2–7
    render_module_placeholders()
