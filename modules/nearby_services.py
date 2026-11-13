"""
modules/nearby_services.py - Module 4: Nearby Agricultural Services
KrishiVaani (Voice of Agriculture)

Provides:
1. Local directory of agricultural service providers (Vets, Seed/Fertilizer shops, Fodder, Equipment rental, Labs).
2. Filtering by service category and taluka (defaulting to farmer's home taluka from profile).
3. Search by keyword and direct contact buttons (click-to-call and WhatsApp inquiry).
4. In-memory registration of new local service providers directly into st.session_state.
5. Pure English & Marathi mode rendering via translations.py.
"""

import streamlit as st
import urllib.parse
from translations import t, get_lang


def render_service_card(srv):
    """Renders a single service provider card with metadata and contact options."""
    with st.container(border=True):
        top_col1, top_col2 = st.columns([4, 1.5])
        with top_col1:
            st.markdown(f"#### 🏢 {srv.get('name')}")
        with top_col2:
            st.markdown(f"⭐ **{srv.get('rating', 4.5)} / 5.0**")

        st.markdown(
            f"`🏷️ {srv.get('category')}` &nbsp;|&nbsp; "
            f"📍 **{srv.get('taluka', '')}** — {srv.get('location', '')}"
        )

        st.caption(f"🕒 **{t('timings_label')}:** {srv.get('timings', 'N/A')}")
        
        st.markdown(f"**{t('available_services_label')}**")
        st.info(f"🛠️ {srv.get('speciality', 'Agricultural support services')}")

        phone_raw = srv.get("phone", "").replace(" ", "").replace("-", "")
        call_link = f"tel:{phone_raw}"
        
        farmer_name = st.session_state.get("farmer_profile", {}).get("name", "Farmer")
        is_mr = get_lang() == "mr"
        
        if is_mr:
            wa_text = urllib.parse.quote(
                f"नमस्कार, मी {farmer_name}. मी कृषीवाणी (KrishiVaani) ॲपवरून आपल्या कृषी सेवेबाबत माहिती विचारण्यासाठी संपर्क करत आहे."
            )
        else:
            wa_text = urllib.parse.quote(
                f"Hello, I am {farmer_name}. I am contacting you via KrishiVaani app regarding your agricultural services."
            )
        wa_link = f"https://wa.me/{phone_raw.replace('+', '')}?text={wa_text}"

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            st.link_button(f"📞 {t('btn_call_now')} ({srv.get('phone')})", call_link, use_container_width=True)
        with btn_col2:
            st.link_button(f"💬 {t('btn_whatsapp')}", wa_link, use_container_width=True)


def render_add_service_form():
    """Allows farmers or community members to add a new local agricultural service."""
    with st.expander(t("add_service_expander")):
        st.caption(t("add_service_caption"))
        
        with st.form("add_service_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_name = st.text_input(t("provider_name_label"), placeholder="e.g. Shri Samarth Krishi Kendra")
                cat_choices = [
                    "Veterinary Doctors & Emergency (पशुवैद्यकीय सेवा)",
                    "Seeds & Fertilizer Shops (बियाणे व खते केंद्र)",
                    "Machinery & Equipment Rental (कृषी अवजारे भाडेतत्त्वावर)",
                    "Fodder & Cattle Feed (पशुखाद्य व वैरण)",
                    "Agricultural Service Centres (कृषी सेवा व माती परीक्षण केंद्र)"
                ]
                new_cat = st.selectbox(t("provider_cat_label"), options=cat_choices)
                new_taluka = st.selectbox(
                    t("provider_taluka_label"),
                    options=["Niphad (निफाड)", "Nashik (नाशिक)", "Dindori (दिंडोरी)", "Chandwad (चांदवड)", "Sinnar (सिन्नर)", "Yeola (येवला)"]
                )
                
            with col2:
                new_location = st.text_input(t("provider_location_label"), placeholder="e.g. Main Chowk, Niphad (2.5 km)")
                new_phone = st.text_input(t("provider_phone_label"), placeholder="+91 98XXX XXXXX")
                new_timings = st.text_input(t("provider_timings_label"), placeholder="e.g. 8:00 AM - 8:00 PM (Emergency 24x7)")

            new_speciality = st.text_area(t("provider_speciality_label"), placeholder="e.g. Onion seeds, drip fittings, bio-fertilizers")

            submitted = st.form_submit_button(t("btn_save_service"), use_container_width=True)

            if submitted:
                if new_name.strip() and new_phone.strip():
                    new_id = f"SRV-{len(st.session_state.nearby_services) + 1:02d}"
                    new_item = {
                        "id": new_id,
                        "name": new_name.strip(),
                        "category": new_cat,
                        "category_key": new_cat.split()[0].lower(),
                        "taluka": new_taluka,
                        "district": "Nashik",
                        "location": new_location.strip() or f"{new_taluka} Area",
                        "phone": new_phone.strip(),
                        "timings": new_timings.strip() or "General Hours",
                        "speciality": new_speciality.strip() or "General agricultural assistance",
                        "rating": 5.0,
                        "verified": True
                    }
                    st.session_state.nearby_services.append(new_item)
                    st.success(t("service_saved_success"))
                    st.rerun()
                else:
                    st.warning(t("service_input_warning"))


def render_nearby_services():
    """
    Main entry point for Module 4: Nearby Agricultural Services.
    Renders filter bars, responsive cards, direct call links, and registration utility.
    """
    profile = st.session_state.get("farmer_profile", {})
    services = st.session_state.get("nearby_services", [])
    farmer_taluka_raw = profile.get("taluka", "Niphad")

    # Top Banner
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #0d47a1 0%, #1976d2 100%);
                    padding: 20px 24px; border-radius: 12px; color: white; margin-bottom: 22px;">
            <h2 style="margin: 0; color: white;">📍 {t('nearby_banner_title')}</h2>
            <p style="margin: 6px 0 0 0; font-size: 14px; opacity: 0.94;">
                {t('nearby_banner_subtitle')}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Filter Controls Bar
    st.markdown(f"### 🔍 {t('search_filter_title')}")
    f_col1, f_col2, f_col3 = st.columns([2, 1.5, 2])

    with f_col1:
        category_options = [
            t("all_categories"),
            "Veterinary Doctors & Emergency (पशुवैद्यकीय सेवा)",
            "Seeds & Fertilizer Shops (बियाणे व खते केंद्र)",
            "Machinery & Equipment Rental (कृषी अवजारे भाडेतत्त्वावर)",
            "Fodder & Cattle Feed (पशुखाद्य व वैरण)",
            "Agricultural Service Centres (कृषी सेवा व माती परीक्षण केंद्र)"
        ]
        selected_category = st.selectbox(t("category_filter_label"), options=category_options, index=0)

    with f_col2:
        taluka_options = [
            t("all_talukas"),
            "Niphad (निफाड)",
            "Nashik (नाशिक)",
            "Dindori (दिंडोरी)",
            "Chandwad (चांदवड)",
            "Sinnar (सिन्नर)"
        ]
        
        default_t_idx = 1 if "niphad" in farmer_taluka_raw.lower() or "निफाड" in farmer_taluka_raw else 0
        selected_taluka = st.selectbox(t("taluka_filter_label"), options=taluka_options, index=default_t_idx)

    with f_col3:
        search_query = st.text_input(t("keyword_search_label"), placeholder=t("keyword_placeholder"))

    # Filter Application Logic
    filtered_services = []
    for srv in services:
        match_cat = True
        if selected_category != t("all_categories"):
            if "veterinary" in selected_category.lower() or "पशुवैद्यकीय" in selected_category:
                if "veterinary" not in srv.get("category", "").lower():
                    match_cat = False
            elif "seeds" in selected_category.lower() or "बियाणे" in selected_category:
                if "seed" not in srv.get("category", "").lower():
                    match_cat = False
            elif "machinery" in selected_category.lower() or "अवजारे" in selected_category:
                if "machinery" not in srv.get("category", "").lower() and "equipment" not in srv.get("category", "").lower():
                    match_cat = False
            elif "fodder" in selected_category.lower() or "पशुखाद्य" in selected_category:
                if "fodder" not in srv.get("category", "").lower():
                    match_cat = False
            elif "centres" in selected_category.lower() or "माती परीक्षण" in selected_category:
                if "service" not in srv.get("category", "").lower() and "testing" not in srv.get("category", "").lower():
                    match_cat = False

        match_taluka = True
        if selected_taluka != t("all_talukas"):
            chosen_t = selected_taluka.split("(")[0].strip().lower()
            srv_t = srv.get("taluka", "").lower()
            if chosen_t not in srv_t:
                match_taluka = False

        match_search = True
        if search_query.strip():
            q = search_query.strip().lower()
            combined_text = (
                f"{srv.get('name', '')} {srv.get('category', '')} {srv.get('location', '')} "
                f"{srv.get('speciality', '')} {srv.get('phone', '')} {srv.get('taluka', '')}"
            ).lower()
            if q not in combined_text:
                match_search = False

        if match_cat and match_taluka and match_search:
            filtered_services.append(srv)

    # Results Counter
    st.markdown(
        f"**{t('showing_label')}:** `{len(filtered_services)}` {t('providers_label')} "
        f"({selected_taluka} | {selected_category.split('(')[0].strip()})"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Render Service Cards in 2-Column Responsive Grid
    if filtered_services:
        cols = st.columns(2)
        for idx, srv in enumerate(filtered_services):
            target_col = cols[idx % 2]
            with target_col:
                render_service_card(srv)
    else:
        st.warning(t("no_providers_found"))

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    # Community Registration Utility
    render_add_service_form()
