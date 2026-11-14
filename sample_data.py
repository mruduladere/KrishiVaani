"""
sample_data.py - Realistic Bilingual Sample Data for KrishiVaani (Voice of Agriculture)
Pre-loaded in-memory data for Maharashtra farmers designed with Strict Pure-Language Separation:
- When lang == 'en': 100% pure English (no Devanagari or parentheses).
- When lang == 'mr': 100% pure Marathi (no raw English or mixed brackets).
Strictly NO external database required (pure Python dictionaries and session state).
"""

import copy

# Realistic sample profile for a progressive farmer in Maharashtra (Niphad, Nashik)
SAMPLE_FARMER = {
    "name": {
        "en": "Ramesh Tukaram Patil",
        "mr": "रमेश तुकाराम पाटील"
    },
    "phone": "+91 98220 12345",
    "pin": "1234",
    "email": "ramesh.patil.krishi@gmail.com",
    "village": {
        "en": "Pimpalgaon Baswant",
        "mr": "पिंपळगाव बसवंत"
    },
    "taluka": {
        "en": "Niphad",
        "mr": "निफाड"
    },
    "district": {
        "en": "Nashik",
        "mr": "नाशिक"
    },
    "state": {
        "en": "Maharashtra",
        "mr": "महाराष्ट्र"
    },
    "pincode": "422209",
    "land_size_acres": 4.5,
    "soil_type": {
        "en": "Medium Black Soil",
        "mr": "काळी मध्यम जमीन"
    },
    "irrigation_type": {
        "en": "Drip Irrigation & Farm Pond",
        "mr": "ठिबक सिंचन व शेततळे"
    },
    "primary_language": {
        "en": "Marathi & English",
        "mr": "मराठी व इंग्रजी"
    },
    "crops_grown": [
        {"key": "Grapes", "en": "Thomson Seedless Grapes", "mr": "थॉमसन सिडलेस द्राक्ष"},
        {"key": "Onion", "en": "Gavran Red Onion", "mr": "गावरान लाल कांदा"},
        {"key": "Soybean", "en": "JS 335 Soybean", "mr": "जेएस ३३५ सोयाबीन"}
    ],
    "livestock_summary": {
        "gir_cows": 2,
        "murrah_buffaloes": 1,
        "goats": 4,
        "total_animals": 7,
        "daily_milk_litres": 39.5
    }
}

# Pre-registered sample farmer accounts for authentication
SAMPLE_REGISTERED_FARMERS = {
    "9822012345": SAMPLE_FARMER,
    "+919822012345": SAMPLE_FARMER,
    "+91 98220 12345": SAMPLE_FARMER,
}

# Detailed Crop Guidance Knowledge Base (Module 2) - Pure English & Pure Marathi
CROP_GUIDES = {
    "Grapes": {
        "display_name": {
            "en": "Thomson Seedless Grapes",
            "mr": "थॉमसन सिडलेस द्राक्ष"
        },
        "season": {
            "en": "Rabi Season (October to March)",
            "mr": "रब्बी हंगाम (ऑक्टोबर ते मार्च)"
        },
        "recommended_soil": {
            "en": "Well-drained light-to-medium black soil with pH 6.5 - 7.5",
            "mr": "उत्तम निचरा होणारी हलकी ते मध्यम काळी जमीन, सामू ६.५ - ७.५"
        },
        "stages": [
            {
                "stage_name": {
                    "en": "Stage 1: Forward Pruning & Sprouting",
                    "mr": "टप्पा १: गोडी छाटणी व फूट अवस्था"
                },
                "duration": {
                    "en": "Day 1 to 25 after pruning",
                    "mr": "छाटणीनंतर १ ते २५ दिवस"
                },
                "fertilizer": {
                    "en": "Basal dose: SSP (200 kg/acre) + MOP (100 kg/acre) + 5 tons FYM. Apply 12:61:00 MAP 5 kg/acre via drip for root development.",
                    "mr": "पायाभूत खत: सिंगल सुपर फॉस्फेट (२०० किलो/एकर) + म्युरेट ऑफ पोटॅश (१०० किलो/एकर) + ५ टन शेणखत. मुळांच्या जोमदार वाढीसाठी १२:६१:०० (५ किलो/एकर) ठिबकद्वारे द्या."
                },
                "irrigation": {
                    "en": "Heavy flood soaking immediately after pruning, followed by controlled drip irrigation (18-22 Litres/vine/day).",
                    "mr": "छाटणीनंतर लगेच भरपूर पाणी भिजवून द्या, त्यानंतर नियंत्रित ठिबक सिंचन (१८-२२ लिटर/वेल/दिवस)."
                },
                "pest_disease": {
                    "en": "Dormex (Hydrogen Cyanamide 35-40 ml/L) application on buds for uniform sprouting. Bordeaux paste on pruning cuts to seal wounds.",
                    "mr": "एकसारख्या फुटीसाठी डोळ्यांवर डॉरमेक्स (३५-४० मिली/लिटर). छाटणीच्या ताज्या जखमांवर १०% बोर्डो पेस्टचा लेप द्या."
                },
                "pro_tip": {
                    "en": "Do not skip Bordeaux paste on fresh cuts; it prevents fungal die-back and trunk disease.",
                    "mr": "ताज्या छाटणीच्या जखमांवर बोर्डो पेस्ट लावणे अत्यंत आवश्यक आहे; यामुळे बुरशीजन्य रोग व मर रोगाचा प्रादुर्भाव टळतो."
                }
            },
            {
                "stage_name": {
                    "en": "Stage 2: Vegetative Canopy & Shoot Growth",
                    "mr": "टप्पा २: शाकीय वाढ व शेंडा व्यवस्थापन"
                },
                "duration": {
                    "en": "Day 26 to 50",
                    "mr": "दिवस २६ ते ५०"
                },
                "fertilizer": {
                    "en": "Foliar spray of 19:19:19 (3 g/L) + Zinc chelate (0.5 g/L) + Boron (1 g/L) for vigorous shoot growth and healthy clusters.",
                    "mr": "१९:१९:१९ (३ ग्रॅम/लिटर) + चिलेटेड झिंक (०.५ ग्रॅम/लिटर) + बोरॉन (१ ग्रॅम/लिटर) फवारणी, ज्यामुळे निरोगी घड व पानांची वाढ होते."
                },
                "irrigation": {
                    "en": "Moderate drip irrigation (22-26 Litres/vine/day) depending on pan evaporation and soil moisture.",
                    "mr": "बाष्पीभवन आणि जमिनीतील ओलाव्यानुसार मध्यम ठिबक सिंचन (२२-२६ लिटर/वेल/दिवस)."
                },
                "pest_disease": {
                    "en": "Watch for Flea Beetle on tender leaves. Spray Sulfur 80% WP (2 g/L) to prevent early Powdery Mildew.",
                    "mr": "कोवळ्या पानांवर उडद्या भुंग्याचा प्रादुर्भाव तपासा. भुरी रोगाच्या प्रतिबंधासाठी ८०% पाण्यात विरघळणारे सल्फर (२ ग्रॅम/लिटर) फवारा."
                },
                "pro_tip": {
                    "en": "Perform timely sub-shoot pinching at 5 leaves above the top bunch to divert energy into cluster development.",
                    "mr": "घडावरील ५ पानांनंतर शेंडा खुडणी (पिंचिंग) वेळेवर करा, ज्यामुळे अन्नद्रव्यांचा प्रवाह थेट घड विकासाकडे वळतो."
                }
            },
            {
                "stage_name": {
                    "en": "Stage 3: Flowering & Berry Setting",
                    "mr": "टप्पा ३: फुलधारणा व मणी सेटिंग"
                },
                "duration": {
                    "en": "Day 51 to 85",
                    "mr": "दिवस ५१ ते ८५"
                },
                "fertilizer": {
                    "en": "Drip application of 0:52:34 MKP (5 kg/acre) + Calcium Nitrate (4 kg/acre). Spray 0:52:34 + Micronutrients.",
                    "mr": "ठिबकद्वारे ०:५२:३४ (५ किलो/एकर) + कॅल्शियम नायट्रेट (४ किलो/एकर). वरून ०:५२:३४ व सूक्ष्मअन्नद्रव्यांची फवारणी."
                },
                "irrigation": {
                    "en": "Strictly reduce irrigation during 80% bloom stage to prevent flower drop. Increase water gradually after berry set.",
                    "mr": "८०% फुलधारणा अवस्थेत पाणी अत्यंत कमी करा जेणेकरून कळीगळ टळेल. मणी धरल्यानंतर हळूहळू पाणी वाढवा."
                },
                "pest_disease": {
                    "en": "High risk of Downy Mildew during humid weather. Spray preventive bio-agent Trichoderma or Copper fungicides. Sticky traps for Thrips.",
                    "mr": "ढगाळ हवामानात डाऊनी मिल्ड्यूचा धोका जास्त असतो. प्रतिबंधक उपाय म्हणून ट्रायकोडर्मा किंवा कॉपर बुरशीनाशक फवारा. फुलकिड्यांसाठी चिकट सापळे लावा."
                },
                "pro_tip": {
                    "en": "First GA3 dipping at 3-4 mm berry size (15 ppm) for optimal export-grade berry elongation.",
                    "mr": "निर्यातक्षम लांबीसाठी मणी ३-४ मिमी आकाराचे असताना पहिली जीए३ (१५ पीपीएम) डीपिंग वेळेत पूर्ण करा."
                }
            },
            {
                "stage_name": {
                    "en": "Stage 4: Berry Softening, Sugar Development & Harvest",
                    "mr": "टप्पा ४: साखर भरणे, पक्वता व काढणी"
                },
                "duration": {
                    "en": "Day 86 to 135 (January to March)",
                    "mr": "दिवस ८६ ते १३५ (जानेवारी ते मार्च)"
                },
                "fertilizer": {
                    "en": "Sulphate of Potash (0:0:50) 6 kg/acre via drip to enhance Berry Brix (target 16-18° Brix) and natural luster.",
                    "mr": "मण्यांत गोडवा (१६-१८ ब्रिक्स) आणि चमकदारपणा आणण्यासाठी पोटॅश ०:०:५० (६ किलो/एकर) ठिबकद्वारे द्या."
                },
                "irrigation": {
                    "en": "Taper off irrigation 7-10 days before harvest to avoid berry cracking and improve shelf-life.",
                    "mr": "काढणीपूर्वी ७-१० दिवस पाणी पूर्णपणे बंद करा, ज्यामुळे मणी तडकणे टळते व साठवणूक क्षमता वाढते."
                },
                "pest_disease": {
                    "en": "Maintain strict Pre-Harvest Interval (PHI) of at least 20 days. No chemical sprays during harvest window.",
                    "mr": "काढणीपूर्व तुटवडा कालावधी (किमान २० दिवस) काटेकोरपणे पाळा. काढणीच्या दिवसांत कोणतीही रासायनिक फवारणी करू नका."
                },
                "pro_tip": {
                    "en": "Harvest early in the morning (6 AM to 10 AM) to maintain berry coolness and prevent post-harvest shrinkage.",
                    "mr": "काढणी सकाळी ६ ते १० च्या दरम्यान करा जेणेकरून फळांचा ताजेपणा टिकून राहतो आणि वजन घटत नाही."
                }
            }
        ]
    },
    "Onion": {
        "display_name": {
            "en": "Gavran Red Onion",
            "mr": "गावरान लाल कांदा"
        },
        "season": {
            "en": "Rabi Season (October to April)",
            "mr": "रब्बी हंगाम (ऑक्टोबर ते एप्रिल)"
        },
        "recommended_soil": {
            "en": "Medium black or sandy loam soil with good drainage and rich organic carbon",
            "mr": "उत्तम निचरा होणारी सेंद्रिय कर्बयुक्त मध्यम काळी किंवा गाळाची जमीन"
        },
        "stages": [
            {
                "stage_name": {
                    "en": "Stage 1: Nursery Sowing & Field Transplanting",
                    "mr": "टप्पा १: रोपवाटिका व पुनर्लागवड"
                },
                "duration": {
                    "en": "Day 1 to 45 (Nursery) & Transplanting",
                    "mr": "रोपवाटिका १ ते ४५ दिवस व पुनर्लागवड"
                },
                "fertilizer": {
                    "en": "Basal dose: 10:26:26 (50 kg/acre) + Single Super Phosphate (50 kg/acre) + 10 tons well-decomposed FYM.",
                    "mr": "पायाभूत खत: १०:२६:२६ (५० किलो/एकर) + सिंगल सुपर फॉस्फेट (५० किलो/एकर) + १० टन चांगले कुजलेले शेणखत."
                },
                "irrigation": {
                    "en": "Light irrigation before transplanting; immediate light irrigation after planting 6-7 week old seedlings.",
                    "mr": "पुनर्लागवडीपूर्वी हलके पाणी द्या; ६-७ आठवड्यांची निरोगी रोपे लावल्यानंतर लगेच दुसरे हलके पाणी द्या."
                },
                "pest_disease": {
                    "en": "Seed treatment with Trichoderma viride. Dip seedling roots in Carbendazim solution before transplanting to prevent damping-off.",
                    "mr": "बियाण्यावर ट्रायकोडर्मा प्रक्रिया करा. पुनर्लागवडीपूर्वी रोपांची मुळे कार्बेन्डाझिम द्रावणात बुडवून लावा."
                },
                "pro_tip": {
                    "en": "Transplant seedlings at 15 cm x 10 cm spacing on raised beds for 25% higher yield and uniform bulb sizing.",
                    "mr": "गादीवाफ्यावर १५ सेमी x १० सेमी अंतरावर पुनर्लागवड केल्यास २५% जास्त उत्पादन व एकसारखा आकार मिळतो."
                }
            },
            {
                "stage_name": {
                    "en": "Stage 2: Vegetative Growth & Foliage Development",
                    "mr": "टप्पा २: शाकीय वाढ व पातीचा विकास"
                },
                "duration": {
                    "en": "Day 15 to 45 after transplanting",
                    "mr": "पुनर्लागवडीनंतर १५ ते ४५ दिवस"
                },
                "fertilizer": {
                    "en": "Top dress with Urea (25 kg/acre) + Sulphur 90% granules (10 kg/acre). Sulphur ensures onion pungency and storage firmness.",
                    "mr": "युरिया (२५ किलो/एकर) + सल्फर ९०% (१० किलो/एकर) खताचा डोस द्या. सल्फरमुळे कांद्याला घट्टपणा व तिखटपणा येतो."
                },
                "irrigation": {
                    "en": "Irrigate at 8-10 day intervals in medium soil; avoid continuous standing water to prevent root rot.",
                    "mr": "मध्यम जमिनीत ८-१० दिवसांच्या अंतराने पाणी द्या; जमिनीत पाणी साचू देऊ नका जेणेकरून मुळकुज टळेल."
                },
                "pest_disease": {
                    "en": "Thrips attack causes silver curling of leaves. Install 15 yellow/blue sticky traps per acre. Spray Neem oil.",
                    "mr": "फुलकिड्यांमुळे पाने चंदेरी होतात. एकरी १५ पिवळे व निळे चिकट सापळे लावा. निंबोळी अर्क फवारा."
                },
                "pro_tip": {
                    "en": "Keep the field free of weeds during the first 40 days as onion has shallow roots that cannot compete with weeds.",
                    "mr": "पहिल्या ४० दिवसांत शेत तणमुक्त ठेवा कारण कांद्याची मुळे उथळ असतात आणि तणांशी स्पर्धा करू शकत नाहीत."
                }
            },
            {
                "stage_name": {
                    "en": "Stage 3: Bulb Initiation & Swelling",
                    "mr": "टप्पा ३: कांदा फुगवण व पोसणे"
                },
                "duration": {
                    "en": "Day 46 to 85 after transplanting",
                    "mr": "पुनर्लागवडीनंतर ४६ ते ८५ दिवस"
                },
                "fertilizer": {
                    "en": "Stop Nitrogen completely to prevent thick-neck bulbs. Apply 0:52:34 (5 kg/acre) + 0:0:50 (5 kg/acre) via fertigation.",
                    "mr": "कांद्याची मान जाड होणे टाळण्यासाठी युरिया पूर्ण बंद करा. ०:५२:३४ (५ किलो/एकर) + ०:०:५० (५ किलो/एकर) ठिबकद्वारे द्या."
                },
                "irrigation": {
                    "en": "Maintain steady, uniform soil moisture. Avoid sudden heavy watering after dry gaps, which causes bulb splitting.",
                    "mr": "नियमित व समान ओलावा ठेवा. पाण्याचा ताण दिल्यानंतर अचानक भरपूर पाणी दिल्यास कांदा फुटतो (डबल कांदा)."
                },
                "pest_disease": {
                    "en": "Purple Blotch and Stemphylium blight risk. Spray Mancozeb or Tebuconazole mixed with sticking agent.",
                    "mr": "जांभळा करपा रोगाच्या नियंत्रणासाठी मॅनकोझेब किंवा टेब्युकोनॅझोल स्टीकरसह मिसळून फवारा."
                },
                "pro_tip": {
                    "en": "Apply micronutrient Boron during bulb swelling to give tough outer skins that resist storage rotting.",
                    "mr": "कांदा फुगवणीच्या काळात बोरॉन फवारल्यास कांद्याची साल घट्ट होते व चाळीत सड टळते."
                }
            },
            {
                "stage_name": {
                    "en": "Stage 4: Maturity, Field Curing & Storage",
                    "mr": "टप्पा ४: पक्वता, काढणी व साठवणूक"
                },
                "duration": {
                    "en": "Day 86 to 110 after transplanting",
                    "mr": "पुनर्लागवडीनंतर ८६ ते ११० दिवस"
                },
                "fertilizer": {
                    "en": "No chemical fertilizers. Allow nutrients to naturally translocate into the bulb.",
                    "mr": "रासायनिक खते पूर्ण बंद. पानांतील अन्नद्रव्ये नैसर्गिकरीत्या कांद्यामध्ये उतरू द्या."
                },
                "irrigation": {
                    "en": "Withhold irrigation 12-15 days prior to harvest when 50% of plant tops naturally fall over.",
                    "mr": "शेतातील ५०% कांद्याची मान पडल्यानंतर काढणीच्या १२-१५ दिवस आधी पाणी पूर्ण बंद करा."
                },
                "pest_disease": {
                    "en": "Ensure bulbs are completely dry before bag packing to stop black mold in storage chawls.",
                    "mr": "चाळीत साठवणुकीपूर्वी कांदा पूर्ण कोरडा असल्याची खात्री करा, जेणेकरून काळी बुरशी लागत नाही."
                },
                "pro_tip": {
                    "en": "Field cure for 3-4 days covering bulbs with foliage, followed by 10 days of shade curing in a ventilated shed.",
                    "mr": "काढणीनंतर ३-४ दिवस शेतात पातीने कांदा झाकून ठेवा, नंतर हवेशीर शेडमध्ये १० दिवस सावलीत सुकवा."
                }
            }
        ]
    },
    "Soybean": {
        "display_name": {
            "en": "JS 335 Soybean",
            "mr": "जेएस ३३५ सोयाबीन"
        },
        "season": {
            "en": "Kharif Season (June to October)",
            "mr": "खरीप हंगाम (जून ते ऑक्टोबर)"
        },
        "recommended_soil": {
            "en": "Medium black cotton soil with good water retention and neutral pH",
            "mr": "मध्यम काळी कसदार जमीन, उत्तम ओलावा टिकवून ठेवणारी"
        },
        "stages": [
            {
                "stage_name": {
                    "en": "Stage 1: Seed Treatment & Sowing",
                    "mr": "टप्पा १: बीजप्रक्रिया व पेरणी"
                },
                "duration": {
                    "en": "Day 1 to 15 after monsoon arrival",
                    "mr": "पावसाच्या आगमनानंतर १ ते १५ दिवस"
                },
                "fertilizer": {
                    "en": "Basal application: Single Super Phosphate (SSP - 100 kg/acre) + MOP (25 kg/acre). SSP supplies essential Sulphur.",
                    "mr": "पायाभूत खत: सिंगल सुपर फॉस्फेट (१०० किलो/एकर) + म्युरेट ऑफ पोटॅश (२५ किलो/एकर). यामुळे फॉस्फरस व गंधक मिळते."
                },
                "irrigation": {
                    "en": "Sow when 75-100 mm rainfall has thoroughly soaked the topsoil. Rainfed crop; ensure proper drainage channels.",
                    "mr": "किमान ७५-१०० मिमी पाऊस झाल्यानंतरच पेरणी करा. पाण्याचा निचरा होण्यासाठी दर ४-६ ओळींनंतर चर काढा."
                },
                "pest_disease": {
                    "en": "Treat seed with Rhizobium japonicum culture + PSB + Thiram to enhance nitrogen-fixing root nodules.",
                    "mr": "रायझोबियम जिवाणू संवर्धन + पीएसबी + थायरम बुरशीनाशकाची बीजप्रक्रिया आवर्जून करा."
                },
                "pro_tip": {
                    "en": "Do not sow soybean deeper than 3-4 cm; deep sowing drastically cuts seed germination.",
                    "mr": "सोयाबीनची पेरणी ३-४ सेमी पेक्षा जास्त खोल करू नका; खोल पेरल्यास उगवण शक्ती घटते."
                }
            },
            {
                "stage_name": {
                    "en": "Stage 2: Vegetative Growth & Nodulation",
                    "mr": "टप्पा २: शाकीय वाढ व मुळांवरील गाठींची निर्मिती"
                },
                "duration": {
                    "en": "Day 16 to 40",
                    "mr": "दिवस १६ ते ४०"
                },
                "fertilizer": {
                    "en": "Foliar spray of 19:19:19 (5 g/L) at 30 days after sowing if growth is stunted.",
                    "mr": "पेरणीनंतर ३० दिवसांनी पिकाची वाढ समाधानकारक नसल्यास १९:१९:१९ (५ ग्रॅम/लिटर) फवारा."
                },
                "irrigation": {
                    "en": "Provide life-saving protective irrigation via sprinkler if monsoon has a dry spell exceeding 12-14 days.",
                    "mr": "पावसाचा खंड १२-१४ दिवसांपेक्षा जास्त पडल्यास तुषार सिंचनाने एक संरक्षणात्मक पाणी द्या."
                },
                "pest_disease": {
                    "en": "Watch for Stem Fly and Girdle Beetle. Spray Chlorantraniliprole 18.5% SC at first sign of damage.",
                    "mr": "खोडमाशी व चक्रीभुंग्याच्या नियंत्रणासाठी क्लोरॲन्ट्रानिलीप्रोल (३ मिली/१० लिटर) वेळेवर फवारा."
                },
                "pro_tip": {
                    "en": "Inter-cultivation (hoeing) at 20 and 35 days suppresses weeds and creates a soil dust mulch.",
                    "mr": "२० व ३५ व्या दिवशी कोळपणी केल्याने तण नष्ट होते आणि जमिनीतील ओलावा टिकून राहतो."
                }
            },
            {
                "stage_name": {
                    "en": "Stage 3: Flowering & Pod Filling",
                    "mr": "टप्पा ३: फुलधारणा व शेंगा भरणे"
                },
                "duration": {
                    "en": "Day 41 to 75",
                    "mr": "दिवस ४१ ते ७५"
                },
                "fertilizer": {
                    "en": "Foliar spray of 0:52:34 (4 g/L) + Boron (1 g/L) at 50% flowering to maximize pod setting.",
                    "mr": "५०% फुलधारणा अवस्थेत ०:५२:३४ (४ ग्रॅम/लिटर) + बोरॉन (१ ग्रॅम/लिटर) फवारल्यास शेंगांची संख्या वाढते."
                },
                "irrigation": {
                    "en": "Critical moisture stage. Moisture stress at pod filling severely shrivels seed size and cuts oil yield.",
                    "mr": "हा ओलाव्यासाठी अत्यंत संवेदनशील काळ आहे. शेंगा भरताना ताण पडल्यास दाण्याचा आकार बारीक राहतो."
                },
                "pest_disease": {
                    "en": "Spodoptera / Leaf eating caterpillar and Pod Borer. Spray Emamectin Benzoate 5% SG.",
                    "mr": "पाने खाणारी लष्करी अळी व शेंगा पोखरणाऱ्या अळीसाठी इमामेक्टिन बेन्झोएट (४ ग्रॅम/१० लिटर) फवारा."
                },
                "pro_tip": {
                    "en": "Never spray chemical insecticides during peak morning bee activity (8 AM - 11 AM) to safeguard pollination.",
                    "mr": "सकाळी ८ ते ११ दरम्यान मधमाश्यांच्या परागीभवनाच्या वेळी कोणतीही कीटकनाशक फवारणी करू नका."
                }
            },
            {
                "stage_name": {
                    "en": "Stage 4: Pod Maturation, Threshing & Storage",
                    "mr": "टप्पा ४: पक्वता, मळणी व साठवणूक"
                },
                "duration": {
                    "en": "Day 76 to 100",
                    "mr": "दिवस ७६ ते १००"
                },
                "fertilizer": {
                    "en": "No chemical fertilizers required during maturity.",
                    "mr": "पक्वतेच्या काळात खतांची आवश्यकता नसते."
                },
                "irrigation": {
                    "en": "Stop irrigation. Let pods turn naturally brown and dry on the vine.",
                    "mr": "पाणी पूर्ण बंद करा. झाडावरील शेंगा नैसर्गिकरीत्या तपकिरी वाळू द्या."
                },
                "pest_disease": {
                    "en": "Protect harvest from sudden rain. Store bags in dry, elevated pallets.",
                    "mr": "कापणी केलेले पीक पावसापासून सुरक्षित ठेवा. गोण्या जमिनीपासून वर लाकडी फळ्यांवर साठवा."
                },
                "pro_tip": {
                    "en": "Thresh at 12-14% seed moisture. Run threshers at low cylinder speed (350-400 RPM) to prevent seed cracking.",
                    "mr": "बियाण्यातील ओलावा १२-१४% असताना मळणी करा. मळणी यंत्राचा वेग कमी ठेवा जेणेकरून बियाणे फुटत नाही."
                }
            }
        ]
    }
}

# Interactive task reminders checklist synced to farmer's crops (Module 2) - Pure English & Pure Marathi
SAMPLE_CROP_TASKS = [
    {
        "id": "TSK-01",
        "crop": {"en": "Grapes", "mr": "द्राक्ष"},
        "title": {
            "en": "Bordeaux paste application on fresh pruning wounds",
            "mr": "ताज्या छाटणीच्या जखमांवर १०% बोर्डो पेस्ट लावणे"
        },
        "stage": {"en": "Forward Pruning", "mr": "गोडी छाटणी"},
        "due_date": {"en": "Within 48 hours", "mr": "४८ तासांच्या आत"},
        "priority": {"en": "High", "mr": "उच्च"},
        "status": True
    },
    {
        "id": "TSK-02",
        "crop": {"en": "Grapes", "mr": "द्राक्ष"},
        "title": {
            "en": "Preventive spray of 80% Wettable Sulphur against Powdery Mildew",
            "mr": "भुरी रोगाच्या प्रतिबंधासाठी ८०% पाण्यात मिसळणारे सल्फर फवारणी"
        },
        "stage": {"en": "Canopy Growth", "mr": "शाकीय वाढ"},
        "due_date": {"en": "Next 3 Days", "mr": "पुढील ३ दिवसांत"},
        "priority": {"en": "High", "mr": "उच्च"},
        "status": False
    },
    {
        "id": "TSK-03",
        "crop": {"en": "Grapes", "mr": "द्राक्ष"},
        "title": {
            "en": "Drip application of 0:52:34 MKP + Calcium Nitrate",
            "mr": "०:५२:३४ खताचा डोस व कॅल्शियम नायट्रेट ठिबकद्वारे देणे"
        },
        "stage": {"en": "Flowering / Setting", "mr": "फुलधारणा व मणी सेटिंग"},
        "due_date": {"en": "This Week", "mr": "या आठवड्यात"},
        "priority": {"en": "Medium", "mr": "मध्यम"},
        "status": False
    },
    {
        "id": "TSK-04",
        "crop": {"en": "Onion", "mr": "कांदा"},
        "title": {
            "en": "Seedling root dip in Trichoderma & Carbendazim before transplanting",
            "mr": "पुनर्लागवडीपूर्वी रोपांची मुळे ट्रायकोडर्मा व कार्बेन्डाझिम द्रावणात बुडवणे"
        },
        "stage": {"en": "Transplanting", "mr": "पुनर्लागवड"},
        "due_date": {"en": "Immediate", "mr": "तातडीने"},
        "priority": {"en": "High", "mr": "उच्च"},
        "status": True
    },
    {
        "id": "TSK-05",
        "crop": {"en": "Onion", "mr": "कांदा"},
        "title": {
            "en": "Install 15 Yellow & Blue sticky traps per acre for Thrips control",
            "mr": "फुलकिडे नियंत्रणासाठी एकरी १५ पिवळे व निळे चिकट सापळे लावणे"
        },
        "stage": {"en": "Vegetative Growth", "mr": "शाकीय वाढ"},
        "due_date": {"en": "In 5 Days", "mr": "५ दिवसांत"},
        "priority": {"en": "Medium", "mr": "मध्यम"},
        "status": False
    },
    {
        "id": "TSK-06",
        "crop": {"en": "Onion", "mr": "कांदा"},
        "title": {
            "en": "Foliar spray of Sulphur 90% + Micronol for bulb strength and pungency",
            "mr": "कांदा आकार व तिखटपणा वाढीसाठी सल्फर ९०% व मायक्रोनॉल फवारणी"
        },
        "stage": {"en": "Vegetative Growth", "mr": "शाकीय वाढ"},
        "due_date": {"en": "Next Week", "mr": "पुढील आठवड्यात"},
        "priority": {"en": "Medium", "mr": "मध्यम"},
        "status": False
    },
    {
        "id": "TSK-07",
        "crop": {"en": "Soybean", "mr": "सोयाबीन"},
        "title": {
            "en": "Post-harvest threshing and bag moisture check (12-14%)",
            "mr": "धान्यातील ओलावा तपासणी (१२-१४%) आणि सुरक्षित गोणी साठवणूक"
        },
        "stage": {"en": "Harvesting", "mr": "काढणी व साठवण"},
        "due_date": {"en": "Completed", "mr": "पूर्ण झाले"},
        "priority": {"en": "Low", "mr": "कमी"},
        "status": True
    }
]

# Realistic livestock records (Module 6) - Pure English & Pure Marathi
SAMPLE_LIVESTOCK = [
    {
        "tag_id": "MH-NSK-0101",
        "name": {"en": "Gauri", "mr": "गौरी"},
        "type": {"en": "Cow", "mr": "गाय"},
        "breed": {"en": "Gir", "mr": "गीर"},
        "age_years": 4.5,
        "daily_milk_yield_litres": 12.0,
        "health_status": {"en": "Attention Needed", "mr": "लसीकरण बाकी"},
        "vaccination_history": [
            {
                "vaccine": {"en": "Foot & Mouth Disease (FMD)", "mr": "लाळ्या खुरखूत"},
                "date_given": "2026-05-10",
                "due_date": "2026-11-10",
                "status": "Overdue"
            },
            {
                "vaccine": {"en": "Brucellosis", "mr": "ब्रुसेलोसिस"},
                "date_given": "2025-06-15",
                "due_date": "2026-06-15",
                "status": "Completed"
            }
        ]
    },
    {
        "tag_id": "MH-NSK-0102",
        "name": {"en": "Lakshmi", "mr": "लक्ष्मी"},
        "type": {"en": "Cow", "mr": "गाय"},
        "breed": {"en": "Gir", "mr": "गीर"},
        "age_years": 3.0,
        "daily_milk_yield_litres": 10.0,
        "health_status": {"en": "Healthy & Productive", "mr": "निरोगी व दुभते"},
        "vaccination_history": [
            {
                "vaccine": {"en": "Foot & Mouth Disease (FMD)", "mr": "लाळ्या खुरखूत"},
                "date_given": "2026-05-22",
                "due_date": "2026-11-22",
                "status": "Upcoming"
            },
            {
                "vaccine": {"en": "Hemorrhagic Septicemia (HS)", "mr": "घटसर्प"},
                "date_given": "2026-07-20",
                "due_date": "2027-07-20",
                "status": "Up-to-Date"
            }
        ]
    },
    {
        "tag_id": "MH-NSK-0201",
        "name": {"en": "Kaveri", "mr": "कावेरी"},
        "type": {"en": "Buffalo", "mr": "म्हैस"},
        "breed": {"en": "Murrah", "mr": "मुऱ्हा"},
        "age_years": 5.0,
        "daily_milk_yield_litres": 9.5,
        "health_status": {"en": "Attention Needed", "mr": "लसीकरण बाकी"},
        "vaccination_history": [
            {
                "vaccine": {"en": "Black Quarter (BQ)", "mr": "फऱ्या"},
                "date_given": "2026-04-12",
                "due_date": "2026-10-12",
                "status": "Overdue"
            },
            {
                "vaccine": {"en": "Foot & Mouth Disease (FMD)", "mr": "लाळ्या खुरखूत"},
                "date_given": "2026-08-15",
                "due_date": "2027-02-15",
                "status": "Up-to-Date"
            }
        ]
    },
    {
        "tag_id": "MH-NSK-0301",
        "name": {"en": "Surabhi", "mr": "सुरभी"},
        "type": {"en": "Cow", "mr": "गाय"},
        "breed": {"en": "Sahiwal", "mr": "साहिवाल"},
        "age_years": 2.5,
        "daily_milk_yield_litres": 8.0,
        "health_status": {"en": "Healthy & Productive", "mr": "निरोगी व दुभते"},
        "vaccination_history": [
            {
                "vaccine": {"en": "Foot & Mouth Disease (FMD)", "mr": "लाळ्या खुरखूत"},
                "date_given": "2026-09-10",
                "due_date": "2027-03-10",
                "status": "Up-to-Date"
            },
            {
                "vaccine": {"en": "Theileriosis", "mr": "थायलेरिओसिस"},
                "date_given": "2026-08-01",
                "due_date": "2027-08-01",
                "status": "Up-to-Date"
            }
        ]
    }
]

# Realistic nearby agricultural services (Module 4) - Pure English & Pure Marathi
SAMPLE_SERVICES = [
    {
        "id": "SRV-01",
        "name": {
            "en": "Dr. Anand Kulkarni - Govt Veterinary Hospital & Emergency Clinic",
            "mr": "डॉ. आनंद कुलकर्णी - शासकीय पशुवैद्यकीय रुग्णालय व आपत्कालीन सेवा"
        },
        "category": {
            "en": "Veterinary Doctors & Emergency",
            "mr": "पशुवैद्यकीय सेवा व आपत्कालीन क्लिनिक"
        },
        "taluka": {"en": "Niphad", "mr": "निफाड"},
        "district": {"en": "Nashik", "mr": "नाशिक"},
        "location": {
            "en": "Niphad Town Main Road, Near Panchayat Samiti (4.2 km)",
            "mr": "निफाड मुख्य रस्ता, पंचायत समितीजवळ (४.२ किमी)"
        },
        "phone": "+91 94222 88411",
        "timings": {
            "en": "9:00 AM - 6:00 PM (Emergency 24x7)",
            "mr": "सकाळी ९:०० ते संध्याकाळी ६:०० (आपत्कालीन २४x७)"
        },
        "speciality": {
            "en": "Cattle vaccination, artificial insemination, emergency surgery & deworming",
            "mr": "पशुधन लसीकरण, कृत्रिम रेतन, जनावरांची शस्त्रक्रिया व जंतनिर्मूलन"
        },
        "rating": 4.9,
        "verified": True
    },
    {
        "id": "SRV-02",
        "name": {
            "en": "Kisan Krishi Seva Kendra",
            "mr": "किसान कृषी सेवा केंद्र"
        },
        "category": {
            "en": "Seeds & Fertilizer Shops",
            "mr": "बियाणे व खते केंद्र"
        },
        "taluka": {"en": "Niphad", "mr": "निफाड"},
        "district": {"en": "Nashik", "mr": "नाशिक"},
        "location": {
            "en": "Pimpalgaon APMC Market Yard Gate 2 (1.8 km)",
            "mr": "पिंपळगाव बाजार समिती गेट २ (१.८ किमी)"
        },
        "phone": "+91 98230 45678",
        "timings": {
            "en": "8:30 AM - 8:30 PM",
            "mr": "सकाळी ८:३० ते रात्री ८:३०"
        },
        "speciality": {
            "en": "Certified onion seeds, water-soluble drip fertilizers (19:19:19, 0:52:34), bio-fungicides",
            "mr": "प्रमाणित कांदा बियाणे, विद्राव्य ठिबक खते (१९:१९:१९, ०:५२:३४) व जैविक बुरशीनाशके"
        },
        "rating": 4.7,
        "verified": True
    },
    {
        "id": "SRV-03",
        "name": {
            "en": "Sahyadri Agro Machinery Custom Hiring Centre",
            "mr": "सह्याद्री कृषी अवजारे भाडे केंद्र"
        },
        "category": {
            "en": "Machinery & Equipment Rental",
            "mr": "कृषी अवजारे व यंत्रसामग्री भाडे केंद्र"
        },
        "taluka": {"en": "Niphad", "mr": "निफाड"},
        "district": {"en": "Nashik", "mr": "नाशिक"},
        "location": {
            "en": "Ozar Airport Road, Niphad (6.5 km)",
            "mr": "ओझर विमानतळ रस्ता, निफाड (६.५ किमी)"
        },
        "phone": "+91 97654 32109",
        "timings": {
            "en": "7:00 AM - 7:00 PM",
            "mr": "सकाळी ७:०० ते संध्याकाळी ७:००"
        },
        "speciality": {
            "en": "Mini tractor rental (24 HP orchard model), boom sprayers for vineyards, rotavator",
            "mr": "द्राक्ष बागेसाठी लहान ट्रॅक्टर भाडे (२४ एचपी), बूम स्प्रेअर व रोटाव्हेटर"
        },
        "rating": 4.8,
        "verified": True
    },
    {
        "id": "SRV-04",
        "name": {
            "en": "Shree Ganesh Animal Fodder & Cattle Feed Traders",
            "mr": "श्री गणेश पशुखाद्य व वैरण केंद्र"
        },
        "category": {
            "en": "Animal Fodder & Feed",
            "mr": "पशुखाद्य व वैरण"
        },
        "taluka": {"en": "Niphad", "mr": "निफाड"},
        "district": {"en": "Nashik", "mr": "नाशिक"},
        "location": {
            "en": "Niphad Phata Highway Junction (3.1 km)",
            "mr": "निफाड फाटा हायवे जंक्शन (३.१ किमी)"
        },
        "phone": "+91 99215 67890",
        "timings": {
            "en": "8:00 AM - 8:00 PM",
            "mr": "सकाळी ८:०० ते रात्री ८:००"
        },
        "speciality": {
            "en": "Corn silage bales, high-protein cotton cake, mineral mixture bags, dry straw",
            "mr": "मका सायलेज गाठी, सरकी पेंड, मिनरल मिक्स्चर व दर्जेदार सुका चारा"
        },
        "rating": 4.6,
        "verified": True
    },
    {
        "id": "SRV-05",
        "name": {
            "en": "MahaAgri Soil & Water Testing Laboratory",
            "mr": "महाॲग्री माती व पाणी परीक्षण प्रयोगशाळा"
        },
        "category": {
            "en": "Agricultural Service Centres",
            "mr": "कृषी सेवा व माती परीक्षण केंद्र"
        },
        "taluka": {"en": "Nashik", "mr": "नाशिक"},
        "district": {"en": "Nashik", "mr": "नाशिक"},
        "location": {
            "en": "KVK Yashwantrao Chavan Open University Campus (11.5 km)",
            "mr": "केव्हीके यशवंतराव चव्हाण मुक्त विद्यापीठ परिसर (११.५ किमी)"
        },
        "phone": "+91 94231 77650",
        "timings": {
            "en": "10:00 AM - 5:00 PM (Monday-Saturday)",
            "mr": "सकाळी १०:०० ते संध्याकाळी ५:०० (सोम-शनि)"
        },
        "speciality": {
            "en": "Complete 14-parameter soil test (NPK, Organic Carbon, Micro-nutrients, pH) & water testing",
            "mr": "१४ घटकांचे संपूर्ण माती परीक्षण (एनपीके, सेंद्रिय कर्ब, सूक्ष्मअन्नद्रव्ये, सामू) व सिंचन पाणी तपासणी"
        },
        "rating": 4.9,
        "verified": True
    }
]

# 12 Core Farm Expense Categories from Problem Statement
EXPENSE_CATEGORIES = [
    {"en": "Seeds & Seedlings", "mr": "बियाणे व रोपे"},
    {"en": "Fertilizers & Nutrients", "mr": "खते व पोषण"},
    {"en": "Pesticides & Bio-agents", "mr": "कीटकनाशके व बुरशीनाशके"},
    {"en": "Labour & Pruning", "mr": "मजुरी व छाटणी"},
    {"en": "Irrigation & Water", "mr": "सिंचन व पाणी"},
    {"en": "Machinery & Rentals", "mr": "यंत्रसामग्री व भाडे"},
    {"en": "Transport & Mandi Hamali", "mr": "वाहतूक व हमाली"},
    {"en": "Animal Fodder & Feed", "mr": "पशुखाद्य व वैरण"},
    {"en": "Veterinary & Healthcare", "mr": "पशुवैद्यकीय उपचार"},
    {"en": "Animal Vaccination", "mr": "पशुधन लसीकरण"},
    {"en": "Fuel & Electricity", "mr": "डिझेल व वीज बिल"},
    {"en": "Repairs & Maintenance", "mr": "दुरुस्ती व देखभाल"}
]

# Realistic categorized farm expenses across seasons & categories (Module 7) - Pure English & Pure Marathi
SAMPLE_EXPENSES = [
    {
        "id": "EXP-001",
        "date": "2026-10-05",
        "month": {"en": "October 2026", "mr": "ऑक्टोबर २०२६"},
        "season": {"en": "Rabi 2026-27", "mr": "रब्बी २०२६-२७"},
        "crop": {"en": "Onion", "mr": "कांदा"},
        "category": {"en": "Seeds & Seedlings", "mr": "बियाणे व रोपे"},
        "description": {
            "en": "Purchased 4 kg certified Fursungi onion seed packets",
            "mr": "४ किलो प्रमाणित फुर्सुंगी कांदा बियाणे खरेदी"
        },
        "amount": 4800,
        "payment_mode": {"en": "UPI", "mr": "यूपीआय"}
    },
    {
        "id": "EXP-002",
        "date": "2026-10-14",
        "month": {"en": "October 2026", "mr": "ऑक्टोबर २०२६"},
        "season": {"en": "Rabi 2026-27", "mr": "रब्बी २०२६-२७"},
        "crop": {"en": "Grapes", "mr": "द्राक्ष"},
        "category": {"en": "Fertilizers & Nutrients", "mr": "खते व पोषण"},
        "description": {
            "en": "Water-soluble 0:52:34 and micronutrient drip application kit",
            "mr": "विद्राव्य खत ०:५२:३४ व सूक्ष्मअन्नद्रव्य ठिबक संच खरेदी"
        },
        "amount": 7600,
        "payment_mode": {"en": "Cash", "mr": "रोख"}
    },
    {
        "id": "EXP-003",
        "date": "2026-10-22",
        "month": {"en": "October 2026", "mr": "ऑक्टोबर २०२६"},
        "season": {"en": "Rabi 2026-27", "mr": "रब्बी २०२६-२७"},
        "crop": {"en": "Grapes", "mr": "द्राक्ष"},
        "category": {"en": "Labour & Pruning", "mr": "मजुरी व छाटणी"},
        "description": {
            "en": "Forward pruning labour charges for 6 workers for 2 days",
            "mr": "गोडी छाटणी मजुरी खर्च (६ मजूर २ दिवस)"
        },
        "amount": 7200,
        "payment_mode": {"en": "Cash", "mr": "रोख"}
    },
    {
        "id": "EXP-004",
        "date": "2026-11-02",
        "month": {"en": "November 2026", "mr": "नोव्हेंबर २०२६"},
        "season": {"en": "Rabi 2026-27", "mr": "रब्बी २०२६-२७"},
        "crop": {"en": "Livestock / Dairy", "mr": "दुग्धव्यवसाय / पशुधन"},
        "category": {"en": "Animal Fodder & Feed", "mr": "पशुखाद्य व वैरण"},
        "description": {
            "en": "5 bags cattle feed pellet and mineral mixture",
            "mr": "५ गोण्या पशुखाद्य पेंड व मिनरल मिक्स्चर खरेदी"
        },
        "amount": 6250,
        "payment_mode": {"en": "UPI", "mr": "यूपीआय"}
    },
    {
        "id": "EXP-005",
        "date": "2026-11-08",
        "month": {"en": "November 2026", "mr": "नोव्हेंबर २०२६"},
        "season": {"en": "Rabi 2026-27", "mr": "रब्बी २०२६-२७"},
        "crop": {"en": "Onion", "mr": "कांदा"},
        "category": {"en": "Labour & Pruning", "mr": "मजुरी व छाटणी"},
        "description": {
            "en": "Nursery bed transplanting labor for 4 women workers",
            "mr": "कांदा पुनर्लागवड मजुरी (४ महिला मजूर)"
        },
        "amount": 2800,
        "payment_mode": {"en": "Cash", "mr": "रोख"}
    },
    {
        "id": "EXP-006",
        "date": "2026-11-12",
        "month": {"en": "November 2026", "mr": "नोव्हेंबर २०२६"},
        "season": {"en": "Rabi 2026-27", "mr": "रब्बी २०२६-२७"},
        "crop": {"en": "Grapes", "mr": "द्राक्ष"},
        "category": {"en": "Pesticides & Bio-agents", "mr": "कीटकनाशके व बुरशीनाशके"},
        "description": {
            "en": "Downy mildew preventive bio-fungicide spray (Trichoderma + Copper)",
            "mr": "डाऊनी मिल्ड्यू प्रतिबंधक ट्रायकोडर्मा व कॉपर बुरशीनाशक फवारणी"
        },
        "amount": 3400,
        "payment_mode": {"en": "UPI", "mr": "यूपीआय"}
    },
    {
        "id": "EXP-007",
        "date": "2026-09-15",
        "month": {"en": "September 2026", "mr": "सप्टेंबर २०२६"},
        "season": {"en": "Kharif 2026", "mr": "खरीप २०२६"},
        "crop": {"en": "Soybean", "mr": "सोयाबीन"},
        "category": {"en": "Machinery & Rentals", "mr": "यंत्रसामग्री व भाडे"},
        "description": {
            "en": "Tractor rotavator & threshing rental for soybean harvest",
            "mr": "सोयाबीन काढणी व मळणी यंत्र ट्रॅक्टर भाडे"
        },
        "amount": 5500,
        "payment_mode": {"en": "Cash", "mr": "रोख"}
    },
    {
        "id": "EXP-008",
        "date": "2026-10-28",
        "month": {"en": "October 2026", "mr": "ऑक्टोबर २०२६"},
        "season": {"en": "Rabi 2026-27", "mr": "रब्बी २०२६-२७"},
        "crop": {"en": "General Farm", "mr": "सामायिक शेती"},
        "category": {"en": "Irrigation & Water", "mr": "सिंचन व पाणी"},
        "description": {
            "en": "Drip lateral pipe replacement and filter valve repairs",
            "mr": "ठिबक लॅटरल नळ्या बदलणे व फिल्टर व्हॉल्व्ह दुरुस्ती"
        },
        "amount": 3200,
        "payment_mode": {"en": "UPI", "mr": "यूपीआय"}
    },
    {
        "id": "EXP-009",
        "date": "2026-11-05",
        "month": {"en": "November 2026", "mr": "नोव्हेंबर २०२६"},
        "season": {"en": "Rabi 2026-27", "mr": "रब्बी २०२६-२७"},
        "crop": {"en": "Livestock / Dairy", "mr": "दुग्धव्यवसाय / पशुधन"},
        "category": {"en": "Veterinary & Healthcare", "mr": "पशुवैद्यकीय उपचार"},
        "description": {
            "en": "Doctor farm visit, cattle deworming & mineral bolus",
            "mr": "पशुवैद्यकीय तपासणी, जनावरांचे जंतनिर्मूलन व खनिज औषधे"
        },
        "amount": 1400,
        "payment_mode": {"en": "Cash", "mr": "रोख"}
    },
    {
        "id": "EXP-010",
        "date": "2026-11-10",
        "month": {"en": "November 2026", "mr": "नोव्हेंबर २०२६"},
        "season": {"en": "Rabi 2026-27", "mr": "रब्बी २०२६-२७"},
        "crop": {"en": "General Farm", "mr": "सामायिक शेती"},
        "category": {"en": "Fuel & Electricity", "mr": "डिझेल व वीज बिल"},
        "description": {
            "en": "MSEDCL agricultural water pump electricity bill payment",
            "mr": "महावितरण शेतीपंप वीज बिल भरणा"
        },
        "amount": 4650,
        "payment_mode": {"en": "Bank Transfer", "mr": "बँक ट्रान्सफर"}
    },
    {
        "id": "EXP-011",
        "date": "2026-09-25",
        "month": {"en": "September 2026", "mr": "सप्टेंबर २०२६"},
        "season": {"en": "Kharif 2026", "mr": "खरीप २०२६"},
        "crop": {"en": "Soybean", "mr": "सोयाबीन"},
        "category": {"en": "Transport & Mandi Hamali", "mr": "वाहतूक व हमाली"},
        "description": {
            "en": "Tempo transport of 18 bags soybean to APMC market",
            "mr": "१८ पोती सोयाबीन बाजार समितीत नेण्यासाठी वाहतूक भाडे"
        },
        "amount": 2200,
        "payment_mode": {"en": "Cash", "mr": "रोख"}
    },
    {
        "id": "EXP-012",
        "date": "2026-10-18",
        "month": {"en": "October 2026", "mr": "ऑक्टोबर २०२६"},
        "season": {"en": "Rabi 2026-27", "mr": "रब्बी २०२६-२७"},
        "crop": {"en": "Grapes", "mr": "द्राक्ष"},
        "category": {"en": "Repairs & Maintenance", "mr": "दुरुस्ती व देखभाल"},
        "description": {
            "en": "Tractor boom sprayer nozzle servicing and diaphragm seal repair",
            "mr": "ट्रॅक्टर बूम स्प्रेअर नोझल सर्व्हिसिंग व डायफ्राम सील दुरुस्ती"
        },
        "amount": 1850,
        "payment_mode": {"en": "UPI", "mr": "यूपीआय"}
    }
]

# Realistic marketplace listings (Module 5) - Pure English & Pure Marathi
SAMPLE_MARKETPLACE = [
    {
        "id": "MKT-101",
        "crop_name": {"en": "Gavran Red Onion", "mr": "गावरान लाल कांदा"},
        "category": {"en": "Vegetables", "mr": "भाजीपाला"},
        "variety": {"en": "Nashik Garwa Quality", "mr": "नाशिक गरवा प्रत"},
        "quality_grade": {"en": "Grade A (Export / Storage)", "mr": "अ दर्जा (निर्यात व साठवणूक)"},
        "quantity_quintals": 55,
        "expected_price_per_quintal": 1950,
        "seller_name": {"en": "Ramesh Tukaram Patil", "mr": "रमेश तुकाराम पाटील"},
        "seller_phone": "+91 98220 12345",
        "village": {"en": "Pimpalgaon Baswant", "mr": "पिंपळगाव बसवंत"},
        "taluka": {"en": "Niphad", "mr": "निफाड"},
        "district": {"en": "Nashik", "mr": "नाशिक"},
        "location": {"en": "Pimpalgaon Baswant, Niphad", "mr": "पिंपळगाव बसवंत, निफाड"},
        "harvest_date": "2026-10-25",
        "status": {"en": "Available", "mr": "उपलब्ध"},
        "notes": {
            "en": "Graded, dry, well-cured medium-to-large size bulbs suitable for storage.",
            "mr": "प्रतवारी केलेला, कोरडा, योग्य वाळवलेला मध्यम व मोठा कांदा चाळीसाठी योग्य."
        }
    },
    {
        "id": "MKT-102",
        "crop_name": {"en": "Thomson Seedless Grapes", "mr": "थॉमसन सिडलेस द्राक्ष"},
        "category": {"en": "Fruits", "mr": "फळे"},
        "variety": {"en": "European Export Standard", "mr": "युरोपियन निर्यात मानक"},
        "quality_grade": {"en": "Export Quality (18mm+)", "mr": "निर्यात प्रत (१८ मिमी+)"},
        "quantity_quintals": 30,
        "expected_price_per_quintal": 6200,
        "seller_name": {"en": "Ramesh Tukaram Patil", "mr": "रमेश तुकाराम पाटील"},
        "seller_phone": "+91 98220 12345",
        "village": {"en": "Pimpalgaon Baswant", "mr": "पिंपळगाव बसवंत"},
        "taluka": {"en": "Niphad", "mr": "निफाड"},
        "district": {"en": "Nashik", "mr": "नाशिक"},
        "location": {"en": "Pimpalgaon Baswant, Niphad", "mr": "पिंपळगाव बसवंत, निफाड"},
        "harvest_date": "Expected Feb 2027",
        "status": {"en": "Advance Booking", "mr": "आगाऊ नोंदणी सुरू"},
        "notes": {
            "en": "18mm+ berry size, residue-free spray schedule maintained for overseas export.",
            "mr": "१८ मिमी+ मणी आकार, परदेशी निर्यातीसाठी कीटकनाशक अवशेषमुक्त नियोजन केलेले."
        }
    },
    {
        "id": "MKT-103",
        "crop_name": {"en": "JS 335 Soybean", "mr": "जेएस ३३५ सोयाबीन"},
        "category": {"en": "Grains & Pulses", "mr": "धान्य व कडधान्ये"},
        "variety": {"en": "Certified Seed Grade", "mr": "प्रमाणित बियाणे प्रत"},
        "quality_grade": {"en": "Grade A (Clean & Bold)", "mr": "अ दर्जा (स्वच्छ व टपोरे)"},
        "quantity_quintals": 42,
        "expected_price_per_quintal": 4650,
        "seller_name": {"en": "Kailas Bhikaji Shinde", "mr": "कैलास भिकाजी शिंदे"},
        "seller_phone": "+91 98501 23456",
        "village": {"en": "Lasalgaon", "mr": "लासलगाव"},
        "taluka": {"en": "Niphad", "mr": "निफाड"},
        "district": {"en": "Nashik", "mr": "नाशिक"},
        "location": {"en": "Lasalgaon, Niphad", "mr": "लासलगाव, निफाड"},
        "harvest_date": "2026-10-18",
        "status": {"en": "Available", "mr": "उपलब्ध"},
        "notes": {
            "en": "11% moisture level, double-cleaned by grader machine, ready for oil mills or seed.",
            "mr": "११% ओलावा, ग्रेडर मशीनने स्वच्छ केलेले, तेल गिरणी किंवा बियाण्यासाठी तयार."
        }
    },
    {
        "id": "MKT-104",
        "crop_name": {"en": "Bhagwa Pomegranate", "mr": "भगवा डाळिंब"},
        "category": {"en": "Fruits", "mr": "फळे"},
        "variety": {"en": "Solapur Super Bhagwa", "mr": "सोलापूर सुपर भगवा"},
        "quality_grade": {"en": "Premium (350g+ Arils)", "mr": "प्रीमियम (३५० ग्रॅम+ फळे)"},
        "quantity_quintals": 25,
        "expected_price_per_quintal": 8400,
        "seller_name": {"en": "Dattatraya Shripad More", "mr": "दत्तात्रय श्रीपाद मोरे"},
        "seller_phone": "+91 97631 89012",
        "village": {"en": "Chandori", "mr": "चांदोरी"},
        "taluka": {"en": "Niphad", "mr": "निफाड"},
        "district": {"en": "Nashik", "mr": "नाशिक"},
        "location": {"en": "Chandori, Niphad", "mr": "चांदोरी, निफाड"},
        "harvest_date": "2026-11-05",
        "status": {"en": "Available", "mr": "उपलब्ध"},
        "notes": {
            "en": "Deep red shining arils, zero fungal spots, packed in 10 kg paper corrugated boxes.",
            "mr": "गडद लाल दाणे, डाग विरहित फळे, १० किलो बॉक्सेसमध्ये पॅकिंग केलेले."
        }
    },
    {
        "id": "MKT-105",
        "crop_name": {"en": "Fresh Green Turmeric", "mr": "ओली हिरवी हळद"},
        "category": {"en": "Vegetables", "mr": "भाजीपाला"},
        "variety": {"en": "Salem High Curcumin", "mr": "सेलम उच्च करक्युमिन"},
        "quality_grade": {"en": "Organic Certified (5.2% Curcumin)", "mr": "सेंद्रिय प्रमाणित (५.२% करक्युमिन)"},
        "quantity_quintals": 18,
        "expected_price_per_quintal": 3200,
        "seller_name": {"en": "Sunita Sanjay Gaikwad", "mr": "सुनिता संजय गायकवाड"},
        "seller_phone": "+91 94231 67890",
        "village": {"en": "Saikheda", "mr": "सायखेडा"},
        "taluka": {"en": "Niphad", "mr": "निफाड"},
        "district": {"en": "Nashik", "mr": "नाशिक"},
        "location": {"en": "Saikheda, Niphad", "mr": "सायखेडा, निफाड"},
        "harvest_date": "2026-11-10",
        "status": {"en": "Available", "mr": "उपलब्ध"},
        "notes": {
            "en": "Freshly harvested, washed organic turmeric fingers ideal for pickle, extract, and medicine.",
            "mr": "ताजी काढलेली स्वच्छ सेंद्रिय हळद, लोणचे, अर्क व औषध निर्मितीसाठी उत्तम."
        }
    },
    {
        "id": "MKT-106",
        "crop_name": {"en": "Lokwan Sharbati Wheat", "mr": "लोकवन शरबती गहू"},
        "category": {"en": "Grains & Pulses", "mr": "धान्य व कडधान्ये"},
        "variety": {"en": "Bhal Golden Grain", "mr": "सुवर्ण दाणा"},
        "quality_grade": {"en": "Grade A (Bold & Heavy)", "mr": "अ दर्जा (टपोरा व वजनदार)"},
        "quantity_quintals": 50,
        "expected_price_per_quintal": 3150,
        "seller_name": {"en": "Ramesh Tukaram Patil", "mr": "रमेश तुकाराम पाटील"},
        "seller_phone": "+91 98220 12345",
        "village": {"en": "Pimpalgaon Baswant", "mr": "पिंपळगाव बसवंत"},
        "taluka": {"en": "Niphad", "mr": "निफाड"},
        "district": {"en": "Nashik", "mr": "नाशिक"},
        "location": {"en": "Pimpalgaon Baswant, Niphad", "mr": "पिंपळगाव बसवंत, निफाड"},
        "harvest_date": "Expected March 2027",
        "status": {"en": "Advance Booking", "mr": "आगाऊ नोंदणी सुरू"},
        "notes": {
            "en": "Golden heavy grain with high gluten quality for soft chapatis. Booking open for retail/wholesale.",
            "mr": "मऊ चपातीसाठी उत्तम ग्लूटेनयुक्त टपोरा गहू. घाऊक व किरकोळ नोंदणी सुरू."
        }
    }
]


def init_session_data(st=None):
    """Initializes in-memory session data."""
    pass


def reset_to_defaults(st=None):
    """Allows resetting session data to initial sample values."""
    pass
