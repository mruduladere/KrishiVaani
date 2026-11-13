"""
modules/auth.py - Ultra-Minimal, Aesthetic Split-Screen Authentication Portal
KrishiVaani (Voice of Agriculture)

Design:
- Modern Apple/Notion-style SaaS card (max-width: 920px, height: 500px, zero scrolling).
- Left: Minimal botanical sprouting crop illustration with subtle breathing animation on soft pastel sage canvas.
- Right: Crisp, uncluttered form panel with zero wasted vertical gaps.
- Zero nested boxes, zero Markdown code-block traps.
"""

import copy
import textwrap
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


def generate_minimal_sprout_svg():
    """
    Generates a clean, minimal botanical illustration of a single green seedling
    sprouting from soil with pure CSS stem growth and gentle breathing leaves.
    """
    svg = """<svg viewBox="0 0 240 240" width="210" height="210" fill="none" xmlns="http://www.w3.org/2000/svg">
<defs>
<radialGradient id="sproutGlow" cx="50%" cy="50%" r="50%">
<stop offset="0%" stop-color="#86EFAC" stop-opacity="0.35"/>
<stop offset="100%" stop-color="#86EFAC" stop-opacity="0"/>
</radialGradient>
</defs>
<circle cx="120" cy="115" r="70" fill="url(#sproutGlow)"/>
<ellipse cx="120" cy="202" rx="50" ry="10" fill="#E2DAC9" opacity="0.6"/>
<path d="M80 202 Q120 195 160 202" stroke="#9A8871" stroke-width="2.5" stroke-linecap="round" fill="none"/>
<circle cx="102" cy="201" r="1.5" fill="#8A765E"/>
<circle cx="138" cy="201" r="1.5" fill="#8A765E"/>
<path class="sprout-stem" d="M120 196 Q119 145 120 95" stroke="#2D6A28" stroke-width="3" stroke-linecap="round" fill="none"/>
<g class="sprout-leaf-left">
<path d="M120 115 C95 105 82 85 92 72 C106 70 118 90 120 115Z" fill="#3D7B38"/>
<path d="M120 115 C105 95 96 82 92 72" stroke="#255521" stroke-width="1.2" stroke-linecap="round" fill="none"/>
</g>
<g class="sprout-leaf-right">
<path d="M120 102 C145 92 158 72 148 59 C134 57 122 77 120 102Z" fill="#52A44B"/>
<path d="M120 102 C135 82 144 69 148 59" stroke="#336E2B" stroke-width="1.2" stroke-linecap="round" fill="none"/>
</g>
<path d="M120 95 Q118 80 120 74 Q122 80 120 95Z" fill="#75C76E"/>
</svg>"""
    return textwrap.dedent(svg)


def render_minimal_left_panel():
    """Renders the aesthetic botanical left showcase column with lots of breathing room."""
    svg_markup = generate_minimal_sprout_svg()
    brand_tag = "KRISHIVAANI" if get_lang() == "en" else "कृषीवाणी"
    tagline = t("auth_minimal_tagline")

    html = f"""<div style="background: linear-gradient(180deg, #F4F7F2 0%, #E6EFE3 100%);
border-radius: 18px;
height: 472px;
padding: 28px 24px;
box-sizing: border-box;
display: flex;
flex-direction: column;
justify-content: space-between;
align-items: center;
text-align: center;">
<div style="font-size: 12.5px; font-weight: 700; color: #2D5A27; letter-spacing: 2px; text-transform: uppercase;">
{brand_tag}
</div>
<div style="margin: auto 0; text-align: center;">
{svg_markup}
</div>
<div style="font-size: 13.5px; color: #4D7248; font-weight: 500; letter-spacing: 0.4px;">
"{tagline}"
</div>
</div>"""
    st.markdown(textwrap.dedent(html), unsafe_allow_html=True)


def render_auth():
    """
    Renders the ultra-minimal, modern split-screen SaaS login card.
    Max width 920px, height 500px, zero nested borders, zero scrolling.
    """
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    # Targeted scoped CSS for clean, single-viewport Apple/Notion feel
    auth_css = """<style>
/* Viewport and Block Container fit */
div[data-testid="stAppViewBlockContainer"] {
    max-width: 920px !important;
    padding: 1.5rem 1rem !important;
    margin: 1.5rem auto 1rem auto !important;
}

/* Remove all nested container/form borders */
div[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    border: none !important;
    background: transparent !important;
    box-shadow: none !important;
    padding: 0 !important;
}

/* Unified clean white SaaS card container */
div[data-testid="stHorizontalBlock"] {
    background: #FFFFFF !important;
    border-radius: 24px !important;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.06) !important;
    padding: 14px !important;
    border: 1px solid #EDF2EE !important;
    min-height: 500px !important;
    align-items: center !important;
}

/* Minimalist Sprout Animations */
@keyframes gentleBreath {
    0%, 100% { transform: scale(1) rotate(0deg); }
    50% { transform: scale(1.04) rotate(1deg); }
}
@keyframes stemGrow {
    0% { stroke-dashoffset: 120; }
    100% { stroke-dashoffset: 0; }
}
.sprout-stem {
    stroke-dasharray: 120;
    animation: stemGrow 1.8s ease-out forwards;
}
.sprout-leaf-left {
    transform-origin: 120px 115px;
    animation: gentleBreath 4s ease-in-out infinite;
}
.sprout-leaf-right {
    transform-origin: 120px 102px;
    animation: gentleBreath 4s ease-in-out infinite 0.4s;
}

/* Polished Minimal Inputs */
div[data-testid="stTextInput"] {
    margin-bottom: 2px !important;
}
div[data-testid="stTextInput"] input {
    border-radius: 9px !important;
    border: 1.2px solid #CBD5E1 !important;
    padding: 8px 12px !important;
    font-size: 14px !important;
    background: #FAFAFA !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #1B4D20 !important;
    box-shadow: 0 0 0 3px rgba(27, 77, 32, 0.12) !important;
    background: #FFFFFF !important;
}

/* Forest Green Solid CTA Button */
div[data-testid="stFormSubmitButton"] > button {
    background: #1B4D20 !important;
    color: #FFFFFF !important;
    border-radius: 9px !important;
    border: none !important;
    font-weight: 600 !important;
    padding: 9px !important;
    font-size: 14px !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stFormSubmitButton"] > button:hover {
    background: #143D19 !important;
    transform: translateY(-1px);
}

/* Secondary Button Outline */
button[kind="secondary"] {
    background-color: transparent !important;
    border: 1px solid #E2E8F0 !important;
    color: #1B4D20 !important;
    border-radius: 9px !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    padding: 7px !important;
}
button[kind="secondary"]:hover {
    background-color: #F4F7F2 !important;
    border-color: #CBD5E1 !important;
}
</style>"""
    st.markdown(textwrap.dedent(auth_css), unsafe_allow_html=True)

    # 50/50 Balanced Split-Screen Columns
    col_visual, col_form = st.columns([1, 1], gap="medium")

    # ----------------- LEFT COLUMN: MINIMAL SAGE SPROUT -----------------
    with col_visual:
        render_minimal_left_panel()

    # ----------------- RIGHT COLUMN: CLEAN FORM PANEL -----------------
    with col_form:
        with st.container():
            # Top Header Row: Title & Language Toggle side-by-side (zero wasted height)
            top_l, top_r = st.columns([1.6, 1])
            with top_l:
                if st.session_state.auth_mode == "login":
                    st.markdown(f"<h3 style='margin: 0; font-size: 22px; font-weight: 700; color: #0F172A; line-height: 1.2;'>{t('auth_minimal_welcome')}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin: 2px 0 8px 0; font-size: 12.5px; color: #64748B;'>{t('auth_minimal_sub')}</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<h3 style='margin: 0; font-size: 20px; font-weight: 700; color: #0F172A; line-height: 1.2;'>{t('auth_register_header')}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin: 2px 0 8px 0; font-size: 12px; color: #64748B;'>{t('auth_register_subtitle')}</p>", unsafe_allow_html=True)
            with top_r:
                render_language_switcher(key="auth_minimal_lang")

            # MODE 1: FARMER LOGIN
            if st.session_state.auth_mode == "login":
                with st.form("minimal_login_form"):
                    phone_input = st.text_input(
                        t("phone_label"),
                        value="98220 12345",
                        placeholder="98220 12345"
                    )
                    pin_input = st.text_input(
                        t("pin_label"),
                        type="password",
                        placeholder="1234"
                    )

                    st.markdown("<div style='height: 2px;'></div>", unsafe_allow_html=True)
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

                # Subtle 1-Click Demo Login
                st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
                if st.button(t("auth_demo_title"), key="demo_btn_minimal", use_container_width=True):
                    st.session_state.is_authenticated = True
                    st.session_state.farmer_profile = copy.deepcopy(SAMPLE_FARMER)
                    st.session_state.active_nav = "dashboard"
                    st.success(t("login_success"))
                    st.rerun()

                st.markdown("<div style='height: 2px;'></div>", unsafe_allow_html=True)

                # Switch to Register
                if st.button(t("auth_minimal_new_reg"), key="reg_toggle_minimal", use_container_width=True):
                    st.session_state.auth_mode = "register"
                    st.rerun()

            # MODE 2: NEW FARMER REGISTRATION
            else:
                with st.form("minimal_registration_form"):
                    reg_name = st.text_input(t("reg_name_label"), placeholder=t("reg_name_placeholder"))
                    
                    r_col1, r_col2 = st.columns(2)
                    with r_col1:
                        reg_phone = st.text_input(t("reg_phone_label"), placeholder="10-digit number")
                        reg_village = st.text_input(t("reg_village_label"), placeholder="Village")
                        soil_choices = [
                            "Medium Black (काळी मध्यम)",
                            "Deep Black (काळी कापशी)",
                            "Red Loamy (तांबडी पोयटा)",
                            "Sandy Loam (वालुकामय)"
                        ]
                        reg_soil = st.selectbox(t("reg_soil_label"), options=soil_choices)
                    with r_col2:
                        reg_pin = st.text_input(t("reg_pin_label"), type="password", placeholder="4-digit PIN")
                        reg_taluka = st.text_input(t("reg_taluka_label"), value="Niphad")
                        reg_land = st.number_input(t("reg_land_label"), min_value=0.1, max_value=500.0, value=3.5, step=0.5)

                    irr_choices = [
                        "Drip Irrigation (ठिबक सिंचन)",
                        "Well & Sprinkler (तुषार सिंचन)",
                        "Canal Flood (कालवा पाटपाणी)",
                        "Borewell (बोअरवेल)"
                    ]
                    reg_irr = st.selectbox(t("reg_irrigation_label"), options=irr_choices)
                    reg_crops = st.text_input(t("reg_crops_label"), placeholder="Grapes, Onion, Soybean")

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
                                "district": "Nashik",
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

                st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
                if st.button(t("auth_minimal_existing"), key="btn_switch_to_login", use_container_width=True):
                    st.session_state.auth_mode = "login"
                    st.rerun()
