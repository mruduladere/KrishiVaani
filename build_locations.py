"""
build_locations.py
Generates maharashtra_locations.json covering all 36 Maharashtra districts,
their major talukas, and prominent farming villages / APMCs / research centers.
"""
import json
from pathlib import Path

MAHARASHTRA_LOCATIONS = {
    "Ahmednagar": {
        "en": "Ahmednagar (Ahilyanagar)",
        "mr": "अहमदनगर (अहिल्यानगर)",
        "lat": 19.0948,
        "lon": 74.7480,
        "talukas": {
            "Rahuri": {
                "en": "Rahuri", "mr": "राहुरी", "lat": 19.3942, "lon": 74.6514,
                "villages": [
                    {"en": "MPKV University Campus", "mr": "म.फु.कृ.वि. विद्यापीठ परिसर", "lat": 19.3917, "lon": 74.6542},
                    {"en": "Rahuri Khurd", "mr": "राहुरी खुर्द", "lat": 19.3850, "lon": 74.6480},
                    {"en": "Vambori", "mr": "वांबोरी", "lat": 19.2940, "lon": 74.7310},
                    {"en": "Baragaon Nandur", "mr": "बारागाव नांदूर", "lat": 19.3420, "lon": 74.6180}
                ]
            },
            "Sangamner": {
                "en": "Sangamner", "mr": "संगमनेर", "lat": 19.5762, "lon": 74.2070,
                "villages": [
                    {"en": "Sangamner City & Market", "mr": "संगमनेर शहर व बाजारपेठ", "lat": 19.5762, "lon": 74.2070},
                    {"en": "Ashwi Khurd", "mr": "आश्वी खुर्द", "lat": 19.6120, "lon": 74.3410},
                    {"en": "Talegaon", "mr": "तळेगाव", "lat": 19.5210, "lon": 74.2670},
                    {"en": "Chandnapuri", "mr": "चंदनापुरी", "lat": 19.5390, "lon": 74.1480}
                ]
            },
            "Kopargaon": {
                "en": "Kopargaon", "mr": "कोपरगाव", "lat": 19.8887, "lon": 74.4764,
                "villages": [
                    {"en": "Kopargaon Mandi", "mr": "कोपरगाव कृषी उत्पन्न बाजार", "lat": 19.8887, "lon": 74.4764},
                    {"en": "Pohegaon", "mr": "पोहेगाव", "lat": 19.8120, "lon": 74.5240},
                    {"en": "Dharangaon", "mr": "धरणगाव", "lat": 19.8510, "lon": 74.4320}
                ]
            },
            "Shrirampur": {
                "en": "Shrirampur", "mr": "श्रीरामपूर", "lat": 19.6190, "lon": 74.6575,
                "villages": [
                    {"en": "Shrirampur Town", "mr": "श्रीरामपूर शहर", "lat": 19.6190, "lon": 74.6575},
                    {"en": "Belapur", "mr": "बेलापूर", "lat": 19.5310, "lon": 74.6390},
                    {"en": "Malunja", "mr": "मालुंजा", "lat": 19.6720, "lon": 74.6120}
                ]
            },
            "Nevasa": {
                "en": "Nevasa", "mr": "नेवासा", "lat": 19.5528, "lon": 74.9192,
                "villages": [
                    {"en": "Nevasa Fata", "mr": "नेवासा फाटा", "lat": 19.5400, "lon": 74.9100},
                    {"en": "Sonai", "mr": "सोनई", "lat": 19.4890, "lon": 74.8320},
                    {"en": "Kukana", "mr": "कुकाणा", "lat": 19.4620, "lon": 75.0510}
                ]
            },
            "Parner": {
                "en": "Parner", "mr": "पारनेर", "lat": 19.0028, "lon": 74.4402,
                "villages": [
                    {"en": "Ralegan Siddhi", "mr": "राळेगण सिद्धी", "lat": 18.9186, "lon": 74.4042},
                    {"en": "Parner Rural", "mr": "पारनेर ग्रामीण", "lat": 19.0028, "lon": 74.4402},
                    {"en": "Nighoj", "mr": "निघोज", "lat": 18.9620, "lon": 74.3180}
                ]
            },
            "Rahata": {
                "en": "Rahata", "mr": "राहाता", "lat": 19.7042, "lon": 74.4851,
                "villages": [
                    {"en": "Shirdi", "mr": "शिर्डी", "lat": 19.7667, "lon": 74.4764},
                    {"en": "Rahata Town", "mr": "राहाता शहर", "lat": 19.7042, "lon": 74.4851},
                    {"en": "Sakuri", "mr": "साकुरी", "lat": 19.7210, "lon": 74.5020}
                ]
            },
            "Akole": {
                "en": "Akole", "mr": "अकोले", "lat": 19.5448, "lon": 73.9318,
                "villages": [
                    {"en": "Akole Town", "mr": "अकोले शहर", "lat": 19.5448, "lon": 73.9318},
                    {"en": "Rajur", "mr": "राजूर", "lat": 19.5320, "lon": 73.7840},
                    {"en": "Kotul", "mr": "कोतुल", "lat": 19.4310, "lon": 73.8920}
                ]
            }
        }
    },
    "Akola": {
        "en": "Akola", "mr": "अकोला", "lat": 20.7002, "lon": 77.0082,
        "talukas": {
            "Akola": {
                "en": "Akola", "mr": "अकोला", "lat": 20.7002, "lon": 77.0082,
                "villages": [
                    {"en": "PDKV Agriculture University", "mr": "डॉ. पं.दे.कृ.वि. विद्यापीठ परिसर", "lat": 20.7050, "lon": 77.0250},
                    {"en": "Shivani", "mr": "शिवणी", "lat": 20.6810, "lon": 77.0450},
                    {"en": "Borgaon Manju", "mr": "बोरगाव मंजू", "lat": 20.6720, "lon": 77.1640}
                ]
            },
            "Murtizapur": {
                "en": "Murtizapur", "mr": "मूर्तिजापूर", "lat": 20.7324, "lon": 77.3629,
                "villages": [
                    {"en": "Murtizapur Town", "mr": "मूर्तिजापूर शहर", "lat": 20.7324, "lon": 77.3629},
                    {"en": "Mana", "mr": "माना", "lat": 20.7100, "lon": 77.2840}
                ]
            },
            "Akot": {
                "en": "Akot", "mr": "अकोट", "lat": 21.0963, "lon": 77.0594,
                "villages": [
                    {"en": "Akot Cotton Market", "mr": "अकोट कापूस बाजार", "lat": 21.0963, "lon": 77.0594},
                    {"en": "Panaj", "mr": "पनाज", "lat": 21.1410, "lon": 77.1240}
                ]
            },
            "Balapur": {
                "en": "Balapur", "mr": "बाळापूर", "lat": 20.6657, "lon": 76.7725,
                "villages": [
                    {"en": "Balapur Rural", "mr": "बाळापूर ग्रामीण", "lat": 20.6657, "lon": 76.7725},
                    {"en": "Paras", "mr": "पारस", "lat": 20.7150, "lon": 76.7920}
                ]
            },
            "Telhara": {
                "en": "Telhara", "mr": "तेल्हारा", "lat": 21.0336, "lon": 76.8406,
                "villages": [
                    {"en": "Telhara Town", "mr": "तेल्हारा शहर", "lat": 21.0336, "lon": 76.8406},
                    {"en": "Adgaon Buzruk", "mr": "आडगाव बुद्रुक", "lat": 21.0820, "lon": 76.7810}
                ]
            },
            "Barshitakli": {
                "en": "Barshitakli", "mr": "बार्शीटाकळी", "lat": 20.5833, "lon": 77.0667,
                "villages": [
                    {"en": "Barshitakli Town", "mr": "बार्शीटाकळी शहर", "lat": 20.5833, "lon": 77.0667},
                    {"en": "Mahan", "mr": "महान", "lat": 20.5120, "lon": 77.1250}
                ]
            },
            "Patur": {
                "en": "Patur", "mr": "पातूर", "lat": 20.4578, "lon": 76.9322,
                "villages": [
                    {"en": "Patur Town", "mr": "पातूर शहर", "lat": 20.4578, "lon": 76.9322},
                    {"en": "Channi", "mr": "चान्नी", "lat": 20.4120, "lon": 76.8840}
                ]
            }
        }
    },
    "Amravati": {
        "en": "Amravati", "mr": "अमरावती", "lat": 20.9374, "lon": 77.7796,
        "talukas": {
            "Amravati": {
                "en": "Amravati", "mr": "अमरावती", "lat": 20.9374, "lon": 77.7796,
                "villages": [
                    {"en": "Walgaon", "mr": "वलगाव", "lat": 20.9820, "lon": 77.7180},
                    {"en": "Badnera", "mr": "बडनेरा", "lat": 20.8650, "lon": 77.7280},
                    {"en": "Nandgaon Peth", "mr": "नांदगाव पेठ", "lat": 21.0250, "lon": 77.8240}
                ]
            },
            "Achalpur": {
                "en": "Achalpur", "mr": "अचलपूर", "lat": 21.2573, "lon": 77.5097,
                "villages": [
                    {"en": "Achalpur Mandi", "mr": "अचलपूर बाजारपेठ", "lat": 21.2573, "lon": 77.5097},
                    {"en": "Paratwada", "mr": "परतवाडा", "lat": 21.2980, "lon": 77.5250}
                ]
            },
            "Morshi": {
                "en": "Morshi", "mr": "मोर्शी", "lat": 21.3197, "lon": 78.0125,
                "villages": [
                    {"en": "Morshi Orange Belt", "mr": "मोर्शी संत्रा पट्टा", "lat": 21.3197, "lon": 78.0125},
                    {"en": "Dhamangaon Gadhi", "mr": "धामणगाव गढी", "lat": 21.3710, "lon": 77.6250}
                ]
            },
            "Warud": {
                "en": "Warud", "mr": "वरुड", "lat": 21.4647, "lon": 78.2633,
                "villages": [
                    {"en": "Warud Nagpur Mandarin Hub", "mr": "वरुड संत्रा निर्यात केंद्र", "lat": 21.4647, "lon": 78.2633},
                    {"en": "Benoda", "mr": "बेनोडा", "lat": 21.4310, "lon": 78.1820}
                ]
            },
            "Chandur Railway": {
                "en": "Chandur Railway", "mr": "चांदूर रेल्वे", "lat": 20.8122, "lon": 77.9739,
                "villages": [
                    {"en": "Chandur Town", "mr": "चांदूर शहर", "lat": 20.8122, "lon": 77.9739},
                    {"en": "Dipori", "mr": "दिपोरी", "lat": 20.7810, "lon": 77.9250}
                ]
            },
            "Daryapur": {
                "en": "Daryapur", "mr": "दर्यापूर", "lat": 20.9286, "lon": 77.3297,
                "villages": [
                    {"en": "Daryapur Cotton Belt", "mr": "दर्यापूर कापूस केंद्र", "lat": 20.9286, "lon": 77.3297},
                    {"en": "Banosa", "mr": "बनोसा", "lat": 20.9350, "lon": 77.3380}
                ]
            }
        }
    },
    "Chhatrapati Sambhajinagar": {
        "en": "Chhatrapati Sambhajinagar (Aurangabad)", "mr": "छत्रपती संभाजीनगर (औरंगाबाद)", "lat": 19.8762, "lon": 75.3433,
        "talukas": {
            "Chhatrapati Sambhajinagar": {
                "en": "Chhatrapati Sambhajinagar", "mr": "छत्रपती संभाजीनगर", "lat": 19.8762, "lon": 75.3433,
                "villages": [
                    {"en": "Chikalthana APMC", "mr": "चिकलठाणा बाजार", "lat": 19.8750, "lon": 75.3950},
                    {"en": "Harsul", "mr": "हर्सूल", "lat": 19.9120, "lon": 75.3520},
                    {"en": "Daulatabad", "mr": "दौलताबाद", "lat": 19.9410, "lon": 75.2150}
                ]
            },
            "Paithan": {
                "en": "Paithan", "mr": "पैठण", "lat": 19.4819, "lon": 75.3853,
                "villages": [
                    {"en": "Jayakwadi Dam Catchment", "mr": "जायकवाडी धरण परिसर", "lat": 19.4950, "lon": 75.3680},
                    {"en": "Pimpalwadi", "mr": "पिंपळवाडी", "lat": 19.5120, "lon": 75.4120},
                    {"en": "Pachod", "mr": "पाचोड", "lat": 19.4210, "lon": 75.5680}
                ]
            },
            "Gangapur": {
                "en": "Gangapur", "mr": "गंगापूर", "lat": 19.7028, "lon": 75.0117,
                "villages": [
                    {"en": "Gangapur Town", "mr": "गंगापूर शहर", "lat": 19.7028, "lon": 75.0117},
                    {"en": "Lasur Station", "mr": "लासूर स्टेशन", "lat": 19.8240, "lon": 75.0620}
                ]
            },
            "Vaijapur": {
                "en": "Vaijapur", "mr": "वैजापूर", "lat": 19.9272, "lon": 74.7297,
                "villages": [
                    {"en": "Vaijapur Mandi", "mr": "वैजापूर कृषी बाजार", "lat": 19.9272, "lon": 74.7297},
                    {"en": "Rotegaon", "mr": "रोटेगाव", "lat": 19.9510, "lon": 74.7080}
                ]
            },
            "Kannad": {
                "en": "Kannad", "mr": "कन्नड", "lat": 20.2647, "lon": 75.1322,
                "villages": [
                    {"en": "Kannad Rural", "mr": "कन्नड ग्रामीण", "lat": 20.2647, "lon": 75.1322},
                    {"en": "Chalisgaon Road Fata", "mr": "चाळीसगाव रोड फाटा", "lat": 20.3120, "lon": 75.1150}
                ]
            },
            "Sillod": {
                "en": "Sillod", "mr": "सिल्लोड", "lat": 20.3047, "lon": 75.6517,
                "villages": [
                    {"en": "Sillod Maize Belt", "mr": "सिल्लोड मका पट्टा", "lat": 20.3047, "lon": 75.6517},
                    {"en": "Ajanta", "mr": "अजिंठा", "lat": 20.5310, "lon": 75.7480}
                ]
            }
        }
    },
    "Beed": {
        "en": "Beed", "mr": "बीड", "lat": 18.9891, "lon": 75.7601,
        "talukas": {
            "Beed": {
                "en": "Beed", "mr": "बीड", "lat": 18.9891, "lon": 75.7601,
                "villages": [
                    {"en": "Beed Rural", "mr": "बीड ग्रामीण", "lat": 18.9891, "lon": 75.7601},
                    {"en": "Nalwandi", "mr": "नाळवंडी", "lat": 19.0410, "lon": 75.7180},
                    {"en": "Pali", "mr": "पाली", "lat": 18.9250, "lon": 75.8120}
                ]
            },
            "Georai": {
                "en": "Georai", "mr": "गेवराई", "lat": 19.2639, "lon": 75.7533,
                "villages": [
                    {"en": "Georai Cotton Hub", "mr": "गेवराई कापूस केंद्र", "lat": 19.2639, "lon": 75.7533},
                    {"en": "Madalmohi", "mr": "मादळमोही", "lat": 19.1820, "lon": 75.6810}
                ]
            },
            "Majalgaon": {
                "en": "Majalgaon", "mr": "माजलगाव", "lat": 19.1486, "lon": 76.2231,
                "villages": [
                    {"en": "Majalgaon Dam Belt", "mr": "माजलगाव धरण परिसर", "lat": 19.1486, "lon": 76.2231},
                    {"en": "Talkhed", "mr": "टाळखेड", "lat": 19.0910, "lon": 76.2840}
                ]
            },
            "Parli": {
                "en": "Parli Vaijnath", "mr": "परळी वैजनाथ", "lat": 18.8489, "lon": 76.5333,
                "villages": [
                    {"en": "Parli Mandi", "mr": "परळी बाजार", "lat": 18.8489, "lon": 76.5333},
                    {"en": "Dharmapuri", "mr": "धर्मापुरी", "lat": 18.8120, "lon": 76.6120}
                ]
            },
            "Ambejogai": {
                "en": "Ambejogai", "mr": "अंबाजोगाई", "lat": 18.7303, "lon": 76.3886,
                "villages": [
                    {"en": "Ambejogai College of Agri", "mr": "अंबाजोगाई कृषी महाविद्यालय परिसर", "lat": 18.7303, "lon": 76.3886},
                    {"en": "Bardapur", "mr": "बर्दापूर", "lat": 18.6720, "lon": 76.4950}
                ]
            },
            "Ashti": {
                "en": "Ashti", "mr": "आष्टी", "lat": 18.8042, "lon": 75.1764,
                "villages": [
                    {"en": "Ashti Town", "mr": "आष्टी शहर", "lat": 18.8042, "lon": 75.1764},
                    {"en": "Kada", "mr": "कडा", "lat": 18.8710, "lon": 75.1120}
                ]
            }
        }
    },
    "Bhandara": {
        "en": "Bhandara", "mr": "भंडारा", "lat": 21.1714, "lon": 79.6547,
        "talukas": {
            "Bhandara": {
                "en": "Bhandara", "mr": "भंडारा", "lat": 21.1714, "lon": 79.6547,
                "villages": [
                    {"en": "Bhandara Rice Belt", "mr": "भंडारा भात पट्टा", "lat": 21.1714, "lon": 79.6547},
                    {"en": "Shahapur", "mr": "शहापूर", "lat": 21.1980, "lon": 79.7120}
                ]
            },
            "Tumsar": {
                "en": "Tumsar", "mr": "तुमसर", "lat": 21.3822, "lon": 79.7425,
                "villages": [
                    {"en": "Tumsar Rice Market", "mr": "तुमसर तांदूळ बाजार", "lat": 21.3822, "lon": 79.7425},
                    {"en": "Sihora", "mr": "सिहोरा", "lat": 21.4510, "lon": 79.8150}
                ]
            },
            "Sakoli": {
                "en": "Sakoli", "mr": "साकोली", "lat": 21.0825, "lon": 79.9889,
                "villages": [
                    {"en": "Sakoli Paddy Hub", "mr": "साकोली भात संकलन केंद्र", "lat": 21.0825, "lon": 79.9889},
                    {"en": "Sendurwafa", "mr": "सेंदूरवाफा", "lat": 21.0950, "lon": 79.9720}
                ]
            },
            "Pauni": {
                "en": "Pauni", "mr": "पवनी", "lat": 20.7917, "lon": 79.6333,
                "villages": [
                    {"en": "Pauni Town", "mr": "पवनी शहर", "lat": 20.7917, "lon": 79.6333},
                    {"en": "Gosikhurd Catchment", "mr": "गोसीखुर्द परिसर", "lat": 20.8520, "lon": 79.6540}
                ]
            }
        }
    },
    "Buldhana": {
        "en": "Buldhana", "mr": "बुलढाणा", "lat": 20.5310, "lon": 76.1847,
        "talukas": {
            "Buldhana": {
                "en": "Buldhana", "mr": "बुलढाणा", "lat": 20.5310, "lon": 76.1847,
                "villages": [
                    {"en": "Buldhana Hill Station", "mr": "बुलढाणा शहर", "lat": 20.5310, "lon": 76.1847},
                    {"en": "Dhad", "mr": "धाड", "lat": 20.4810, "lon": 76.0820}
                ]
            },
            "Chikhli": {
                "en": "Chikhli", "mr": "चिखली", "lat": 20.3522, "lon": 76.2578,
                "villages": [
                    {"en": "Chikhli Mandi", "mr": "चिखली बाजार", "lat": 20.3522, "lon": 76.2578},
                    {"en": "Amrapur", "mr": "अमरापूर", "lat": 20.3810, "lon": 76.3540}
                ]
            },
            "Khamgaon": {
                "en": "Khamgaon", "mr": "खामगाव", "lat": 20.6869, "lon": 76.5658,
                "villages": [
                    {"en": "Khamgaon Cotton Ginning Hub", "mr": "खामगाव जिनिंग केंद्र", "lat": 20.6869, "lon": 76.5658},
                    {"en": "Jalamb", "mr": "जलंब", "lat": 20.7410, "lon": 76.6210}
                ]
            },
            "Malkapur": {
                "en": "Malkapur", "mr": "मलकापूर", "lat": 20.8833, "lon": 76.2000,
                "villages": [
                    {"en": "Malkapur Town", "mr": "मलकापूर शहर", "lat": 20.8833, "lon": 76.2000},
                    {"en": "Dudhana", "mr": "दुधना", "lat": 20.8240, "lon": 76.1720}
                ]
            },
            "Mehkar": {
                "en": "Mehkar", "mr": "मेहकर", "lat": 20.1550, "lon": 76.5714,
                "villages": [
                    {"en": "Mehkar Rural", "mr": "मेहकर ग्रामीण", "lat": 20.1550, "lon": 76.5714},
                    {"en": "Janephal", "mr": "जानेफळ", "lat": 20.2180, "lon": 76.6120}
                ]
            },
            "Lonar": {
                "en": "Lonar", "mr": "लोणार", "lat": 19.9833, "lon": 76.5167,
                "villages": [
                    {"en": "Lonar Crater Belt", "mr": "लोणार सरोवर परिसर", "lat": 19.9833, "lon": 76.5167},
                    {"en": "Bibi", "mr": "बिबी", "lat": 19.9410, "lon": 76.4320}
                ]
            }
        }
    },
    "Chandrapur": {
        "en": "Chandrapur", "mr": "चंद्रपूर", "lat": 19.9615, "lon": 79.2961,
        "talukas": {
            "Chandrapur": {
                "en": "Chandrapur", "mr": "चंद्रपूर", "lat": 19.9615, "lon": 79.2961,
                "villages": [
                    {"en": "Chandrapur Rural", "mr": "चंद्रपूर ग्रामीण", "lat": 19.9615, "lon": 79.2961},
                    {"en": "Ballarpur APMC", "mr": "बल्लारपूर बाजार", "lat": 19.8540, "lon": 79.3380}
                ]
            },
            "Warora": {
                "en": "Warora", "mr": "वरोरा", "lat": 20.2319, "lon": 79.0064,
                "villages": [
                    {"en": "Warora Cotton & Soybean Hub", "mr": "वरोरा कृषी केंद्र", "lat": 20.2319, "lon": 79.0064},
                    {"en": "Anandwan", "mr": "आनंदवन", "lat": 20.2180, "lon": 79.0340}
                ]
            },
            "Bhadravati": {
                "en": "Bhadravati", "mr": "भद्रावती", "lat": 20.0989, "lon": 79.1247,
                "villages": [
                    {"en": "Bhadravati Town", "mr": "भद्रावती शहर", "lat": 20.0989, "lon": 79.1247},
                    {"en": "Chandanwahi", "mr": "चंदनवाही", "lat": 20.1420, "lon": 79.1820}
                ]
            },
            "Rajura": {
                "en": "Rajura", "mr": "राजुरा", "lat": 19.7833, "lon": 79.3667,
                "villages": [
                    {"en": "Rajura Town", "mr": "राजुरा शहर", "lat": 19.7833, "lon": 79.3667},
                    {"en": "Gadchandur", "mr": "गडचांदूर", "lat": 19.7310, "lon": 79.2450}
                ]
            },
            "Nagbhir": {
                "en": "Nagbhir", "mr": "नागभीड", "lat": 20.5833, "lon": 79.6667,
                "villages": [
                    {"en": "Nagbhir Paddy Belt", "mr": "नागभीड भात पट्टा", "lat": 20.5833, "lon": 79.6667},
                    {"en": "Talodhi", "mr": "तळोधी", "lat": 20.5120, "lon": 79.6910}
                ]
            }
        }
    },
    "Dhule": {
        "en": "Dhule", "mr": "धुळे", "lat": 20.9042, "lon": 74.7749,
        "talukas": {
            "Dhule": {
                "en": "Dhule", "mr": "धुळे", "lat": 20.9042, "lon": 74.7749,
                "villages": [
                    {"en": "Dhule APMC Market", "mr": "धुळे कृषी बाजार", "lat": 20.9042, "lon": 74.7749},
                    {"en": "Kusumba", "mr": "कुसुंबा", "lat": 20.9850, "lon": 74.6540},
                    {"en": "Mohadi", "mr": "मोहाडी", "lat": 20.8710, "lon": 74.8210}
                ]
            },
            "Shirpur": {
                "en": "Shirpur", "mr": "शिरपूर", "lat": 21.3503, "lon": 74.8803,
                "villages": [
                    {"en": "Shirpur Pattern Water Project", "mr": "शिरपूर पॅटर्न जल संवर्धन परिसर", "lat": 21.3503, "lon": 74.8803},
                    {"en": "Boradi", "mr": "बोराडी", "lat": 21.4120, "lon": 74.9350},
                    {"en": "Holnanthe", "mr": "होळनांथे", "lat": 21.3120, "lon": 74.8150}
                ]
            },
            "Sakri": {
                "en": "Sakri", "mr": "साक्री", "lat": 20.9328, "lon": 74.3164,
                "villages": [
                    {"en": "Sakri Town", "mr": "साक्री शहर", "lat": 20.9328, "lon": 74.3164},
                    {"en": "Nijampur", "mr": "निजामपूर", "lat": 21.0420, "lon": 74.3850},
                    {"en": "Dahivel", "mr": "दहीवेल", "lat": 20.9810, "lon": 74.2150}
                ]
            },
            "Sindkheda": {
                "en": "Sindkheda", "mr": "शिंदखेडा", "lat": 21.2647, "lon": 74.7508,
                "villages": [
                    {"en": "Sindkheda Town", "mr": "शिंदखेडा शहर", "lat": 21.2647, "lon": 74.7508},
                    {"en": "Dondaicha APMC (Chilli Hub)", "mr": "दोंडाईचा मिरची बाजार", "lat": 21.3250, "lon": 74.5750},
                    {"en": "Chimthane", "mr": "चिमठाणे", "lat": 21.2150, "lon": 74.8410}
                ]
            }
        }
    },
    "Gadchiroli": {
        "en": "Gadchiroli", "mr": "गडचिरोली", "lat": 20.1809, "lon": 79.9939,
        "talukas": {
            "Gadchiroli": {
                "en": "Gadchiroli", "mr": "गडचिरोली", "lat": 20.1809, "lon": 79.9939,
                "villages": [
                    {"en": "Gadchiroli APMC", "mr": "गडचिरोली कृषी बाजार", "lat": 20.1809, "lon": 79.9939},
                    {"en": "Porla", "mr": "पोरला", "lat": 20.2450, "lon": 80.0520}
                ]
            },
            "Armori": {
                "en": "Armori", "mr": "आरमोरी", "lat": 20.4633, "lon": 79.9886,
                "villages": [
                    {"en": "Armori Rice Belt", "mr": "आरमोरी भात पट्टा", "lat": 20.4633, "lon": 79.9886},
                    {"en": "Wadadha", "mr": "वडधा", "lat": 20.5120, "lon": 80.0210}
                ]
            },
            "Chamorshi": {
                "en": "Chamorshi", "mr": "चामोर्शी", "lat": 19.9328, "lon": 79.8972,
                "villages": [
                    {"en": "Chamorshi Rural", "mr": "चामोर्शी ग्रामीण", "lat": 19.9328, "lon": 79.8972},
                    {"en": "Ghot", "mr": "घोट", "lat": 19.8650, "lon": 80.0120}
                ]
            },
            "Aheri": {
                "en": "Aheri", "mr": "अहेरी", "lat": 19.4181, "lon": 79.9961,
                "villages": [
                    {"en": "Aheri Forest Agriculture", "mr": "अहेरी कृषी परिसर", "lat": 19.4181, "lon": 79.9961},
                    {"en": "Allapalli", "mr": "आल्लापल्ली", "lat": 19.4290, "lon": 80.0620}
                ]
            }
        }
    },
    "Gondia": {
        "en": "Gondia", "mr": "गोंदिया", "lat": 21.4624, "lon": 80.1981,
        "talukas": {
            "Gondia": {
                "en": "Gondia", "mr": "गोंदिया", "lat": 21.4624, "lon": 80.1981,
                "villages": [
                    {"en": "Gondia Rice Mill Cluster", "mr": "गोंदिया राईस मिल क्लस्टर", "lat": 21.4624, "lon": 80.1981},
                    {"en": "Kudwa", "mr": "कुडवा", "lat": 21.4780, "lon": 80.2150}
                ]
            },
            "Tirora": {
                "en": "Tirora", "mr": "तिरोडा", "lat": 21.4111, "lon": 79.9353,
                "villages": [
                    {"en": "Tirora Paddy Market", "mr": "तिरोडा धान बाजार", "lat": 21.4111, "lon": 79.9353},
                    {"en": "Kachewani", "mr": "काचेवानी", "lat": 21.4420, "lon": 79.9120}
                ]
            },
            "Goregaon": {
                "en": "Goregaon", "mr": "गोरेगाव", "lat": 21.3411, "lon": 80.2319,
                "villages": [
                    {"en": "Goregaon Rural", "mr": "गोरेगाव ग्रामीण", "lat": 21.3411, "lon": 80.2319},
                    {"en": "Mundikota", "mr": "मुंडीकोटा", "lat": 21.3810, "lon": 80.1750}
                ]
            },
            "Amgaon": {
                "en": "Amgaon", "mr": "आमगाव", "lat": 21.3653, "lon": 80.3789,
                "villages": [
                    {"en": "Amgaon Mandi", "mr": "आमगाव बाजार", "lat": 21.3653, "lon": 80.3789},
                    {"en": "Padampur", "mr": "पदमपूर", "lat": 21.4010, "lon": 80.4120}
                ]
            }
        }
    },
    "Hingoli": {
        "en": "Hingoli", "mr": "हिंगोली", "lat": 19.7197, "lon": 77.1478,
        "talukas": {
            "Hingoli": {
                "en": "Hingoli", "mr": "हिंगोली", "lat": 19.7197, "lon": 77.1478,
                "villages": [
                    {"en": "Hingoli Mandi", "mr": "हिंगोली कृषी बाजार", "lat": 19.7197, "lon": 77.1478},
                    {"en": "Kalyan Girgaon", "mr": "कल्याण गिरगाव", "lat": 19.7540, "lon": 77.1850}
                ]
            },
            "Basmath": {
                "en": "Basmath", "mr": "वसमत", "lat": 19.5167, "lon": 77.1667,
                "villages": [
                    {"en": "Basmath Turmeric Market", "mr": "वसमत हळद बाजार", "lat": 19.5167, "lon": 77.1667},
                    {"en": "Kurunda", "mr": "कुरुंदा", "lat": 19.4620, "lon": 77.2150}
                ]
            },
            "Kalamnuri": {
                "en": "Kalamnuri", "mr": "कलमनुरी", "lat": 19.6667, "lon": 77.3333,
                "villages": [
                    {"en": "Kalamnuri Town", "mr": "कलमनुरी शहर", "lat": 19.6667, "lon": 77.3333},
                    {"en": "Akhada Balapur", "mr": "आखाडा बाळापूर", "lat": 19.6120, "lon": 77.4010}
                ]
            },
            "Senggaon": {
                "en": "Senggaon", "mr": "सेनगाव", "lat": 19.7947, "lon": 76.9744,
                "villages": [
                    {"en": "Senggaon Soybean Belt", "mr": "सेनगाव सोयाबीन पट्टा", "lat": 19.7947, "lon": 76.9744},
                    {"en": "Kadti", "mr": "कडती", "lat": 19.8310, "lon": 76.9320}
                ]
            },
            "Aundha Nagnath": {
                "en": "Aundha Nagnath", "mr": "औंढा नागनाथ", "lat": 19.5333, "lon": 77.0333,
                "villages": [
                    {"en": "Aundha Rural", "mr": "औंढा ग्रामीण", "lat": 19.5333, "lon": 77.0333},
                    {"en": "Rupur", "mr": "रुपर", "lat": 19.5710, "lon": 77.0720}
                ]
            }
        }
    },
    "Jalgaon": {
        "en": "Jalgaon", "mr": "जळगाव", "lat": 21.0077, "lon": 75.5626,
        "talukas": {
            "Jalgaon": {
                "en": "Jalgaon", "mr": "जळगाव", "lat": 21.0077, "lon": 75.5626,
                "villages": [
                    {"en": "Jalgaon APMC Market", "mr": "जळगाव कृषी उत्पन्न बाजार", "lat": 21.0077, "lon": 75.5626},
                    {"en": "Neri", "mr": "नेरी", "lat": 20.9540, "lon": 75.6450},
                    {"en": "Asoda", "mr": "आसोदा", "lat": 21.0520, "lon": 75.6010}
                ]
            },
            "Raver": {
                "en": "Raver", "mr": "रावेर", "lat": 21.2503, "lon": 75.9667,
                "villages": [
                    {"en": "Raver Banana Capital", "mr": "रावेर केळी राजधानी", "lat": 21.2503, "lon": 75.9667},
                    {"en": "Savda", "mr": "सावदा", "lat": 21.1500, "lon": 75.8833},
                    {"en": "Ainpur", "mr": "ऐनपूर", "lat": 21.2840, "lon": 76.0120}
                ]
            },
            "Yawal": {
                "en": "Yawal", "mr": "यावल", "lat": 21.1683, "lon": 75.6961,
                "villages": [
                    {"en": "Yawal Banana Belt", "mr": "यावल केळी पट्टा", "lat": 21.1683, "lon": 75.6961},
                    {"en": "Bhalod", "mr": "भालोद", "lat": 21.1920, "lon": 75.7680}
                ]
            },
            "Chalisgaon": {
                "en": "Chalisgaon", "mr": "चाळीसगाव", "lat": 20.4633, "lon": 75.0181,
                "villages": [
                    {"en": "Chalisgaon Cotton Market", "mr": "चाळीसगाव कापूस बाजार", "lat": 20.4633, "lon": 75.0181},
                    {"en": "Mehunsbare", "mr": "मेहुणबारे", "lat": 20.5310, "lon": 74.9540}
                ]
            },
            "Pachora": {
                "en": "Pachora", "mr": "पाचोरा", "lat": 20.6667, "lon": 75.3500,
                "villages": [
                    {"en": "Pachora Town", "mr": "पाचोरा शहर", "lat": 20.6667, "lon": 75.3500},
                    {"en": "Shewale", "mr": "शेवाळे", "lat": 20.6120, "lon": 75.4120}
                ]
            },
            "Chopda": {
                "en": "Chopda", "mr": "चोपडा", "lat": 21.2500, "lon": 75.3000,
                "villages": [
                    {"en": "Chopda Tapi Basin", "mr": "चोपडा तापी खोरे", "lat": 21.2500, "lon": 75.3000},
                    {"en": "Adavad", "mr": "अडावद", "lat": 21.2810, "lon": 75.4210}
                ]
            },
            "Amalner": {
                "en": "Amalner", "mr": "अमळनेर", "lat": 21.0500, "lon": 75.0667,
                "villages": [
                    {"en": "Amalner Mandi", "mr": "अमळनेर बाजार", "lat": 21.0500, "lon": 75.0667},
                    {"en": "Marwad", "mr": "मारवड", "lat": 21.1240, "lon": 75.0120}
                ]
            },
            "Bhusawal": {
                "en": "Bhusawal", "mr": "भुसावळ", "lat": 21.0450, "lon": 75.7900,
                "villages": [
                    {"en": "Bhusawal Junction & APMC", "mr": "भुसावळ कृषी बाजार", "lat": 21.0450, "lon": 75.7900},
                    {"en": "Varangaon", "mr": "वरणगाव", "lat": 21.0180, "lon": 75.9080}
                ]
            }
        }
    },
    "Jalna": {
        "en": "Jalna", "mr": "जालना", "lat": 19.8347, "lon": 75.8816,
        "talukas": {
            "Jalna": {
                "en": "Jalna", "mr": "जालना", "lat": 19.8347, "lon": 75.8816,
                "villages": [
                    {"en": "Jalna Hybrid Seed Capital & APMC", "mr": "जालना संकरित बियाणे व कृषी बाजार", "lat": 19.8347, "lon": 75.8816},
                    {"en": "Ramnagar", "mr": "रामनगर", "lat": 19.8720, "lon": 75.9250},
                    {"en": "Pirekalyan", "mr": "पिरेकल्याण", "lat": 19.7910, "lon": 75.8240}
                ]
            },
            "Ambad": {
                "en": "Ambad", "mr": "अंबड", "lat": 19.6158, "lon": 75.7950,
                "villages": [
                    {"en": "Ambad Mosambi Belt", "mr": "अंबड मोसंबी पट्टा", "lat": 19.6158, "lon": 75.7950},
                    {"en": "Wadigodri", "mr": "वाडीगोद्री", "lat": 19.5420, "lon": 75.7250}
                ]
            },
            "Partur": {
                "en": "Partur", "mr": "परतूर", "lat": 19.5956, "lon": 76.2167,
                "villages": [
                    {"en": "Partur Town", "mr": "परतूर शहर", "lat": 19.5956, "lon": 76.2167},
                    {"en": "Watur", "mr": "वाटूर", "lat": 19.5210, "lon": 76.1420}
                ]
            },
            "Ghansawangi": {
                "en": "Ghansawangi", "mr": "घनसावंगी", "lat": 19.5317, "lon": 75.9922,
                "villages": [
                    {"en": "Ghansawangi Cotton Hub", "mr": "घनसावंगी कापूस केंद्र", "lat": 19.5317, "lon": 75.9922},
                    {"en": "Kumbhar Pimpalgaon", "mr": "कुंभार पिंपळगाव", "lat": 19.4620, "lon": 76.0840}
                ]
            },
            "Bhokardan": {
                "en": "Bhokardan", "mr": "भोकरदन", "lat": 20.2567, "lon": 75.7683,
                "villages": [
                    {"en": "Bhokardan Town", "mr": "भोकरदन शहर", "lat": 20.2567, "lon": 75.7683},
                    {"en": "Hasanabad", "mr": "हसनाबाद", "lat": 20.1510, "lon": 75.8450}
                ]
            },
            "Badnapur": {
                "en": "Badnapur", "mr": "बदनपूर", "lat": 19.8697, "lon": 75.7228,
                "villages": [
                    {"en": "Badnapur Agri Research Station", "mr": "बदनपूर कृषी संशोधन केंद्र", "lat": 19.8697, "lon": 75.7228},
                    {"en": "Roshangaon", "mr": "रोशनगाव", "lat": 19.9210, "lon": 75.7640}
                ]
            }
        }
    },
    "Kolhapur": {
        "en": "Kolhapur", "mr": "कोल्हापूर", "lat": 16.7050, "lon": 74.2433,
        "talukas": {
            "Karveer": {
                "en": "Karveer", "mr": "करवीर", "lat": 16.7050, "lon": 74.2433,
                "villages": [
                    {"en": "Kolhapur APMC & Jaggery Market", "mr": "कोल्हापूर गुळ बाजार व कृषी उत्पन्न", "lat": 16.7050, "lon": 74.2433},
                    {"en": "Uchgaon", "mr": "उचगाव", "lat": 16.6850, "lon": 74.2810},
                    {"en": "Gandhinagar", "mr": "गांधीनगर", "lat": 16.7120, "lon": 74.2890}
                ]
            },
            "Shirol": {
                "en": "Shirol", "mr": "शिरोळ", "lat": 16.7333, "lon": 74.6000,
                "villages": [
                    {"en": "Jaysingpur APMC", "mr": "जयसिंगपूर कृषी बाजार", "lat": 16.7833, "lon": 74.5667},
                    {"en": "Kurundwad", "mr": "कुरुंदवाड", "lat": 16.6833, "lon": 74.6000},
                    {"en": "Nandre", "mr": "नांद्रे", "lat": 16.7540, "lon": 74.5210}
                ]
            },
            "Hatkanangale": {
                "en": "Hatkanangale", "mr": "हातकणंगले", "lat": 16.7500, "lon": 74.4500,
                "villages": [
                    {"en": "Ichalkaranji Sugarcane Belt", "mr": "इचलकरंजी ऊस पट्टा", "lat": 16.7000, "lon": 74.4667},
                    {"en": "Rukadi", "mr": "रुकडी", "lat": 16.7180, "lon": 74.3720},
                    {"en": "Hupari Silver & Agri", "mr": "हुपरी परिसर", "lat": 16.6180, "lon": 74.4020}
                ]
            },
            "Radhanagari": {
                "en": "Radhanagari", "mr": "राधानगरी", "lat": 16.4167, "lon": 74.0000,
                "villages": [
                    {"en": "Radhanagari Dam Belt", "mr": "राधानगरी धरण परिसर", "lat": 16.4167, "lon": 74.0000},
                    {"en": "Kasaba Tarale", "mr": "कसबा तारळे", "lat": 16.4820, "lon": 74.0850}
                ]
            },
            "Kagal": {
                "en": "Kagal", "mr": "कागल", "lat": 16.5833, "lon": 74.3167,
                "villages": [
                    {"en": "Kagal Sugar Factory Belt", "mr": "कागल साखर कारखाना परिसर", "lat": 16.5833, "lon": 74.3167},
                    {"en": "Murgud", "mr": "मुरगूड", "lat": 16.4850, "lon": 74.2250}
                ]
            },
            "Panhala": {
                "en": "Panhala", "mr": "पन्हाळा", "lat": 16.8167, "lon": 74.1167,
                "villages": [
                    {"en": "Panhala Hills", "mr": "पन्हाळा परिसर", "lat": 16.8167, "lon": 74.1167},
                    {"en": "Kodoli", "mr": "कोडोली", "lat": 16.8840, "lon": 74.1950}
                ]
            }
        }
    },
    "Latur": {
        "en": "Latur", "mr": "लातूर", "lat": 18.4088, "lon": 76.5604,
        "talukas": {
            "Latur": {
                "en": "Latur", "mr": "लातूर", "lat": 18.4088, "lon": 76.5604,
                "villages": [
                    {"en": "Latur National Pulse & Oilseed APMC", "mr": "लातूर राष्ट्रीय डाळ व तेलबिया बाजार", "lat": 18.4088, "lon": 76.5604},
                    {"en": "Harangul", "mr": "हरंगुळ", "lat": 18.3840, "lon": 76.5120},
                    {"en": "Murud", "mr": "मुरुड", "lat": 18.4310, "lon": 76.4180}
                ]
            },
            "Ausa": {
                "en": "Ausa", "mr": "औसा", "lat": 18.2514, "lon": 76.5056,
                "villages": [
                    {"en": "Ausa Soybean Belt", "mr": "औसा सोयाबीन पट्टा", "lat": 18.2514, "lon": 76.5056},
                    {"en": "Matola", "mr": "मातोळा", "lat": 18.2910, "lon": 76.5640},
                    {"en": "Belkund", "mr": "बेलकुंड", "lat": 18.2150, "lon": 76.4420}
                ]
            },
            "Nilanga": {
                "en": "Nilanga", "mr": "निलंगा", "lat": 18.1258, "lon": 76.7644,
                "villages": [
                    {"en": "Nilanga Mandi", "mr": "निलंगा कृषी बाजार", "lat": 18.1258, "lon": 76.7644},
                    {"en": "Aurad Shahajani", "mr": "औरद शहाजानी", "lat": 18.0620, "lon": 76.9150}
                ]
            },
            "Udgir": {
                "en": "Udgir", "mr": "उदगीर", "lat": 18.3942, "lon": 76.8684,
                "villages": [
                    {"en": "Udgir Veterinary College & APMC", "mr": "उदगीर पशुवैद्यकीय महाविद्यालय व बाजार", "lat": 18.3942, "lon": 76.8684},
                    {"en": "Her", "mr": "हेर", "lat": 18.4410, "lon": 76.9320},
                    {"en": "Deoni (Cow Breed Center)", "mr": "देवणी (देवणी गाय संशोधन केंद्र)", "lat": 18.2680, "lon": 77.0420}
                ]
            },
            "Ahmedpur": {
                "en": "Ahmedpur", "mr": "अहमदपूर", "lat": 18.7050, "lon": 76.9325,
                "villages": [
                    {"en": "Ahmedpur Town", "mr": "अहमदपूर शहर", "lat": 18.7050, "lon": 76.9325},
                    {"en": "Shirur Tajband", "mr": "शिरूर ताजबंद", "lat": 18.6650, "lon": 76.9850}
                ]
            },
            "Chakur": {
                "en": "Chakur", "mr": "चाकूर", "lat": 18.5714, "lon": 76.8042,
                "villages": [
                    {"en": "Chakur Rural", "mr": "चाकूर ग्रामीण", "lat": 18.5714, "lon": 76.8042},
                    {"en": "Nalegaon", "mr": "नालेगाव", "lat": 18.5120, "lon": 76.7540}
                ]
            }
        }
    },
    "Mumbai City": {
        "en": "Mumbai City", "mr": "मुंबई शहर", "lat": 18.9388, "lon": 72.8354,
        "talukas": {
            "Mumbai City": {
                "en": "Mumbai City", "mr": "मुंबई शहर", "lat": 18.9388, "lon": 72.8354,
                "villages": [
                    {"en": "Nariman Point / Mantralaya", "mr": "मंत्रालय व प्रशासकीय केंद्र", "lat": 18.9270, "lon": 72.8235},
                    {"en": "Byculla Market", "mr": "भायखळा भाजीपाला बाजार", "lat": 18.9750, "lon": 72.8320}
                ]
            }
        }
    },
    "Mumbai Suburban": {
        "en": "Mumbai Suburban", "mr": "मुंबई उपनगर", "lat": 19.0760, "lon": 72.8777,
        "talukas": {
            "Bandra": {
                "en": "Bandra", "mr": "वांद्रे", "lat": 19.0596, "lon": 72.8295,
                "villages": [
                    {"en": "Bandra West", "mr": "वांद्रे पश्चिम", "lat": 19.0596, "lon": 72.8295},
                    {"en": "BKC", "mr": "बीकेसी", "lat": 19.0660, "lon": 72.8680}
                ]
            },
            "Kurla": {
                "en": "Kurla", "mr": "कुर्ला", "lat": 19.0728, "lon": 72.8800,
                "villages": [
                    {"en": "Vashi APMC Agri Terminal", "mr": "वाशी नवी मुंबई एपीएमसी बाजार", "lat": 19.0750, "lon": 73.0020},
                    {"en": "Ghatkopar", "mr": "घाटकोपर", "lat": 19.0860, "lon": 72.9080}
                ]
            },
            "Borivali": {
                "en": "Borivali", "mr": "बोरिवली", "lat": 19.2307, "lon": 72.8567,
                "villages": [
                    {"en": "Aarey Milk Colony", "mr": "आरे दुग्ध वसाहत", "lat": 19.1480, "lon": 72.8750},
                    {"en": "Gorai", "mr": "गोराई", "lat": 19.2450, "lon": 72.8020}
                ]
            }
        }
    },
    "Nagpur": {
        "en": "Nagpur", "mr": "नागपूर", "lat": 21.1458, "lon": 79.0882,
        "talukas": {
            "Nagpur Urban": {
                "en": "Nagpur Urban", "mr": "नागपूर शहर", "lat": 21.1458, "lon": 79.0882,
                "villages": [
                    {"en": "Kalamna Wholesale Grain & Orange Market", "mr": "कळमना धान्य व संत्रा बाजार", "lat": 21.1850, "lon": 79.1350},
                    {"en": "College of Agriculture Nagpur", "mr": "कृषी महाविद्यालय नागपूर परिसर", "lat": 21.1480, "lon": 79.0710}
                ]
            },
            "Katol": {
                "en": "Katol", "mr": "काटोल", "lat": 21.2722, "lon": 78.5836,
                "villages": [
                    {"en": "Katol Orange Export Hub", "mr": "काटोल संत्रा निर्यात केंद्र", "lat": 21.2722, "lon": 78.5836},
                    {"en": "Yenwa", "mr": "येनवा", "lat": 21.3120, "lon": 78.6450}
                ]
            },
            "Narkhed": {
                "en": "Narkhed", "mr": "नरखेड", "lat": 21.3667, "lon": 78.5333,
                "villages": [
                    {"en": "Narkhed Citrus Belt", "mr": "नरखेड लिंबूवर्गीय संत्रा पट्टा", "lat": 21.3667, "lon": 78.5333},
                    {"en": "Mowad", "mr": "मोवाड", "lat": 21.4120, "lon": 78.4850}
                ]
            },
            "Saoner": {
                "en": "Saoner", "mr": "सावनेर", "lat": 21.3853, "lon": 78.9186,
                "villages": [
                    {"en": "Saoner Town", "mr": "सावनेर शहर", "lat": 21.3853, "lon": 78.9186},
                    {"en": "Khapa", "mr": "खापा", "lat": 21.4180, "lon": 79.0120}
                ]
            },
            "Ramtek": {
                "en": "Ramtek", "mr": "रामटेक", "lat": 21.3972, "lon": 79.3297,
                "villages": [
                    {"en": "Ramtek Totladoh Belt", "mr": "रामटेक तोतलाडोह परिसर", "lat": 21.3972, "lon": 79.3297},
                    {"en": "Mansar", "mr": "मानसर", "lat": 21.3750, "lon": 79.2840}
                ]
            },
            "Umred": {
                "en": "Umred", "mr": "उमरेड", "lat": 20.8528, "lon": 79.3297,
                "villages": [
                    {"en": "Umred Chilli & Soybean Hub", "mr": "उमरेड मिरची व सोयाबीन केंद्र", "lat": 20.8528, "lon": 79.3297},
                    {"en": "Bhiwapur", "mr": "भिवापूर (प्रसिद्ध मिरची)", "lat": 20.7680, "lon": 79.5150}
                ]
            },
            "Hingna": {
                "en": "Hingna", "mr": "हिंगणा", "lat": 21.0667, "lon": 78.9667,
                "villages": [
                    {"en": "Hingna Agri Corridor", "mr": "हिंगणा कृषी परिसर", "lat": 21.0667, "lon": 78.9667},
                    {"en": "Kanhan Pipri", "mr": "कान्हन पिपरी", "lat": 21.0250, "lon": 78.9240}
                ]
            }
        }
    },
    "Nanded": {
        "en": "Nanded", "mr": "नांदेड", "lat": 19.1557, "lon": 77.3116,
        "talukas": {
            "Nanded": {
                "en": "Nanded", "mr": "नांदेड", "lat": 19.1557, "lon": 77.3116,
                "villages": [
                    {"en": "Nanded Cotton & Banana APMC", "mr": "नांदेड कापूस व केळी बाजार", "lat": 19.1557, "lon": 77.3116},
                    {"en": "Wajegaon", "mr": "वाजेगाव", "lat": 19.1250, "lon": 77.2840},
                    {"en": "Taroda", "mr": "तरोडा", "lat": 19.1850, "lon": 77.3240}
                ]
            },
            "Loha": {
                "en": "Loha", "mr": "लोहा", "lat": 18.9483, "lon": 77.1217,
                "villages": [
                    {"en": "Loha Town", "mr": "लोहा शहर", "lat": 18.9483, "lon": 77.1217},
                    {"en": "Sonkhed", "mr": "सोनखेड", "lat": 19.0120, "lon": 77.1850}
                ]
            },
            "Kandhar": {
                "en": "Kandhar", "mr": "कंधार", "lat": 18.8917, "lon": 77.1950,
                "villages": [
                    {"en": "Kandhar Rural", "mr": "कंधार ग्रामीण", "lat": 18.8917, "lon": 77.1950},
                    {"en": "Shewadi", "mr": "शेवडी", "lat": 18.8410, "lon": 77.2450}
                ]
            },
            "Degloor": {
                "en": "Degloor", "mr": "देगलूर", "lat": 18.5528, "lon": 77.5750,
                "villages": [
                    {"en": "Degloor Border APMC", "mr": "देगलूर कृषी उत्पन्न बाजार", "lat": 18.5528, "lon": 77.5750},
                    {"en": "Shahapur", "mr": "शहापूर", "lat": 18.5850, "lon": 77.6250}
                ]
            },
            "Mudkhed": {
                "en": "Mudkhed", "mr": "मुदखेड", "lat": 19.1667, "lon": 77.5167,
                "villages": [
                    {"en": "Mudkhed Banana Belt", "mr": "मुदखेड केळी पट्टा", "lat": 19.1667, "lon": 77.5167},
                    {"en": "Mugad", "mr": "मुगट", "lat": 19.1240, "lon": 77.4620}
                ]
            },
            "Bhokar": {
                "en": "Bhokar", "mr": "भोकर", "lat": 19.2167, "lon": 77.6667,
                "villages": [
                    {"en": "Bhokar Town", "mr": "भोकर शहर", "lat": 19.2167, "lon": 77.6667},
                    {"en": "Matul", "mr": "मातुल", "lat": 19.2650, "lon": 77.7120}
                ]
            },
            "Hadgaon": {
                "en": "Hadgaon", "mr": "हदगाव", "lat": 19.5000, "lon": 77.6667,
                "villages": [
                    {"en": "Hadgaon Cotton Hub", "mr": "हदगाव कापूस केंद्र", "lat": 19.5000, "lon": 77.6667},
                    {"en": "Tamsa", "mr": "तामसा", "lat": 19.4210, "lon": 77.7210}
                ]
            },
            "Kinwat": {
                "en": "Kinwat", "mr": "किनवट", "lat": 19.6333, "lon": 78.2000,
                "villages": [
                    {"en": "Kinwat Forest Agriculture", "mr": "किनवट कृषी पट्टा", "lat": 19.6333, "lon": 78.2000},
                    {"en": "Bodadi", "mr": "बोडडी", "lat": 19.6820, "lon": 78.1450}
                ]
            }
        }
    },
    "Nandurbar": {
        "en": "Nandurbar", "mr": "नंदुरबार", "lat": 21.3742, "lon": 74.2408,
        "talukas": {
            "Nandurbar": {
                "en": "Nandurbar", "mr": "नंदुरबार", "lat": 21.3742, "lon": 74.2408,
                "villages": [
                    {"en": "Nandurbar Red Chilli Capital & APMC", "mr": "नंदुरबार लाल मिरची बाजार व मुख्य केंद्र", "lat": 21.3742, "lon": 74.2408},
                    {"en": "Koparli", "mr": "कोपरली", "lat": 21.4120, "lon": 74.3120},
                    {"en": "Waghode", "mr": "वाघोदे", "lat": 21.3250, "lon": 74.1950}
                ]
            },
            "Shahada": {
                "en": "Shahada", "mr": "शहादा", "lat": 21.5453, "lon": 74.4719,
                "villages": [
                    {"en": "Shahada Banana & Papaya Hub", "mr": "शहादा केळी व पपई पट्टा", "lat": 21.5453, "lon": 74.4719},
                    {"en": "Prakasha (Dakshin Kashi)", "mr": "प्रकाशा", "lat": 21.5120, "lon": 74.3850},
                    {"en": "Mohida", "mr": "मोहिदा", "lat": 21.5820, "lon": 74.5120}
                ]
            },
            "Taloda": {
                "en": "Taloda", "mr": "तळोदा", "lat": 21.5647, "lon": 74.2181,
                "villages": [
                    {"en": "Taloda Rural", "mr": "तळोदा ग्रामीण", "lat": 21.5647, "lon": 74.2181},
                    {"en": "Borad", "mr": "बोराड", "lat": 21.5210, "lon": 74.3010}
                ]
            },
            "Navapur": {
                "en": "Navapur", "mr": "नवापूर", "lat": 21.1667, "lon": 73.8000,
                "villages": [
                    {"en": "Navapur Poultry & Agri Hub", "mr": "नवापूर कुक्कुटपालन व शेती केंद्र", "lat": 21.1667, "lon": 73.8000},
                    {"en": "Chinchpada", "mr": "चिंचपाडा", "lat": 21.2120, "lon": 73.9120}
                ]
            },
            "Dhadgaon": {
                "en": "Dhadgaon (Akrani)", "mr": "धडगाव (अक्राणी)", "lat": 21.8286, "lon": 74.2250,
                "villages": [
                    {"en": "Toranmal Hills", "mr": "तोरणमाळ परिसर", "lat": 21.8740, "lon": 74.4560},
                    {"en": "Dhadgaon Town", "mr": "धडगाव शहर", "lat": 21.8286, "lon": 74.2250}
                ]
            },
            "Akkalkuwa": {
                "en": "Akkalkuwa", "mr": "अक्कलकुवा", "lat": 21.5583, "lon": 74.0250,
                "villages": [
                    {"en": "Akkalkuwa Town", "mr": "अक्कलकुवा शहर", "lat": 21.5583, "lon": 74.0250},
                    {"en": "Molgi", "mr": "मोलगी", "lat": 21.6850, "lon": 73.9850}
                ]
            }
        }
    },
    "Nashik": {
        "en": "Nashik", "mr": "नाशिक", "lat": 19.9975, "lon": 73.7898,
        "talukas": {
            "Nashik": {
                "en": "Nashik", "mr": "नाशिक", "lat": 19.9975, "lon": 73.7898,
                "villages": [
                    {"en": "Nashik City APMC", "mr": "नाशिक कृषी उत्पन्न बाजार", "lat": 19.9975, "lon": 73.7898},
                    {"en": "Adgaon Vegetable Hub", "mr": "आडगाव भाजीपाला पट्टा", "lat": 20.0420, "lon": 73.8540},
                    {"en": "Gangapur Grape Belt", "mr": "गंगापूर द्राक्ष परिसर", "lat": 20.0210, "lon": 73.7120}
                ]
            },
            "Niphad": {
                "en": "Niphad", "mr": "निफाड", "lat": 20.0764, "lon": 74.1086,
                "villages": [
                    {"en": "Pimpalgaon Baswant (Tomato & Grape APMC)", "mr": "पिंपळगाव बसवंत (टोमॅटो व द्राक्ष बाजार)", "lat": 20.1742, "lon": 73.9878},
                    {"en": "Niphad Town", "mr": "निफाड शहर", "lat": 20.0764, "lon": 74.1086},
                    {"en": "Lasalgaon (Asia's Largest Onion Market)", "mr": "लासलगाव (आशियातील सर्वात मोठी कांदा बाजारपेठ)", "lat": 20.1469, "lon": 74.2289},
                    {"en": "Ozar", "mr": "ओझर", "lat": 20.0950, "lon": 73.9310},
                    {"en": "Ranwad", "mr": "रानवड", "lat": 20.1250, "lon": 74.0840}
                ]
            },
            "Dindori": {
                "en": "Dindori", "mr": "दिंडोरी", "lat": 20.2017, "lon": 73.8322,
                "villages": [
                    {"en": "Dindori Vineyard Belt", "mr": "दिंडोरी द्राक्ष बागायत पट्टा", "lat": 20.2017, "lon": 73.8322},
                    {"en": "Vani (Saptashrungi Foothills)", "mr": "वणी", "lat": 20.3240, "lon": 73.8950},
                    {"en": "Mokhada Road Fata", "mr": "मोखाडा रोड फाटा", "lat": 20.1850, "lon": 73.7840}
                ]
            },
            "Yeola": {
                "en": "Yeola", "mr": "येवला", "lat": 20.0422, "lon": 74.4864,
                "villages": [
                    {"en": "Yeola Onion & Maize APMC", "mr": "येवला कांदा व मका बाजार", "lat": 20.0422, "lon": 74.4864},
                    {"en": "Andarsul", "mr": "अंदरसुल", "lat": 20.0120, "lon": 74.5680}
                ]
            },
            "Sinnar": {
                "en": "Sinnar", "mr": "सिन्नर", "lat": 19.8458, "lon": 73.9981,
                "villages": [
                    {"en": "Sinnar Mandi", "mr": "सिन्नर कृषी बाजार", "lat": 19.8458, "lon": 73.9981},
                    {"en": "Wavi", "mr": "वावी", "lat": 19.8820, "lon": 74.1520},
                    {"en": "Musalgaon MIDC & Agri", "mr": "मुसळगाव", "lat": 19.8710, "lon": 74.0410}
                ]
            },
            "Kalwan": {
                "en": "Kalwan", "mr": "कळवण", "lat": 20.4950, "lon": 73.9889,
                "villages": [
                    {"en": "Kalwan Onion Belt", "mr": "कळवण कांदा पट्टा", "lat": 20.4950, "lon": 73.9889},
                    {"en": "Abhona", "mr": "अभsplitONA", "lat": 20.5510, "lon": 73.8920}
                ]
            },
            "Satana": {
                "en": "Satana (Baglan)", "mr": "सटाणा (बागलाण)", "lat": 20.5917, "lon": 74.2000,
                "villages": [
                    {"en": "Satana Pomegranate & Onion Hub", "mr": "सटाणा डाळिंब व कांदा केंद्र", "lat": 20.5917, "lon": 74.2000},
                    {"en": "Taharabad", "mr": "तहाराबाद", "lat": 20.6540, "lon": 74.0850}
                ]
            },
            "Malegaon": {
                "en": "Malegaon", "mr": "मालेगाव", "lat": 20.5539, "lon": 74.5289,
                "villages": [
                    {"en": "Malegaon APMC", "mr": "मालेगाव कृषी उत्पन्न बाजार", "lat": 20.5539, "lon": 74.5289},
                    {"en": "Camp Malegaon", "mr": "मालेगाव कॅम्प", "lat": 20.5710, "lon": 74.5020},
                    {"en": "Ravalgon (Sugar)", "mr": "रावळगाव", "lat": 20.6120, "lon": 74.4210}
                ]
            },
            "Chandwad": {
                "en": "Chandwad", "mr": "चांदवड", "lat": 20.3297, "lon": 74.2417,
                "villages": [
                    {"en": "Chandwad Onion APMC", "mr": "चांदवड कांदा बाजार", "lat": 20.3297, "lon": 74.2417},
                    {"en": "Vadner Bhairao", "mr": "वडनेर भैरव (द्राक्ष पट्टा)", "lat": 20.2520, "lon": 74.1540}
                ]
            },
            "Deola": {
                "en": "Deola", "mr": "देवळा", "lat": 20.5217, "lon": 74.1850,
                "villages": [
                    {"en": "Deola Onion Mandi", "mr": "देवळा कांदा बाजार", "lat": 20.5217, "lon": 74.1850},
                    {"en": "Vajirwade", "mr": "वजीरवाडे", "lat": 20.5620, "lon": 74.2210}
                ]
            },
            "Igatpuri": {
                "en": "Igatpuri", "mr": "इगतपुरी", "lat": 19.6967, "lon": 73.5636,
                "villages": [
                    {"en": "Igatpuri Rice Belt", "mr": "इगतपुरी भात पट्टा", "lat": 19.6967, "lon": 73.5636},
                    {"en": "Ghoti APMC", "mr": "घोटी भात बाजार", "lat": 19.7250, "lon": 73.6450}
                ]
            },
            "Trimbakeshwar": {
                "en": "Trimbakeshwar", "mr": "त्र्यंबकेश्वर", "lat": 19.9328, "lon": 73.5317,
                "villages": [
                    {"en": "Trimbak Rural", "mr": "त्र्यंबक ग्रामीण", "lat": 19.9328, "lon": 73.5317},
                    {"en": "Anjaneri", "mr": "अंजनेरी", "lat": 19.9540, "lon": 73.6120}
                ]
            }
        }
    },
    "Dharashiv": {
        "en": "Dharashiv (Osmanabad)", "mr": "धाराशिव (उस्मानाबाद)", "lat": 18.1861, "lon": 76.0419,
        "talukas": {
            "Dharashiv": {
                "en": "Dharashiv", "mr": "धाराशिव", "lat": 18.1861, "lon": 76.0419,
                "villages": [
                    {"en": "Dharashiv APMC", "mr": "धाराशिव कृषी उत्पन्न बाजार", "lat": 18.1861, "lon": 76.0419},
                    {"en": "Ter (Historical Agri Center)", "mr": "तेर", "lat": 18.3120, "lon": 76.1450},
                    {"en": "Doki", "mr": "ढोकी (साखर कारखाना परिसर)", "lat": 18.3240, "lon": 76.0820}
                ]
            },
            "Tuljapur": {
                "en": "Tuljapur", "mr": "तुळजापूर", "lat": 18.0117, "lon": 76.0717,
                "villages": [
                    {"en": "Tuljapur Rural", "mr": "तुळजापूर ग्रामीण", "lat": 18.0117, "lon": 76.0717},
                    {"en": "Naldurg", "mr": "नळदुर्ग", "lat": 17.8180, "lon": 76.2950}
                ]
            },
            "Omerga": {
                "en": "Omerga", "mr": "उमरगा", "lat": 17.8417, "lon": 76.6250,
                "villages": [
                    {"en": "Omerga Mandi", "mr": "उमरगा बाजार", "lat": 17.8417, "lon": 76.6250},
                    {"en": "Murum", "mr": "मुरुम", "lat": 17.8120, "lon": 76.5120}
                ]
            },
            "Kalamb": {
                "en": "Kalamb", "mr": "कळंब", "lat": 18.4417, "lon": 76.0417,
                "villages": [
                    {"en": "Kalamb Soybean Hub", "mr": "कळंब सोयाबीन केंद्र", "lat": 18.4417, "lon": 76.0417},
                    {"en": "Shiradhon", "mr": "शिराढोण", "lat": 18.4950, "lon": 76.0950}
                ]
            },
            "Bhoom": {
                "en": "Bhoom", "mr": "भूम", "lat": 18.4667, "lon": 75.6667,
                "villages": [
                    {"en": "Bhoom Town", "mr": "भूम शहर", "lat": 18.4667, "lon": 75.6667},
                    {"en": "Walwad", "mr": "वालवड", "lat": 18.5120, "lon": 75.7240}
                ]
            },
            "Paranda": {
                "en": "Paranda", "mr": "परांडा", "lat": 18.2583, "lon": 75.4500,
                "villages": [
                    {"en": "Paranda Mandi", "mr": "परांडा बाजार", "lat": 18.2583, "lon": 75.4500},
                    {"en": "Kandar", "mr": "कंदर", "lat": 18.2910, "lon": 75.5120}
                ]
            }
        }
    },
    "Palghar": {
        "en": "Palghar", "mr": "पालघर", "lat": 19.6967, "lon": 72.7697,
        "talukas": {
            "Palghar": {
                "en": "Palghar", "mr": "पालघर", "lat": 19.6967, "lon": 72.7697,
                "villages": [
                    {"en": "Palghar Agri APMC", "mr": "पालघर कृषी बाजार", "lat": 19.6967, "lon": 72.7697},
                    {"en": "Boisar", "mr": "बोईसर", "lat": 19.8010, "lon": 72.7540},
                    {"en": "Saphale", "mr": "सफाळे", "lat": 19.5750, "lon": 72.8210}
                ]
            },
            "Dahanu": {
                "en": "Dahanu", "mr": "डहाणू", "lat": 19.9728, "lon": 72.7328,
                "villages": [
                    {"en": "Gholvad (GI Chikoo / Sapota Hub)", "mr": "घोलवड (जी.आय. मानांकित चिकू केंद्र)", "lat": 20.0350, "lon": 72.7480},
                    {"en": "Bordi", "mr": "बोर्डी", "lat": 20.1020, "lon": 72.7310},
                    {"en": "Dahanu Beach Belt", "mr": "डहाणू बागायत पट्टा", "lat": 19.9728, "lon": 72.7328}
                ]
            },
            "Wada": {
                "en": "Wada", "mr": "वाडा", "lat": 19.6547, "lon": 73.1364,
                "villages": [
                    {"en": "Wada Kolam Rice Belt", "mr": "वाडा कोलम भात पट्टा", "lat": 19.6547, "lon": 73.1364},
                    {"en": "Kudus", "mr": "कुडूस", "lat": 19.6120, "lon": 73.0840}
                ]
            },
            "Jawhar": {
                "en": "Jawhar", "mr": "जव्हार", "lat": 19.9242, "lon": 73.2325,
                "villages": [
                    {"en": "Jawhar Hill Agriculture", "mr": "जव्हार डोंगरी शेती", "lat": 19.9242, "lon": 73.2325},
                    {"en": "Khadkhad", "mr": "खडखड", "lat": 19.9710, "lon": 73.2840}
                ]
            },
            "Mokhada": {
                "en": "Mokhada", "mr": "मोखाडा", "lat": 19.9333, "lon": 73.3333,
                "villages": [
                    {"en": "Mokhada Rural", "mr": "मोखाडा ग्रामीण", "lat": 19.9333, "lon": 73.3333},
                    {"en": "Khodala", "mr": "खोडाळा", "lat": 19.8650, "lon": 73.4120}
                ]
            },
            "Talasari": {
                "en": "Talasari", "mr": "तलासरी", "lat": 20.1258, "lon": 72.9250,
                "villages": [
                    {"en": "Talasari Town", "mr": "तलासरी शहर", "lat": 20.1258, "lon": 72.9250},
                    {"en": "Zari", "mr": "झरी", "lat": 20.1850, "lon": 72.9640}
                ]
            }
        }
    },
    "Parbhani": {
        "en": "Parbhani", "mr": "परभणी", "lat": 19.2611, "lon": 76.7761,
        "talukas": {
            "Parbhani": {
                "en": "Parbhani", "mr": "परभणी", "lat": 19.2611, "lon": 76.7761,
                "villages": [
                    {"en": "VNMKV University Campus (State Agri Research)", "mr": "वasantराव नाईक मराठवाडा कृषी विद्यापीठ परिसर", "lat": 19.2667, "lon": 76.7850},
                    {"en": "Parbhani APMC", "mr": "परभणी कृषी बाजार", "lat": 19.2611, "lon": 76.7761},
                    {"en": "Pedgaon", "mr": "पेडगाव", "lat": 19.2150, "lon": 76.8450}
                ]
            },
            "Gangakhed": {
                "en": "Gangakhed", "mr": "गंगाखेड", "lat": 18.9667, "lon": 76.7500,
                "villages": [
                    {"en": "Gangakhed Godavari Basin", "mr": "गंगाखेड गोदावरी काठ", "lat": 18.9667, "lon": 76.7500},
                    {"en": "Ranisawargaon", "mr": "राणीसावरगाव", "lat": 18.9120, "lon": 76.8120}
                ]
            },
            "Jintur": {
                "en": "Jintur", "mr": "जिंतूर", "lat": 19.6167, "lon": 76.6833,
                "villages": [
                    {"en": "Jintur Town", "mr": "जिंतूर शहर", "lat": 19.6167, "lon": 76.6833},
                    {"en": "Bori", "mr": "बोरी", "lat": 19.5420, "lon": 76.7450}
                ]
            },
            "Sailu": {
                "en": "Sailu", "mr": "सेलू", "lat": 19.4583, "lon": 76.4500,
                "villages": [
                    {"en": "Sailu Cotton Market", "mr": "सेलू कापूस बाजार", "lat": 19.4583, "lon": 76.4500},
                    {"en": "Walur", "mr": "वालूर", "lat": 19.5120, "lon": 76.5120}
                ]
            },
            "Pathri": {
                "en": "Pathri", "mr": "पाथरी", "lat": 19.2500, "lon": 76.4500,
                "villages": [
                    {"en": "Pathri Rural", "mr": "पाथरी ग्रामीण", "lat": 19.2500, "lon": 76.4500},
                    {"en": "Hadgaon", "mr": "हदगाव", "lat": 19.2950, "lon": 76.5020}
                ]
            },
            "Purna": {
                "en": "Purna", "mr": "पूर्णा", "lat": 19.1833, "lon": 77.0500,
                "villages": [
                    {"en": "Purna Sugar Belt", "mr": "पूर्णा साखर पट्टा", "lat": 19.1833, "lon": 77.0500},
                    {"en": "Tadkalas", "mr": "ताडकळस", "lat": 19.1250, "lon": 77.1120}
                ]
            }
        }
    },
    "Pune": {
        "en": "Pune", "mr": "पुणे", "lat": 18.5204, "lon": 73.8567,
        "talukas": {
            "Haveli": {
                "en": "Haveli", "mr": "हवेली", "lat": 18.5204, "lon": 73.8567,
                "villages": [
                    {"en": "Gultekdi Pune APMC", "mr": "गुलटेकडी पुणे मुख्य बाजार", "lat": 18.4980, "lon": 73.8650},
                    {"en": "Hadapsar Vegetable Market", "mr": "हडपसर भाजीपाला बाजार", "lat": 18.5089, "lon": 73.9258},
                    {"en": "Manjari VSI (Vasantdada Sugar Institute)", "mr": "मांजरी (वसंतदादा शुगर इन्स्टिट्यूट)", "lat": 18.5250, "lon": 73.9820},
                    {"en": "Uruli Kanchan (BAIF Agri-Cattle Center)", "mr": "उरुळी कांचन (बायफ संशोधन केंद्र)", "lat": 18.4890, "lon": 74.1350}
                ]
            },
            "Baramati": {
                "en": "Baramati", "mr": "बारामती", "lat": 18.1517, "lon": 74.5777,
                "villages": [
                    {"en": "Baramati KVK (Krishi Vigyan Kendra)", "mr": "बारामती कृषी विज्ञान केंद्र परिसर", "lat": 18.1620, "lon": 74.5890},
                    {"en": "Baramati APMC", "mr": "बारामती कृषी बाजार", "lat": 18.1517, "lon": 74.5777},
                    {"en": "Malegaon Khurd (Sugar Factory)", "mr": "मालेगाव खुर्द", "lat": 18.1850, "lon": 74.5120},
                    {"en": "Songaon", "mr": "सोमेश्वर / सोनगाव", "lat": 18.1120, "lon": 74.4560}
                ]
            },
            "Shirur": {
                "en": "Shirur", "mr": "शिरूर", "lat": 18.8258, "lon": 74.3789,
                "villages": [
                    {"en": "Shirur Mandi", "mr": "शिरूर कृषी बाजार", "lat": 18.8258, "lon": 74.3789},
                    {"en": "Shikrapur", "mr": "शिक्रापूर", "lat": 18.7350, "lon": 74.1250},
                    {"en": "Ranjangaon Ganpati", "mr": "रांजणगाव गणपती", "lat": 18.7560, "lon": 74.2420}
                ]
            },
            "Junnar": {
                "en": "Junnar", "mr": "जुन्नर", "lat": 19.2083, "lon": 73.8750,
                "villages": [
                    {"en": "Narayangaon (Tomato APMC Capital)", "mr": "नारायणगाव (टोमॅटो महाबाजार)", "lat": 19.1214, "lon": 73.9786},
                    {"en": "Alephata (Agri Trading Hub)", "mr": "आळेफाटा कृषी व्यापारी केंद्र", "lat": 19.1850, "lon": 74.1120},
                    {"en": "Otur", "mr": "ओतूर", "lat": 19.2620, "lon": 73.9850}
                ]
            },
            "Ambegaon": {
                "en": "Ambegaon", "mr": "आंबेगाव", "lat": 19.0333, "lon": 73.8500,
                "villages": [
                    {"en": "Manchar APMC", "mr": "मंचर कृषी बाजार", "lat": 19.0083, "lon": 73.9417},
                    {"en": "Ghodegaon", "mr": "घोडेगाव", "lat": 19.0540, "lon": 73.8320}
                ]
            },
            "Khed": {
                "en": "Khed (Rajgurunagar)", "mr": "खेड (राजगुरुनगर)", "lat": 18.8550, "lon": 73.9050,
                "villages": [
                    {"en": "Rajgurunagar APMC (Potato/Onion)", "mr": "राजगुरुनगर बटाटा व कांदा बाजार", "lat": 18.8550, "lon": 73.9050},
                    {"en": "Chakan APMC", "mr": "चाकण कृषी उत्पन्न बाजार", "lat": 18.7583, "lon": 73.8569},
                    {"en": "Alandi", "mr": "आळंदी", "lat": 18.6750, "lon": 73.8980}
                ]
            },
            "Indapur": {
                "en": "Indapur", "mr": "इंदापूर", "lat": 18.1167, "lon": 75.0333,
                "villages": [
                    {"en": "Indapur Town & Sugar Belt", "mr": "इंदापूर शहर व साखर पट्टा", "lat": 18.1167, "lon": 75.0333},
                    {"en": "Bawada", "mr": "बावडा", "lat": 18.0450, "lon": 75.0120},
                    {"en": "Nimbgaon Ketki", "mr": "निंबगाव केतकी", "lat": 18.1820, "lon": 74.9540}
                ]
            },
            "Daund": {
                "en": "Daund", "mr": "दौंड", "lat": 18.4633, "lon": 74.5822,
                "villages": [
                    {"en": "Daund Sugarcane Belt", "mr": "दौंड ऊस पट्टा", "lat": 18.4633, "lon": 74.5822},
                    {"en": "Kedgaon", "mr": "केडगाव", "lat": 18.4720, "lon": 74.3820},
                    {"en": "Patas", "mr": "पाटस", "lat": 18.4410, "lon": 74.4520}
                ]
            },
            "Purandar": {
                "en": "Purandar (Saswad)", "mr": "पुरंदर (सासवड)", "lat": 18.3444, "lon": 74.0306,
                "villages": [
                    {"en": "Saswad (GI Fig / Anjeer Hub)", "mr": "सासवड (जी.आय. मानांकित अंजीर केंद्र)", "lat": 18.3444, "lon": 74.0306},
                    {"en": "Jejuri", "mr": "जेजुरी", "lat": 18.2833, "lon": 74.1667},
                    {"en": "Rajewadi", "mr": "राजेवाडी", "lat": 18.3820, "lon": 74.1520}
                ]
            },
            "Bhor": {
                "en": "Bhor", "mr": "भोर", "lat": 18.1478, "lon": 73.8447,
                "villages": [
                    {"en": "Bhor Rice Belt", "mr": "भोर भात पट्टा", "lat": 18.1478, "lon": 73.8447},
                    {"en": "Nasrapur", "mr": "नसरापूर", "lat": 18.2540, "lon": 73.8950}
                ]
            },
            "Maval": {
                "en": "Maval", "mr": "मावळ", "lat": 18.7500, "lon": 73.5833,
                "villages": [
                    {"en": "Talegaon Dabhade (Floriculture Hub)", "mr": "तळेगाव दाभाडे (फुलशेती केंद्र)", "lat": 18.7300, "lon": 73.6800},
                    {"en": "Vadgaon Maval", "mr": "वडगाव मावळ", "lat": 18.7500, "lon": 73.5833},
                    {"en": "Kamshet", "mr": "कामशेत", "lat": 18.7610, "lon": 73.5540}
                ]
            }
        }
    },
    "Raigad": {
        "en": "Raigad", "mr": "रायगड", "lat": 18.5158, "lon": 73.1812,
        "talukas": {
            "Alibag": {
                "en": "Alibag", "mr": "अलिबाग", "lat": 18.6414, "lon": 72.8722,
                "villages": [
                    {"en": "Alibag White Onion GI Belt", "mr": "अलिबाग पांढरा कांदा जी.आय. पट्टा", "lat": 18.6414, "lon": 72.8722},
                    {"en": "Chaul", "mr": "चौल", "lat": 18.5620, "lon": 72.9320},
                    {"en": "Mandwa", "mr": "मांडवा", "lat": 18.7850, "lon": 72.8640}
                ]
            },
            "Pen": {
                "en": "Pen", "mr": "पेण", "lat": 18.7358, "lon": 73.0936,
                "villages": [
                    {"en": "Pen Rice Belt", "mr": "पेण भात पट्टा", "lat": 18.7358, "lon": 73.0936},
                    {"en": "Wavandhal", "mr": "वावंढळ", "lat": 18.7820, "lon": 73.1420}
                ]
            },
            "Panvel": {
                "en": "Panvel", "mr": "पनवेल", "lat": 18.9894, "lon": 73.1175,
                "villages": [
                    {"en": "Panvel APMC", "mr": "पनवेल कृषी बाजार", "lat": 18.9894, "lon": 73.1175},
                    {"en": "Kalamboli", "mr": "कळंबोली", "lat": 19.0310, "lon": 73.0980}
                ]
            },
            "Mahad": {
                "en": "Mahad", "mr": "महाड", "lat": 18.0833, "lon": 73.4167,
                "villages": [
                    {"en": "Mahad Rural", "mr": "महाड ग्रामीण", "lat": 18.0833, "lon": 73.4167},
                    {"en": "Birwadi", "mr": "बिरवाडी", "lat": 18.1250, "lon": 73.4540}
                ]
            },
            "Roha": {
                "en": "Roha", "mr": "रोहा", "lat": 18.4333, "lon": 73.1167,
                "villages": [
                    {"en": "Roha Town", "mr": "रोहा शहर", "lat": 18.4333, "lon": 73.1167},
                    {"en": "Kolad", "mr": "कोलाड", "lat": 18.4120, "lon": 73.2010}
                ]
            },
            "Mangaon": {
                "en": "Mangaon", "mr": "माणगाव", "lat": 18.2500, "lon": 73.2833,
                "villages": [
                    {"en": "Mangaon Mandi", "mr": "माणगाव बाजार", "lat": 18.2500, "lon": 73.2833},
                    {"en": "Indapur Raigad", "mr": "इंदापूर रायगड", "lat": 18.3120, "lon": 73.3420}
                ]
            }
        }
    },
    "Ratnagiri": {
        "en": "Ratnagiri", "mr": "रत्नागिरी", "lat": 16.9902, "lon": 73.3120,
        "talukas": {
            "Ratnagiri": {
                "en": "Ratnagiri", "mr": "रत्नागिरी", "lat": 16.9902, "lon": 73.3120,
                "villages": [
                    {"en": "Alphonso (Hapus) Mango Export Hub", "mr": "हापूस आंबा निर्यात केंद्र", "lat": 16.9902, "lon": 73.3120},
                    {"en": "Mirya", "mr": "मिऱ्या", "lat": 17.0250, "lon": 73.2840},
                    {"en": "Pawas (Cashew / Coconut)", "mr": "पावस (काजू व नारळ बागा)", "lat": 16.8920, "lon": 73.3150}
                ]
            },
            "Dapoli": {
                "en": "Dapoli", "mr": "दापोली", "lat": 17.7558, "lon": 73.1856,
                "villages": [
                    {"en": "Dr. BSKKV Konkan Agriculture University", "mr": "डॉ. बाळासाहेब सावंत कोकण कृषी विद्यापीठ", "lat": 17.7650, "lon": 73.1920},
                    {"en": "Harnai Fish & Fruit Port", "mr": "हर्णे बंदर", "lat": 17.8120, "lon": 73.0950},
                    {"en": "Anjarle", "mr": "आंजर्ले", "lat": 17.8450, "lon": 73.1120}
                ]
            },
            "Guhagar": {
                "en": "Guhagar", "mr": "गुहागर", "lat": 17.4833, "lon": 73.2000,
                "villages": [
                    {"en": "Guhagar Betel Nut & Coconut Belt", "mr": "गुहागर सुपारी व नारळ पट्टा", "lat": 17.4833, "lon": 73.2000},
                    {"en": "Hedvi", "mr": "हेडवी", "lat": 17.3910, "lon": 73.2420}
                ]
            },
            "Chiplun": {
                "en": "Chiplun", "mr": "चिपळूण", "lat": 17.5325, "lon": 73.5186,
                "villages": [
                    {"en": "Chiplun APMC", "mr": "चिपळूण कृषी उत्पन्न बाजार", "lat": 17.5325, "lon": 73.5186},
                    {"en": "Kherdi", "mr": "खेर्डी", "lat": 17.5540, "lon": 73.5520}
                ]
            },
            "Khed": {
                "en": "Khed Ratnagiri", "mr": "खेड रत्नागिरी", "lat": 17.7167, "lon": 73.3833,
                "villages": [
                    {"en": "Khed Mandi", "mr": "खेड बाजार", "lat": 17.7167, "lon": 73.3833},
                    {"en": "Lote Parshuram", "mr": "लोटे परशुराम", "lat": 17.6540, "lon": 73.4410}
                ]
            },
            "Sangameshwar": {
                "en": "Sangameshwar", "mr": "संगमेश्वर", "lat": 17.1833, "lon": 73.5500,
                "villages": [
                    {"en": "Devrukh", "mr": "देवरुख", "lat": 17.0620, "lon": 73.6210},
                    {"en": "Makhjan", "mr": "माखजन", "lat": 17.2250, "lon": 73.4850}
                ]
            },
            "Rajapur": {
                "en": "Rajapur", "mr": "राजापूर", "lat": 16.6583, "lon": 73.5167,
                "villages": [
                    {"en": "Rajapur Mango & Spice Belt", "mr": "राजापूर हापूस व मसाल्याची शेती", "lat": 16.6583, "lon": 73.5167},
                    {"en": "Nate", "mr": "नाटे", "lat": 16.6120, "lon": 73.3950}
                ]
            }
        }
    },
    "Sangli": {
        "en": "Sangli", "mr": "सांगली", "lat": 16.8524, "lon": 74.5815,
        "talukas": {
            "Miraj": {
                "en": "Miraj", "mr": "मिरज", "lat": 16.8272, "lon": 74.6433,
                "villages": [
                    {"en": "Sangli Turmeric & Jaggery APMC", "mr": "सांगली हळद व गूळ महाबाजार", "lat": 16.8524, "lon": 74.5815},
                    {"en": "Miraj Rural", "mr": "मिरज ग्रामीण", "lat": 16.8272, "lon": 74.6433},
                    {"en": "Kupwad", "mr": "कुपवाड", "lat": 16.8650, "lon": 74.6120}
                ]
            },
            "Tasgaon": {
                "en": "Tasgaon", "mr": "तासगाव", "lat": 17.0347, "lon": 74.6017,
                "villages": [
                    {"en": "Tasgaon (National Raisin & Bedana APMC)", "mr": "तासगाव (राष्ट्रीय बेदाणा महाबाजार)", "lat": 17.0347, "lon": 74.6017},
                    {"en": "Savalaj", "mr": "सावळज", "lat": 17.0850, "lon": 74.7120},
                    {"en": "Manerajuri", "mr": "मनेराजुरी", "lat": 16.9820, "lon": 74.6540}
                ]
            },
            "Walwa": {
                "en": "Walwa (Islampur)", "mr": "वाळवा (इस्लामपूर)", "lat": 17.0500, "lon": 74.2667,
                "villages": [
                    {"en": "Islampur Sugarcane Hub", "mr": "इस्लामपूर ऊस केंद्र", "lat": 17.0500, "lon": 74.2667},
                    {"en": "Ashta", "mr": "आष्टा", "lat": 16.9500, "lon": 74.4167},
                    {"en": "Kasegaon", "mr": "कासेगाव", "lat": 17.1120, "lon": 74.2150}
                ]
            },
            "Palus": {
                "en": "Palus", "mr": "पलूस", "lat": 17.1000, "lon": 74.4500,
                "villages": [
                    {"en": "Palus Grape & Sugar Belt", "mr": "पलूस द्राक्ष व ऊस पट्टा", "lat": 17.1000, "lon": 74.4500},
                    {"en": "Kundal", "mr": "कुंडल", "lat": 17.1620, "lon": 74.4120}
                ]
            },
            "Khanapur": {
                "en": "Khanapur (Vita)", "mr": "खानापूर (विटा)", "lat": 17.2667, "lon": 74.5333,
                "villages": [
                    {"en": "Vita Pomegranate & Maize Mandi", "mr": "विटा डाळिंब व मका बाजार", "lat": 17.2667, "lon": 74.5333},
                    {"en": "Bhalwani", "mr": "भालवणी", "lat": 17.3120, "lon": 74.5820}
                ]
            },
            "Jat": {
                "en": "Jat", "mr": "जत", "lat": 17.0458, "lon": 75.3283,
                "villages": [
                    {"en": "Jat Pomegranate Capital", "mr": "जत डाळिंब केंद्र", "lat": 17.0458, "lon": 75.3283},
                    {"en": "Madgyal", "mr": "माडग्याळ (माडग्याळ मेंढी केंद्र)", "lat": 17.1120, "lon": 75.4120},
                    {"en": "Sankh", "mr": "संख", "lat": 16.9820, "lon": 75.4850}
                ]
            },
            "Kavathe Mahankal": {
                "en": "Kavathe Mahankal", "mr": "कवठे महांकाळ", "lat": 16.9833, "lon": 74.8667,
                "villages": [
                    {"en": "Kavathe Mahankal Grape Belt", "mr": "कवठे महांकाळ द्राक्ष पट्टा", "lat": 16.9833, "lon": 74.8667},
                    {"en": "Dhalgaon", "mr": "ढालगाव", "lat": 17.0410, "lon": 74.9540}
                ]
            },
            "Shirala": {
                "en": "Shirala", "mr": "शिराळा", "lat": 16.9833, "lon": 74.1333,
                "villages": [
                    {"en": "Shirala Western Ghats Agri", "mr": "शिराळा घाटमाथा शेती", "lat": 16.9833, "lon": 74.1333},
                    {"en": "Kokrud", "mr": "कोकरुड", "lat": 17.0540, "lon": 74.0620}
                ]
            }
        }
    },
    "Satara": {
        "en": "Satara", "mr": "सातारा", "lat": 17.6805, "lon": 74.0183,
        "talukas": {
            "Satara": {
                "en": "Satara", "mr": "सातारा", "lat": 17.6805, "lon": 74.0183,
                "villages": [
                    {"en": "Satara APMC", "mr": "सातारा कृषी उत्पन्न बाजार", "lat": 17.6805, "lon": 74.0183},
                    {"en": "Shendre", "mr": "शेंद्रे", "lat": 17.6410, "lon": 74.0520},
                    {"en": "Medha Road", "mr": "मेढा रोड परिसर", "lat": 17.7210, "lon": 73.9850}
                ]
            },
            "Karad": {
                "en": "Karad", "mr": "कराड", "lat": 17.2897, "lon": 74.1814,
                "villages": [
                    {"en": "Karad Krishna-Koyna Basin (Sugar/Turmeric)", "mr": "कराड कृष्णा-कोयना प्रीतीसंगम (ऊस व हळद)", "lat": 17.2897, "lon": 74.1814},
                    {"en": "Ogalewadi", "mr": "ओगलेवाडी", "lat": 17.3120, "lon": 74.2150},
                    {"en": "Kole", "mr": "कोळे", "lat": 17.2450, "lon": 74.1420}
                ]
            },
            "Mahabaleshwar": {
                "en": "Mahabaleshwar", "mr": "महाबळेश्वर", "lat": 17.9237, "lon": 73.6586,
                "villages": [
                    {"en": "Mahabaleshwar Strawberry Capital", "mr": "महाबळेश्वर स्ट्रॉबेरी केंद्र", "lat": 17.9237, "lon": 73.6586},
                    {"en": "Panchgani (Strawberry Cluster)", "mr": "पाचगणी स्ट्रॉबेरी क्लस्टर", "lat": 17.9242, "lon": 73.8008},
                    {"en": "Bhilawadi / Bhilar (Pustakanche Gaav & Strawberry)", "mr": "भिलार (पुस्तकांचे गाव व स्ट्रॉबेरी)", "lat": 17.9120, "lon": 73.7650}
                ]
            },
            "Wai": {
                "en": "Wai", "mr": "वाई", "lat": 17.9483, "lon": 73.8917,
                "villages": [
                    {"en": "Wai Turmeric & Ginger Belt", "mr": "वाई हळद व आले पट्टा", "lat": 17.9483, "lon": 73.8917},
                    {"en": "Bhuinj", "mr": "भुईंज", "lat": 18.0120, "lon": 73.9820}
                ]
            },
            "Phaltan": {
                "en": "Phaltan", "mr": "फलटण", "lat": 17.9833, "lon": 74.4333,
                "villages": [
                    {"en": "Phaltan Nimbkar Agricultural Research (NARI)", "mr": "फलटण निंबकर कृषी संशोधन केंद्र", "lat": 17.9833, "lon": 74.4333},
                    {"en": "Taradgaon", "mr": "तरडगाव", "lat": 18.0410, "lon": 74.3210},
                    {"en": "Barad", "mr": "बरड", "lat": 17.9210, "lon": 74.5240}
                ]
            },
            "Khatav": {
                "en": "Khatav (Vaduj)", "mr": "खटाव (वडूज)", "lat": 17.6000, "lon": 74.4333,
                "villages": [
                    {"en": "Vaduj Pomegranate Hub", "mr": "वडूज डाळिंब केंद्र", "lat": 17.6000, "lon": 74.4333},
                    {"en": "Mayani Bird Sanctuary Area", "mr": "मायणी परिसर", "lat": 17.4350, "lon": 74.5420}
                ]
            },
            "Koregaon": {
                "en": "Koregaon", "mr": "कोरेगाव", "lat": 17.7000, "lon": 74.1833,
                "villages": [
                    {"en": "Koregaon Ginger Mandi", "mr": "कोरेगाव आले बाजार", "lat": 17.7000, "lon": 74.1833},
                    {"en": "Rahimatpur", "mr": "रहिमतपूर", "lat": 17.6020, "lon": 74.2050}
                ]
            },
            "Patan": {
                "en": "Patan", "mr": "पाटण", "lat": 17.3667, "lon": 73.9000,
                "villages": [
                    {"en": "Koyna Catchment Area", "mr": "कोयना धरण पाणलोट परिसर", "lat": 17.4010, "lon": 73.7540},
                    {"en": "Dhebewadi", "mr": "ढेबेवाडी", "lat": 17.2910, "lon": 73.9540}
                ]
            }
        }
    },
    "Sindhudurg": {
        "en": "Sindhudurg", "mr": "सिंधुदुर्ग", "lat": 16.1242, "lon": 73.7125,
        "talukas": {
            "Kudal": {
                "en": "Kudal", "mr": "कुडाळ", "lat": 16.0167, "lon": 73.6833,
                "villages": [
                    {"en": "Kudal APMC & Cashew Processing Hub", "mr": "कुडाळ काजू प्रक्रिया व कृषी केंद्र", "lat": 16.0167, "lon": 73.6833},
                    {"en": "Pinguli", "mr": "पिंगुळी", "lat": 15.9850, "lon": 73.6950}
                ]
            },
            "Sawantwadi": {
                "en": "Sawantwadi", "mr": "सावंतवाडी", "lat": 15.9000, "lon": 73.8167,
                "villages": [
                    {"en": "Sawantwadi Horticulture Center", "mr": "सावंतवाडी फलोत्पादन केंद्र", "lat": 15.9000, "lon": 73.8167},
                    {"en": "Banda Border Mandi", "mr": "बांदा बाजारपेठ", "lat": 15.8120, "lon": 73.8640},
                    {"en": "Amboli Hill Belt", "mr": "आंबोली घाट परिसर", "lat": 15.9610, "lon": 73.9980}
                ]
            },
            "Malvan": {
                "en": "Malvan", "mr": "मालवण", "lat": 16.0667, "lon": 73.4667,
                "villages": [
                    {"en": "Malvan Coastal Agriculture & Coconut", "mr": "मालवण नारळ व बागायत शेती", "lat": 16.0667, "lon": 73.4667},
                    {"en": "Achara", "mr": "आचरा", "lat": 16.1950, "lon": 73.4420}
                ]
            },
            "Vengurla": {
                "en": "Vengurla", "mr": "वेंगुर्ला", "lat": 15.8667, "lon": 73.6333,
                "villages": [
                    {"en": "ICAR Cashew & Mango Research Station", "mr": "काजू व आंबा संशोधन केंद्र वेंगुर्ला", "lat": 15.8667, "lon": 73.6333},
                    {"en": "Shiroda", "mr": "शिरोडा", "lat": 15.7810, "lon": 73.6820}
                ]
            },
            "Kankavli": {
                "en": "Kankavli", "mr": "कणकवली", "lat": 16.2667, "lon": 73.7167,
                "villages": [
                    {"en": "Kankavli Central APMC", "mr": "कणकवली मुख्य बाजार", "lat": 16.2667, "lon": 73.7167},
                    {"en": "Phondaghat", "mr": "फोंडाघाट", "lat": 16.3810, "lon": 73.8240}
                ]
            },
            "Devgad": {
                "en": "Devgad", "mr": "देवगड", "lat": 16.3833, "lon": 73.3833,
                "villages": [
                    {"en": "Devgad Alphonso Mango Hub (GI Certified)", "mr": "देवगड हापूस आंबा मुख्य पट्टा (जी.आय.)", "lat": 16.3833, "lon": 73.3833},
                    {"en": "Jamsande", "mr": "जामसंडे", "lat": 16.3620, "lon": 73.3950},
                    {"en": "Shirgaon", "mr": "शिरगाव", "lat": 16.4410, "lon": 73.4520}
                ]
            }
        }
    },
    "Solapur": {
        "en": "Solapur", "mr": "सोलापूर", "lat": 17.6599, "lon": 75.9064,
        "talukas": {
            "Solapur North": {
                "en": "Solapur North", "mr": "उत्तर सोलापूर", "lat": 17.6599, "lon": 75.9064,
                "villages": [
                    {"en": "Solapur APMC (Jowar/Pomegranate)", "mr": "सोलापूर कृषी उत्पन्न बाजार (ज्वारी/डाळिंब)", "lat": 17.6599, "lon": 75.9064},
                    {"en": "Kegaon (ICAR National Pomegranate Research NRCG)", "mr": "केगाव (राष्ट्रीय डाळिंब संशोधन केंद्र परिसर)", "lat": 17.7120, "lon": 75.8520},
                    {"en": "Shelgi", "mr": "शेळगी", "lat": 17.6950, "lon": 75.9320}
                ]
            },
            "Pandharpur": {
                "en": "Pandharpur", "mr": "पंढरपूर", "lat": 17.6778, "lon": 75.3283,
                "villages": [
                    {"en": "Pandharpur Sugarcane & Pomegranate Belt", "mr": "पंढरपूर ऊस व डाळिंब पट्टा", "lat": 17.6778, "lon": 75.3283},
                    {"en": "Kasegaon", "mr": "कासेगाव", "lat": 17.7240, "lon": 75.3850},
                    {"en": "Bhalwani", "mr": "भालवणी", "lat": 17.6210, "lon": 75.2540}
                ]
            },
            "Barshi": {
                "en": "Barshi", "mr": "बार्शी", "lat": 18.2333, "lon": 75.6833,
                "villages": [
                    {"en": "Barshi Tur & Pulse APMC", "mr": "बार्शी तूर व डाळ महाबाजार", "lat": 18.2333, "lon": 75.6833},
                    {"en": "Vairag", "mr": "वैराग", "lat": 18.0620, "lon": 75.8120},
                    {"en": "Pangri", "mr": "पांगरी", "lat": 18.3120, "lon": 75.6120}
                ]
            },
            "Malshiras": {
                "en": "Malshiras", "mr": "माळशिरस", "lat": 17.8333, "lon": 74.9667,
                "villages": [
                    {"en": "Akluj (Asia's Largest Sugar Factory Hub)", "mr": "अकलूज (साखर कारखाना व बागायत केंद्र)", "lat": 17.8833, "lon": 75.0167},
                    {"en": "Natepute", "mr": "नातेपुते", "lat": 17.9120, "lon": 74.7840}
                ]
            },
            "Sangola": {
                "en": "Sangola", "mr": "सांगोला", "lat": 17.4333, "lon": 75.2000,
                "villages": [
                    {"en": "Sangola Pomegranate Capital (Bhagwa)", "mr": "सांगोला भगवा डाळिंब राजधानी", "lat": 17.4333, "lon": 75.2000},
                    {"en": "Javla", "mr": "जवळा", "lat": 17.4850, "lon": 75.2840},
                    {"en": "Mahud", "mr": "महुद", "lat": 17.4910, "lon": 75.1120}
                ]
            },
            "Karmala": {
                "en": "Karmala", "mr": "करमाळा", "lat": 18.4167, "lon": 75.2000,
                "villages": [
                    {"en": "Karmala Ujani Catchment Belt", "mr": "करमाळा उजनी पाणलोट क्षेत्र", "lat": 18.4167, "lon": 75.2000},
                    {"en": "Jeur", "mr": "जेऊर", "lat": 18.2950, "lon": 75.2840}
                ]
            },
            "Mangalwedha": {
                "en": "Mangalwedha", "mr": "मंगळवेढा", "lat": 17.5167, "lon": 75.4500,
                "villages": [
                    {"en": "Mangalwedha Maldandi Jowar (GI Hub)", "mr": "मंगळवेढा मालदांडी शाळू ज्वारी केंद्र", "lat": 17.5167, "lon": 75.4500},
                    {"en": "Borale", "mr": "बोराळे", "lat": 17.4620, "lon": 75.5210}
                ]
            },
            "Akkalkot": {
                "en": "Akkalkot", "mr": "अक्कलकोट", "lat": 17.5258, "lon": 76.2044,
                "villages": [
                    {"en": "Akkalkot Mandi", "mr": "अक्कलकोट बाजार", "lat": 17.5258, "lon": 76.2044},
                    {"en": "Maindargi", "mr": "मैंदर्गी", "lat": 17.4710, "lon": 76.3120}
                ]
            },
            "Madha": {
                "en": "Madha", "mr": "माढा", "lat": 18.0333, "lon": 75.5167,
                "villages": [
                    {"en": "Kurduvadi Junction Mandi", "mr": "कुर्डूवाडी कृषी बाजार", "lat": 18.0833, "lon": 75.4333},
                    {"en": "Madha Rural", "mr": "माढा ग्रामीण", "lat": 18.0333, "lon": 75.5167}
                ]
            },
            "Mohol": {
                "en": "Mohol", "mr": "मोहोळ", "lat": 17.8167, "lon": 75.6500,
                "villages": [
                    {"en": "Mohol Jowar Research Station", "mr": "मोहोळ ज्वारी संशोधन केंद्र परिसर", "lat": 17.8167, "lon": 75.6500},
                    {"en": "Penur", "mr": "पेनूर", "lat": 17.7540, "lon": 75.5840}
                ]
            }
        }
    },
    "Thane": {
        "en": "Thane", "mr": "ठाणे", "lat": 19.2183, "lon": 72.9781,
        "talukas": {
            "Thane": {
                "en": "Thane", "mr": "ठाणे", "lat": 19.2183, "lon": 72.9781,
                "villages": [
                    {"en": "Thane APMC", "mr": "ठाणे बाजार", "lat": 19.2183, "lon": 72.9781},
                    {"en": "Kalyan APMC", "mr": "कल्याण कृषी उत्पन्न बाजार", "lat": 19.2437, "lon": 73.1355}
                ]
            },
            "Shahapur": {
                "en": "Shahapur", "mr": "शहापूर", "lat": 19.4500, "lon": 73.3333,
                "villages": [
                    {"en": "Bhatsa Dam Catchment Agri", "mr": "भातसा धरण पाणलोट परिसर", "lat": 19.4950, "lon": 73.3850},
                    {"en": "Asangaon", "mr": "आसनगाव", "lat": 19.4310, "lon": 73.3020}
                ]
            },
            "Murbad": {
                "en": "Murbad", "mr": "मुरबाड", "lat": 19.2500, "lon": 73.4000,
                "villages": [
                    {"en": "Murbad Rice Belt", "mr": "मुरबाड भात पट्टा", "lat": 19.2500, "lon": 73.4000},
                    {"en": "Saralgaon", "mr": "सरळगाव", "lat": 19.3120, "lon": 73.4820}
                ]
            },
            "Bhiwandi": {
                "en": "Bhiwandi", "mr": "भिवंडी", "lat": 19.3000, "lon": 73.0667,
                "villages": [
                    {"en": "Bhiwandi Warehousing & Rice Hub", "mr": "भिवंडी धान्य वखार केंद्र", "lat": 19.3000, "lon": 73.0667},
                    {"en": "Padgha", "mr": "पडघा", "lat": 19.3820, "lon": 73.1640}
                ]
            }
        }
    },
    "Wardha": {
        "en": "Wardha", "mr": "वर्धा", "lat": 20.7453, "lon": 78.6022,
        "talukas": {
            "Wardha": {
                "en": "Wardha", "mr": "वर्धा", "lat": 20.7453, "lon": 78.6022,
                "villages": [
                    {"en": "Sevagram (Ashram Organic Agriculture)", "mr": "सेवाग्राम सेंद्रिय शेती परिसर", "lat": 20.7180, "lon": 78.6540},
                    {"en": "Wardha APMC (Cotton/Soybean)", "mr": "वर्धा कृषी उत्पन्न बाजार", "lat": 20.7453, "lon": 78.6022},
                    {"en": "Sindi", "mr": "शिंदी", "lat": 20.8120, "lon": 78.8540}
                ]
            },
            "Deoli": {
                "en": "Deoli", "mr": "देवळी", "lat": 20.6558, "lon": 78.4833,
                "villages": [
                    {"en": "Deoli Cotton Hub", "mr": "देवळी कापूस केंद्र", "lat": 20.6558, "lon": 78.4833},
                    {"en": "Pulgaon", "mr": "पुलगाव", "lat": 20.7250, "lon": 78.3240}
                ]
            },
            "Hinganghat": {
                "en": "Hinganghat", "mr": "हिंगणघाट", "lat": 20.5500, "lon": 78.8333,
                "villages": [
                    {"en": "Hinganghat National Cotton Market", "mr": "हिंगणघाट राष्ट्रीय कापूस महाबाजार", "lat": 20.5500, "lon": 78.8333},
                    {"en": "Wadner", "mr": "वडनेर", "lat": 20.4850, "lon": 78.9120}
                ]
            },
            "Arvi": {
                "en": "Arvi", "mr": "आर्वी", "lat": 20.9833, "lon": 78.2333,
                "villages": [
                    {"en": "Arvi Cotton & Soybean Mandi", "mr": "आर्वी कापूस व सोयाबीन बाजार", "lat": 20.9833, "lon": 78.2333},
                    {"en": "Rohana", "mr": "रोहणा", "lat": 20.9120, "lon": 78.3120}
                ]
            },
            "Seloo": {
                "en": "Seloo", "mr": "सेलू", "lat": 20.8333, "lon": 78.7000,
                "villages": [
                    {"en": "Seloo Rural", "mr": "सेलू ग्रामीण", "lat": 20.8333, "lon": 78.7000},
                    {"en": "Bor Dam Catchment", "mr": "बोर धरण पाणलोट परिसर", "lat": 20.9420, "lon": 78.6850}
                ]
            }
        }
    },
    "Washim": {
        "en": "Washim", "mr": "वाशीम", "lat": 20.1117, "lon": 77.1358,
        "talukas": {
            "Washim": {
                "en": "Washim", "mr": "वाशीम", "lat": 20.1117, "lon": 77.1358,
                "villages": [
                    {"en": "Washim Soybean Capital APMC", "mr": "वाशीम सोयाबीन मुख्य कृषी बाजार", "lat": 20.1117, "lon": 77.1358},
                    {"en": "Kata", "mr": "काटा", "lat": 20.1850, "lon": 77.2120},
                    {"en": "Shelu Bazar", "mr": "शेलू बाजार", "lat": 20.2540, "lon": 77.1420}
                ]
            },
            "Risod": {
                "en": "Risod", "mr": "रिसोड", "lat": 19.9667, "lon": 76.7833,
                "villages": [
                    {"en": "Risod Soybean Hub", "mr": "रिसोड सोयाबीन केंद्र", "lat": 19.9667, "lon": 76.7833},
                    {"en": "Shirpur Jain", "mr": "शिरपूर जैन", "lat": 20.0850, "lon": 76.9250}
                ]
            },
            "Malegaon": {
                "en": "Malegaon Washim", "mr": "मालेगाव वाशीम", "lat": 20.2833, "lon": 76.9667,
                "villages": [
                    {"en": "Malegaon Mandi", "mr": "मालेगाव बाजार", "lat": 20.2833, "lon": 76.9667},
                    {"en": "Shirna", "mr": "शिर्णा", "lat": 20.3210, "lon": 76.9120}
                ]
            },
            "Karanja": {
                "en": "Karanja (Lad)", "mr": "कारंजा (लाड)", "lat": 20.4833, "lon": 77.4833,
                "villages": [
                    {"en": "Karanja Lad Pulse & Oilseed APMC", "mr": "कारंजा लाड डाळ व तेलबिया बाजार", "lat": 20.4833, "lon": 77.4833},
                    {"en": "Kamtha", "mr": "कामठा", "lat": 20.5240, "lon": 77.4120}
                ]
            },
            "Mangrulpir": {
                "en": "Mangrulpir", "mr": "मंगरुळपीर", "lat": 20.3167, "lon": 77.3500,
                "villages": [
                    {"en": "Mangrulpir Town", "mr": "मंगरुळपीर शहर", "lat": 20.3167, "lon": 77.3500},
                    {"en": "Amla", "mr": "आम्ला", "lat": 20.3850, "lon": 77.2950}
                ]
            },
            "Manora": {
                "en": "Manora", "mr": "मनोरा", "lat": 20.2167, "lon": 77.5500,
                "villages": [
                    {"en": "Manora Rural", "mr": "मनोरा ग्रामीण", "lat": 20.2167, "lon": 77.5500},
                    {"en": "Poharadevi", "mr": "पोहरादेवी तीर्थक्षेत्र व शेती परिसर", "lat": 20.1620, "lon": 77.4950}
                ]
            }
        }
    },
    "Yavatmal": {
        "en": "Yavatmal", "mr": "यवतमाळ", "lat": 20.3888, "lon": 78.1204,
        "talukas": {
            "Yavatmal": {
                "en": "Yavatmal", "mr": "यवतमाळ", "lat": 20.3888, "lon": 78.1204,
                "villages": [
                    {"en": "Yavatmal White Gold Cotton APMC", "mr": "यवतमाळ पांढरे सोने कापूस बाजार", "lat": 20.3888, "lon": 78.1204},
                    {"en": "Lohara", "mr": "लोहारा", "lat": 20.4120, "lon": 78.1850},
                    {"en": "Ghatanji Road", "mr": "घाटंजी रोड परिसर", "lat": 20.3250, "lon": 78.1420}
                ]
            },
            "Pusad": {
                "en": "Pusad", "mr": "पुसद", "lat": 19.9111, "lon": 77.5750,
                "villages": [
                    {"en": "Pusad Agriculture College & Mandi", "mr": "पुसद कृषी महाविद्यालय व बाजार", "lat": 19.9111, "lon": 77.5750},
                    {"en": "Kharbi", "mr": "खारबी", "lat": 19.9650, "lon": 77.6320}
                ]
            },
            "Umarkhed": {
                "en": "Umarkhed", "mr": "उमरखेड", "lat": 19.6000, "lon": 77.7000,
                "villages": [
                    {"en": "Umarkhed Cotton & Turmeric Belt", "mr": "उमरखेड कापूस व हळद पट्टा", "lat": 19.6000, "lon": 77.7000},
                    {"en": "Danki", "mr": "डाणकी", "lat": 19.6540, "lon": 77.7850}
                ]
            },
            "Wani": {
                "en": "Wani", "mr": "वणी", "lat": 20.0667, "lon": 78.9500,
                "villages": [
                    {"en": "Wani Cotton Ginning Hub", "mr": "वणी जिनिंग व कृषी केंद्र", "lat": 20.0667, "lon": 78.9500},
                    {"en": "Maregaon Road", "mr": "मारेगाव रोड परिसर", "lat": 20.0210, "lon": 78.8950}
                ]
            },
            "Digras": {
                "en": "Digras", "mr": "दिग्रस", "lat": 20.1000, "lon": 77.7167,
                "villages": [
                    {"en": "Digras APMC", "mr": "दिग्रस कृषी बाजार", "lat": 20.1000, "lon": 77.7167},
                    {"en": "Kalamb Road Fata", "mr": "कळंब रोड फाटा", "lat": 20.1450, "lon": 77.7850}
                ]
            },
            "Darwha": {
                "en": "Darwha", "mr": "दारव्हा", "lat": 20.3167, "lon": 77.7667,
                "villages": [
                    {"en": "Darwha Cotton Belt", "mr": "दारव्हा कापूस पट्टा", "lat": 20.3167, "lon": 77.7667},
                    {"en": "Lohhi", "mr": "लोही", "lat": 20.2710, "lon": 77.8420}
                ]
            },
            "Ralegaon": {
                "en": "Ralegaon", "mr": "राळेगाव", "lat": 20.4167, "lon": 78.5167,
                "villages": [
                    {"en": "Ralegaon Rural", "mr": "राळेगाव ग्रामीण", "lat": 20.4167, "lon": 78.5167},
                    {"en": "Zari Jamni", "mr": "झरी जामणी", "lat": 19.9450, "lon": 78.7120}
                ]
            }
        }
    }
}

if __name__ == "__main__":
    target_path = Path("C:/Users/91935/Desktop/KrishiVaani/static/maharashtra_locations.json")
    try:
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(MAHARASHTRA_LOCATIONS, f, ensure_ascii=False, indent=2)
        print(f"Generated {len(MAHARASHTRA_LOCATIONS)} districts successfully into {target_path}")
    except Exception as e:
        print("Note on saving json file:", e)

