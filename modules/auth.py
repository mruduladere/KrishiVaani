"""
modules/auth.py - Authentication & Registration Module
KrishiVaani (Voice of Agriculture)

Provides:
1. 1-Click Demo Login for Smart India Hackathon evaluators (Ramesh Patil account).
2. Credential-based Farmer Login (Mobile + 4-digit PIN validated in-memory).
3. New Farmer Registration (saves directly into st.session_state.registered_farmers).
4. Dual-language toggle (English / मराठी) support directly on the auth screen.
"""

import copy
import streamlit as st
from sample_data import SAMPLE_FARMER
from translations import t, render_language_switcher


def normalize_phone(phone_str):
    """Normalizes phone string by removing spaces, hyphens, and standard country code."""
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


def render_auth():
    """Renders the KrishiVaani authentication and registration screen."""
    # Top Language Switcher Bar
    top_col1, top_col2 = st.columns([3, 1])
    with top_col1:
        st.markdown(f"## 🌾 {t('app_title')} — {t('app_subtitle')}")
        st.caption(f"🏆 {t('sih_badge')}")
    with top_col2:
        render_language_switcher(key="auth_top")

    st.markdown("<br>", unsafe_allow_html=True)

    # Center-aligned portal container
    center_col1, center_col2, center_col3 = st.columns([1, 6, 1])

    with center_col2:
        with st.container(border=True):
            st.markdown(f"### 🚪 {t('login_portal_title')}")
            st.write(t("login_portal_subtitle"))

            # ----------------- 1-CLICK DEMO LOGIN -----------------
            st.markdown(
                """
                <div style="background-color: #e8f5e9; border: 1px solid #c8e6c9; border-radius: 8px; padding: 14px; margin-bottom: 14px;">
                    <b style="color: #1b5e20;">⚡ परीक्षकांसाठी जलद लॉगिन (Quick Evaluator Access)</b><br>
                    <span style="font-size: 13px; color: #2e7d32;">
                        कोणतीही माहिती टाईप न करता थेट नाशिक शेतकरी 'रमेश पाटील' यांच्या खात्यात प्रवेश करण्यासाठी खालील बटण दाबा.
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(t("demo_login_button"), use_container_width=True, type="primary"):
                st.session_state.is_authenticated = True
                st.session_state.farmer_profile = copy.deepcopy(SAMPLE_FARMER)
                st.session_state.active_nav = "dashboard"
                st.success(t("login_success"))
                st.rerun()

            st.caption(t("demo_login_caption"))
            st.markdown(f"<div style='text-align: center; margin: 15px 0; color: #9e9e9e;'>── {t('or_divider')} ──</div>", unsafe_allow_html=True)

            # ----------------- TABS: LOGIN vs REGISTRATION -----------------
            tab_login, tab_register = st.tabs([t("tab_login"), t("tab_register")])

            # Tab 1: Regular Farmer Login
            with tab_login:
                with st.form("farmer_login_form"):
                    phone_val = st.text_input(t("phone_label"), value="98220 12345", placeholder=t("phone_placeholder"))
                    pin_val = st.text_input(t("pin_label"), type="password", placeholder=t("pin_placeholder"))
                    
                    submit_login = st.form_submit_button(t("login_button"), use_container_width=True)

                    if submit_login:
                        matched = find_farmer_by_credentials(phone_val, pin_val)
                        if matched:
                            st.session_state.is_authenticated = True
                            st.session_state.farmer_profile = copy.deepcopy(matched)
                            st.session_state.active_nav = "dashboard"
                            st.success(t("login_success"))
                            st.rerun()
                        else:
                            st.error(t("login_failed"))

            # Tab 2: New Farmer Registration
            with tab_register:
                st.caption("नवीन शेतकऱ्यांची नोंदणी थेट ॲप मेमरीमध्ये सेव्ह होते (Saves in session memory).")
                with st.form("farmer_registration_form"):
                    r_col1, r_col2 = st.columns(2)
                    
                    with r_col1:
                        new_name = st.text_input(t("reg_name_label"), placeholder=t("reg_name_placeholder"))
                        new_phone = st.text_input(t("reg_phone_label"), placeholder=t("reg_phone_placeholder"))
                        new_pin = st.text_input(t("reg_pin_label"), type="password", placeholder=t("reg_pin_placeholder"))
                        new_village = st.text_input(t("reg_village_label"), placeholder=t("reg_village_placeholder"))
                        new_taluka = st.text_input(t("reg_taluka_label"), placeholder=t("reg_taluka_placeholder"))
                        
                    with r_col2:
                        new_district = st.text_input(t("reg_district_label"), value="Nashik")
                        new_land = st.number_input(t("reg_land_label"), min_value=0.1, max_value=500.0, value=3.5, step=0.5)
                        
                        soil_choices = [
                            "Medium Black Soil (काळी मध्यम जमीन)",
                            "Deep Black Cotton Soil (भारी काळी कापशी जमीन)",
                            "Red Loamy Soil (तांबडी पोयट्याची जमीन)",
                            "Sandy Loam Soil (हलकी वालुकामय जमीन)"
                        ]
                        new_soil = st.selectbox(t("reg_soil_label"), options=soil_choices)
                        
                        irr_choices = [
                            "Drip Irrigation & Farm Pond (ठिबक सिंचन व शेततळे)",
                            "Well & Sprinkler System (विहीर व तुषार सिंचन)",
                            "Canal Flood Irrigation (कालवा पाटपाणी)",
                            "Borewell & Direct Pipeline (बोअरवेल व पाईपलाईन)"
                        ]
                        new_irr = st.selectbox(t("reg_irrigation_label"), options=irr_choices)

                    new_crops_raw = st.text_input(t("reg_crops_label"), placeholder=t("reg_crops_placeholder"))

                    submit_register = st.form_submit_button(t("register_button"), use_container_width=True)

                    if submit_register:
                        clean_name = new_name.strip()
                        clean_phone = normalize_phone(new_phone)
                        clean_pin = new_pin.strip()

                        if len(clean_name) >= 2 and len(clean_phone) >= 10 and len(clean_pin) >= 4:
                            parsed_crops = [c.strip() for c in new_crops_raw.split(",") if c.strip()]
                            if not parsed_crops:
                                parsed_crops = ["Onion (कांदा)", "Soybean (सोयाबीन)"]

                            new_profile = {
                                "name": clean_name,
                                "phone": f"+91 {clean_phone}",
                                "pin": clean_pin,
                                "email": f"{clean_name.lower().replace(' ', '.')}@krishivaani.in",
                                "village": new_village.strip() or "Pimpalgaon",
                                "taluka": new_taluka.strip() or "Niphad",
                                "district": new_district.strip() or "Nashik",
                                "state": "Maharashtra",
                                "pincode": "422001",
                                "land_size_acres": float(new_land),
                                "soil_type": new_soil,
                                "irrigation_type": new_irr,
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

                            # Save to in-memory registered users registry
                            st.session_state.registered_farmers[clean_phone] = new_profile
                            st.session_state.registered_farmers[f"+91 {clean_phone}"] = new_profile
                            
                            # Log user directly in
                            st.session_state.farmer_profile = new_profile
                            st.session_state.is_authenticated = True
                            st.session_state.active_nav = "dashboard"
                            st.success(t("reg_success"))
                            st.rerun()
                        else:
                            st.warning(t("reg_validation_error"))

        st.markdown(
            f"<div style='text-align: center; font-size: 13px; color: #757575; margin-top: 15px;'>{t('footer_text')}</div>",
            unsafe_allow_html=True
        )
