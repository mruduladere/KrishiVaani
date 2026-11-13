"""
modules/auth.py - Compact & Balanced Split-Screen Authentication Portal
KrishiVaani (Voice of Agriculture)

Provides:
1. Centered split-screen SaaS login card (max-width: 960px, min-height: 540px).
2. Clean custom SVG agricultural illustration (compact 180px height).
3. Zero-indentation HTML rendering via textwrap.dedent to avoid Markdown code-block traps.
4. Balanced Left showcase panel & Right white form panel.
5. 1-Click Demo Login, Credential Login, and In-Memory Registration.
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


def generate_showcase_svg(is_mr):
    """Generates a compact, clean vector SVG agricultural ecosystem diagram (180px height)."""
    crop_lbl = "पीक" if is_mr else "Crops"
    livestock_lbl = "पशुधन" if is_mr else "Cattle"
    expense_lbl = "खर्च" if is_mr else "Finance"
    service_lbl = "सेवा" if is_mr else "Services"
    hub_lbl = "कृषीवाणी" if is_mr else "KrishiVaani"

    svg = f"""<svg viewBox="0 0 360 180" width="100%" height="180" fill="none" xmlns="http://www.w3.org/2000/svg">
<defs>
<radialGradient id="hubGlow" cx="50%" cy="50%" r="50%">
<stop offset="0%" stop-color="#34D399" stop-opacity="0.3"/>
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
<circle cx="180" cy="90" r="75" fill="url(#hubGlow)"/>
<circle cx="180" cy="90" r="55" stroke="#34D399" stroke-width="1" stroke-dasharray="3 4" opacity="0.4"/>
<line x1="180" y1="90" x2="65" y2="45" stroke="#6EE7B7" stroke-width="1.5" stroke-dasharray="3 3" opacity="0.75"/>
<line x1="180" y1="90" x2="295" y2="45" stroke="#FDE68A" stroke-width="1.5" stroke-dasharray="3 3" opacity="0.75"/>
<line x1="180" y1="90" x2="65" y2="135" stroke="#7DD3FC" stroke-width="1.5" stroke-dasharray="3 3" opacity="0.75"/>
<line x1="180" y1="90" x2="295" y2="135" stroke="#FCA5A5" stroke-width="1.5" stroke-dasharray="3 3" opacity="0.75"/>
<circle cx="180" cy="90" r="32" fill="url(#hubGrad)" stroke="#FBBF24" stroke-width="2"/>
<path d="M180 102V82M180 82C175 78 168 78 166 81C166 87 173 90 180 92M180 82C185 78 192 78 194 81C194 87 187 90 180 92" stroke="#FEF3C7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="180" cy="76" r="2.5" fill="#FBBF24"/>
<text x="180" y="132" text-anchor="middle" fill="#ECFDF5" font-size="10.5" font-weight="700" letter-spacing="0.4">{hub_lbl}</text>
<circle cx="65" cy="45" r="22" fill="url(#nodeGrad)" stroke="#34D399" stroke-width="1.6"/>
<path d="M60 47C60 38 69 36 72 36C72 45 63 54 60 54C60 51 63 47 69 42" stroke="#6EE7B7" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
<text x="65" y="78" text-anchor="middle" fill="#D1FAE5" font-size="9.5" font-weight="600">{crop_lbl}</text>
<circle cx="295" cy="45" r="22" fill="url(#nodeGrad)" stroke="#FBBF24" stroke-width="1.6"/>
<path d="M286 42C286 39 290 37 295 37C300 37 304 39 304 42M289 45H301M291 52C291 54 293 55 295 55C297 55 299 54 299 52" stroke="#FDE68A" stroke-width="1.6" stroke-linecap="round"/>
<text x="295" y="78" text-anchor="middle" fill="#FEF3C7" font-size="9.5" font-weight="600">{livestock_lbl}</text>
<circle cx="65" cy="135" r="22" fill="url(#nodeGrad)" stroke="#38BDF8" stroke-width="1.6"/>
<path d="M60 141L64 135L67 138L71 131M71 131H68M71 131V134" stroke="#BAE6FD" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
<text x="65" y="168" text-anchor="middle" fill="#E0F2FE" font-size="9.5" font-weight="600">{expense_lbl}</text>
<circle cx="295" cy="135" r="22" fill="url(#nodeGrad)" stroke="#F87171" stroke-width="1.6"/>
<path d="M295 127C291 127 289 129 289 133C289 138 295 144 295 144C295 144 301 138 301 133C301 129 299 127 295 127ZM295 135C293.8 135 293 134 293 133C293 132 293.8 131 295 131C296.2 131 297 132 297 133C297 134 296.2 135 295 135Z" stroke="#FECACA" stroke-width="1.5" stroke-linejoin="round"/>
<text x="295" y="168" text-anchor="middle" fill="#FEE2E2" font-size="9.5" font-weight="600">{service_lbl}</text>
</svg>"""
    return textwrap.dedent(svg)


def render_showcase_panel():
    """Renders the clean and minimalist left column showcase card."""
    is_mr = get_lang() == "mr"
    svg_markup = generate_showcase_svg(is_mr)
    badge_text = t("auth_showcase_badge")
    headline_text = t("auth_headline")
    subheadline_text = t("auth_subheadline")

    showcase_card = f"""<div style="background: linear-gradient(145deg, #14532D 0%, #166534 100%);
border-radius: 20px;
padding: 30px 26px;
color: white;
box-shadow: 0 16px 36px -8px rgba(20, 83, 45, 0.35);
height: 540px;
min-height: 540px;
display: flex;
flex-direction: column;
justify-content: space-between;
box-sizing: border-box;">
<div>
<div style="display: inline-block; padding: 5px 12px; background: rgba(255, 255, 255, 0.14); border: 1px solid rgba(255, 255, 255, 0.25); border-radius: 999px; font-size: 12px; font-weight: 600; color: #ECFDF5; letter-spacing: 0.3px;">
{badge_text}
</div>
<div style="margin-top: 20px; text-align: center;">
{svg_markup}
</div>
</div>
<div style="margin-top: auto;">
<h3 style="color: #FFFFFF; font-size: 22px; font-weight: 700; margin: 0 0 8px 0; line-height: 1.3;">
{headline_text}
</h3>
<p style="color: #A7F3D0; font-size: 13.5px; line-height: 1.5; margin: 0; opacity: 0.95;">
{subheadline_text}
</p>
</div>
</div>"""
    st.markdown(textwrap.dedent(showcase_card), unsafe_allow_html=True)


def render_auth():
    """
    Renders the modern split-screen SaaS login and registration interface.
    Enforces balanced 540px height and centered 960px container without raw HTML code blocks.
    """
    # Active auth mode: "login" or "register"
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    # Inject scoped layout CSS for the authentication page
    auth_styles = """<style>
div[data-testid="stAppViewBlockContainer"] {
    max-width: 960px !important;
    margin: 1.5rem auto 2rem auto !important;
    padding-top: 1rem !important;
    padding-bottom: 2rem !important;
}
div[data-testid="stColumn"]:nth-of-type(2) div[data-testid="stVerticalBlockBorderWrapper"] {
    min-height: 540px !important;
    border-radius: 20px !important;
    padding: 24px 26px !important;
    box-sizing: border-box !important;
    box-shadow: 0 16px 36px -8px rgba(0, 0, 0, 0.06) !important;
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
}
</style>"""
    st.markdown(textwrap.dedent(auth_styles), unsafe_allow_html=True)

    # Balanced split-screen columns: 1 : 1
    col_showcase, col_form = st.columns([1, 1], gap="medium")

    # ----------------- LEFT COLUMN: SHOWCASE CARD -----------------
    with col_showcase:
        render_showcase_panel()

    # ----------------- RIGHT COLUMN: CRISP WHITE FORM CARD -----------------
    with col_form:
        with st.container(border=True):
            # Top row: Brand caption and right-aligned Language pill switcher
            top_bar_col1, top_bar_col2 = st.columns([1, 1])
            with top_bar_col1:
                st.caption("🌱 **KrishiVaani** • SIH 2026")
            with top_bar_col2:
                render_language_switcher(key="auth_panel_pill")

            st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)

            # Mode 1: FARMER LOGIN
            if st.session_state.auth_mode == "login":
                st.markdown(f"### {t('auth_welcome_title')}")
                st.caption(t("auth_welcome_subtitle"))

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

                # Subtle divider (zero indentation to prevent Markdown code block)
                divider_html = f"""<div style="display: flex; align-items: center; text-align: center; margin: 10px 0 8px 0;">
<div style="flex-grow: 1; height: 1px; background: #E2E8F0;"></div>
<span style="padding: 0 10px; color: #94A3B8; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;">{t('auth_or_text')}</span>
<div style="flex-grow: 1; height: 1px; background: #E2E8F0;"></div>
</div>"""
                st.markdown(textwrap.dedent(divider_html), unsafe_allow_html=True)

                # ⚡ 1-Click Demo Login Button
                if st.button(t("auth_demo_title"), key="demo_login_split", use_container_width=True):
                    st.session_state.is_authenticated = True
                    st.session_state.farmer_profile = copy.deepcopy(SAMPLE_FARMER)
                    st.session_state.active_nav = "dashboard"
                    st.success(t("login_success"))
                    st.rerun()

                st.caption(t("demo_login_caption"))

                st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

                # Bottom Switcher to Registration
                if st.button(f"👉 {t('auth_switch_to_register')}", key="btn_switch_to_reg", use_container_width=True):
                    st.session_state.auth_mode = "register"
                    st.rerun()

            # Mode 2: NEW FARMER REGISTRATION
            else:
                st.markdown(f"### {t('auth_register_header')}")
                st.caption(t("auth_register_subtitle"))

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

                st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

                # Bottom Switcher back to Login
                if st.button(f"👈 {t('auth_switch_to_login')}", key="btn_switch_to_login", use_container_width=True):
                    st.session_state.auth_mode = "login"
                    st.rerun()

    # Footer note (zero indentation)
    footer_html = f"""<div style="text-align: center; font-size: 11.5px; color: #94A3B8; margin-top: 18px; padding-bottom: 10px;">
{t('footer_text')}
</div>"""
    st.markdown(textwrap.dedent(footer_html), unsafe_allow_html=True)
