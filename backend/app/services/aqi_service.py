from datetime import datetime, timezone
from typing import Optional
import httpx

from app.config import settings
from app.schemas import HourlyPoint, PollutantMetrics, WeatherMetrics

# Well-known fallback coordinates when offline geocoding is unavailable
KNOWN_CITIES: dict[str, tuple[str, float, float]] = {
    "bengaluru": ("Bengaluru, India", 12.9716, 77.5946),
    "bangalore": ("Bengaluru, India", 12.9716, 77.5946),
    "delhi": ("New Delhi, India", 28.6139, 77.2090),
    "new delhi": ("New Delhi, India", 28.6139, 77.2090),
    "mumbai": ("Mumbai, India", 19.0760, 72.8777),
    "mysuru": ("Mysuru, India", 12.2958, 76.6394),
    "mysore": ("Mysuru, India", 12.2958, 76.6394),
    "hyderabad": ("Hyderabad, India", 17.3850, 78.4867),
    "chennai": ("Chennai, India", 13.0827, 80.2707),
    "kolkata": ("Kolkata, India", 22.5726, 88.3639),
    "pune": ("Pune, India", 18.5204, 73.8567),
    "london": ("London, UK", 51.5072, -0.1276),
    "new york": ("New York, USA", 40.7128, -74.0060),
    "san francisco": ("San Francisco, USA", 37.7749, -122.4194),
    "tokyo": ("Tokyo, Japan", 35.6762, 139.6503),
}

WEATHER_CODE_LABELS: dict[int, dict[str, str]] = {
    0: {"en": "Clear sky", "kn": "ಸ್ಪಷ್ಟ ಆಕಾಶ", "hi": "साफ़ आसमान"},
    1: {"en": "Mainly clear", "kn": "ಮುಖ್ಯವಾಗಿ ಸ್ಪಷ್ಟ", "hi": "मुख्यतः साफ़"},
    2: {"en": "Partly cloudy", "kn": "ಭಾಗಶಃ ಮೋಡ", "hi": "आंशिक बादल"},
    3: {"en": "Overcast", "kn": "ಮೋಡ ಕವಿದ ವಾತಾವರಣ", "hi": "घने बादल"},
    45: {"en": "Foggy", "kn": "ಮಂಜು", "hi": "कोहरा"},
    48: {"en": "Depositing rime fog", "kn": "ದಟ್ಟ ಮಂಜು", "hi": "घना कोहरा"},
    51: {"en": "Light drizzle", "kn": "ಸಣ್ಣ ತುಂತುರು ಮಳೆ", "hi": "हल्की बूंदाबांदी"},
    53: {"en": "Moderate drizzle", "kn": "ಮಧ್ಯಮ ತುಂತುರು ಮಳೆ", "hi": "मध्यम बूंदाबांदी"},
    61: {"en": "Slight rain", "kn": "ಸ್ವಲ್ಪ ಮಳೆ", "hi": "हल्की बारिश"},
    63: {"en": "Moderate rain", "kn": "ಮಧ್ಯಮ ಮಳೆ", "hi": "मध्यम बारिश"},
    65: {"en": "Heavy rain", "kn": "ಭಾರೀ ಮಳೆ", "hi": "तेज़ बारिश"},
    80: {"en": "Rain showers", "kn": "ಮಳೆ ಹನಿಗಳು", "hi": "बारिश की बौछारें"},
    95: {"en": "Thunderstorm", "kn": "ಗುಡುಗು ಸಹಿತ ಮಳೆ", "hi": "गरज के साथ तूफ़ान"},
}

DEMO_NOTICES: dict[str, str] = {
    "en": "Live air quality API is currently unreachable. Displaying clearly labeled demonstration readings so you can test all features safely.",
    "kn": "ಲೈವ್ ವಾಯು ಗುಣಮಟ್ಟ API ಪ್ರಸ್ತುತ ಲಭ್ಯವಿಲ್ಲ. ಎಲ್ಲಾ ವೈಶಿಷ್ಟ್ಯಗಳನ್ನು ಪರೀಕ್ಷಿಸಲು ಪ್ರದರ್ಶನ (ಡೆಮೊ) ಡೇಟಾವನ್ನು ತೋರಿಸಲಾಗುತ್ತಿದೆ.",
    "hi": "लाइव वायु गुणवत्ता API अभी उपलब्ध नहीं है। सभी सुविधाओं का परीक्षण करने के लिए स्पष्ट रूप से चिह्नित डेमो डेटा दिखाया जा रहा है।",
}


def _weather_label(code: Optional[int], lang: str) -> str:
    if code is None:
        return {"en": "Partly cloudy", "kn": "ಭಾಗಶಃ ಮೋಡ", "hi": "आंशिक बादल"}.get(lang, "Partly cloudy")
    if code in WEATHER_CODE_LABELS:
        return WEATHER_CODE_LABELS[code].get(lang, WEATHER_CODE_LABELS[code]["en"])
    if code >= 80:
        return {"en": "Showers / Stormy", "kn": "ಮಳೆ / ಬಿರುಗಾಳಿ", "hi": "बौछार / तूफ़ान"}.get(lang, "Showers")
    if code >= 50:
        return {"en": "Rainy", "kn": "ಮಳೆ", "hi": "बारिश"}.get(lang, "Rainy")
    return {"en": "Cloudy", "kn": "ಮೋಡ", "hi": "बादल"}.get(lang, "Cloudy")


async def _resolve_location(
    city: Optional[str],
    lat: Optional[float],
    lon: Optional[float],
) -> tuple[str, float, float]:
    if lat is not None and lon is not None:
        label = city.strip() if city and city.strip() else f"{lat:.2f}, {lon:.2f}"
        return label, lat, lon

    target_city = (city or settings.DEFAULT_CITY).strip()
    city_key = target_city.lower()

    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": target_city, "count": 1, "language": "en", "format": "json"},
            )
            if resp.status_code == 200:
                payload = resp.json()
                results = payload.get("results") or []
                if results:
                    top = results[0]
                    name = top.get("name", target_city)
                    country = top.get("country", "")
                    display = f"{name}, {country}" if country else name
                    return display, float(top["latitude"]), float(top["longitude"])
    except Exception:
        pass

    if city_key in KNOWN_CITIES:
        return KNOWN_CITIES[city_key]

    return target_city, settings.DEFAULT_LAT, settings.DEFAULT_LON


def _build_demo_payload(
    location: str,
    lat: float,
    lon: float,
    lang: str,
) -> dict:
    # Deterministic demonstration profile (never claimed as live)
    city_lower = location.lower()
    if "delhi" in city_lower:
        aqi, pm25, pm10, co, no2, so2, o3 = 186, 108.4, 174.2, 1180.0, 62.5, 19.4, 54.0
        temp, hum, wind = 24.0, 58.0, 7.5
    elif "mumbai" in city_lower:
        aqi, pm25, pm10, co, no2, so2, o3 = 112, 41.2, 82.6, 740.0, 38.0, 14.2, 49.0
        temp, hum, wind = 29.5, 72.0, 14.2
    else:
        aqi, pm25, pm10, co, no2, so2, o3 = 88, 29.4, 58.1, 510.0, 27.6, 9.8, 44.5
        temp, hum, wind = 25.2, 61.0, 11.4

    hourly: list[HourlyPoint] = []
    offsets = [-14, -10, -8, -4, 0, 6, 12, 16, 10, 4, -3, -8]
    hours = ["06:00", "08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00", "22:00", "00:00", "02:00", "04:00"]
    for idx, hr in enumerate(hours):
        delta = offsets[idx]
        h_aqi = max(25, aqi + delta)
        h_pm25 = round(max(6.0, pm25 + delta * 0.45), 1)
        h_pm10 = round(max(12.0, pm10 + delta * 0.75), 1)
        h_o3 = round(max(15.0, o3 + (8 if 12 <= idx * 2 <= 18 else -4)), 1)
        hourly.append(HourlyPoint(time=hr, aqi=h_aqi, pm25=h_pm25, pm10=h_pm10, o3=h_o3))

    return {
        "location": location,
        "latitude": lat,
        "longitude": lon,
        "is_live": False,
        "data_source": "Demonstration Dataset (Not Live)",
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "notice": DEMO_NOTICES.get(lang, DEMO_NOTICES["en"]),
        "pollutants": PollutantMetrics(
            aqi=aqi,
            pm25=pm25,
            pm10=pm10,
            co=co,
            no2=no2,
            so2=so2,
            o3=o3,
        ),
        "weather": WeatherMetrics(
            temperature_c=temp,
            humidity_pct=hum,
            wind_speed_kmh=wind,
            condition=_weather_label(2, lang),
            apparent_temp_c=round(temp + 0.8, 1),
        ),
        "hourly_trend": hourly,
    }


async def _fetch_open_meteo(
    location: str,
    lat: float,
    lon: float,
    lang: str,
) -> dict:
    async with httpx.AsyncClient(timeout=10.0) as client:
        aq_resp = await client.get(
            "https://air-quality-api.open-meteo.com/v1/air-quality",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "us_aqi,pm2_5,pm10,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone",
                "hourly": "us_aqi,pm2_5,pm10,ozone",
                "forecast_days": 1,
                "timezone": "auto",
            },
        )
        wx_resp = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,weather_code",
                "timezone": "auto",
            },
        )
        aq_resp.raise_for_status()
        wx_resp.raise_for_status()
        aq_data = aq_resp.json()
        wx_data = wx_resp.json()

    cur_aq = aq_data.get("current") or {}
    cur_wx = wx_data.get("current") or {}

    if "us_aqi" not in cur_aq or cur_aq.get("us_aqi") is None:
        raise ValueError("Missing live AQI field from Open-Meteo response")

    pollutants = PollutantMetrics(
        aqi=int(round(float(cur_aq.get("us_aqi", 0)))),
        pm25=round(float(cur_aq.get("pm2_5") or 0.0), 1),
        pm10=round(float(cur_aq.get("pm10") or 0.0), 1),
        co=round(float(cur_aq.get("carbon_monoxide") or 0.0), 1),
        no2=round(float(cur_aq.get("nitrogen_dioxide") or 0.0), 1),
        so2=round(float(cur_aq.get("sulphur_dioxide") or 0.0), 1),
        o3=round(float(cur_aq.get("ozone") or 0.0), 1),
    )

    weather = WeatherMetrics(
        temperature_c=round(float(cur_wx.get("temperature_2m") or 0.0), 1),
        humidity_pct=round(float(cur_wx.get("relative_humidity_2m") or 0.0), 1),
        wind_speed_kmh=round(float(cur_wx.get("wind_speed_10m") or 0.0), 1),
        condition=_weather_label(cur_wx.get("weather_code"), lang),
        apparent_temp_c=round(float(cur_wx.get("apparent_temperature") or cur_wx.get("temperature_2m") or 0.0), 1),
    )

    hourly_raw = aq_data.get("hourly") or {}
    times = hourly_raw.get("time") or []
    h_aqi = hourly_raw.get("us_aqi") or []
    h_pm25 = hourly_raw.get("pm2_5") or []
    h_pm10 = hourly_raw.get("pm10") or []
    h_o3 = hourly_raw.get("ozone") or []

    hourly_points: list[HourlyPoint] = []
    # Sample every 2 hours for a clean 12-point daily chart
    for idx in range(0, min(len(times), 24), 2):
        t_str = str(times[idx])
        short_time = t_str.split("T")[1][:5] if "T" in t_str else t_str[-5:]
        hourly_points.append(
            HourlyPoint(
                time=short_time,
                aqi=int(round(float(h_aqi[idx] or pollutants.aqi))) if idx < len(h_aqi) else pollutants.aqi,
                pm25=round(float(h_pm25[idx] or pollutants.pm25), 1) if idx < len(h_pm25) else pollutants.pm25,
                pm10=round(float(h_pm10[idx] or pollutants.pm10), 1) if idx < len(h_pm10) else pollutants.pm10,
                o3=round(float(h_o3[idx] or pollutants.o3), 1) if idx < len(h_o3) else pollutants.o3,
            )
        )

    last_updated = cur_aq.get("time") or datetime.now(timezone.utc).isoformat()

    return {
        "location": location,
        "latitude": lat,
        "longitude": lon,
        "is_live": True,
        "data_source": "Open-Meteo Air Quality & Weather API (Live)",
        "last_updated": str(last_updated),
        "notice": None,
        "pollutants": pollutants,
        "weather": weather,
        "hourly_trend": hourly_points,
    }


async def fetch_air_quality_and_weather(
    city: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    lang: str = "en",
) -> dict:
    """Fetch live air quality & weather data, or return clearly labeled demonstration data on failure."""
    resolved_name, resolved_lat, resolved_lon = await _resolve_location(city, lat, lon)
    try:
        return await _fetch_open_meteo(resolved_name, resolved_lat, resolved_lon, lang)
    except Exception:
        return _build_demo_payload(resolved_name, resolved_lat, resolved_lon, lang)
