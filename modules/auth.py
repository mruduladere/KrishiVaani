"""
modules/auth.py - Modern Split-Screen Authentication & Registration Portal
KrishiVaani (Voice of Agriculture)

Provides:
1. Centered split-screen SaaS login card (Left showcase visual panel + Right clean form panel).
2. Clean custom SVG agricultural illustration showing connected platform modules.
3. 1-Click Demo Login (Ramesh Patil) for Hackathon evaluators.
4. Credential-based Farmer Login & In-Memory New Farmer Registration.
5. Neat language toggle (English | मराठी) in the top-right corner of the form card.
"""

import copy
import streamlit as st
from sample_data import SAMPLE_FARMER
from translations import t, get_lang, render_language_switcher


def normalize_phone(phone_str):
    """Normalizes phone string by removing whitespace, hyphens, and standard country code."""
    cleaned = phone_str.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if cleaned.startswith("+91"):
        cleaned = cleaned[3:]
    elif cleaned.startswith("0"):
        cleaned = cleaned[1:]
    return cleaned


def find_farmer_by_credentials(phone_input, pin_input):
    """
    Looks up a farmer by normalized phone and checks their 4-digit PIN in session state.
    Returns farmer profile dictionary if matched, else None.
    """
    registered = st.session_state.get("registered_farmers", {})
    norm_input = normalize_phone(phone_input)

    for reg_phone, profile in registered.items():
        norm_reg = normalize_phone(reg_phone)
        if norm_input == norm_reg or norm_input in norm_reg or norm_reg in norm_input:
            expected_pin = str(profile.get("pin", "1234")).strip()
            if str(pin_input).strip() == expected_pin:
                return profile
    return None


def generate_showcase_svg(is_mr):
    """Generates a modern, clean vector SVG agricultural ecosystem diagram."""
    crop_lbl = "पीक सल्ला" if is_mr else "Crop Advisory"
    livestock_lbl = "पशुधन काळजी" if is_mr else "Livestock Care"
    expense_lbl = "खर्च विश्लेषण" if is_mr else "Expense Analytics"
    service_lbl = "स्थानिक सेवा" if is_mr else "Local Services"
    hub_lbl = "कृषीवाणी केंद्र" if is_mr else "KrishiVaani Hub"

    return f"""
    <svg viewBox="0 0 440 260" width="100%" height="230" fill="none" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0 4px 12px rgba(0,0,0,0.15));">
      <defs>
        <radialGradient id="hubGlow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#34D399" stop-opacity="0.35"/>
          <stop offset="100%" stop-color="#34D399" stop-opacity="0"/>
        </radialGradient>
        <linearGradient id="hubGrad" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#059669"/>
          <stop offset="100%" stop-color="#047857"/>
        </linearGradient>
        <linearGradient id="nodeGrad" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#064E3B"/>
          <stop offset="100%" stop-color="#022C22"/>
        </linearGradient>
      </defs>

      <!-- Glow Rings -->
      <circle cx="220" cy="130" r="105" fill="url(#hubGlow)" />
      <circle cx="220" cy="130" r="75" stroke="#34D399" stroke-width="1.2" stroke-dasharray="4 6" opacity="0.45" />

      <!-- Interconnecting Circuit Lines -->
      <line x1="220" y1="130" x2="85" y2="60" stroke="#6EE7B7" stroke-width="1.8" stroke-dasharray="4 4" opacity="0.8"/>
      <line x1="220" y1="130" x2="355" y2="60" stroke="#FDE68A" stroke-width="1.8" stroke-dasharray="4 4" opacity="0.8"/>
      <line x1="220" y1="130" x2="85" y2="200" stroke="#7DD3FC" stroke-width="1.8" stroke-dasharray="4 4" opacity="0.8"/>
      <line x1="220" y1="130" x2="355" y2="200" stroke="#FCA5A5" stroke-width="1.8" stroke-dasharray="4 4" opacity="0.8"/>

      <!-- Center Hub Node -->
      <circle cx="220" cy="130" r="40" fill="url(#hubGrad)" stroke="#FBBF24" stroke-width="2.5" />
      <path d="M220 148V120M220 120C214 114 206 114 204 118C204 126 212 130 220 132M220 120C226 114 234 114 236 118C236 126 228 130 220 132" stroke="#FEF3C7" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="220" cy="112" r="3" fill="#FBBF24"/>
      <text x="220" y="185" text-anchor="middle" fill="#ECFDF5" font-size="11" font-weight="700" letter-spacing="0.5">{hub_lbl}</text>

      <!-- Satellite Node 1: Crop Advisory -->
      <circle cx="85" cy="60" r="28" fill="url(#nodeGrad)" stroke="#34D399" stroke-width="2"/>
      <path d="M78 63C78 51 90 49 94 49C94 61 82 73 78 73C78 69 82 63 90 57" stroke="#6EE7B7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      <text x="85" y="104" text-anchor="middle" fill="#D1FAE5" font-size="11" font-weight="600">{crop_lbl}</text>

      <!-- Satellite Node 2: Livestock Care -->
      <circle cx="355" cy="60" r="28" fill="url(#nodeGrad)" stroke="#FBBF24" stroke-width="2"/>
      <path d="M343 55C343 51 349 49 355 49C361 49 367 51 367 55M347 59H363M350 69C350 71 352 73 355 73C358 73 360 71 360 69" stroke="#FDE68A" stroke-width="2" stroke-linecap="round"/>
      <text x="355" y="104" text-anchor="middle" fill="#FEF3C7" font-size="11" font-weight="600">{livestock_lbl}</text>

      <!-- Satellite Node 3: Expense Analytics -->
      <circle cx="85" cy="200" r="28" fill="url(#nodeGrad)" stroke="#38BDF8" stroke-width="2"/>
      <path d="M79 207L84 200L88 204L93 195M93 195H89M93 195V199" stroke="#BAE6FD" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      <text x="85" y="244" text-anchor="middle" fill="#E0F2FE" font-size="11" font-weight="600">{expense_lbl}</text>

      <!-- Satellite Node 4: Nearby Services -->
      <circle cx="355" cy="200" r="28" fill="url(#nodeGrad)" stroke="#F87171" stroke-width="2"/>
      <path d="M355 190C350 190 347 193 347 198C347 204 355 212 355 212C355 212 363 204 363 198C363 193 360 190 355 190ZM355 200C353.5 200 352.5 198.8 352.5 197.5C352.5 196.2 353.5 195 355 195C356.5 195 357.5 196.2 357.5 197.5C357.5 198.8 356.5 200 355 200Z" stroke="#FECACA" stroke-width="1.8" stroke-linejoin="round"/>
      <text x="355" y="244" text-anchor="middle" fill="#FEE2E2" font-size="11" font-weight="600">{service_lbl}</text>
    </svg>
    """


def render_showcase_panel():
    """Renders the left column showcase card with gradient styling and vector diagram."""
    is_mr = get_lang() == "mr"
    svg_markup = generate_showcase_svg(is_mr)
    
    badge_text = t("auth_showcase_badge")
    tagline_text = t("auth_showcase_tagline")
    desc_text = t("auth_showcase_desc")

    pills_html = f"""
    <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px;">
        <span style="background: rgba(255, 255, 255, 0.12); border: 1px solid rgba(255, 255, 255, 0.18); border-radius: 999px; padding: 5px 12px; font-size: 12px; color: #ECFDF5; font-weight: 500;">
            {t('auth_pill_crop')}
        </span>
        <span style="background: rgba(255, 255, 255, 0.12); border: 1px solid rgba(255, 255, 255, 0.18); border-radius: 999px; padding: 5px 12px; font-size: 12px; color: #ECFDF5; font-weight: 500;">
            {t('auth_pill_livestock')}
        </span>
        <span style="background: rgba(255, 255, 255, 0.12); border: 1px solid rgba(255, 255, 255, 0.18); border-radius: 999px; padding: 5px 12px; font-size: 12px; color: #ECFDF5; font-weight: 500;">
            {t('auth_pill_expenses')}
        </span>
        <span style="background: rgba(255, 255, 255, 0.12); border: 1px solid rgba(255, 255, 255, 0.18); border-radius: 999px; padding: 5px 12px; font-size: 12px; color: #ECFDF5; font-weight: 500;">
            {t('auth_pill_services')}
        </span>
    </div>
    """

    showcase_card = f"""
    <div style="
        background: linear-gradient(150deg, #14532D 0%, #166534 50%, #064E3B 100%);
        border-radius: 20px;
        padding: 38px 34px;
        color: white;
        box-shadow: 0 20px 45px -12px rgba(20, 83, 45, 0.45);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 560px;
        box-sizing: border-box;
    ">
        <div>
            <!-- Top Badge -->
            <div style="display: inline-flex; align-items: center; padding: 6px 14px; background: rgba(255, 255, 255, 0.12); border: 1px solid rgba(255, 255, 255, 0.22); border-radius: 999px; font-size: 13px; font-weight: 600; color: #ECFDF5; margin-bottom: 24px;">
                {badge_text}
            </div>

            <!-- Custom Vector Illustration -->
            <div style="margin: 10px 0 20px 0; text-align: center;">
                {svg_markup}
            </div>
        </div>

        <div>
            <!-- Bottom Tagline & Description -->
            <h3 style="color: #FFFFFF; font-size: 21px; font-weight: 700; line-height: 1.35; margin: 0 0 10px 0;">
                "{tagline_text}"
            </h3>
            <p style="color: #A7F3D0; font-size: 13.5px; line-height: 1.55; margin: 0; opacity: 0.95;">
                {desc_text}
            </p>
            {pills_html}
        </div>
    </div>
    """
    st.markdown(showcase_card, unsafe_allow_html=True)


def render_auth():
    """
    Renders the modern split-screen SaaS login and registration interface.
    Left: Visual showcase card.
    Right: Clean white form card with top-right pill language toggle.
    """
    # Active auth mode: "login" or "register"
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    # Container-level spacing
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # Centered split-screen 2-column layout (1.15 : 1)
    col_showcase, col_form = st.columns([1.15, 1], gap="large")

    # ----------------- LEFT COLUMN: SHOWCASE CARD -----------------
    with col_showcase:
        render_showcase_panel()

    # ----------------- RIGHT COLUMN: CLEAN FORM CARD -----------------
    with col_form:
        # Wrap form inside clean white card container
        with st.container(border=True):
            # Top row: Brand caption and right-aligned Language pill switcher
            top_bar_col1, top_bar_col2 = st.columns([1, 1])
            with top_bar_col1:
                st.caption(f"🌱 **KrishiVaani** • SIH 2026")
            with top_bar_col2:
                render_language_switcher(key="auth_panel_pill")

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

            # Mode 1: FARMER LOGIN
            if st.session_state.auth_mode == "login":
                st.markdown(f"## {t('auth_welcome_title')}")
                st.caption(t("auth_welcome_subtitle"))

                st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

                with st.form("split_login_form"):
                    phone_input = st.text_input(
                        t("phone_label"),
                        value="98220 12345",
                        placeholder=t("phone_placeholder")
                    )
                    pin_input = st.text_input(
                        t("pin_label"),
                        type="password",
                        placeholder=t("pin_placeholder")
                    )

                    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
                    submit_login = st.form_submit_button(t("login_button"), use_container_width=True)

                    if submit_login:
                        matched = find_farmer_by_credentials(phone_input, pin_input)
                        if matched:
                            st.session_state.is_authenticated = True
                            st.session_state.farmer_profile = copy.deepcopy(matched)
                            st.session_state.active_nav = "dashboard"
                            st.success(t("login_success"))
                            st.rerun()
                        else:
                            st.error(t("login_failed"))

                # Subtle divider
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: center; text-align: center; margin: 18px 0 14px 0;">
                        <div style="flex-grow: 1; height: 1px; background: #E2E8F0;"></div>
                        <span style="padding: 0 12px; color: #94A3B8; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">
                            {t('auth_or_text')}
                        </span>
                        <div style="flex-grow: 1; height: 1px; background: #E2E8F0;"></div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # ⚡ 1-Click Demo Login Button
                if st.button(t("auth_demo_title"), key="demo_login_split", use_container_width=True):
                    st.session_state.is_authenticated = True
                    st.session_state.farmer_profile = copy.deepcopy(SAMPLE_FARMER)
                    st.session_state.active_nav = "dashboard"
                    st.success(t("login_success"))
                    st.rerun()

                st.caption(t("demo_login_caption"))

                st.markdown("<hr style='margin: 20px 0 14px 0; border: none; border-top: 1px solid #F1F5F9;'>", unsafe_allow_html=True)

                # Bottom Switcher to Registration
                if st.button(f"👉 {t('auth_switch_to_register')}", key="btn_switch_to_reg", use_container_width=True):
                    st.session_state.auth_mode = "register"
                    st.rerun()

            # Mode 2: NEW FARMER REGISTRATION
            else:
                st.markdown(f"## {t('auth_register_header')}")
                st.caption(t("auth_register_subtitle"))

                st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

                with st.form("split_registration_form"):
                    reg_name = st.text_input(t("reg_name_label"), placeholder=t("reg_name_placeholder"))
                    
                    p_col1, p_col2 = st.columns(2)
                    with p_col1:
                        reg_phone = st.text_input(t("reg_phone_label"), placeholder=t("reg_phone_placeholder"))
                    with p_col2:
                        reg_pin = st.text_input(t("reg_pin_label"), type="password", placeholder=t("reg_pin_placeholder"))

                    l_col1, l_col2 = st.columns(2)
                    with l_col1:
                        reg_village = st.text_input(t("reg_village_label"), placeholder=t("reg_village_placeholder"))
                    with l_col2:
                        reg_taluka = st.text_input(t("reg_taluka_label"), placeholder=t("reg_taluka_placeholder"))

                    reg_district = st.text_input(t("reg_district_label"), value="Nashik")
                    reg_land = st.number_input(t("reg_land_label"), min_value=0.1, max_value=500.0, value=3.5, step=0.5)

                    soil_choices = [
                        "Medium Black Soil (काळी मध्यम जमीन)",
                        "Deep Black Cotton Soil (भारी काळी कापशी जमीन)",
                        "Red Loamy Soil (तांबडी पोयट्याची जमीन)",
                        "Sandy Loam Soil (हलकी वालुकामय जमीन)"
                    ]
                    reg_soil = st.selectbox(t("reg_soil_label"), options=soil_choices)

                    irr_choices = [
                        "Drip Irrigation & Farm Pond (ठिबक सिंचन व शेततळे)",
                        "Well & Sprinkler System (विहीर व तुषार सिंचन)",
                        "Canal Flood Irrigation (कालवा पाटपाणी)",
                        "Borewell & Direct Pipeline (बोअरवेल व पाईपलाईन)"
                    ]
                    reg_irr = st.selectbox(t("reg_irrigation_label"), options=irr_choices)
                    reg_crops = st.text_input(t("reg_crops_label"), placeholder=t("reg_crops_placeholder"))

                    submit_reg = st.form_submit_button(t("register_button"), use_container_width=True)

                    if submit_reg:
                        clean_name = reg_name.strip()
                        clean_phone = normalize_phone(reg_phone)
                        clean_pin = reg_pin.strip()

                        if len(clean_name) >= 2 and len(clean_phone) >= 10 and len(clean_pin) >= 4:
                            parsed_crops = [c.strip() for c in reg_crops.split(",") if c.strip()]
                            if not parsed_crops:
                                parsed_crops = ["Onion (कांदा)", "Soybean (सोयाबीन)"]

                            new_profile = {
                                "name": clean_name,
                                "phone": f"+91 {clean_phone}",
                                "pin": clean_pin,
                                "email": f"{clean_name.lower().replace(' ', '.')}@krishivaani.in",
                                "village": reg_village.strip() or "Pimpalgaon",
                                "taluka": reg_taluka.strip() or "Niphad",
                                "district": reg_district.strip() or "Nashik",
                                "state": "Maharashtra",
                                "pincode": "422001",
                                "land_size_acres": float(reg_land),
                                "soil_type": reg_soil,
                                "irrigation_type": reg_irr,
                                "primary_language": "Marathi & English",
                                "crops_grown": parsed_crops,
                                "livestock_summary": {
                                    "gir_cows": 1,
                                    "murrah_buffaloes": 0,
                                    "goats": 2,
                                    "total_animals": 3,
                                    "daily_milk_litres": 9.0
                                }
                            }

                            st.session_state.registered_farmers[clean_phone] = new_profile
                            st.session_state.registered_farmers[f"+91 {clean_phone}"] = new_profile

                            st.session_state.farmer_profile = new_profile
                            st.session_state.is_authenticated = True
                            st.session_state.active_nav = "dashboard"
                            st.success(t("reg_success"))
                            st.rerun()
                        else:
                            st.warning(t("reg_validation_error"))

                st.markdown("<hr style='margin: 18px 0 12px 0; border: none; border-top: 1px solid #F1F5F9;'>", unsafe_allow_html=True)

                # Bottom Switcher back to Login
                if st.button(f"👈 {t('auth_switch_to_login')}", key="btn_switch_to_login", use_container_width=True):
                    st.session_state.auth_mode = "login"
                    st.rerun()

    # Footer note
    st.markdown(
        f"""
        <div style="text-align: center; font-size: 12px; color: #94A3B8; margin-top: 25px; padding-bottom: 20px;">
            {t('footer_text')}
        </div>
        """,
        unsafe_allow_html=True
    )
