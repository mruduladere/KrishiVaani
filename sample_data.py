"""
sample_data.py - Realistic Sample Data for KrishiVaani (Voice of Agriculture)
Pre-loaded in-memory data for Maharashtra farmers to make the prototype feel alive immediately.
No external database required (pure Python dictionaries and session state).
"""

import copy

# Realistic sample profile for a progressive farmer in Maharashtra (Niphad, Nashik)
SAMPLE_FARMER = {
    "name": "Ramesh Tukaram Patil (रमेश तुकाराम पाटील)",
    "phone": "+91 98220 12345",
    "email": "ramesh.patil.krishi@gmail.com",
    "village": "Pimpalgaon Baswant (पिंपळगाव बसवंत)",
    "taluka": "Niphad (निफाड)",
    "district": "Nashik (नाशिक)",
    "state": "Maharashtra",
    "pincode": "422209",
    "land_size_acres": 4.5,
    "soil_type": "Medium Black Soil (काळी मध्यम जमीन)",
    "irrigation_type": "Drip Irrigation & Farm Pond (ठिबक सिंचन व शेततळे)",
    "primary_language": "Marathi & English",
    "crops_grown": [
        "Grapes - Thomson Seedless (द्राक्ष)",
        "Onion - Gavran / Fursungi (कांदा)",
        "Soybean - JS 335 (सोयाबीन)"
    ],
    "livestock_summary": {
        "gir_cows": 2,
        "murrah_buffaloes": 1,
        "goats": 4,
        "total_animals": 7,
        "daily_milk_litres": 22.0
    }
}

# Realistic livestock records (ready for Module 6)
SAMPLE_LIVESTOCK = [
    {
        "tag_id": "MH-NSK-0101",
        "name": "Gauri (गौरी)",
        "type": "Cow",
        "breed": "Gir (गीर)",
        "age_years": 4.5,
        "daily_milk_yield_litres": 12.0,
        "vaccination_history": [
            {"vaccine": "Foot & Mouth Disease (FMD)", "date_given": "2026-05-10", "due_date": "2026-11-10", "status": "Overdue"},
            {"vaccine": "Brucellosis", "date_given": "2025-06-15", "due_date": "2026-06-15", "status": "Completed"}
        ]
    },
    {
        "tag_id": "MH-NSK-0102",
        "name": "Lakshmi (लक्ष्मी)",
        "type": "Cow",
        "breed": "Gir (गीर)",
        "age_years": 3.0,
        "daily_milk_yield_litres": 10.0,
        "vaccination_history": [
            {"vaccine": "Foot & Mouth Disease (FMD)", "date_given": "2026-09-01", "due_date": "2027-03-01", "status": "Up-to-date"},
            {"vaccine": "Hemorrhagic Septicemia (HS)", "date_given": "2026-07-20", "due_date": "2027-07-20", "status": "Up-to-date"}
        ]
    },
    {
        "tag_id": "MH-NSK-0201",
        "name": "Kaveri (कावेरी)",
        "type": "Buffalo",
        "breed": "Murrah (मुऱ्हा)",
        "age_years": 5.0,
        "daily_milk_yield_litres": 9.5,
        "vaccination_history": [
            {"vaccine": "Black Quarter (BQ)", "date_given": "2026-04-12", "due_date": "2026-10-12", "status": "Overdue"},
            {"vaccine": "Foot & Mouth Disease (FMD)", "date_given": "2026-08-15", "due_date": "2027-02-15", "status": "Up-to-date"}
        ]
    }
]

# Realistic nearby agricultural services in Niphad/Nashik region (ready for Module 4)
SAMPLE_SERVICES = [
    {
        "id": "SRV-01",
        "name": "Dr. Anand Kulkarni - Govt Veterinary Dispensary",
        "category": "Veterinary Services & Emergency",
        "location": "Niphad Town Main Road (4.2 km)",
        "phone": "+91 94222 88411",
        "timings": "9:00 AM - 5:00 PM (Emergency 24x7)",
        "speciality": "Cattle vaccination, artificial insemination, livestock emergency care",
        "rating": 4.8
    },
    {
        "id": "SRV-02",
        "name": "Kisan Krishi Seva Kendra (बियाणे व खते केंद्र)",
        "category": "Seeds & Fertilizers",
        "location": "Pimpalgaon APMC Market Yard (1.8 km)",
        "phone": "+91 98230 45678",
        "timings": "8:30 AM - 8:00 PM",
        "speciality": "Certified onion seeds, bio-fertilizers, micronutrient spray kits",
        "rating": 4.6
    },
    {
        "id": "SRV-03",
        "name": "Sahyadri Agro Equipment & Custom Hiring Centre",
        "category": "Machinery & Equipment Rental",
        "location": "Ozar Road, Niphad (6.5 km)",
        "phone": "+91 97654 32109",
        "timings": "7:00 AM - 7:00 PM",
        "speciality": "Mini tractor hire, power sprayers, rotavator, boom sprayers for vineyards",
        "rating": 4.7
    },
    {
        "id": "SRV-04",
        "name": "Shree Ganesh Animal Fodder & Feed Traders",
        "category": "Fodder & Cattle Feed",
        "location": "Niphad Phata (3.1 km)",
        "phone": "+91 99215 67890",
        "timings": "8:00 AM - 8:00 PM",
        "speciality": "Dry silage, sugarcane tops, mineral mixture bags, cotton seed cake",
        "rating": 4.5
    },
    {
        "id": "SRV-05",
        "name": "MahaAgri Soil & Water Testing Laboratory",
        "category": "Soil & Testing Lab",
        "location": "Krishi Vigyan Kendra (KVK) Yashwantrao Chavan Campus (11 km)",
        "phone": "+91 94231 77650",
        "timings": "10:00 AM - 5:00 PM (Mon-Sat)",
        "speciality": "NPK, pH, electrical conductivity analysis, water salinity testing",
        "rating": 4.9
    }
]

# Realistic marketplace listings (ready for Module 5)
SAMPLE_MARKETPLACE = [
    {
        "id": "MKT-101",
        "crop_name": "Red Onion (गावरान लाल कांदा)",
        "variety": "Nashik Garwa Quality",
        "quantity_quintals": 55,
        "expected_price_per_quintal": 1950,
        "seller_name": "Ramesh Tukaram Patil",
        "seller_phone": "+91 98220 12345",
        "location": "Pimpalgaon Baswant, Nashik",
        "harvest_date": "2026-10-25",
        "status": "Available",
        "notes": "Graded, dry, well-cured medium-to-large size bulbs suitable for storage/transport."
    },
    {
        "id": "MKT-102",
        "crop_name": "Export Grade Grapes (थॉमसन सिडलेस द्राक्ष)",
        "variety": "Thomson Seedless",
        "quantity_quintals": 30,
        "expected_price_per_quintal": 6200,
        "seller_name": "Ramesh Tukaram Patil",
        "seller_phone": "+91 98220 12345",
        "location": "Pimpalgaon Baswant, Nashik",
        "harvest_date": "Expected Feb 2027",
        "status": "Advance Booking",
        "notes": "18mm+ berry size, residue-free spray schedule maintained."
    },
    {
        "id": "MKT-103",
        "crop_name": "Certified Soybean Seed (सोयाबीन बियाणे)",
        "variety": "JS 335 (Graded)",
        "quantity_quintals": 18,
        "expected_price_per_quintal": 4400,
        "seller_name": "Sunil Bhaurao Gaikwad",
        "seller_phone": "+91 98901 22334",
        "location": "Chandwad, Nashik",
        "harvest_date": "2026-10-15",
        "status": "Available",
        "notes": "High germination test passed (85%+), moisture 10%."
    }
]

# Realistic categorized farm expenses (ready for Module 7)
SAMPLE_EXPENSES = [
    {
        "id": "EXP-001",
        "date": "2026-10-05",
        "month": "October 2026",
        "season": "Rabi 2026-27",
        "crop": "Onion",
        "category": "Seeds & Seedlings",
        "description": "Purchased 4 kg certified Fursungi onion seed packets",
        "amount": 4800,
        "payment_mode": "UPI"
    },
    {
        "id": "EXP-002",
        "date": "2026-10-14",
        "month": "October 2026",
        "season": "Rabi 2026-27",
        "crop": "Grapes",
        "category": "Fertilizers & Nutrients",
        "description": "Water-soluble 0:52:34 and micronutrient drip application kit",
        "amount": 7600,
        "payment_mode": "Cash"
    },
    {
        "id": "EXP-003",
        "date": "2026-10-22",
        "month": "October 2026",
        "season": "Rabi 2026-27",
        "crop": "Grapes",
        "category": "Labor & Pruning",
        "description": "Forward pruning labour charges (6 workers for 2 days)",
        "amount": 7200,
        "payment_mode": "Cash"
    },
    {
        "id": "EXP-004",
        "date": "2026-11-02",
        "month": "November 2026",
        "season": "Rabi 2026-27",
        "crop": "Livestock / Dairy",
        "category": "Livestock Feed & Healthcare",
        "description": "5 bags cattle feed pellet (Godrej Agrovet) + mineral mixture",
        "amount": 6250,
        "payment_mode": "UPI"
    },
    {
        "id": "EXP-005",
        "date": "2026-11-08",
        "month": "November 2026",
        "season": "Rabi 2026-27",
        "crop": "Onion",
        "category": "Labor & Pruning",
        "description": "Nursery bed transplanting labor (4 women workers)",
        "amount": 2800,
        "payment_mode": "Cash"
    },
    {
        "id": "EXP-006",
        "date": "2026-11-12",
        "month": "November 2026",
        "season": "Rabi 2026-27",
        "crop": "Grapes",
        "category": "Pesticides & Bio-agents",
        "description": "Downy mildew preventive bio-fungicide spray (Trichoderma + Copper)",
        "amount": 3400,
        "payment_mode": "UPI"
    }
]


def init_session_data(st):
    """
    Initializes runtime in-memory session data inside Streamlit session state.
    This fulfills the strict NO-DATABASE requirement while ensuring any farmer edits
    remain reactive and intact during their session.
    """
    if "farmer_profile" not in st.session_state:
        st.session_state.farmer_profile = copy.deepcopy(SAMPLE_FARMER)

    if "livestock_records" not in st.session_state:
        st.session_state.livestock_records = copy.deepcopy(SAMPLE_LIVESTOCK)

    if "nearby_services" not in st.session_state:
        st.session_state.nearby_services = copy.deepcopy(SAMPLE_SERVICES)

    if "marketplace_listings" not in st.session_state:
        st.session_state.marketplace_listings = copy.deepcopy(SAMPLE_MARKETPLACE)

    if "farm_expenses" not in st.session_state:
        st.session_state.farm_expenses = copy.deepcopy(SAMPLE_EXPENSES)

    if "active_nav" not in st.session_state:
        st.session_state.active_nav = "dashboard"


def reset_to_defaults(st):
    """Allows resetting session data to initial sample values."""
    st.session_state.farmer_profile = copy.deepcopy(SAMPLE_FARMER)
    st.session_state.livestock_records = copy.deepcopy(SAMPLE_LIVESTOCK)
    st.session_state.nearby_services = copy.deepcopy(SAMPLE_SERVICES)
    st.session_state.marketplace_listings = copy.deepcopy(SAMPLE_MARKETPLACE)
    st.session_state.farm_expenses = copy.deepcopy(SAMPLE_EXPENSES)
