"""
modules/nearby_services.py - Module 4: Nearby Agricultural Services
KrishiVaani (Voice of Agriculture)

Provides:
1. Local directory of agricultural service providers (Vets, Seed/Fertilizer shops, Fodder, Equipment rental, Labs).
2. Filtering by service category and taluka (defaulting to farmer's home taluka from profile).
3. Search by keyword and direct contact buttons (click-to-call and WhatsApp inquiry).
4. In-memory registration of new local service providers directly into st.session_state.
"""

import streamlit as st
import urllib.parse


def render_service_card(srv):
    """Renders a single service provider card with metadata and contact options."""
    with st.container(border=True):
        # Header row: Name, Verified badge, Rating
        top_col1, top_col2 = st.columns([4, 1.5])
        with top_col1:
            st.markdown(f"#### 🏢 {srv.get('name')}")
        with top_col2:
            st.markdown(f"⭐ **{srv.get('rating', 4.5)} / 5.0**")

        # Category and Location tags
        st.markdown(
            f"`🏷️ {srv.get('category')}` &nbsp;|&nbsp; "
            f"📍 **{srv.get('taluka', '')}** — {srv.get('location', '')}"
        )

        st.caption(f"🕒 **वेळ (Timings):** {srv.get('timings', 'N/A')}")
        
        # Specialities / Services offered
        st.markdown(f"**उपलब्ध सेवा (Available Services):**")
        st.info(f"🛠️ {srv.get('speciality', 'Agricultural support services')}")

        # Action bar: Direct Call & WhatsApp
        phone_raw = srv.get("phone", "").replace(" ", "").replace("-", "")
        call_link = f"tel:{phone_raw}"
        
        # Pre-fill WhatsApp message
        farmer_name = st.session_state.get("farmer_profile", {}).get("name", "Farmer")
        wa_text = urllib.parse.quote(
            f"नमस्कार, मी {farmer_name}. मी कृषीवाणी (KrishiVaani) ॲपवरून आपल्या कृषी सेवेबाबत माहिती विचारण्यासाठी संपर्क करत आहे."
        )
        wa_link = f"https://wa.me/{phone_raw.replace('+', '')}?text={wa_text}"

        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            st.link_button(f"📞 कॉल करा ({srv.get('phone')})", call_link, use_container_width=True)
        with btn_col2:
            st.link_button("💬 व्हॉट्सॲप चौकशी (WhatsApp)", wa_link, use_container_width=True)


def render_add_service_form():
    """Allows farmers or community members to add a new local agricultural service."""
    with st.expander("➕ नवीन कृषी सेवा प्रदाता नोंदवा (Register a New Local Service / Doctor)"):
        st.caption("तुमच्या भागातील इतर शेतकरी मित्रांच्या सोयीसाठी खात्रीशीर सेवा प्रदात्यांची माहिती जोडा.")
        
        with st.form("add_service_form"):
            col1, col2 = st.columns(2)
            with col1:
                new_name = st.text_input("प्रदाता किंवा केंद्राचे नाव (Provider / Centre Name)", placeholder="उदा. श्री समर्थ कृषी सेवा केंद्र")
                cat_choices = [
                    "Veterinary Doctors & Emergency (पशुवैद्यकीय सेवा)",
                    "Seeds & Fertilizer Shops (बियाणे व खते केंद्र)",
                    "Machinery & Equipment Rental (कृषी अवजारे भाडेतत्त्वावर)",
                    "Fodder & Cattle Feed (पशुखाद्य व वैरण)",
                    "Agricultural Service Centres (कृषी सेवा व माती परीक्षण केंद्र)"
                ]
                new_cat = st.selectbox("सेवेचा प्रकार (Category)", options=cat_choices)
                new_taluka = st.selectbox(
                    "तालुका (Taluka)",
                    options=["Niphad (निफाड)", "Nashik (नाशिक)", "Dindori (दिंडोरी)", "Chandwad (चांदवड)", "Sinnar (सिन्नर)", "Yeola (येवला)"]
                )
                
            with col2:
                new_location = st.text_input("पत्ता व अंतर (Location & Distance)", placeholder="उदा. चांदवड नाका, निफाड (२.५ किमी)")
                new_phone = st.text_input("संपर्क क्रमांक (Phone Number)", placeholder="+91 98XXX XXXXX")
                new_timings = st.text_input("कामाची वेळ (Timings)", placeholder="उदा. सकाळी ८ ते रात्री ८ (Emergency 24x7)")

            new_speciality = st.text_area("उपलब्ध सेवा व वैशिष्ट्ये (Services & Specialities)", placeholder="उदा. कांदा बियाणे, ठिबक फिटिंग्स, खते")

            submitted = st.form_submit_button("✅ प्रदाता जतन करा (Save Service Provider)", use_container_width=True)

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
                    st.success("✅ सेवा प्रदाता यशस्वीरीत्या जोडला गेला! (Service provider registered)")
                    st.rerun()
                else:
                    st.warning("कृपया प्रदात्याचे नाव व फोन नंबर प्रविष्ट करा (Please provide name and phone).")


def render_nearby_services():
    """
    Main entry point for Module 4: Nearby Agricultural Services.
    Renders filter bars, responsive cards, direct call links, and registration utility.
    """
    profile = st.session_state.get("farmer_profile", {})
    services = st.session_state.get("nearby_services", [])

    # Farmer's home taluka from profile
    farmer_taluka_raw = profile.get("taluka", "Niphad")

    # Top Banner
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #0d47a1 0%, #1976d2 100%);
                    padding: 20px 24px; border-radius: 12px; color: white; margin-bottom: 22px;">
            <h2 style="margin: 0; color: white;">📍 जवळपासची कृषी सेवा केंद्र (Nearby Agricultural Services)</h2>
            <p style="margin: 6px 0 0 0; font-size: 14px; opacity: 0.94;">
                पशुवैद्यकीय डॉक्टर, बियाणे-खत दुकाने, कृषी अवजारे भाडे केंद्र व माती परीक्षण प्रयोगशाळांची खात्रीशीर माहिती.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Filter Controls Bar
    st.markdown("### 🔍 सेवा शोधा व फिल्टर करा (Find & Filter Services)")
    f_col1, f_col2, f_col3 = st.columns([2, 1.5, 2])

    with f_col1:
        category_options = [
            "सर्व सेवा (All Categories)",
            "पशुवैद्यकीय सेवा (Veterinary Doctors & Emergency)",
            "बियाणे व खते केंद्र (Seeds & Fertilizer Shops)",
            "कृषी अवजारे भाडेतत्त्वावर (Machinery Rental)",
            "पशुखाद्य व वैरण (Fodder & Feed)",
            "कृषी सेवा व माती परीक्षण केंद्र (Service Centres & Labs)"
        ]
        selected_category = st.selectbox("सेवेचा प्रकार निवडा (Category):", options=category_options, index=0)

    with f_col2:
        # Build taluka options including farmer's default
        taluka_options = [
            "सर्व तालुके (All Talukas)",
            "Niphad (निफाड)",
            "Nashik (नाशिक)",
            "Dindori (दिंडोरी)",
            "Chandwad (चांदवड)",
            "Sinnar (सिन्नर)"
        ]
        
        # Default index matches farmer's profile taluka if possible
        default_t_idx = 1 if "niphad" in farmer_taluka_raw.lower() or "निफाड" in farmer_taluka_raw else 0
        selected_taluka = st.selectbox("तालुका निवडा (Taluka):", options=taluka_options, index=default_t_idx)

    with f_col3:
        search_query = st.text_input("कीवर्ड शोधा (Search by Name/Crop/Equipment):", placeholder="उदा. Kulkarni, ट्रॅक्टर, कांदा बियाणे")

    # Filter Application Logic
    filtered_services = []
    for srv in services:
        # 1. Category Filter
        match_cat = True
        if selected_category != "सर्व सेवा (All Categories)":
            if "पशुवैद्यकीय" in selected_category and "veterinary" not in srv.get("category", "").lower():
                match_cat = False
            elif "बियाणे" in selected_category and "seed" not in srv.get("category", "").lower():
                match_cat = False
            elif "अवजारे" in selected_category and "machinery" not in srv.get("category", "").lower() and "equipment" not in srv.get("category", "").lower():
                match_cat = False
            elif "पशुखाद्य" in selected_category and "fodder" not in srv.get("category", "").lower():
                match_cat = False
            elif "माती परीक्षण" in selected_category and "service" not in srv.get("category", "").lower() and "testing" not in srv.get("category", "").lower():
                match_cat = False

        # 2. Taluka Filter
        match_taluka = True
        if selected_taluka != "सर्व तालुके (All Talukas)":
            chosen_t = selected_taluka.split("(")[0].strip().lower()
            srv_t = srv.get("taluka", "").lower()
            if chosen_t not in srv_t:
                match_taluka = False

        # 3. Keyword Search Filter
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
        f"**दाखवत आहे (Showing):** `{len(filtered_services)}` सेवा प्रदाते (तालुका: *{selected_taluka}* | प्रकार: *{selected_category.split('(')[0].strip()}*)"
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
        st.warning("या निकषांनुसार कोणताही सेवा प्रदाता सापडला नाही. कृपया फिल्टर बदला किंवा खालील फॉर्ममधून नवीन प्रदाता जोडा.")

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    # Community Registration Utility
    render_add_service_form()
