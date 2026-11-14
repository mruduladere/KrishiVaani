"""
translations.py - Comprehensive Pure-Language Bilingual (English & Marathi) Translation Engine
KrishiVaani (Voice of Agriculture)

Provides:
- Strict 100% pure English ('en') and 100% pure Marathi ('mr') dictionaries.
- Zero mixed parentheses (no 'Name (नाव)' or 'Seeds (बियाणे)').
- t(key, lang=None) helper for UI string resolution.
- pick(val, lang=None) universal bilingual extractor for strings, dictionaries, and dynamic data.
"""

try:
    from flask import session as flask_session
except ImportError:
    flask_session = None

try:
    import streamlit as st
except ImportError:
    st = None


TRANSLATIONS = {
    "en": {
        # App Branding & Meta
        "app_title": "KrishiVaani",
        "app_subtitle": "Voice of Agriculture",
        "sih_badge": "Smart India Hackathon Prototype",
        "footer_text": "🌱 KrishiVaani • Pure Python • No Database • Designed for Maharashtra Farmers",
        "lang_name_mr": "Marathi",
        "lang_name_en": "English",

        # Auth & Login Portal
        "auth_minimal_welcome": "Welcome back",
        "auth_minimal_sub": "Sign in to manage your crops and cattle",
        "auth_minimal_tagline": "Voice of Agriculture",
        "auth_minimal_new_reg": "New farmer? Register here",
        "auth_minimal_existing": "Already registered? Sign in",
        "auth_welcome_title": "Welcome back, Farmer",
        "auth_welcome_subtitle": "Enter your mobile number and 4-digit PIN to access your farm portal.",
        "auth_landscape_headline": "Empowering Every Harvest",
        "auth_landscape_sub": "Unified crop advisory, livestock care and market insights.",
        "auth_headline": "Smart Farming, Simplified",
        "auth_subheadline": "One unified digital platform for everyday Maharashtra farming.",
        "auth_showcase_badge": "KrishiVaani • Voice of Agriculture",
        "auth_showcase_title": "Smart Farming Platform",
        "auth_showcase_tagline": "One unified digital platform for everyday Maharashtra farming",
        "auth_showcase_desc": "Empowering farmers across Nashik and Maharashtra with actionable crop advisories, livestock reminders, market discovery, and financial tracking.",
        "auth_register_header": "Create Farmer Account",
        "auth_register_subtitle": "Register your land and crops in memory to get instant digital advisory.",
        "auth_switch_to_register": "Don't have an account? Register here",
        "auth_switch_to_login": "Already registered? Sign in here",
        "auth_or_text": "or continue with demo account",
        "auth_demo_title": "1-Click Demo Login (Ramesh Patil)",
        "auth_pill_crop": "Crop Advisory",
        "auth_pill_livestock": "Livestock Care",
        "auth_pill_expenses": "Expense Tracking",
        "auth_pill_services": "Local Services",
        "login_portal_title": "KrishiVaani Farmer Portal",
        "login_portal_subtitle": "Unified Digital Agriculture Platform for Maharashtra Farmers",
        "demo_login_button": "1-Click Demo Login (Ramesh Patil)",
        "demo_login_caption": "Instant 1-click access with pre-loaded Nashik farm data for Hackathon evaluators.",
        "or_divider": "OR SIGN IN WITH CREDENTIALS",
        "tab_login": "Farmer Login",
        "tab_register": "New Farmer Registration",
        "phone_label": "Registered Mobile Number",
        "phone_placeholder": "e.g. 9822012345",
        "pin_label": "4-Digit Security PIN",
        "pin_placeholder": "Enter 4-digit PIN (Demo: 1234)",
        "login_button": "Log In to My Farm",
        "login_failed": "Invalid Mobile Number or PIN. For demo, use 9822012345 with PIN 1234, or use 1-Click Demo Login above.",
        "login_success": "Login successful! Welcome to KrishiVaani.",

        # Registration
        "reg_name_label": "Full Name",
        "reg_name_placeholder": "e.g. Ramesh Tukaram Patil",
        "reg_phone_label": "Mobile Number",
        "reg_phone_placeholder": "10-digit mobile number",
        "reg_pin_label": "Create 4-Digit Security PIN",
        "reg_pin_placeholder": "4-digit numeric PIN",
        "reg_village_label": "Village",
        "reg_village_placeholder": "e.g. Pimpalgaon Baswant",
        "reg_taluka_label": "Taluka",
        "reg_taluka_placeholder": "e.g. Niphad",
        "reg_district_label": "District",
        "reg_land_label": "Total Land Size (Acres)",
        "reg_soil_label": "Soil Type",
        "reg_irrigation_label": "Irrigation Method",
        "reg_crops_label": "Crops Grown (comma-separated)",
        "reg_crops_placeholder": "e.g. Grapes, Onion, Soybean",
        "register_button": "Complete Registration & Enter Farm",
        "reg_validation_error": "Please provide Full Name, 10-digit Mobile Number, and a 4-digit PIN.",
        "reg_success": "Registration completed successfully! Welcome to KrishiVaani.",

        # Sidebar & Navigation
        "nav_header": "Main Navigation",
        "nav_dashboard": "1. Profile & Dashboard",
        "nav_crop_helper": "2. Crop & Farming Helper",
        "nav_ai_assistant": "3. Multilingual AI Assistant",
        "nav_nearby_services": "4. Nearby Agri Services",
        "nav_marketplace": "5. Farmer Marketplace",
        "nav_livestock": "6. Livestock & Vaccines",
        "nav_expense_tracker": "7. Farm Expense Tracker",
        "logout_button": "Log Out",
        "farmer_badge": "Farmer",
        "location_badge": "Location",
        "land_badge": "Land Holding",
        "back_to_dashboard": "Back to Farmer Dashboard",

        # Module 1: Dashboard
        "greeting_welcome": "Namaskar",
        "greeting_season": "Season: Rabi 2026-27",
        "greeting_land": "Land",
        "quick_overview": "Quick Farm Overview",
        "metric_land": "Total Farm Land",
        "metric_crops": "Active Crops",
        "metric_livestock": "Total Livestock",
        "metric_expenses": "Current Month Spend",
        "crops_count_suffix": "Crops",
        "animals_count_suffix": "Animals",
        "logs_suffix": "logs",
        "profile_heading": "Farmer Profile & Farm Details",
        "btn_view_profile": "View Profile",
        "btn_edit_profile": "Edit Profile",
        "btn_save_profile": "Save Profile Changes",
        "btn_cancel": "Cancel",
        "full_name": "Full Name",
        "contact_phone": "Phone Number",
        "contact_email": "Email Address",
        "pref_language": "Preferred Language",
        "address_label": "Location / Address",
        "land_size_label": "Land Size",
        "soil_type_label": "Soil Type",
        "irrigation_label": "Irrigation Method",
        "livestock_summary_label": "Livestock Holding",
        "daily_milk_label": "Daily Milk Yield",
        "crops_cultivated_label": "Crops Currently Cultivated",
        "profile_updated_success": "Profile updated successfully!",
        "reset_defaults_title": "Reset to Sample Data Defaults",
        "reset_defaults_desc": "If you edited data and want to restore baseline demonstration values, click below.",
        "btn_reset_defaults": "Restore Sample Defaults",
        "reset_success": "Baseline sample data restored successfully!",
        "services_hub_title": "Platform Services & Modules",
        "services_hub_caption": "Click on any module below to navigate directly.",
        "btn_open_module": "Open",
        "btn_view_info": "View Scope",

        # Module 2: Crop Helper
        "crop_helper_banner_title": "Crop & Farming Helper",
        "crop_helper_banner_subtitle": "Stage-by-stage agronomy advice, fertilizer schedules, and actionable farming reminders for Maharashtra crops.",
        "select_crop_title": "Select Crop to Inspect",
        "your_farm_crop": "From Your Farm",
        "other_crop": "Available Guide",
        "crop_name_label": "Crop Name",
        "marathi_name_label": "Regional Name",
        "season_label": "Season",
        "soil_label": "Recommended Soil",
        "stage_1_tab": "Stage 1: Sowing / Pruning",
        "stage_2_tab": "Stage 2: Vegetative Growth",
        "stage_3_tab": "Stage 3: Flowering / Fruiting",
        "stage_4_tab": "Stage 4: Harvest & Storage",
        "duration_label": "Duration / Window",
        "fertilizer_heading": "Fertilizer & Nutrition Management",
        "irrigation_heading": "Irrigation Schedule",
        "pest_heading": "Pest & Disease Prevention",
        "pro_tip_heading": "Agronomy Expert Pro Tip",
        "checklist_title": "Farm Tasks & Action Checklist",
        "checklist_caption": "Timely farming reminders and tasks synced with your crop stages.",
        "filter_tasks_label": "Filter Tasks:",
        "filter_current_crop": "Current Crop Only",
        "filter_all_tasks": "All Farm Tasks",
        "progress_label": "Progress",
        "completed_label": "tasks completed",
        "priority_high": "High",
        "priority_med": "Medium",
        "priority_low": "Low",
        "add_task_expander": "Add New Farm Task / Reminder",
        "task_desc_label": "Task Description",
        "task_crop_label": "Related Crop",
        "task_stage_label": "Stage / Category",
        "task_due_label": "Due Period",
        "task_priority_label": "Priority",
        "btn_save_task": "Save Task",
        "task_saved_success": "Task added to checklist successfully!",
        "task_input_warning": "Please enter a task description.",

        # Module 4: Nearby Services
        "nearby_banner_title": "Nearby Agricultural Services",
        "nearby_banner_subtitle": "Find certified veterinary doctors, seed and fertilizer shops, equipment rental, and soil testing labs near your farm.",
        "search_filter_title": "Find & Filter Services",
        "category_filter_label": "Select Category:",
        "taluka_filter_label": "Select Taluka:",
        "keyword_search_label": "Search by Keyword:",
        "keyword_placeholder": "e.g. Kulkarni, Tractor, Onion Seed, Clinic",
        "all_categories": "All Categories",
        "all_talukas": "All Talukas",
        "showing_label": "Showing",
        "providers_label": "service providers",
        "timings_label": "Timings",
        "available_services_label": "Available Services & Specialities:",
        "btn_call_now": "Call Now",
        "btn_whatsapp": "WhatsApp Inquiry",
        "no_providers_found": "No service providers found matching these filters. Try changing your filters or add a new provider below.",
        "add_service_expander": "Register a New Local Service / Doctor",
        "add_service_caption": "Contribute trusted local service provider details to assist fellow farmers in your taluka.",
        "provider_name_label": "Provider / Centre Name",
        "provider_cat_label": "Service Category",
        "provider_taluka_label": "Taluka",
        "provider_location_label": "Location & Distance",
        "provider_phone_label": "Contact Number",
        "provider_timings_label": "Operating Hours / Timings",
        "provider_speciality_label": "Services & Specialities",
        "btn_save_service": "Save Service Provider",
        "service_saved_success": "Service provider registered successfully in directory!",
        "service_input_warning": "Please provide provider name and phone.",

        # Module 6: Livestock Records & Vaccines
        "livestock_banner_title": "Livestock Records & Vaccine Reminders",
        "livestock_banner_subtitle": "Digital health registry, daily milk yield tracking, and automated overdue vaccination alerts for your cattle and goats.",
        "kpi_total_cattle": "Total Livestock",
        "kpi_daily_milk": "Daily Milk Yield",
        "kpi_vaccines_overdue": "Vaccines Overdue",
        "kpi_vaccines_upcoming": "Due Within 14 Days",
        "btn_add_animal": "Register Animal",
        "animal_tag_label": "Tag / ID",
        "animal_name_label": "Animal Name",
        "animal_type_label": "Species / Type",
        "animal_breed_label": "Breed",
        "animal_age_label": "Age (Years)",
        "animal_milk_label": "Daily Milk Yield",
        "animal_health_label": "Health Condition",
        "vaccination_schedule_title": "Vaccination Schedule & History",
        "vaccine_col_name": "Vaccine",
        "vaccine_col_last": "Administered Date",
        "vaccine_col_due": "Due Date",
        "vaccine_col_status": "Status",
        "vaccine_col_action": "Action",
        "btn_mark_vaccinated": "Mark Completed",
        "status_overdue_badge": "Overdue",
        "status_upcoming_badge": "Due in 14 Days",
        "status_uptodate_badge": "Up-to-Date",
        "health_healthy": "Healthy & Productive",
        "health_attention": "Vaccine Overdue",
        "add_animal_modal_title": "Register New Farm Animal",
        "btn_save_animal": "Save Animal Record",
        "vaccine_updated_success": "Vaccination record updated! Next scheduled date calculated.",
        "animal_added_success": "New animal successfully registered in livestock registry!",

        # Module 7: Farm Expense Tracker & Analytics
        "expense_banner_title": "Farm Expense Tracker & Analytics",
        "expense_banner_subtitle": "Categorized accounting of input investments, labor, fuel, and veterinary expenses with interactive charts and seasonal breakdowns.",
        "kpi_total_spend": "Total Farm Expenditure",
        "kpi_top_category": "Highest Expense Category",
        "kpi_current_month": "Current Month Spend",
        "kpi_total_entries": "Logged Entries",
        "btn_add_expense": "Log Farm Expense",
        "add_expense_modal_title": "Log New Farm Expenditure",
        "expense_amount_label": "Amount (₹)",
        "expense_date_label": "Date of Expense",
        "expense_category_label": "Expense Category",
        "expense_season_label": "Agricultural Season",
        "expense_crop_label": "Linked Crop / Enterprise",
        "expense_mode_label": "Payment Mode",
        "expense_desc_label": "Description / Purpose",
        "btn_save_expense": "Save Expense Record",
        "tab_recent_logs": "Recent Expense Transactions",
        "tab_category_summary": "Category-wise Breakdown",
        "tab_crop_summary": "Crop-wise Allocation",
        "tab_seasonal_summary": "Seasonal Breakdown",
        "chart_category_heading": "Category-wise Expense Distribution",
        "chart_monthly_heading": "Monthly Expenditure Trend (₹)",
        "chart_crop_heading": "Crop-wise Cost Allocation",
        "col_category": "Category",
        "col_amount": "Total Amount (₹)",
        "col_percentage": "Share (%)",
        "col_entries": "Transactions",
        "col_crop": "Crop / Enterprise",
        "col_season": "Season",
        "col_date": "Date",
        "col_desc": "Description",
        "col_mode": "Payment Mode",
        "col_action": "Action",
        "btn_delete_expense": "Delete",
        "expense_added_success": "Expense entry logged successfully in farm ledger!",
        "expense_deleted_success": "Expense entry removed from farm ledger!",

        # Common Crops & Categories Mapping
        "Grapes": "Grapes",
        "Onion": "Onion",
        "Soybean": "Soybean",
        "Cotton": "Cotton",
        "Sugarcane": "Sugarcane",
        "Wheat": "Wheat",
        "Livestock / Dairy": "Livestock / Dairy",
        "General Farm": "General Farm",
        "Seeds & Seedlings": "Seeds & Seedlings",
        "Fertilizers & Nutrients": "Fertilizers & Nutrients",
        "Pesticides & Bio-agents": "Pesticides & Bio-agents",
        "Labour & Pruning": "Labour & Pruning",
        "Irrigation & Water": "Irrigation & Water",
        "Machinery & Rentals": "Machinery & Rentals",
        "Transport & Mandi Hamali": "Transport & Mandi Hamali",
        "Animal Fodder & Feed": "Animal Fodder & Feed",
        "Veterinary & Healthcare": "Veterinary & Healthcare",
        "Animal Vaccination": "Animal Vaccination",
        "Fuel & Electricity": "Fuel & Electricity",
        "Repairs & Maintenance": "Repairs & Maintenance",
        "UPI": "UPI / Online",
        "Cash": "Cash",
        "Bank Transfer": "Bank Transfer",
        "Credit / Udhar": "Credit / Udhar",
        "Rabi 2026-27": "Rabi 2026-27",
        "Kharif 2026": "Kharif 2026",
        "Zaid / Summer 2026": "Zaid / Summer 2026",
        "Cow": "Cow",
        "Buffalo": "Buffalo",
        "Goat": "Goat",
        "Bull": "Bull",
        "Sheep": "Sheep",
        "Acres": "Acres",
        "L / day": "L / day",
        "Yrs": "Years",

        # Extra Pure UI Labels (Modules 2, 4, 6, 7)
        "module_6_badge": "Module 6 • Maharashtra Dairy & Cattle Care",
        "module_7_badge": "Module 7 • Farm Financial Ledger & Analytics",
        "kpi_total_entries_suffix": "logged transactions",
        "kpi_across_label": "Across",
        "kpi_current_month_sub": "November 2026 active window",
        "kpi_top_crop": "Top Invested Crop",
        "kpi_share_suffix": "share",
        "kpi_budget_share": "of budget",
        "chart_12_categories": "12 Core Agro Categories",
        "chart_season_timeline": "Season Timeline",
        "chart_cat_caption": "Fertilizers, Labour & Feeds account for major operating investments",
        "chart_month_caption": "Peak expenditure observed during forward pruning & basal fertilizer application",
        "livestock_registry_title": "Individual Animal Health & Vaccine Registry",
        "livestock_registry_subtitle": "Vaccination overdue calculation evaluated automatically with Python datetime",
        "today_label": "Today",
        "registered_in_registry": "Registered in farm registry",
        "average_yield_prefix": "Average:",
        "per_animal_suffix": "L / animal",
        "requires_immediate_vet": "Requires immediate vet scheduling",
        "next_14_days_window": "Next 14 days calendar window",
        "vaccines_count_suffix": "Vaccines",
        "vaccines_tracked": "Vaccines Tracked",
        "last_dose_label": "Last:",
        "due_date_label": "Due:",
        "days_late": "days late",
        "in_days": "in",
        "days_suffix": "days",
        "status_scheduled": "Scheduled",
        "initial_vaccine_label": "Initial Vaccine Schedule",
        "add_record_btn": "Add Record",
        "delete_confirm": "Delete this expense?",
        "clear_filters": "Clear search filters",
        "no_providers_title": "No Service Providers Found",
        "verified_directory": "Verified regional directory",
        "stages_count_suffix": "Stages",
        "lifecycle_advisory": "Lifecycle Advisory",
        "growth_lifecycle_title": "Stage-by-Stage Agricultural Lifecycle",
        "growth_lifecycle_sub": "Step-by-step nutrition, water management, and disease prophylaxis",
        "add_inmemory_task": "Add In-Memory Farm Task",
        "next_3_days": "Next 3 Days",
        "high_priority": "High",
        "medium_priority": "Medium",
        "low_priority": "Low",
        "apply_filters_btn": "Apply Filters",
        "module_2_badge": "Module 2 • Maharashtra Dynamic Agronomy Advisory",
        "active_crop_label": "Active Crop",
        "farm_crop_badge": "Farm Crop",
        "agronomy_knowledge_base": "Agronomic Knowledge Base",
        "task_placeholder": "e.g. Apply 13:0:45 potassium nitrate via drip irrigation",

        # Under Construction Placeholders
        "under_dev_badge": "Under Development",
        "planned_features_heading": "Planned Features in this Module:",
    },
    "mr": {
        # App Branding & Meta
        "app_title": "कृषीवाणी",
        "app_subtitle": "शेतकऱ्यांचा डिजिटल आवाज",
        "sih_badge": "स्मार्ट इंडिया हॅकाथॉन प्रोटोटाईप",
        "footer_text": "🌱 कृषीवाणी • प्युअर पायथन • डेटाबेस विरहित • महाराष्ट्रातील बळीराजासाठी",
        "lang_name_mr": "मराठी",
        "lang_name_en": "इंग्रजी",

        # Auth & Login Portal
        "auth_minimal_welcome": "पुन्हा स्वागत आहे",
        "auth_minimal_sub": "पिके व शेती व्यवस्थापनासाठी लॉगिन करा",
        "auth_minimal_tagline": "शेतीचा आवाज",
        "auth_minimal_new_reg": "नवीन शेतकरी आहात? येथे नोंदणी करा",
        "auth_minimal_existing": "आधीच खाते आहे? लॉगिन करा",
        "auth_welcome_title": "पुन्हा स्वागत आहे, शेतकरी दादा",
        "auth_welcome_subtitle": "आपल्या शेती पोर्टलमध्ये प्रवेश करण्यासाठी मोबाईल नंबर व ४-अंकी पिन प्रविष्ट करा.",
        "auth_landscape_headline": "प्रत्येक हंगामाचे सक्षमीकरण",
        "auth_landscape_sub": "एकात्मिक पीक सल्ला, पशुधन काळजी आणि बाजारपेठ माहिती.",
        "auth_headline": "स्मार्ट शेती, सोपे व्यवस्थापन",
        "auth_subheadline": "महाराष्ट्रातील शेतकऱ्यांसाठी एकात्मिक डिजिटल कृषी व्यासपीठ.",
        "auth_showcase_badge": "कृषीवाणी • शेतकऱ्यांचा डिजिटल आवाज",
        "auth_showcase_title": "स्मार्ट डिजिटल शेती",
        "auth_showcase_tagline": "महाराष्ट्रातील दैनंदिन शेतीसाठी एकसंध डिजिटल व्यासपीठ",
        "auth_showcase_desc": "नाशिक व महाराष्ट्रातील शेतकऱ्यांसाठी पीक सल्ला, पशुधन लसीकरण, स्थानिक सेवा आणि शेतखर्च नोंदी एकाच ठिकाणी.",
        "auth_register_header": "नवीन शेतकरी नोंदणी",
        "auth_register_subtitle": "आपली शेतजमीन व पिकांची नोंद करून थेट डिजिटल कृषी सेवा मिळवा.",
        "auth_switch_to_register": "नवीन शेतकरी आहात? येथे नोंदणी करा",
        "auth_switch_to_login": "आधीच नोंदणी झाली आहे? येथे लॉगिन करा",
        "auth_or_text": "किंवा डेमो खात्याने थेट प्रवेश करा",
        "auth_demo_title": "१-क्लिक डेमो लॉगिन (रमेश पाटील)",
        "auth_pill_crop": "पीक सल्लागार",
        "auth_pill_livestock": "पशुधन व्यवस्थापन",
        "auth_pill_expenses": "शेतखर्च नोंदवही",
        "auth_pill_services": "स्थानिक सेवा केंद्र",
        "login_portal_title": "कृषीवाणी शेतकरी पोर्टल",
        "login_portal_subtitle": "महाराष्ट्रातील शेतकऱ्यांसाठी एकात्मिक डिजिटल कृषी व्यासपीठ",
        "demo_login_button": "१-क्लिक डेमो लॉगिन (रमेश पाटील)",
        "demo_login_caption": "परीक्षक व परीक्षणासाठी नाशिक शेती डेटासह त्वरित १-क्लिक प्रवेश.",
        "or_divider": "किंवा मोबाईल व पिन प्रविष्ट करून लॉगिन करा",
        "tab_login": "शेतकरी लॉगिन",
        "tab_register": "नवीन शेतकरी नोंदणी",
        "phone_label": "नोंदणीकृत मोबाईल क्रमांक",
        "phone_placeholder": "उदा. 9822012345",
        "pin_label": "४-अंकी सुरक्षा पिन",
        "pin_placeholder": "४-अंकी पिन प्रविष्ट करा (डेमो: 1234)",
        "login_button": "शेतात प्रवेश करा",
        "login_failed": "अवैध मोबाईल क्रमांक किंवा पिन. डेमोसाठी 9822012345 आणि पिन 1234 वापरा किंवा वरील १-क्लिक डेमो लॉगिन वापरा.",
        "login_success": "लॉगिन यशस्वी! कृषीवाणीमध्ये आपले स्वागत आहे.",

        # Registration
        "reg_name_label": "पूर्ण नाव",
        "reg_name_placeholder": "उदा. रमेश तुकाराम पाटील",
        "reg_phone_label": "मोबाईल क्रमांक",
        "reg_phone_placeholder": "१० अंकी मोबाईल नंबर",
        "reg_pin_label": "४-अंकी सुरक्षा पिन तयार करा",
        "reg_pin_placeholder": "४ अंकी संख्यात्मक पिन",
        "reg_village_label": "गाव",
        "reg_village_placeholder": "उदा. पिंपळगाव बसवंत",
        "reg_taluka_label": "तालुका",
        "reg_taluka_placeholder": "उदा. निफाड",
        "reg_district_label": "जिल्हा",
        "reg_land_label": "एकूण शेतजमीन (एकर)",
        "reg_soil_label": "मातीचा प्रकार",
        "reg_irrigation_label": "सिंचन पद्धत",
        "reg_crops_label": "पिके (स्वल्पविरामाने वेगळे करा)",
        "reg_crops_placeholder": "उदा. द्राक्ष, कांदा, सोयाबीन",
        "register_button": "नोंदणी पूर्ण करा व शेतात प्रवेश करा",
        "reg_validation_error": "कृपया पूर्ण नाव, १०-अंकी मोबाईल नंबर आणि ४-अंकी पिन प्रविष्ट करा.",
        "reg_success": "नोंदणी यशस्वीरीत्या पूर्ण झाली! कृषीवाणीमध्ये आपले स्वागत आहे.",

        # Sidebar & Navigation
        "nav_header": "मुख्य विभाग",
        "nav_dashboard": "१. शेतकरी प्रोफाइल व डॅशबोर्ड",
        "nav_crop_helper": "२. पीक सल्लागार व मार्गदर्शन",
        "nav_ai_assistant": "३. AI शेती सहाय्यक",
        "nav_nearby_services": "४. जवळपासची कृषी सेवा केंद्र",
        "nav_marketplace": "५. शेतकरी थेट बाजारपेठ",
        "nav_livestock": "६. पशुधन नोंदी व लसीकरण",
        "nav_expense_tracker": "७. शेतखर्च ट्रॅकर व नफा",
        "logout_button": "लॉगआउट करा",
        "farmer_badge": "शेतकरी",
        "location_badge": "पत्ता",
        "land_badge": "शेतजमीन",
        "back_to_dashboard": "शेतकरी डॅशबोर्डवर परत जा",

        # Module 1: Dashboard
        "greeting_welcome": "नमस्कार",
        "greeting_season": "हंगाम: रब्बी २०२६-२७",
        "greeting_land": "जमीन",
        "quick_overview": "शेती सारांश",
        "metric_land": "एकूण शेतजमीन",
        "metric_crops": "सक्रिय पिके",
        "metric_livestock": "एकूण पशुधन",
        "metric_expenses": "चालू महिना खर्च",
        "crops_count_suffix": "पिके",
        "animals_count_suffix": "जनावरे",
        "logs_suffix": "नोंदी",
        "profile_heading": "शेतकरी प्रोफाइल व शेतजमीन माहिती",
        "btn_view_profile": "प्रोफाइल पहा",
        "btn_edit_profile": "प्रोफाइल संपादन",
        "btn_save_profile": "बदल जतन करा",
        "btn_cancel": "रद्द करा",
        "full_name": "पूर्ण नाव",
        "contact_phone": "मोबाईल क्रमांक",
        "contact_email": "ईमेल पत्ता",
        "pref_language": "पसंतीची भाषा",
        "address_label": "पत्ता व ठिकाण",
        "land_size_label": "शेतजमीन धारणा",
        "soil_type_label": "मातीचा प्रकार",
        "irrigation_label": "सिंचन सुविधा",
        "livestock_summary_label": "पशुधन माहिती",
        "daily_milk_label": "दैनंदिन दूध उत्पादन",
        "crops_cultivated_label": "सध्या शेतात असलेली पिके",
        "profile_updated_success": "प्रोफाइल यशस्वीरीत्या जतन केले!",
        "reset_defaults_title": "नमुना डेटा रिसेट करा",
        "reset_defaults_desc": "जर तुम्ही डेटा बदलला असेल आणि पुन्हा मूळ नमुना डेटा आणायचा असेल, तर खालील बटण दाबा.",
        "btn_reset_defaults": "मूळ नमुना डेटा पुनर्स्थापित करा",
        "reset_success": "मूळ नमुना डेटा पूर्ववत करण्यात आला!",
        "services_hub_title": "कृषीवाणी सेवा केंद्र व विभाग",
        "services_hub_caption": "खालील सेवांवर क्लिक करून थेट त्या विभागात जा.",
        "btn_open_module": "उघडा",
        "btn_view_info": "माहिती पहा",

        # Module 2: Crop Helper
        "crop_helper_banner_title": "पीक सल्लागार व शेती मार्गदर्शन",
        "crop_helper_banner_subtitle": "महाराष्ट्रातील हवामानानुसार पिकांचे टप्प्याटप्प्याने खत, पाणी व रोग नियंत्रण मार्गदर्शन आणि दैनंदिन शेतकाम चेकलिस्ट.",
        "select_crop_title": "तपासणीसाठी पीक निवडा",
        "your_farm_crop": "तुमच्या शेतातील",
        "other_crop": "इतर उपलब्ध पीक",
        "crop_name_label": "पीक नाव",
        "marathi_name_label": "स्थानिक नाव",
        "season_label": "हंगाम",
        "soil_label": "योग्य जमीन",
        "stage_1_tab": "टप्पा १: लागवड / छाटणी",
        "stage_2_tab": "टप्पा २: शाकीय वाढ",
        "stage_3_tab": "टप्पा ३: फुलधारणा / फळधारणा",
        "stage_4_tab": "टप्पा ४: काढणी व साठवणूक",
        "duration_label": "कालावधी / टप्पा वेळ",
        "fertilizer_heading": "खत व्यवस्थापन",
        "irrigation_heading": "पाणी व्यवस्थापन",
        "pest_heading": "रोग व कीड नियंत्रण",
        "pro_tip_heading": "कृषी तज्ज्ञ विशेष सल्ला",
        "checklist_title": "शेतकाम चेकलिस्ट व स्मरणपत्रे",
        "checklist_caption": "तुमच्या पिकांच्या चालू टप्प्यानुसार आवश्यक शेती कामांची नोंद व स्मरणपत्रे.",
        "filter_tasks_label": "फिल्टर निवडा:",
        "filter_current_crop": "केवळ निवडलेले पीक",
        "filter_all_tasks": "सर्व पिकांची कामे",
        "progress_label": "प्रगती",
        "completed_label": "कामे पूर्ण",
        "priority_high": "उच्च",
        "priority_med": "मध्यम",
        "priority_low": "कमी",
        "add_task_expander": "नवीन शेतकाम / स्मरणपत्र जोडा",
        "task_desc_label": "कामाचे नाव व तपशील",
        "task_crop_label": "संबंधित पीक",
        "task_stage_label": "टप्पा / विभाग",
        "task_due_label": "अपेक्षित वेळ / मुदत",
        "task_priority_label": "प्राधान्य",
        "btn_save_task": "काम सेव्ह करा",
        "task_saved_success": "नवीन काम यशस्वीरीत्या चेकलिस्टमध्ये जोडले!",
        "task_input_warning": "कृपया कामाचे नाव प्रविष्ट करा.",

        # Module 4: Nearby Services
        "nearby_banner_title": "जवळपासची कृषी सेवा केंद्र",
        "nearby_banner_subtitle": "पशुवैद्यकीय डॉक्टर, बियाणे-खत दुकाने, कृषी अवजारे भाडे केंद्र व माती परीक्षण प्रयोगशाळांची खात्रीशीर माहिती.",
        "search_filter_title": "सेवा शोधा व फिल्टर करा",
        "category_filter_label": "सेवेचा प्रकार निवडा:",
        "taluka_filter_label": "तालुका निवडा:",
        "keyword_search_label": "कीवर्ड शोधा:",
        "keyword_placeholder": "उदा. कुलकर्णी, ट्रॅक्टर, कांदा बियाणे, क्लिनिक",
        "all_categories": "सर्व सेवा",
        "all_talukas": "सर्व तालुके",
        "showing_label": "दाखवत आहे",
        "providers_label": "सेवा प्रदाते",
        "timings_label": "कामाची वेळ",
        "available_services_label": "उपलब्ध सेवा व वैशिष्ट्ये:",
        "btn_call_now": "कॉल करा",
        "btn_whatsapp": "व्हॉट्सॲप चौकशी",
        "no_providers_found": "या निकषांनुसार कोणताही सेवा प्रदाता सापडला नाही. कृपया फिल्टर बदला किंवा खालील फॉर्ममधून नवीन प्रदाता जोडा.",
        "add_service_expander": "नवीन कृषी सेवा प्रदाता नोंदवा",
        "add_service_caption": "तुमच्या भागातील इतर शेतकरी मित्रांच्या सोयीसाठी खात्रीशीर सेवा प्रदात्यांची माहिती जोडा.",
        "provider_name_label": "प्रदाता किंवा केंद्राचे नाव",
        "provider_cat_label": "सेवेचा प्रकार",
        "provider_taluka_label": "तालुका",
        "provider_location_label": "पत्ता व अंतर",
        "provider_phone_label": "संपर्क क्रमांक",
        "provider_timings_label": "कामाची वेळ",
        "provider_speciality_label": "उपलब्ध सेवा व वैशिष्ट्ये",
        "btn_save_service": "सेवा प्रदाता जतन करा",
        "service_saved_success": "सेवा प्रदाता यशस्वीरीत्या जोडला गेला!",
        "service_input_warning": "कृपया प्रदात्याचे नाव व फोन नंबर प्रविष्ट करा.",

        # Module 6: Livestock Records & Vaccines
        "livestock_banner_title": "पशुधन नोंदी व लसीकरण वेळापत्रक",
        "livestock_banner_subtitle": "जनावरांचे डिजिटल आरोग्य कार्ड, दैनंदिन दूध उत्पादन नोंद आणि स्वयंचलित लसीकरण अलर्ट.",
        "kpi_total_cattle": "एकूण पशुधन",
        "kpi_daily_milk": "दैनंदिन दूध उत्पादन",
        "kpi_vaccines_overdue": "थकबाकी लसीकरण",
        "kpi_vaccines_upcoming": "येत्या १४ दिवसांतील लसी",
        "btn_add_animal": "नवीन जनावर नोंदवा",
        "animal_tag_label": "टॅग / आयडी",
        "animal_name_label": "नाव",
        "animal_type_label": "प्रकार",
        "animal_breed_label": "जात / नस्ल",
        "animal_age_label": "वय (वर्षे)",
        "animal_milk_label": "दैनंदिन दूध (लिटर)",
        "animal_health_label": "आरोग्य स्थिती",
        "vaccination_schedule_title": "लसीकरण वेळापत्रक व इतिहास",
        "vaccine_col_name": "लस",
        "vaccine_col_last": "दिलेली तारीख",
        "vaccine_col_due": "देय तारीख",
        "vaccine_col_status": "स्थिती",
        "vaccine_col_action": "कृती",
        "btn_mark_vaccinated": "लसीकरण पूर्ण नोंदवा",
        "status_overdue_badge": "मुदत संपली",
        "status_upcoming_badge": "येत्या १४ दिवसांत देय",
        "status_uptodate_badge": "अद्ययावत",
        "health_healthy": "निरोगी व दुभते",
        "health_attention": "लसीकरण बाकी (तातडीचे)",
        "add_animal_modal_title": "नवीन जनावराची नोंदणी",
        "btn_save_animal": "पशुधन नोंद जतन करा",
        "vaccine_updated_success": "लसीकरण नोंदवले गेले व पुढील देय तारीख अद्ययावत झाली!",
        "animal_added_success": "नवीन जनावर डिजिटल नोंदवहीत यशस्वीरीत्या जोडले!",

        # Module 7: Farm Expense Tracker & Analytics
        "expense_banner_title": "शेतखर्च ट्रॅकर व नफा विश्लेषण",
        "expense_banner_subtitle": "बियाणे, खते, मजुरी, इंधन व इतर खर्चाची अचूक नोंद, आलेख आणि हंगामनिहाय विश्लेषण.",
        "kpi_total_spend": "एकूण झालेला शेतखर्च",
        "kpi_top_category": "सर्वाधिक खर्चाचा प्रकार",
        "kpi_current_month": "चालू महिन्याचा खर्च",
        "kpi_total_entries": "एकूण नोंदी",
        "btn_add_expense": "नवीन खर्च नोंदवा",
        "add_expense_modal_title": "नवीन शेतखर्चाची नोंद करा",
        "expense_amount_label": "रक्कम (₹)",
        "expense_date_label": "खर्चाची तारीख",
        "expense_category_label": "खर्चाचा प्रकार",
        "expense_season_label": "हंगाम",
        "expense_crop_label": "संबंधित पीक / व्यवसाय",
        "expense_mode_label": "पेमेंट पद्धत",
        "expense_desc_label": "तपशील / कारण",
        "btn_save_expense": "खर्च जतन करा",
        "tab_recent_logs": "खर्चाच्या अलीकडील नोंदी",
        "tab_category_summary": "प्रकारनिहाय सारांश तक्ता",
        "tab_crop_summary": "पीकनिहाय खर्च तक्ता",
        "tab_seasonal_summary": "हंगामनिहाय सारांश",
        "chart_category_heading": "प्रकारनिहाय खर्चाचे वर्गीकरण",
        "chart_monthly_heading": "मासिक खर्च कल (₹)",
        "chart_crop_heading": "पीकनिहाय खर्च वाटप",
        "col_category": "खर्चाचा प्रकार",
        "col_amount": "एकूण रक्कम (₹)",
        "col_percentage": "वाटा (%)",
        "col_entries": "नोंदी संख्या",
        "col_crop": "पीक / घटक",
        "col_season": "हंगाम",
        "col_date": "तारीख",
        "col_desc": "तपशील",
        "col_mode": "पेमेंट माध्यम",
        "col_action": "कृती",
        "btn_delete_expense": "हटवा",
        "expense_added_success": "शेतखर्चाची नोंद यशस्वीरीत्या जमा झाली!",
        "expense_deleted_success": "खर्चाची नोंद शेत नोंदवहीतून हटवण्यात आली!",

        # Common Crops & Categories Mapping
        "Grapes": "द्राक्ष",
        "Onion": "कांदा",
        "Soybean": "सोयाबीन",
        "Cotton": "कापूस",
        "Sugarcane": "ऊस",
        "Wheat": "गहू",
        "Livestock / Dairy": "दुग्धव्यवसाय / पशुधन",
        "General Farm": "सामायिक शेती",
        "Seeds & Seedlings": "बियाणे व रोपे",
        "Fertilizers & Nutrients": "खते व पोषण",
        "Pesticides & Bio-agents": "कीटकनाशके व बुरशीनाशके",
        "Labour & Pruning": "मजुरी व छाटणी",
        "Irrigation & Water": "सिंचन व पाणी",
        "Machinery & Rentals": "यंत्रसामग्री व भाडे",
        "Transport & Mandi Hamali": "वाहतूक व हमाली",
        "Animal Fodder & Feed": "पशुखाद्य व वैरण",
        "Veterinary & Healthcare": "पशुवैद्यकीय उपचार",
        "Animal Vaccination": "पशुधन लसीकरण",
        "Fuel & Electricity": "डिझेल व वीज बिल",
        "Repairs & Maintenance": "दुरुस्ती व देखभाल",
        "UPI": "यूपीआय / ऑनलाइन",
        "Cash": "रोख",
        "Bank Transfer": "बँक ट्रान्सफर",
        "Credit / Udhar": "उधार / देणे",
        "Rabi 2026-27": "रब्बी २०२६-२७",
        "Kharif 2026": "खरीप २०२६",
        "Zaid / Summer 2026": "उन्हाळी २०२६",
        "Cow": "गाय",
        "Buffalo": "म्हैस",
        "Goat": "शेळी",
        "Bull": "बैल",
        "Sheep": "मेंढी",
        "Acres": "एकर",
        "L / day": "लिटर/दिवस",
        "Yrs": "वर्षे",

        # Extra Pure UI Labels (Modules 2, 4, 6, 7)
        "module_6_badge": "विभाग ६ • महाराष्ट्र दुग्ध व पशुधन व्यवस्थापन",
        "module_7_badge": "विभाग ७ • शेतखर्च नोंदवही व आर्थिक विश्लेषण",
        "kpi_total_entries_suffix": "नोंदवलेले व्यवहार",
        "kpi_across_label": "एकूण",
        "kpi_current_month_sub": "नोव्हेंबर २०२६ चालू कालावधी",
        "kpi_top_crop": "सर्वाधिक खर्च झालेले पीक",
        "kpi_share_suffix": "वाटा",
        "kpi_budget_share": "खर्चाचा वाटा",
        "chart_12_categories": "१२ मुख्य कृषी खर्च प्रकार",
        "chart_season_timeline": "हंगाम कालमर्यादा",
        "chart_cat_caption": "खते, मजुरी आणि पशुखाद्य यांवर सर्वाधिक खर्च नोंदवला गेला आहे",
        "chart_month_caption": "गोडी छाटणी आणि पायाभूत खत व्यवस्थापनादरम्यान खर्चात वाढ दिसून आली",
        "livestock_registry_title": "प्रत्येक जनावराचे आरोग्य व लसीकरण नोंदवही",
        "livestock_registry_subtitle": "पायथन डेटटाइम प्रणालीद्वारे स्वयंचलित मुदत गणना",
        "today_label": "आज",
        "registered_in_registry": "शेत नोंदवहीत नोंदणीकृत",
        "average_yield_prefix": "सरासरी:",
        "per_animal_suffix": "लिटर / जनावर",
        "requires_immediate_vet": "तातडीने पशुवैद्यकीय भेटीची गरज",
        "next_14_days_window": "पुढील १४ दिवसांचे वेळापत्रक",
        "vaccines_count_suffix": "लसी",
        "vaccines_tracked": "नोंदवलेल्या लसी",
        "last_dose_label": "मागील:",
        "due_date_label": "देय:",
        "days_late": "दिवस उशीर",
        "in_days": "येत्या",
        "days_suffix": "दिवसांत",
        "status_scheduled": "नियोजित",
        "initial_vaccine_label": "पहिली लस वेळापत्रक",
        "add_record_btn": "नोंद जोडा",
        "delete_confirm": "ही खर्चाची नोंद हटवायची का?",
        "clear_filters": "फिल्टर काढा",
        "no_providers_title": "एकही सेवा केंद्र आढळले नाही",
        "verified_directory": "प्रमाणित प्रादेशिक डिरेक्टरी",
        "stages_count_suffix": "टप्पे",
        "lifecycle_advisory": "हंगामनिहाय मार्गदर्शन",
        "growth_lifecycle_title": "टप्प्याटप्प्याने शेती व्यवस्थापन",
        "growth_lifecycle_sub": "खत व्यवस्थापन, सिंचन आणि कीड नियंत्रण वेळापत्रक",
        "add_inmemory_task": "नवीन शेतकाम जोडा",
        "next_3_days": "पुढील ३ दिवसांत",
        "high_priority": "उच्च",
        "medium_priority": "मध्यम",
        "low_priority": "कमी",
        "apply_filters_btn": "फिल्टर लावा",
        "module_2_badge": "विभाग २ • महाराष्ट्र कृषी पीक सल्ला व व्यवस्थापन",
        "active_crop_label": "सक्रिय पीक",
        "farm_crop_badge": "शेत पीक",
        "agronomy_knowledge_base": "कृषी ज्ञान केंद्र",
        "task_placeholder": "उदा. ठिबक सिंचनातून १३:००:४५ पोटॅशियम नायट्रेट द्या",

        # Under Construction Placeholders
        "under_dev_badge": "विकासाधीन",
        "planned_features_heading": "या विभागात समाविष्ट होणारी मुख्य वैशिष्ट्ये:",
    }
}


def get_lang():
    """Returns active language string ('mr' or 'en') from session state or Flask session."""
    if flask_session is not None:
        try:
            return flask_session.get("lang", "mr")
        except RuntimeError:
            pass
    if st is not None and hasattr(st, "session_state"):
        try:
            return st.session_state.get("lang", "mr")
        except Exception:
            pass
    return "mr"


def t(key, lang=None):
    """
    Translates a key into the active language with graceful fallbacks.
    If key is missing in active language, falls back to English, then to raw key.
    """
    if lang is None:
        lang = get_lang()
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS.get("mr", {}))
    return lang_dict.get(key, TRANSLATIONS.get("en", {}).get(key, key))


def pick(val, lang=None):
    """
    Strict Pure-Language Selector:
    - If dict with 'en'/'mr', picks active language strictly.
    - If string is a key in TRANSLATIONS, resolves it.
    - If string has mixed parentheses like 'Seeds (बियाणे)', strips to pure language.
    Guarantees 100% pure English when lang=='en' and 100% pure Marathi when lang=='mr'.
    """
    if lang is None:
        lang = get_lang()
    
    if val is None:
        return ""
        
    if isinstance(val, dict):
        if lang in val:
            return val[lang]
        if "en" in val and lang == "en":
            return val["en"]
        if "mr" in val and lang == "mr":
            return val["mr"]
        return val.get(lang, val.get("en", val.get("mr", "")))
        
    if isinstance(val, str):
        val_str = val.strip()
        
        # Check direct dictionary key
        if val_str in TRANSLATIONS.get(lang, {}):
            return TRANSLATIONS[lang][val_str]
        if lang == "mr" and val_str in TRANSLATIONS.get("en", {}):
            return TRANSLATIONS["mr"].get(val_str, val_str)
        if lang == "en":
            for k, mr_v in TRANSLATIONS.get("mr", {}).items():
                if mr_v == val_str:
                    return TRANSLATIONS.get("en", {}).get(k, k)

        # Check if string contains mixed parentheses like 'Onion (कांदा)'
        if "(" in val_str and ")" in val_str:
            parts = val_str.split("(", 1)
            left = parts[0].strip()
            right = parts[1].replace(")", "").strip()
            
            # Detect Devanagari characters
            left_is_mr = any('\u0900' <= char <= '\u097F' for char in left)
            right_is_mr = any('\u0900' <= char <= '\u097F' for char in right)
            
            if lang == "mr":
                if right_is_mr:
                    return right
                elif left_is_mr:
                    return left
                return right
            else:
                if left_is_mr and not right_is_mr:
                    return right
                elif right_is_mr and not left_is_mr:
                    return left
                return left
                
        return val_str
        
    return str(val)


def render_language_switcher(key="global"):
    """
    Renders an interactive language mode selector (Streamlit compatibility).
    """
    if st is None or not hasattr(st, "session_state"):
        return
    current_lang = get_lang()
    current_idx = 0 if current_lang == "mr" else 1

    selected = st.radio(
        label="Language / भाषा",
        options=["मराठी", "English"],
        index=current_idx,
        horizontal=True,
        key=f"lang_toggle_{key}",
        label_visibility="collapsed"
    )

    new_lang = "mr" if selected == "मराठी" else "en"
    if new_lang != current_lang:
        st.session_state.lang = new_lang
        st.rerun()
