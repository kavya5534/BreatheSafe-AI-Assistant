from app.models import UserPreferencesRecord
from app.schemas import DailyUpdateItem, PollutantMetrics, PrecautionItem, SeverityInfo


SEVERITY_TABLE = [
    (
        50,
        "good",
        "#10b981",
        {
            "en": "Good",
            "kn": "ಉತ್ತಮ",
            "hi": "अच्छा",
        },
        {
            "en": "Air quality is clean and poses minimal risk for outdoor activities.",
            "kn": "ಗಾಳಿಯ ಗುಣಮಟ್ಟ ಶುದ್ಧವಾಗಿದೆ ಮತ್ತು ಹೊರಾಂಗಣ ಚಟುವಟಿಕೆಗಳಿಗೆ ಸುರಕ್ಷಿತವಾಗಿದೆ.",
            "hi": "वायु गुणवत्ता साफ़ है और बाहरी गतिविधियों के लिए सुरक्षित है।",
        },
    ),
    (
        100,
        "moderate",
        "#38bdf8",
        {
            "en": "Moderate",
            "kn": "ಮಧ್ಯಮ",
            "hi": "मध्यम",
        },
        {
            "en": "Air quality is acceptable; unusually sensitive individuals should monitor symptoms during heavy exertion.",
            "kn": "ಗಾಳಿಯ ಗುಣಮಟ್ಟ ಸ್ವೀಕಾರಾರ್ಹವಾಗಿದೆ; ಸೂಕ್ಷ್ಮ ಆರೋಗ್ಯದವರು ಹೆಚ್ಚು ಶ್ರಮದ ಕೆಲಸದಲ್ಲಿ ಎಚ್ಚರಿಕೆ ವಹಿಸಬೇಕು.",
            "hi": "वायु गुणवत्ता स्वीकार्य है; संवेदनशील लोगों को भारी व्यायाम के दौरान सावधानी रखनी चाहिए।",
        },
    ),
    (
        150,
        "sensitive",
        "#f59e0b",
        {
            "en": "Unhealthy for Sensitive Groups",
            "kn": "ಸೂಕ್ಷ್ಮ ಗುಂಪುಗಳಿಗೆ ಅನಾರೋಗ್ಯಕರ",
            "hi": "संवेदनशील समूहों के लिए अस्वस्थ",
        },
        {
            "en": "Children, older adults, and people with respiratory sensitivity should limit prolonged outdoor exertion.",
            "kn": "ಮಕ್ಕಳು, ಹಿರಿಯರು ಮತ್ತು ಉಸಿರಾಟದ ಸೂಕ್ಷ್ಮತೆ ಇರುವವರು ದೀರ್ಘಕಾಲದ ಹೊರಾಂಗಣ ಶ್ರಮವನ್ನು ಕಡಿಮೆ ಮಾಡಬೇಕು.",
            "hi": "बच्चों, बुजुर्गों और सांस की संवेदनशीलता वाले लोगों को लंबे समय तक बाहर मेहनत से बचना चाहिए।",
        },
    ),
    (
        200,
        "unhealthy",
        "#f97316",
        {
            "en": "Unhealthy",
            "kn": "ಅನಾರೋಗ್ಯಕರ",
            "hi": "अस्वस्थ",
        },
        {
            "en": "Everyone may begin to experience health effects; shift workouts indoors and wear a well-fitted N95 mask outdoors.",
            "kn": "ಎಲ್ಲರಿಗೂ ಆರೋಗ್ಯ ಪರಿಣಾಮಗಳು ಉಂಟಾಗಬಹುದು; ವ್ಯಾಯಾಮವನ್ನು ಒಳಾಂಗಣಕ್ಕೆ ಬದಲಾಯಿಸಿ ಮತ್ತು ಹೊರಗೆ N95 ಮಾಸ್ಕ್ ಧರಿಸಿ.",
            "hi": "सभी पर स्वास्थ्य प्रभाव पड़ सकता है; व्यायाम घर के अंदर करें और बाहर N95 मास्क पहनें।",
        },
    ),
    (
        300,
        "very_unhealthy",
        "#ef4444",
        {
            "en": "Very Unhealthy",
            "kn": "ಅತ್ಯಂತ ಅನಾರೋಗ್ಯಕರ",
            "hi": "बहुत अस्वस्थ",
        },
        {
            "en": "Health alert: minimize all outdoor exposure, keep windows sealed, and run HEPA filtration indoors.",
            "kn": "ಆರೋಗ್ಯ ಎಚ್ಚರಿಕೆ: ಎಲ್ಲಾ ಹೊರಾಂಗಣ ಚಟುವಟಿಕೆಗಳನ್ನು ಕಡಿಮೆ ಮಾಡಿ, ಕಿಟಕಿಗಳನ್ನು ಮುಚ್ಚಿ ಮತ್ತು ಒಳಾಂಗಣ ಗಾಳಿ ಶುದ್ಧೀಕರಣ ಬಳಸಿ.",
            "hi": "स्वास्थ्य चेतावनी: बाहर निकलना न्यूनतम करें, खिड़कियाँ बंद रखें और घर के अंदर HEPA फ़िल्टर चलाएं।",
        },
    ),
    (
        9999,
        "hazardous",
        "#9333ea",
        {
            "en": "Hazardous",
            "kn": "ಅಪಾಯಕಾರಿ",
            "hi": "खतरनाक",
        },
        {
            "en": "Emergency conditions: stay indoors with purified air and seek medical help immediately if breathing distress occurs.",
            "kn": "ತುರ್ತು ಪರಿಸ್ಥಿತಿ: ಶುದ್ಧೀಕರಿಸಿದ ಗಾಳಿಯೊಂದಿಗೆ ಒಳಾಂಗಣದಲ್ಲಿಯೇ ಇರಿ ಮತ್ತು ಉಸಿರಾಟದ ತೊಂದರೆ ಕಂಡರೆ ತಕ್ಷಣ ವೈದ್ಯಕೀಯ ಸಹಾಯ ಪಡೆಯಿರಿ.",
            "hi": "आपातकालीन स्थिति: शुद्ध हवा के साथ घर के अंदर रहें और सांस लेने में कठिनाई होने पर तुरंत चिकित्सा सहायता लें।",
        },
    ),
]


def classify_severity(aqi: int, lang: str) -> SeverityInfo:
    for threshold, level, color_hex, labels, summaries in SEVERITY_TABLE:
        if aqi <= threshold:
            return SeverityInfo(
                level=level,
                label=labels.get(lang, labels["en"]),
                color_hex=color_hex,
                summary=summaries.get(lang, summaries["en"]),
            )
    last = SEVERITY_TABLE[-1]
    return SeverityInfo(
        level=last[1],
        label=last[3].get(lang, last[3]["en"]),
        color_hex=last[2],
        summary=last[4].get(lang, last[4]["en"]),
    )


def build_precautions(
    pollutants: PollutantMetrics,
    prefs: UserPreferencesRecord,
    lang: str,
) -> list[PrecautionItem]:
    items: list[PrecautionItem] = []
    aqi = pollutants.aqi
    family = set(prefs.family_categories or ["general"])

    if aqi > 100:
        items.append(
            PrecautionItem(
                title={
                    "en": "Use a Well-Fitted N95/FFP2 Mask Outdoors",
                    "kn": "ಹೊರಾಂಗಣದಲ್ಲಿ ಸರಿಯಾಗಿ ಹೊಂದಿಕೊಳ್ಳುವ N95/FFP2 ಮಾಸ್ಕ್ ಧರಿಸಿ",
                    "hi": "बाहर जाते समय फिटेड N95/FFP2 मास्क पहनें",
                }[lang],
                detail={
                    "en": f"With AQI at {aqi} and PM2.5 at {pollutants.pm25} µg/m³, wear a sealed N95 mask during commutes.",
                    "kn": f"AQI {aqi} ಮತ್ತು PM2.5 {pollutants.pm25} µg/m³ ಇರುವುದರಿಂದ ಪ್ರಯಾಣದ ವೇಳೆ N95 ಮಾಸ್ಕ್ ಧರಿಸಿ.",
                    "hi": f"AQI {aqi} और PM2.5 {pollutants.pm25} µg/m³ होने के कारण यात्रा के दौरान N95 मास्क पहनें।",
                }[lang],
                reason={
                    "en": "Fine PM2.5 particles penetrate deep into lungs; cloth masks do not filter microscopic aerosols effectively.",
                    "kn": "ಸೂಕ್ಷ್ಮ PM2.5 ಕಣಗಳು ಶ್ವಾಸಕೋಶದ ಆಳಕ್ಕೆ ತಲುಪುತ್ತವೆ; ಬಟ್ಟೆ ಮಾಸ್ಕ್‌ಗಳು ಇವುಗಳನ್ನು ತಡೆಯುವುದಿಲ್ಲ.",
                    "hi": "सूक्ष्म PM2.5 कण फेफड़ों की गहराई तक पहुँचते हैं; कपड़े के मास्क इन्हें प्रभावी ढंग से नहीं रोक पाते।",
                }[lang],
                audience={
                    "en": "All commuters",
                    "kn": "ಎಲ್ಲಾ ಪ್ರಯಾಣಿಕರು",
                    "hi": "सभी यात्री",
                }[lang],
            )
        )
    else:
        items.append(
            PrecautionItem(
                title={
                    "en": "Ventilate Rooms During Cleaner Morning Hours",
                    "kn": "ಶುದ್ಧ ಬೆಳಗಿನ ಸಮಯದಲ್ಲಿ ಕೋಣೆಗಳಿಗೆ ಗಾಳಿ ಆಡುವಂತೆ ಮಾಡಿ",
                    "hi": "साफ़ सुबह के समय कमरों में वेंटिलेशन करें",
                }[lang],
                detail={
                    "en": f"Current AQI is {aqi}. Open cross-ventilation windows for 20–30 minutes away from main traffic roads.",
                    "kn": f"ಪ್ರಸ್ತುತ AQI {aqi} ಇದೆ. ಮುಖ್ಯ ರಸ್ತೆಯಿಂದ ದೂರವಿರುವ ಕಿಟಕಿಗಳನ್ನು 20–30 ನಿಮಿಷ ತೆರೆಯಿರಿ.",
                    "hi": f"वर्तमान AQI {aqi} है। मुख्य सड़क से दूर वाली खिड़कियाँ 20–30 मिनट के लिए खोलें।",
                }[lang],
                reason={
                    "en": "Controlled cross-ventilation flushes trapped indoor CO2 and VOCs when outdoor air is relatively clean.",
                    "kn": "ಹೊರಗಿನ ಗಾಳಿ ತುಲನಾತ್ಮಕವಾಗಿ ಶುದ್ಧವಾಗಿದ್ದಾಗ ಒಳಗಿನ CO2 ಮತ್ತು ಕಲ್ಮಶಗಳನ್ನು ಹೊರಹಾಕಲು ಇದು ಸಹಾಯಕ.",
                    "hi": "जब बाहर की हवा अपेक्षाकृत साफ़ हो, तो वेंटिलेशन से घर के अंदर की CO2 और VOC गैसें बाहर निकलती हैं।",
                }[lang],
                audience={
                    "en": "Home & Office",
                    "kn": "ಮನೆ ಮತ್ತು ಕಚೇರಿ",
                    "hi": "घर और कार्यालय",
                }[lang],
            )
        )

    if family.intersection({"children", "elderly", "pregnant", "respiratory_sensitive"}) or prefs.age_group in ("child", "senior"):
        items.append(
            PrecautionItem(
                title={
                    "en": "Protect Vulnerable Family Members",
                    "kn": "ಕುಟುಂಬದ ಸೂಕ್ಷ್ಮ ಸದಸ್ಯರನ್ನು ರಕ್ಷಿಸಿ",
                    "hi": "संवेदनशील परिवार के सदस्यों की सुरक्षा करें",
                }[lang],
                detail={
                    "en": "Keep children, seniors, and respiratory-sensitive members indoors during peak traffic (8–10 AM, 6–9 PM).",
                    "kn": "ಹೆಚ್ಚು ವಾಹನ ದಟ್ಟಣೆಯ ವೇಳೆಯಲ್ಲಿ (ಬೆಳಿಗ್ಗೆ 8–10, ಸಂಜೆ 6–9) ಮಕ್ಕಳು, ಹಿರಿಯರು ಮತ್ತು ಉಸಿರಾಟದ ಸೂಕ್ಷ್ಮತೆ ಇರುವವರು ಒಳಾಂಗಣದಲ್ಲಿ ಇರಿ.",
                    "hi": "पीक ट्रैफ़िक (सुबह 8–10, शाम 6–9) के दौरान बच्चों, बुजुर्गों और संवेदनशील सदस्यों को घर के अंदर रखें।",
                }[lang],
                reason={
                    "en": "Traffic corridors spike NO2 and ultrafine particles, which irritate developing or sensitive airways.",
                    "kn": "ವಾಹನ ದಟ್ಟಣೆ ವೇಳೆ NO2 ಮತ್ತು ಸೂಕ್ಷ್ಮ ಕಣಗಳು ಹೆಚ್ಚಾಗಿ ಸೂಕ್ಷ್ಮ ಶ್ವಾಸನಾಳಗಳಿಗೆ ಕಿರಿಕಿರಿ ಉಂಟುಮಾಡುತ್ತವೆ.",
                    "hi": "ट्रैफ़िक के समय NO2 और सूक्ष्म कण बढ़ जाते हैं, जो संवेदनशील श्वसन तंत्र को प्रभावित करते हैं।",
                }[lang],
                audience={
                    "en": "Children, Seniors & Sensitive",
                    "kn": "ಮಕ್ಕಳು, ಹಿರಿಯರು ಮತ್ತು ಸೂಕ್ಷ್ಮ ಗುಂಪು",
                    "hi": "बच्चे, बुजुर्ग व संवेदनशील",
                }[lang],
            )
        )

    items.append(
        PrecautionItem(
            title={
                "en": "Indoor Air Hygiene & Hydration",
                "kn": "ಒಳಾಂಗಣ ಗಾಳಿಯ ಸ್ವಚ್ಛತೆ ಮತ್ತು ನೀರಿನ ಸೇವನೆ",
                "hi": "घर के अंदर की हवा की स्वच्छता और हाइड्रेशन",
            }[lang],
            detail={
                "en": "Wet-mop floors instead of dry sweeping, avoid indoor incense/smoke, and stay well hydrated.",
                "kn": "ಒಣ ಕಸ ಗುಡಿಸುವ ಬದಲು ಒದ್ದೆ ಬಟ್ಟೆಯಿಂದ ನೆಲ ಒರೆಸಿ, ಒಳಗೆ ಧೂಪ/ಹೊಗೆ ತಪ್ಪಿಸಿ ಮತ್ತು ಸಾಕಷ್ಟು ನೀರು ಕುಡಿಯಿರಿ.",
                "hi": "सूखी झाड़ू के बजाय गीला पोंछा लगाएं, घर के अंदर धुआं/अगरबत्ती से बचें और पर्याप्त पानी पिएं।",
            }[lang],
            reason={
                "en": "Wet-mopping traps settled PM10 dust without resuspending it, and hydration keeps airway mucosa clear.",
                "kn": "ಒದ್ದೆ ಪೋಚಾ ಧೂಳನ್ನು ಮತ್ತೆ ಗಾಳಿಯಲ್ಲಿ ಹಾರದಂತೆ ತಡೆಯುತ್ತದೆ ಮತ್ತು ನೀರು ಶ್ವಾಸನಾಳವನ್ನು ತೇವವಾಗಿರಿಸುತ್ತದೆ.",
                "hi": "गीला पोंछा जमी हुई धूल (PM10) को हवा में वापस उड़ने से रोकता है और पानी श्वसन मार्ग को नम रखता है।",
            }[lang],
            audience={
                "en": "Every Household",
                "kn": "ಪ್ರತಿ ಮನೆ",
                "hi": "हर परिवार",
            }[lang],
        )
    )

    return items


def build_daily_updates(pollutants: PollutantMetrics, lang: str) -> list[DailyUpdateItem]:
    dominant = "PM2.5"
    if pollutants.pm10 > pollutants.pm25 * 2.2:
        dominant = "PM10"
    elif pollutants.o3 > 100:
        dominant = "O3"
    elif pollutants.no2 > 80:
        dominant = "NO2"

    return [
        DailyUpdateItem(
            title={
                "en": f"Primary Pollutant Watch: {dominant}",
                "kn": f"ಪ್ರಮುಖ ಮಾಲಿನ್ಯಕಾರಕ ಗಮನ: {dominant}",
                "hi": f"मुख्य प्रदूषक निगरानी: {dominant}",
            }[lang],
            detail={
                "en": f"{dominant} is currently driving local air stress (PM2.5: {pollutants.pm25} µg/m³, PM10: {pollutants.pm10} µg/m³).",
                "kn": f"ಪ್ರಸ್ತುತ ಸ್ಥಳೀಯ ಗಾಳಿಯ ಒತ್ತಡಕ್ಕೆ {dominant} ಪ್ರಮುಖ ಕಾರಣವಾಗಿದೆ (PM2.5: {pollutants.pm25}, PM10: {pollutants.pm10} µg/m³).",
                "hi": f"वर्तमान में स्थानीय वायु दबाव का मुख्य कारण {dominant} है (PM2.5: {pollutants.pm25}, PM10: {pollutants.pm10} µg/m³)।",
            }[lang],
            category="pollutant",
        ),
        DailyUpdateItem(
            title={
                "en": "Best Outdoor Window Today",
                "kn": "ಇಂದಿನ ಉತ್ತಮ ಹೊರಾಂಗಣ ಸಮಯ",
                "hi": "आज बाहर जाने का सबसे अच्छा समय",
            }[lang],
            detail={
                "en": "Midday to early afternoon (12:00–16:00) typically offers stronger atmospheric mixing and lower trapped particulate buildup.",
                "kn": "ಮಧ್ಯಾಹ್ನ (12:00–16:00) ವಾತಾವರಣದ ಗಾಳಿ ಚಲನೆ ಹೆಚ್ಚಾಗಿರುವುದರಿಂದ ಧೂಳು ಕಡಿಮೆ ಇರುತ್ತದೆ.",
                "hi": "दोपहर (12:00–16:00) के समय हवा का बहाव बेहतर रहता है, जिससे सतह पर प्रदूषक कम जमा होते हैं।",
            }[lang],
            category="timing",
        ),
        DailyUpdateItem(
            title={
                "en": "Medical Safety Note",
                "kn": "ವೈದ್ಯಕೀಯ ಸುರಕ್ಷತಾ ಸೂಚನೆ",
                "hi": "चिकित्सा सुरक्षा नोट",
            }[lang],
            detail={
                "en": "This dashboard gives general environmental guidance, not medical diagnosis. Consult a doctor for persistent cough, or seek emergency care for severe breathing difficulty.",
                "kn": "ಈ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್ ಸಾಮಾನ್ಯ ಪರಿಸರ ಮಾರ್ಗದರ್ಶನ ನೀಡುತ್ತದೆ, ವೈದ್ಯಕೀಯ ರೋಗನಿರ್ಣಯವಲ್ಲ. ನಿರಂತರ ಕೆಮ್ಮಿಗೆ ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ; ತೀವ್ರ ಉಸಿರಾಟದ ತೊಂದರೆಗೆ ತುರ್ತು ಸೇವೆ ಪಡೆಯಿರಿ.",
                "hi": "यह डैशबोर्ड सामान्य पर्यावरण मार्गदर्शन देता है, चिकित्सा निदान नहीं। लगातार खांसी पर डॉक्टर से मिलें और गंभीर सांस लेने में कठिनाई पर आपातकालीन सेवा लें।",
            }[lang],
            category="safety",
        ),
    ]


def build_personalized_routine(
    pollutants: PollutantMetrics,
    prefs: UserPreferencesRecord,
    lang: str,
) -> list[DailyUpdateItem]:
    is_high = pollutants.aqi > 120
    transport = prefs.transportation_type

    if transport in ("walking", "cycling", "two_wheeler"):
        commute_detail = {
            "en": (
                f"You commute via {transport.replace('_', ' ')}. Use side-streets away from diesel buses and wear a protective mask while AQI is {pollutants.aqi}."
                if is_high
                else f"You commute via {transport.replace('_', ' ')}. AQI ({pollutants.aqi}) is favorable—stick to tree-lined routes to minimize road exhaust."
            ),
            "kn": (
                f"ನೀವು {transport.replace('_', ' ')} ಬಳಸುತ್ತೀರಿ. AQI {pollutants.aqi} ಇರುವುದರಿಂದ ಕಡಿಮೆ ದಟ್ಟಣೆಯ ರಸ್ತೆಗಳನ್ನು ಆರಿಸಿ ಮತ್ತು ಮಾಸ್ಕ್ ಧರಿಸಿ."
                if is_high
                else f"ನೀವು {transport.replace('_', ' ')} ಬಳಸುತ್ತೀರಿ. AQI ({pollutants.aqi}) ಅನುಕೂಲಕರವಾಗಿದೆ—ಮರಗಳಿರುವ ರಸ್ತೆಗಳನ್ನು ಆಯ್ಕೆಮಾಡಿ."
            ),
            "hi": (
                f"आप {transport.replace('_', ' ')} से यात्रा करते हैं। AQI {pollutants.aqi} होने के कारण कम ट्रैफ़िक वाले रास्ते चुनें और मास्क पहनें।"
                if is_high
                else f"आप {transport.replace('_', ' ')} से यात्रा करते हैं। AQI ({pollutants.aqi}) अनुकूल है—पेड़ों वाले रास्तों का उपयोग करें।"
            ),
        }[lang]
    else:
        commute_detail = {
            "en": "Keep vehicle AC on recirculation mode in traffic jams to avoid drawing NO2 and PM2.5 into the cabin.",
            "kn": "ವಾಹನ ದಟ್ಟಣೆಯಲ್ಲಿ NO2 ಮತ್ತು PM2.5 ಒಳಗೆ ಬರದಂತೆ ವಾಹನದ AC ಯನ್ನು ರೀಸರ್ಕ್ಯುಲೇಷನ್ ಮೋಡ್‌ನಲ್ಲಿಡಿ.",
            "hi": "ट्रैफ़िक जाम में NO2 और PM2.5 को अंदर आने से रोकने के लिए वाहन का AC रीसर्कुलेशन मोड पर रखें।",
        }[lang]

    outdoor_note = {
        "en": (
            f"Tailored for {prefs.lifestyle} lifestyle ({prefs.age_group}): swap intense outdoor runs for indoor stretching or low-dust midday walks."
            if is_high
            else f"Tailored for {prefs.lifestyle} lifestyle ({prefs.age_group}): your preferred activities ({', '.join(prefs.outdoor_preferences or ['walk'])}) are safe with hydration breaks."
        ),
        "kn": (
            f"ನಿಮ್ಮ {prefs.lifestyle} ಜೀವನಶೈಲಿಗೆ ({prefs.age_group}) ಸಲಹೆ: ತೀವ್ರ ಹೊರಾಂಗಣ ಓಟದ ಬದಲು ಒಳಾಂಗಣ ವ್ಯಾಯಾಮ ಮಾಡಿ."
            if is_high
            else f"ನಿಮ್ಮ {prefs.lifestyle} ಜೀವನಶೈಲಿಗೆ ({prefs.age_group}) ಸಲಹೆ: ನಿಮ್ಮ ಆಯ್ದ ಹೊರಾಂಗಣ ಚಟುವಟಿಕೆಗಳು ಸುರಕ್ಷಿತವಾಗಿವೆ."
        ),
        "hi": (
            f"आपकी {prefs.lifestyle} जीवनशैली ({prefs.age_group}) के अनुसार: भारी बाहरी दौड़ के बजाय घर के अंदर स्ट्रेचिंग या हल्की गतिविधि करें।"
            if is_high
            else f"आपकी {prefs.lifestyle} जीवनशैली ({prefs.age_group}) के अनुसार: आपकी पसंदीदा बाहरी गतिविधियाँ पानी के ब्रेक के साथ सुरक्षित हैं।"
        ),
    }[lang]

    return [
        DailyUpdateItem(
            title={
                "en": "Smart Commute Plan",
                "kn": "ಸ್ಮಾರ್ಟ್ ಪ್ರಯಾಣ ಯೋಜನೆ",
                "hi": "स्मार्ट यात्रा योजना",
            }[lang],
            detail=commute_detail,
            category="commute",
        ),
        DailyUpdateItem(
            title={
                "en": "Activity & Routine Adjustment",
                "kn": "ದೈನಂದಿನ ಚಟುವಟಿಕೆ ಹೊಂದಾಣಿಕೆ",
                "hi": "दैनिक गतिविधि समायोजन",
            }[lang],
            detail=outdoor_note,
            category="activity",
        ),
    ]
