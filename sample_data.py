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

# Detailed Crop Guidance Knowledge Base (Module 2)
# Organized by stage: Sowing/Planting, Vegetative, Flowering/Fruiting, Harvesting
CROP_GUIDES = {
    "Grapes": {
        "marathi_name": "द्राक्ष (थॉमसन सिडलेस)",
        "display_name": "Grapes - Thomson Seedless (द्राक्ष)",
        "season": "Rabi Season (रब्बी हंगाम - October to March)",
        "recommended_soil": "Well-drained light-to-medium black soil with pH 6.5 - 7.5",
        "stages": [
            {
                "stage_name": "1. Forward Pruning & Sprouting (गोडी छाटणी व फूट अवस्था)",
                "duration": "Day 1 to 25 after pruning (ऑक्टोबर)",
                "fertilizer": "Basal dose: SSP (200 kg/acre) + MOP (100 kg/acre) + 5 tons FYM (शेणखत). Apply 12:61:00 (MAP) 5 kg/acre through drip for root development.",
                "irrigation": "Heavy flood soaking immediately after pruning, followed by controlled drip irrigation (18-22 Litres/vine/day).",
                "pest_disease": "Dormex (Hydrogen Cyanamide 35-40 ml/L) application on buds for uniform sprouting. Bordeaux paste (१०% बोर्डो पेस्ट) on pruning cuts to seal wounds.",
                "pro_tip": "Do not skip Bordeaux paste on fresh cuts; it prevents fungal die-back and trunk disease."
            },
            {
                "stage_name": "2. Vegetative Canopy & Shoot Growth (शाकीय वाढ व शेंडा व्यवस्थापन)",
                "duration": "Day 26 to 50",
                "fertilizer": "Foliar spray of 19:19:19 (3 g/L) + Zinc chelate (0.5 g/L) + Boron (1 g/L) for vigorous shoot growth and healthy cluster emergence.",
                "irrigation": "Moderate drip irrigation (22-26 Litres/vine/day) depending on pan evaporation and soil moisture.",
                "pest_disease": "Watch for Flea Beetle (उडद्या भुंगा) on tender leaves. Spray Sulfur 80% WP (2 g/L) to prevent early Powdery Mildew (भुरी).",
                "pro_tip": "Perform timely sub-shoot pinching (शेंडा खुडणे) at 5 leaves above the top bunch to divert energy into cluster development."
            },
            {
                "stage_name": "3. Flowering & Berry Setting (फुलधारणा व मणी सेटिंग/विकास)",
                "duration": "Day 51 to 85",
                "fertilizer": "Drip application of 0:52:34 (MKP - 5 kg/acre) + Calcium Nitrate (4 kg/acre). Spray 0:52:34 + Micronutrients.",
                "irrigation": "Strictly reduce irrigation during 80% bloom stage to prevent flower dropping (कळी गळ). Increase water gradually after berry setting.",
                "pest_disease": "High risk of Downy Mildew (डाऊनी मिल्ड्यू) during cloudy or humid weather. Spray preventive bio-agent Trichoderma or Copper-based fungicides. Blue sticky traps for Thrips.",
                "pro_tip": "First GA3 (Gibberellic Acid) berry elongation dipping at 3-4 mm berry size (15 ppm) for optimal export-grade berry stretch."
            },
            {
                "stage_name": "4. Berry Softening, Sugar Development & Harvest (मणी मऊ होणे, साखर भरणे व काढणी)",
                "duration": "Day 86 to 135 (जानेवारी - मार्च)",
                "fertilizer": "Sulphate of Potash (0:0:50) 6 kg/acre via drip to enhance Berry Brix (साखरेचे प्रमाण - target 16-18° Brix) and natural luster.",
                "irrigation": "Taper off irrigation 7-10 days before harvest to avoid berry cracking (मणी तडकणे) and improve shelf-life.",
                "pest_disease": "Maintain strict Pre-Harvest Interval (PHI - कीटकनाशक तुटवडा कालावधी) of at least 20 days. No chemical sprays during harvest window.",
                "pro_tip": "Harvest early in the morning (6 AM to 10 AM) to maintain berry coolness and prevent post-harvest shrinkage."
            }
        ]
    },
    "Onion": {
        "marathi_name": "कांदा (गावरान / फुर्सुंगी)",
        "display_name": "Onion - Gavran / Fursungi (कांदा)",
        "season": "Late Kharif / Rabi (रांगडा व रब्बी हंगाम - Oct to April)",
        "recommended_soil": "Medium black or sandy loam soil rich in organic carbon with good drainage",
        "stages": [
            {
                "stage_name": "1. Nursery Sowing & Field Transplanting (रोपवाटिका व पुनर्लागवड)",
                "duration": "Day 1 to 45 (रोप) & Transplanting",
                "fertilizer": "Basal dose: 10:26:26 (50 kg/acre) + Single Super Phosphate (50 kg/acre) + 10 tons well-decomposed FYM.",
                "irrigation": "Light irrigation before transplanting; immediate light irrigation after planting 6-7 week old seedlings.",
                "pest_disease": "Seed treatment with Trichoderma viride (5 g/kg seed). Dip seedling roots in Carbendazim (1 g/L) solution for 15 minutes before planting to prevent damping-off.",
                "pro_tip": "Transplant seedlings at 15 cm x 10 cm spacing on raised beds (गादीवाफा) for 25% higher yield and uniform bulb sizing."
            },
            {
                "stage_name": "2. Vegetative Growth & Foliage Development (शाकीय वाढ व पातीची जोमदार वाढ)",
                "duration": "Day 15 to 45 after transplanting",
                "fertilizer": "Top dress with Urea (25 kg/acre) + Sulphur 90% granules (10 kg/acre). Sulphur is critical for onion pungency and storage firmness.",
                "irrigation": "Irrigate at 8-10 day intervals in medium soil; avoid continuous standing water to prevent root rot.",
                "pest_disease": "Thrips (फुलकिडे/मावा) attack causes silver curling of leaves. Install 15 yellow/blue sticky traps per acre. Spray Neem oil (1500 ppm, 3 ml/L) or Fipronil 5% SC if infestation rises.",
                "pro_tip": "Keep the field free of weeds during the first 40 days as onion has shallow fibrous roots that cannot compete with weeds."
            },
            {
                "stage_name": "3. Bulb Initiation & Swelling (कांदा फुगवण व पोसणे)",
                "duration": "Day 46 to 85 after transplanting",
                "fertilizer": "Stop Nitrogen (Urea) completely to prevent thick-neck bulbs (डेंगळे/जाड मान). Apply 0:52:34 (5 kg/acre) + 0:0:50 (5 kg/acre) through fertigation or spray.",
                "irrigation": "Maintain steady, uniform soil moisture. Avoid sudden heavy watering after dry gaps, which causes bulb splitting (कांदा फुटणे).",
                "pest_disease": "Purple Blotch (जांभळा करपा) and Stemphylium blight. Spray Mancozeb (2.5 g/L) or Tebuconazole (1 ml/L) mixed with sticker (स्प्रेडर).",
                "pro_tip": "Apply micronutrient Boron (20% - 1 g/L) during bulb swelling to give tough outer skins that resist storage rotting."
            },
            {
                "stage_name": "4. Maturity, Field Curing & Storage (पक्वता, काढणी व वाळवणी)",
                "duration": "Day 86 to 110 after transplanting",
                "fertilizer": "No fertilizer. Allow plant nutrients to naturally translocate into the bulb.",
                "irrigation": "Withhold irrigation 12-15 days prior to harvest when 50% of plant necks drop naturally (५०% मान पडणे).",
                "pest_disease": "Ensure bulbs are completely dry before bag packing to stop black mold (Aspergillus niger) in storage chawls.",
                "pro_tip": "Field cure for 3-4 days covering bulbs with cut onion foliage, followed by 10 days of shade curing in a well-ventilated shed."
            }
        ]
    },
    "Soybean": {
        "marathi_name": "सोयाबीन (जेएस ३३५)",
        "display_name": "Soybean - JS 335 (सोयाबीन)",
        "season": "Kharif Season (खरीप हंगाम - June to October)",
        "recommended_soil": "Medium black cotton soil with good water retention and neutral pH",
        "stages": [
            {
                "stage_name": "1. Seed Treatment & Sowing (बियाणे प्रक्रिया व पेरणी)",
                "duration": "Day 1 to 15 (पावसाच्या आगमनानंतर)",
                "fertilizer": "Basal application: Single Super Phosphate (SSP - 100 kg/acre) + MOP (25 kg/acre). SSP supplies essential Sulphur and Phosphorus.",
                "irrigation": "Sow when 75-100 mm rainfall has soaked the topsoil. Rainfed cultivation; ensure drainage furrows every 4-6 rows.",
                "pest_disease": "Treat seed with Rhizobium japonicum (250 g/10 kg seed) + PSB culture + Thiram (3 g/kg seed) to boost nitrogen-fixing nodules.",
                "pro_tip": "Do not sow soybean deeper than 3-4 cm; deep sowing drastically cuts germination percentage."
            },
            {
                "stage_name": "2. Vegetative Growth & Nodulation (शाकीय वाढ व मुळांवरील गाठींची वाढ)",
                "duration": "Day 16 to 40",
                "fertilizer": "Foliar spray of 19:19:19 (5 g/L) at 30 days after sowing if growth is stunted.",
                "irrigation": "Provide one life-saving protective irrigation via sprinkler if Kharif monsoon has a dry spell exceeding 12-14 days.",
                "pest_disease": "Stem Fly (खोडमाशी) and Girdle Beetle (चक्रीभुंगा). Spray Chlorantraniliprole 18.5% SC (3 ml / 10 L water) at first sign of stem girdling.",
                "pro_tip": "Inter-cultivation (कोळपणी) at 20 and 35 days suppresses weeds and creates a soil dust mulch that conserves moisture."
            },
            {
                "stage_name": "3. Flowering & Pod Filling (फुलधारणा व शेंगा भरणे अवस्था)",
                "duration": "Day 41 to 75",
                "fertilizer": "Foliar spray of 0:52:34 (4 g/L) + Boron (1 g/L) at 50% flowering to maximize pod setting and seed weight.",
                "irrigation": "Critical moisture stage. Moisture stress at pod filling severely shrivels seed size and lowers oil content.",
                "pest_disease": "Spodoptera / Leaf eating caterpillar (लष्करी अळी) and Pod Borer. Install 5 pheromone traps per acre; spray Emamectin Benzoate 5% SG (4 g/10 L).",
                "pro_tip": "Never spray chemical insecticides during peak morning bee activity (8 AM - 11 AM) to safeguard natural cross-pollination."
            },
            {
                "stage_name": "4. Pod Maturation & Threshing (शेंगा पक्वता व मळणी)",
                "duration": "Day 76 to 100",
                "fertilizer": "None.",
                "irrigation": "None required.",
                "pest_disease": "Protect harvested crop stacks from unexpected post-monsoon showers (अवकाळी पाऊस) using tarpaulins.",
                "pro_tip": "Thresh when grain moisture is between 12-14% (seed rattles inside pod). High cylinder speed cracks seeds, destroying germination quality."
            }
        ]
    },
    "Sugarcane": {
        "marathi_name": "ऊस (को ८६०३२)",
        "display_name": "Sugarcane - Co 86032 (ऊस)",
        "season": "Suru / Pre-seasonal / Adsali",
        "recommended_soil": "Deep fertile black clay-loam soil with minimum 1 meter depth",
        "stages": [
            {
                "stage_name": "1. Planting & Germination (ऊस बेणे लागवड व उगवण)",
                "duration": "Day 1 to 45",
                "fertilizer": "Basal dose: DAP 50 kg + MOP 50 kg + Urea 25 kg + Zinc Sulphate 10 kg per acre.",
                "irrigation": "Light irrigation at planting; regular light irrigations every 6-8 days until uniform sprouting.",
                "pest_disease": "Sett treatment with Carbendazim (1 g/L) + Chlorpyrifos (2 ml/L) for 15 minutes before planting.",
                "pro_tip": "Use single-eye bud sets with drip irrigation for 30% water saving and better cane thickness."
            },
            {
                "stage_name": "2. Tillering & Formative Stage (फुटवे फुटणे व बाळबांधणी)",
                "duration": "Day 46 to 120",
                "fertilizer": "Apply Urea (50 kg) + SSP (50 kg) + micronutrients during initial earthing-up (बाळबांधणी).",
                "irrigation": "Irrigate at 8-10 day intervals. Maintain continuous ridge moisture.",
                "pest_disease": "Early Shoot Borer (खोडकीड). Install pheromone traps or apply Cartap Hydrochloride granules.",
                "pro_tip": "Perform earthing up (मोठी बांधणी) at 120 days to anchor cane roots against lodging during wind."
            },
            {
                "stage_name": "3. Grand Growth & Cane Elongation (कांड्या सुटणे व मोठी वाढ)",
                "duration": "Day 121 to 270",
                "fertilizer": "Drip fertigation with 12:61:00 and 0:0:50 weekly schedule.",
                "irrigation": "Peak water demand phase (30,000 to 35,000 L/acre/day in summer).",
                "pest_disease": "White grub (हुमणी) and Pyrilla control. Drench Metarhizium anisopliae bio-control agent.",
                "pro_tip": "Detrash dead dry leaves (पाचट काढणे) at 6th and 8th month to improve field aeration and sunlight."
            },
            {
                "stage_name": "4. Cane Ripening & Harvest (पक्वता, साखर भरणे व तोडणी)",
                "duration": "Day 271 to 360",
                "fertilizer": "Stop nitrogen 90 days before harvest. Apply SOP (0:0:50) for sucrose accumulation.",
                "irrigation": "Stop irrigation 15 days before mill cutting.",
                "pest_disease": "Watch for wild boar and rodent damage; clear boundary weeds.",
                "pro_tip": "Cut cane at ground level (मुळाशी तोडणी) because bottom internodes hold the highest sugar concentration."
            }
        ]
    }
}

# Interactive task reminders checklist synced to farmer's crops (Module 2)
SAMPLE_CROP_TASKS = [
    {
        "id": "TSK-01",
        "crop": "Grapes",
        "title": "Bordeaux paste application on fresh pruning wounds (बोर्डो पेस्ट लावणे)",
        "stage": "Forward Pruning",
        "due_date": "Within 48 hours",
        "priority": "High",
        "status": True
    },
    {
        "id": "TSK-02",
        "crop": "Grapes",
        "title": "Preventive spray of 80% Wettable Sulphur (भुरी प्रतिबंधक सल्फर फवारणी)",
        "stage": "Canopy Growth",
        "due_date": "Next 3 Days",
        "priority": "High",
        "status": False
    },
    {
        "id": "TSK-03",
        "crop": "Grapes",
        "title": "Drip application of 0:52:34 MKP + Calcium Nitrate (0:52:34 खताचा डोस)",
        "stage": "Flowering / Setting",
        "due_date": "This Week",
        "priority": "Medium",
        "status": False
    },
    {
        "id": "TSK-04",
        "crop": "Onion",
        "title": "Seedling root dip in Trichoderma & Carbendazim before transplanting",
        "stage": "Transplanting",
        "due_date": "Immediate",
        "priority": "High",
        "status": True
    },
    {
        "id": "TSK-05",
        "crop": "Onion",
        "title": "Install 15 Yellow & Blue sticky traps per acre for Thrips (चिकट सापळे लावणे)",
        "stage": "Vegetative Growth",
        "due_date": "In 5 Days",
        "priority": "Medium",
        "status": False
    },
    {
        "id": "TSK-06",
        "crop": "Onion",
        "title": "Foliar spray of Sulphur 90% + Micronol for leaf strength and bulb pungency",
        "stage": "Vegetative Growth",
        "due_date": "Next Week",
        "priority": "Medium",
        "status": False
    },
    {
        "id": "TSK-07",
        "crop": "Soybean",
        "title": "Post-harvest threshing and bag moisture check (धान्यातील ओलावा तपासणी - १२-१४%)",
        "stage": "Harvesting",
        "due_date": "Pending",
        "priority": "Low",
        "status": True
    }
]

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

# Realistic nearby agricultural services across Nashik district talukas (Module 4)
SAMPLE_SERVICES = [
    {
        "id": "SRV-01",
        "name": "Dr. Anand Kulkarni - Govt Veterinary Hospital & Emergency Clinic",
        "category": "Veterinary Doctors & Emergency (पशुवैद्यकीय सेवा)",
        "category_key": "veterinary",
        "taluka": "Niphad (निफाड)",
        "district": "Nashik",
        "location": "Niphad Town Main Road, Near Panchayat Samiti (4.2 km)",
        "phone": "+91 94222 88411",
        "timings": "9:00 AM - 6:00 PM (Emergency 24x7)",
        "speciality": "Cattle vaccination (FMD/HS/BQ), artificial insemination, livestock emergency surgery & deworming",
        "rating": 4.9,
        "verified": True
    },
    {
        "id": "SRV-02",
        "name": "Kisan Krishi Seva Kendra (बियाणे व खते केंद्र)",
        "category": "Seeds & Fertilizer Shops (बियाणे व खते केंद्र)",
        "category_key": "seeds_fertilizers",
        "taluka": "Niphad (निफाड)",
        "district": "Nashik",
        "location": "Pimpalgaon APMC Market Yard Gate 2 (1.8 km)",
        "phone": "+91 98230 45678",
        "timings": "8:30 AM - 8:30 PM",
        "speciality": "Certified onion & wheat seeds, water-soluble drip fertilizers (19:19:19, 0:52:34), bio-fungicides",
        "rating": 4.7,
        "verified": True
    },
    {
        "id": "SRV-03",
        "name": "Sahyadri Agro Machinery Custom Hiring Centre",
        "category": "Machinery & Equipment Rental (कृषी अवजारे भाडेतत्त्वावर)",
        "category_key": "machinery",
        "taluka": "Niphad (निफाड)",
        "district": "Nashik",
        "location": "Ozar Airport Road, Niphad (6.5 km)",
        "phone": "+91 97654 32109",
        "timings": "7:00 AM - 7:00 PM",
        "speciality": "Mini tractor rental (24 HP orchard model), boom sprayers for vineyards, rotavator, laser land leveler",
        "rating": 4.8,
        "verified": True
    },
    {
        "id": "SRV-04",
        "name": "Shree Ganesh Animal Fodder & Cattle Feed Traders",
        "category": "Fodder & Cattle Feed (पशुखाद्य व वैरण)",
        "category_key": "fodder",
        "taluka": "Niphad (निफाड)",
        "district": "Nashik",
        "location": "Niphad Phata Highway Junction (3.1 km)",
        "phone": "+91 99215 67890",
        "timings": "8:00 AM - 8:00 PM",
        "speciality": "Corn silage bales (मका सायलेज), high-protein cotton cake (सरकी पेंड), mineral mixture bags, dry straw",
        "rating": 4.6,
        "verified": True
    },
    {
        "id": "SRV-05",
        "name": "MahaAgri Soil & Water Testing Laboratory",
        "category": "Agricultural Service Centres (कृषी सेवा व माती परीक्षण केंद्र)",
        "category_key": "service_centres",
        "taluka": "Nashik (नाशिक)",
        "district": "Nashik",
        "location": "KVK Yashwantrao Chavan Open University Campus (11.5 km)",
        "phone": "+91 94231 77650",
        "timings": "10:00 AM - 5:00 PM (Monday-Saturday)",
        "speciality": "Complete 14-parameter soil test (NPK, Organic Carbon, Micro-nutrients, pH, EC) & irrigation water testing",
        "rating": 4.9,
        "verified": True
    },
    {
        "id": "SRV-06",
        "name": "Dr. Vikas Deshmukh - Mobile Cattle Clinic & AI Centre",
        "category": "Veterinary Doctors & Emergency (पशुवैद्यकीय सेवा)",
        "category_key": "veterinary",
        "taluka": "Dindori (दिंडोरी)",
        "district": "Nashik",
        "location": "Dindori Main Chowk (14.0 km - Doorstep Farm Visits)",
        "phone": "+91 98902 33445",
        "timings": "8:00 AM - 8:00 PM (Call for Farm Visit)",
        "speciality": "Doorstep cattle health checkup, sexed semen artificial insemination, mastitis treatment",
        "rating": 4.8,
        "verified": True
    },
    {
        "id": "SRV-07",
        "name": "Baliraja Krishi Seva Kendra & Bio-Pesticides",
        "category": "Seeds & Fertilizer Shops (बियाणे व खते केंद्र)",
        "category_key": "seeds_fertilizers",
        "taluka": "Chandwad (चांदवड)",
        "district": "Nashik",
        "location": "Chandwad Bus Stand Road (18.2 km)",
        "phone": "+91 98229 11223",
        "timings": "8:30 AM - 8:00 PM",
        "speciality": "Organic bio-stimulants, sticky traps, pheromone lures, certified tomato and onion seeds",
        "rating": 4.5,
        "verified": True
    },
    {
        "id": "SRV-08",
        "name": "Panchavati Agro Drone Spraying & Tech Services",
        "category": "Agricultural Service Centres (कृषी सेवा व माती परीक्षण केंद्र)",
        "category_key": "service_centres",
        "taluka": "Nashik (नाशिक)",
        "district": "Nashik",
        "location": "Amrutdham, Panchavati, Nashik (16.0 km)",
        "phone": "+91 98500 66778",
        "timings": "6:00 AM - 6:00 PM",
        "speciality": "Agricultural drone spraying for vineyards & orchards, 10 acres covered in 2 hours, uniform canopy coverage",
        "rating": 4.9,
        "verified": True
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

    if "crop_tasks" not in st.session_state:
        st.session_state.crop_tasks = copy.deepcopy(SAMPLE_CROP_TASKS)

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
    st.session_state.crop_tasks = copy.deepcopy(SAMPLE_CROP_TASKS)
    st.session_state.livestock_records = copy.deepcopy(SAMPLE_LIVESTOCK)
    st.session_state.nearby_services = copy.deepcopy(SAMPLE_SERVICES)
    st.session_state.marketplace_listings = copy.deepcopy(SAMPLE_MARKETPLACE)
    st.session_state.farm_expenses = copy.deepcopy(SAMPLE_EXPENSES)
