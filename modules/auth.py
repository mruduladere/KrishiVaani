"""
modules/auth.py - High-End Modern SaaS Split-Screen Authentication Portal
KrishiVaani (Voice of Agriculture)

Provides:
1. Zero nested boxes, single-viewport fit (100vh without vertical scrolling).
2. Left: Rich animated crop & sunrise landscape with pure CSS swaying crops and glassmorphic card.
3. Right: Seamless minimalist white form panel without nested borders.
4. 1-Click Demo Login, Mobile + PIN Login, and In-Memory Registration.
5. Zero-indentation HTML ensuring crisp DOM rendering without Markdown code-block traps.
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


def generate_animated_landscape_svg():
    """
    Generates a lush SVG agricultural landscape featuring a golden sunrise,
    rolling emerald hills, crop furrows, and gently swaying foreground crops.
    """
    svg = """<svg viewBox="0 0 460 520" width="100%" height="520" preserveAspectRatio="xMidYMid slice" fill="none" xmlns="http://www.w3.org/2000/svg">
<defs>
<linearGradient id="skyGrad" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="#FEF3C7"/>
<stop offset="38%" stop-color="#FDE68A"/>
<stop offset="70%" stop-color="#D1FAE5"/>
<stop offset="100%" stop-color="#A7F3D0"/>
</linearGradient>
<radialGradient id="sunGlow" cx="50%" cy="50%" r="50%">
<stop offset="0%" stop-color="#F59E0B" stop-opacity="0.9"/>
<stop offset="35%" stop-color="#FBBF24" stop-opacity="0.6"/>
<stop offset="70%" stop-color="#FDE68A" stop-opacity="0.2"/>
<stop offset="100%" stop-color="#FEF3C7" stop-opacity="0"/>
</radialGradient>
<linearGradient id="distantHillGrad" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="#86EFAC"/>
<stop offset="100%" stop-color="#4ADE80"/>
</linearGradient>
<linearGradient id="midHillGrad" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="#22C55E"/>
<stop offset="100%" stop-color="#16A34A"/>
</linearGradient>
<linearGradient id="foreHillGrad" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="#16A34A"/>
<stop offset="100%" stop-color="#14532D"/>
</linearGradient>
<linearGradient id="wheatGrad" x1="0" y1="0" x2="1" y2="1">
<stop offset="0%" stop-color="#FEF08A"/>
<stop offset="50%" stop-color="#F59E0B"/>
<stop offset="100%" stop-color="#D97706"/>
</linearGradient>
</defs>
<rect width="460" height="520" fill="url(#skyGrad)"/>
<g class="sun-pulse">
<circle cx="280" cy="120" r="110" fill="url(#sunGlow)"/>
<circle cx="280" cy="120" r="40" fill="#F59E0B"/>
<circle cx="280" cy="120" r="30" fill="#FEF08A"/>
</g>
<path d="M120 75 Q125 70 130 75 Q135 70 140 75" stroke="#065F46" stroke-width="1.6" fill="none" opacity="0.6"/>
<path d="M148 65 Q152 61 156 65 Q160 61 164 65" stroke="#065F46" stroke-width="1.3" fill="none" opacity="0.5"/>
<path d="M100 88 Q103 84 107 88 Q111 84 115 88" stroke="#065F46" stroke-width="1.2" fill="none" opacity="0.45"/>
<path d="M0 240 Q110 180 230 215 T460 210 V520 H0 Z" fill="url(#distantHillGrad)" opacity="0.75"/>
<path d="M0 270 Q140 230 280 265 T460 250 V520 H0 Z" fill="url(#midHillGrad)"/>
<path d="M20 285 Q150 250 280 280 T450 268" stroke="#15803D" stroke-width="1.4" stroke-dasharray="6 4" fill="none" opacity="0.5"/>
<path d="M0 310 Q140 270 270 300 T460 290" stroke="#15803D" stroke-width="1.4" stroke-dasharray="6 4" fill="none" opacity="0.5"/>
<path d="M0 340 Q130 300 260 335 T460 310 V520 H0 Z" fill="url(#foreHillGrad)"/>
<path d="M-10 380 Q140 335 280 370 T470 345" stroke="#14532D" stroke-width="1.8" stroke-dasharray="8 5" fill="none" opacity="0.45"/>
<path d="M-10 420 Q160 370 300 410 T470 385" stroke="#0F3E22" stroke-width="2" stroke-dasharray="10 6" fill="none" opacity="0.4"/>
<g class="crop-sway-1">
<path d="M70 480 Q68 400 62 330" stroke="#D97706" stroke-width="3" stroke-linecap="round" fill="none"/>
<path d="M62 330 Q58 310 60 295 Q64 310 62 330Z" fill="url(#wheatGrad)"/>
<ellipse cx="61" cy="300" rx="4.5" ry="7" fill="url(#wheatGrad)"/>
<ellipse cx="58" cy="312" rx="4.5" ry="7" fill="url(#wheatGrad)"/>
<ellipse cx="64" cy="312" rx="4.5" ry="7" fill="url(#wheatGrad)"/>
<ellipse cx="59" cy="324" rx="4" ry="6.5" fill="url(#wheatGrad)"/>
<ellipse cx="64" cy="324" rx="4" ry="6.5" fill="url(#wheatGrad)"/>
<line x1="60" y1="295" x2="54" y2="275" stroke="#F59E0B" stroke-width="1.2"/>
<line x1="60" y1="295" x2="63" y2="272" stroke="#F59E0B" stroke-width="1.2"/>
<line x1="60" y1="295" x2="70" y2="278" stroke="#F59E0B" stroke-width="1.2"/>
</g>
<g class="crop-sway-2">
<path d="M125 490 Q130 410 135 340" stroke="#D97706" stroke-width="3" stroke-linecap="round" fill="none"/>
<ellipse cx="135" cy="310" rx="4.5" ry="7.5" fill="url(#wheatGrad)"/>
<ellipse cx="131" cy="322" rx="4.5" ry="7" fill="url(#wheatGrad)"/>
<ellipse cx="139" cy="322" rx="4.5" ry="7" fill="url(#wheatGrad)"/>
<ellipse cx="132" cy="334" rx="4" ry="6.5" fill="url(#wheatGrad)"/>
<ellipse cx="138" cy="334" rx="4" ry="6.5" fill="url(#wheatGrad)"/>
<line x1="135" y1="305" x2="132" y2="285" stroke="#F59E0B" stroke-width="1.2"/>
<line x1="135" y1="305" x2="142" y2="288" stroke="#F59E0B" stroke-width="1.2"/>
</g>
<g class="crop-sway-3">
<path d="M210 500 Q208 430 205 365" stroke="#16A34A" stroke-width="3.5" stroke-linecap="round" fill="none"/>
<path d="M205 420 Q170 410 160 425 Q180 440 205 425Z" fill="#22C55E"/>
<path d="M205 405 Q240 395 250 410 Q230 425 205 410Z" fill="#4ADE80"/>
<path d="M205 380 Q175 365 170 380 Q190 395 205 380Z" fill="#16A34A"/>
<path d="M205 365 Q235 350 240 365 Q220 380 205 368Z" fill="#22C55E"/>
</g>
<g class="crop-sway-1">
<path d="M310 490 Q315 415 320 345" stroke="#D97706" stroke-width="3" stroke-linecap="round" fill="none"/>
<ellipse cx="320" cy="315" rx="4.5" ry="7.5" fill="url(#wheatGrad)"/>
<ellipse cx="316" cy="327" rx="4.5" ry="7" fill="url(#wheatGrad)"/>
<ellipse cx="324" cy="327" rx="4.5" ry="7" fill="url(#wheatGrad)"/>
<ellipse cx="317" cy="339" rx="4" ry="6.5" fill="url(#wheatGrad)"/>
<ellipse cx="323" cy="339" rx="4" ry="6.5" fill="url(#wheatGrad)"/>
<line x1="320" y1="310" x2="315" y2="290" stroke="#F59E0B" stroke-width="1.2"/>
<line x1="320" y1="310" x2="326" y2="292" stroke="#F59E0B" stroke-width="1.2"/>
</g>
<g class="crop-sway-2">
<path d="M380 500 Q375 425 372 360" stroke="#D97706" stroke-width="3" stroke-linecap="round" fill="none"/>
<ellipse cx="372" cy="330" rx="4.5" ry="7" fill="url(#wheatGrad)"/>
<ellipse cx="368" cy="342" rx="4" ry="6.5" fill="url(#wheatGrad)"/>
<ellipse cx="376" cy="342" rx="4" ry="6.5" fill="url(#wheatGrad)"/>
<line x1="372" y1="325" x2="368" y2="305" stroke="#F59E0B" stroke-width="1.2"/>
<line x1="372" y1="325" x2="378" y2="308" stroke="#F59E0B" stroke-width="1.2"/>
</g>
</svg>"""
    return textwrap.dedent(svg)


def render_landscape_panel():
    """
    Renders the left visual column with animated sunrise, swaying crops,
    and a clean floating glassmorphic card at the bottom.
    """
    svg_markup = generate_animated_landscape_svg()
    badge_text = t("auth_showcase_badge")
    headline_text = t("auth_landscape_headline")
    subtitle_text = t("auth_landscape_sub")

    html = f"""<div style="border-radius: 18px; overflow: hidden; height: 520px; position: relative; width: 100%; box-shadow: 0 10px 30px rgba(20, 83, 45, 0.2);">
{svg_markup}
<div style="position: absolute; bottom: 16px; left: 16px; right: 16px; backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); background: rgba(20, 83, 45, 0.85); border: 1px solid rgba(255, 255, 255, 0.25); color: white; border-radius: 14px; padding: 16px 18px; box-shadow: 0 10px 25px rgba(0,0,0,0.25);">
<div style="display: inline-block; padding: 3px 10px; background: rgba(255, 255, 255, 0.16); border: 1px solid rgba(255, 255, 255, 0.25); border-radius: 999px; font-size: 11px; font-weight: 600; color: #ECFDF5; letter-spacing: 0.3px; margin-bottom: 6px;">
{badge_text}
</div>
<h3 style="color: #FFFFFF; font-size: 18px; font-weight: 700; margin: 0 0 4px 0; line-height: 1.25;">
{headline_text}
</h3>
<p style="color: #D1FAE5; font-size: 12.5px; line-height: 1.4; margin: 0; opacity: 0.95;">
{subtitle_text}
</p>
</div>
</div>"""
    st.markdown(textwrap.dedent(html), unsafe_allow_html=True)


def render_auth():
    """
    Renders the modern split-screen SaaS login portal.
    Zero nested boxes, single-viewport fit (100vh), zero Markdown code-block traps.
    """
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    # Targeted CSS to flatten default forms, center the unified card, and animate crops
    auth_css = """<style>
/* Viewport and Block Container fit */
div[data-testid="stAppViewBlockContainer"] {
    max-width: 1040px !important;
    padding: 1.5rem 2rem !important;
    margin: 0 auto !important;
}

/* Remove/flatten Streamlit default form borders and gray boxes */
div[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
}

/* Remove any container border wrappers */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border: none !important;
    background: transparent !important;
    box-shadow: none !important;
    padding: 0 !important;
}

/* Unified SaaS Card wrapper for columns */
div[data-testid="stHorizontalBlock"] {
    background: #FFFFFF !important;
    border-radius: 24px !important;
    box-shadow: 0 20px 50px rgba(15, 23, 42, 0.08) !important;
    padding: 16px !important;
    border: 1px solid #F1F5F9 !important;
    align-items: stretch !important;
}

/* Pure CSS Keyframes for Landscape Animation */
@keyframes pulseGlow {
    0%, 100% { transform: scale(1); opacity: 0.85; }
    50% { transform: scale(1.06); opacity: 1; }
}
@keyframes swayLeft {
    0%, 100% { transform: rotate(-2deg); }
    50% { transform: rotate(2.5deg); }
}
@keyframes swayRight {
    0%, 100% { transform: rotate(2deg); }
    50% { transform: rotate(-2.5deg); }
}
.sun-pulse {
    transform-origin: 280px 120px;
    animation: pulseGlow 4s ease-in-out infinite;
}
.crop-sway-1 {
    transform-origin: bottom center;
    animation: swayLeft 4.5s ease-in-out infinite;
}
.crop-sway-2 {
    transform-origin: bottom center;
    animation: swayRight 5.2s ease-in-out infinite 0.5s;
}
.crop-sway-3 {
    transform-origin: bottom center;
    animation: swayLeft 4.8s ease-in-out infinite 1s;
}

/* Tighten form inputs for single-screen fit */
div[data-testid="stTextInput"] {
    margin-bottom: 2px !important;
}
div[data-testid="stTextInput"] input {
    padding: 8px 12px !important;
    font-size: 14px !important;
}
</style>"""
    st.markdown(textwrap.dedent(auth_css), unsafe_allow_html=True)

    # Main split-screen columns: 1.15 : 1 (sitting inside the unified white card)
    col_landscape, col_form = st.columns([1.15, 1], gap="large")

    # ----------------- LEFT COLUMN: ANIMATED CROP LANDSCAPE -----------------
    with col_landscape:
        render_landscape_panel()

    # ----------------- RIGHT COLUMN: SEAMLESS MINIMALIST FORM -----------------
    with col_form:
        # Container without any border=True
        with st.container():
            # Top Bar: Brand text & Compact Language Switcher
            bar_l, bar_r = st.columns([1, 1])
            with bar_l:
                st.markdown("<div style='font-size: 15px; font-weight: 700; color: #15803D; padding-top: 4px;'>🌱 <b>KrishiVaani</b></div>", unsafe_allow_html=True)
            with bar_r:
                render_language_switcher(key="auth_top_pill")

            st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)

            # MODE 1: FARMER LOGIN
            if st.session_state.auth_mode == "login":
                st.markdown(f"<h3 style='margin: 4px 0 2px 0; font-size: 21px; font-weight: 800; color: #0F172A;'>{t('auth_welcome_title')}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='margin: 0 0 10px 0; font-size: 12.5px; color: #64748B;'>{t('auth_welcome_subtitle')}</p>", unsafe_allow_html=True)

                # Form without any border=True
                with st.form("clean_login_form"):
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
                divider_html = f"""<div style="display: flex; align-items: center; text-align: center; margin: 8px 0 6px 0;">
<div style="flex-grow: 1; height: 1px; background: #E2E8F0;"></div>
<span style="padding: 0 10px; color: #94A3B8; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;">{t('auth_or_text')}</span>
<div style="flex-grow: 1; height: 1px; background: #E2E8F0;"></div>
</div>"""
                st.markdown(textwrap.dedent(divider_html), unsafe_allow_html=True)

                # ⚡ 1-Click Demo Login
                if st.button(t("auth_demo_title"), key="demo_login_split", use_container_width=True):
                    st.session_state.is_authenticated = True
                    st.session_state.farmer_profile = copy.deepcopy(SAMPLE_FARMER)
                    st.session_state.active_nav = "dashboard"
                    st.success(t("login_success"))
                    st.rerun()

                st.caption(t("demo_login_caption"))

                st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)

                # Bottom Switcher
                if st.button(f"👉 {t('auth_switch_to_register')}", key="btn_switch_to_reg", use_container_width=True):
                    st.session_state.auth_mode = "register"
                    st.rerun()

            # MODE 2: NEW FARMER REGISTRATION
            else:
                st.markdown(f"<h3 style='margin: 4px 0 2px 0; font-size: 20px; font-weight: 800; color: #0F172A;'>{t('auth_register_header')}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='margin: 0 0 8px 0; font-size: 12px; color: #64748B;'>{t('auth_register_subtitle')}</p>", unsafe_allow_html=True)

                with st.form("clean_registration_form"):
                    reg_name = st.text_input(t("reg_name_label"), placeholder=t("reg_name_placeholder"))
                    
                    r_col1, r_col2 = st.columns(2)
                    with r_col1:
                        reg_phone = st.text_input(t("reg_phone_label"), placeholder=t("reg_phone_placeholder"))
                        reg_village = st.text_input(t("reg_village_label"), placeholder=t("reg_village_placeholder"))
                        soil_choices = [
                            "Medium Black Soil (काळी मध्यम)",
                            "Deep Black Soil (काळी कापशी)",
                            "Red Loamy (तांबडी पोयटा)",
                            "Sandy Loam (वालुकामय)"
                        ]
                        reg_soil = st.selectbox(t("reg_soil_label"), options=soil_choices)
                    with r_col2:
                        reg_pin = st.text_input(t("reg_pin_label"), type="password", placeholder=t("reg_pin_placeholder"))
                        reg_taluka = st.text_input(t("reg_taluka_label"), value="Niphad")
                        reg_land = st.number_input(t("reg_land_label"), min_value=0.1, max_value=500.0, value=3.5, step=0.5)

                    irr_choices = [
                        "Drip Irrigation (ठिबक सिंचन)",
                        "Well & Sprinkler (तुषार सिंचन)",
                        "Canal Flood (कालवा पाटपाणी)",
                        "Borewell (बोअरवेल)"
                    ]
                    reg_irr = st.selectbox(t("reg_irrigation_label"), options=irr_choices)
                    reg_crops = st.text_input(t("reg_crops_label"), placeholder="e.g. Grapes, Onion, Soybean")

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

                if st.button(f"👈 {t('auth_switch_to_login')}", key="btn_switch_to_login", use_container_width=True):
                    st.session_state.auth_mode = "login"
                    st.rerun()

    # Subtle footer note
    footer_html = f"""<div style="text-align: center; font-size: 11px; color: #94A3B8; margin-top: 14px; padding-bottom: 4px;">
{t('footer_text')}
</div>"""
    st.markdown(textwrap.dedent(footer_html), unsafe_allow_html=True)
