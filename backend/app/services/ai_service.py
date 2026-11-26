from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Optional
import httpx

from app.config import settings
from app.models import UserPreferencesRecord
from app.schemas import ChatResponse, SetupGuide


LANGUAGE_NAMES = {
    "en": "English",
    "kn": "Kannada (ಕನ್ನಡ)",
    "hi": "Hindi (हिन्दी)",
}


def is_ai_configured() -> bool:
    settings.refresh_ai_settings()
    return bool(settings.AI_API_KEY and settings.AI_API_KEY.strip())


def build_setup_guide(lang: str) -> SetupGuide:
    guides = {
        "en": SetupGuide(
            title="AI Provider Not Configured Yet",
            explanation=(
                "BreatheSafe AI uses a real LLM API on the backend and never fakes AI replies. "
                "Add your AI_API_KEY in the .env file to activate live multilingual AI guidance."
            ),
            steps=[
                "Copy BreatheSafe_AI/.env.example to BreatheSafe_AI/.env.",
                "Set AI_PROVIDER=openai_compatible (for OpenAI, Groq, OpenRouter, Together, or Ollama) or AI_PROVIDER=gemini.",
                "Set AI_API_KEY=your_real_api_key and AI_MODEL (e.g., gpt-4o-mini or gemini-2.5-flash).",
                "Restart the FastAPI backend server so the new environment variables load.",
            ],
            env_example=(
                "AI_PROVIDER=openai_compatible\n"
                "AI_BASE_URL=https://api.openai.com/v1\n"
                "AI_MODEL=gpt-4o-mini\n"
                "AI_API_KEY=sk-..."
            ),
        ),
        "kn": SetupGuide(
            title="AI ಪೂರೈಕೆದಾರರನ್ನು ಇನ್ನೂ ಕಾನ್ಫಿಗರ್ ಮಾಡಲಾಗಿಲ್ಲ",
            explanation=(
                "BreatheSafe AI ನಿಜವಾದ LLM API ಅನ್ನು ಬ್ಯಾಕ್‌ಎಂಡ್‌ನಲ್ಲಿ ಬಳಸುತ್ತದೆ ಮತ್ತು ನಕಲಿ AI ಉತ್ತರಗಳನ್ನು ನೀಡುವುದಿಲ್ಲ. "
                "ಲೈವ್ ಬಹುಭಾಷಾ AI ಮಾರ್ಗದರ್ಶನವನ್ನು ಸಕ್ರಿಯಗೊಳಿಸಲು .env ಫೈಲ್‌ನಲ್ಲಿ AI_API_KEY ಸೇರಿಸಿ."
            ),
            steps=[
                "BreatheSafe_AI/.env.example ಫೈಲ್ ಅನ್ನು BreatheSafe_AI/.env ಆಗಿ ನಕಲಿಸಿ.",
                "AI_PROVIDER=openai_compatible ಅಥವಾ AI_PROVIDER=gemini ಎಂದು ಹೊಂದಿಸಿ.",
                "AI_API_KEY=ನಿಮ್ಮ_ನಿಜವಾದ_ಕೀ ಮತ್ತು AI_MODEL (ಉದಾ: gpt-4o-mini) ಸೇರಿಸಿ.",
                "ಹೊಸ ಸೆಟ್ಟಿಂಗ್‌ಗಳು ಲೋಡ್ ಆಗಲು FastAPI ಬ್ಯಾಕ್‌ಎಂಡ್ ಅನ್ನು ಮರುಪ್ರಾರಂಭಿಸಿ.",
            ],
            env_example=(
                "AI_PROVIDER=openai_compatible\n"
                "AI_BASE_URL=https://api.openai.com/v1\n"
                "AI_MODEL=gpt-4o-mini\n"
                "AI_API_KEY=sk-..."
            ),
        ),
        "hi": SetupGuide(
            title="AI प्रदाता अभी कॉन्फ़िगर नहीं है",
            explanation=(
                "BreatheSafe AI बैकएंड पर वास्तविक LLM API का उपयोग करता है और कभी भी नकली उत्तर नहीं देता। "
                "लाइव बहुभाषी AI सहायता शुरू करने के लिए .env फ़ाइल में AI_API_KEY जोड़ें।"
            ),
            steps=[
                "BreatheSafe_AI/.env.example को BreatheSafe_AI/.env के रूप में कॉपी करें।",
                "AI_PROVIDER=openai_compatible या AI_PROVIDER=gemini सेट करें।",
                "AI_API_KEY=आपकी_असली_कुंजी और AI_MODEL (जैसे gpt-4o-mini) भरें।",
                "नई सेटिंग्स लोड करने के लिए FastAPI बैकएंड सर्वर को रीस्टार्ट करें।",
            ],
            env_example=(
                "AI_PROVIDER=openai_compatible\n"
                "AI_BASE_URL=https://api.openai.com/v1\n"
                "AI_MODEL=gpt-4o-mini\n"
                "AI_API_KEY=sk-..."
            ),
        ),
    }
    return guides.get(lang, guides["en"])


def _build_system_prompt(
    language: str,
    prefs: UserPreferencesRecord,
    aqi_context: Optional[dict],
) -> str:
    target_lang = LANGUAGE_NAMES.get(language, "English")

    context_block = "No air quality readings were attached."
    if aqi_context:
        p = aqi_context.get("pollutants", {})
        w = aqi_context.get("weather", {})
        source_status = "LIVE API" if aqi_context.get("is_live") else "DEMONSTRATION DATA (not live)"
        context_block = (
            f"Location: {aqi_context.get('location', prefs.location)}\n"
            f"Data Status: {source_status} ({aqi_context.get('data_source', 'unknown')})\n"
            f"Last Updated: {aqi_context.get('last_updated', 'unknown')}\n"
            f"AQI (US EPA): {p.get('aqi')} | PM2.5: {p.get('pm25')} µg/m³ | PM10: {p.get('pm10')} µg/m³ | "
            f"CO: {p.get('co')} µg/m³ | NO2: {p.get('no2')} µg/m³ | SO2: {p.get('so2')} µg/m³ | O3: {p.get('o3')} µg/m³\n"
            f"Weather: {w.get('temperature_c')}°C, Humidity {w.get('humidity_pct')}%, Wind {w.get('wind_speed_kmh')} km/h, {w.get('condition')}"
        )

    prefs_block = (
        f"Saved Location: {prefs.location}\n"
        f"Age Group: {prefs.age_group}\n"
        f"Lifestyle: {prefs.lifestyle}\n"
        f"Family Categories: {', '.join(prefs.family_categories)}\n"
        f"Transportation: {prefs.transportation_type}\n"
        f"Outdoor Preferences: {', '.join(prefs.outdoor_preferences)}"
    )

    return f"""You are BreatheSafe AI Assistant — an empathetic, scientifically grounded environmental air quality & family protection assistant.
Tagline: "Breathe Better. Live Better. Protect Everyone."

CRITICAL LANGUAGE RULE:
- Understand user messages written in English, Kannada, or Hindi.
- You MUST write your ENTIRE response strictly in {target_lang}. Use natural, clear phrasing in {target_lang}.

CAPABILITIES & QUALITY RULES:
1. Explain AQI and pollutants (PM2.5, PM10, CO, NO2, SO2, O3) clearly in everyday language.
2. Provide practical family safety advice, indoor air improvements, sustainable eco-friendly alternatives, and personalized daily routines tailored to the user's preferences below.
3. Explain WHY each recommendation is useful (cause-and-effect).
4. Reference the current AQI & weather context below when helpful, and be honest if the context is labeled DEMONSTRATION DATA rather than live readings.

STRICT HEALTH SAFETY GUARDRAILS:
- NEVER diagnose any medical condition or disease.
- NEVER prescribe medicines, inhalers, dosages, or treatments.
- Clearly distinguish general air-pollution safety guidance from professional medical advice.
- Give extra care precautions for vulnerable groups (children, older adults, pregnant individuals, and people with respiratory sensitivity).
- Recommend consulting a qualified doctor/healthcare professional for persistent or concerning symptoms.
- Recommend seeking emergency medical services immediately if anyone experiences severe breathing difficulty, chest pain, or bluish lips.

USER PROFILE:
{prefs_block}

CURRENT AIR QUALITY CONTEXT:
{context_block}
"""


class BaseAIProvider(ABC):
    @abstractmethod
    async def generate(self, messages: list[dict[str, str]]) -> tuple[str, str]:
        """Return (reply_text, model_used)."""


class OpenAICompatibleProvider(BaseAIProvider):
    def __init__(self, api_key: str, model: str, base_url: str, timeout: float) -> None:
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._is_ollama = "11434" in self.base_url

    async def generate(self, messages: list[dict[str, str]]) -> tuple[str, str]:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload: dict = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.4,
            "max_tokens": 900,
        }
        # Ollama needs explicit context window size for large system prompts
        if self._is_ollama:
            payload["num_ctx"] = 8192

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(url, headers=headers, json=payload)
            if resp.status_code >= 400:
                raise RuntimeError(f"LLM API error ({resp.status_code}): {resp.text[:300]}")
            data = resp.json()
            choices = data.get("choices") or []
            if not choices:
                raise RuntimeError("LLM API returned no response choices.")
            content = choices[0].get("message", {}).get("content", "").strip()
            if not content:
                raise RuntimeError("LLM API returned an empty message. The system prompt may exceed the model's context window.")
            return content, str(data.get("model") or self.model)


class GeminiProvider(BaseAIProvider):
    def __init__(self, api_key: str, model: str, timeout: float) -> None:
        self.api_key = api_key
        self.model = model or "gemini-2.5-flash"
        self.timeout = timeout

    async def generate(self, messages: list[dict[str, str]]) -> tuple[str, str]:
        system_instruction = ""
        contents = []
        for msg in messages:
            if msg["role"] == "system":
                system_instruction = msg["content"]
            else:
                role = "model" if msg["role"] == "assistant" else "user"
                contents.append({"role": role, "parts": [{"text": msg["content"]}]})

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent?key={self.api_key}"
        )
        payload: dict = {
            "contents": contents,
            "generationConfig": {"temperature": 0.4, "maxOutputTokens": 900},
        }
        if system_instruction:
            payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code >= 400:
                raise RuntimeError(f"Gemini API error ({resp.status_code}): {resp.text[:300]}")
            data = resp.json()
            candidates = data.get("candidates") or []
            if not candidates:
                raise RuntimeError("Gemini API returned no candidates.")
            parts = candidates[0].get("content", {}).get("parts") or []
            text = "".join(part.get("text", "") for part in parts).strip()
            if not text:
                raise RuntimeError("Gemini API returned an empty response.")
            return text, self.model


def get_ai_provider() -> BaseAIProvider:
    if settings.AI_PROVIDER == "gemini":
        return GeminiProvider(
            api_key=settings.AI_API_KEY,
            model=settings.AI_MODEL,
            timeout=settings.AI_TIMEOUT_SECONDS,
        )
    return OpenAICompatibleProvider(
        api_key=settings.AI_API_KEY,
        model=settings.AI_MODEL,
        base_url=settings.AI_BASE_URL,
        timeout=settings.AI_TIMEOUT_SECONDS,
    )


async def chat_with_assistant(
    user_message: str,
    language: str,
    prefs: UserPreferencesRecord,
    history: list[dict[str, str]],
    aqi_context: Optional[dict] = None,
) -> ChatResponse:
    now_iso = datetime.now(timezone.utc).isoformat()
    if not is_ai_configured():
        return ChatResponse(
            configured=False,
            language=language,
            reply=None,
            model_used=None,
            provider=settings.AI_PROVIDER,
            aqi_context_used=aqi_context,
            error="AI_API_KEY is not configured.",
            setup_guide=build_setup_guide(language),
            created_at=now_iso,
        )

    system_prompt = _build_system_prompt(language, prefs, aqi_context)
    messages: list[dict[str, str]] = [{"role": "system", "content": system_prompt}]
    for item in history[-10:]:
        messages.append({"role": item["role"], "content": item["content"]})
    messages.append({"role": "user", "content": user_message})

    provider = get_ai_provider()
    reply_text, model_used = await provider.generate(messages)
    return ChatResponse(
        configured=True,
        language=language,
        reply=reply_text,
        model_used=model_used,
        provider=settings.AI_PROVIDER,
        aqi_context_used=aqi_context,
        error=None,
        setup_guide=None,
        created_at=now_iso,
    )
