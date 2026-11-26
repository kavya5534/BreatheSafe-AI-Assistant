# BreatheSafe AI

**Tagline:** Breathe Better. Live Better. Protect Everyone.

A full-stack, multilingual environmental intelligence dashboard and AI air-quality assistant built with **React + Tailwind CSS**, **FastAPI**, and **SQLite**.

## Features Implemented
- **Multilingual UI & AI Responses:** Full support for **English**, **Kannada (ಕನ್ನಡ)**, and **Hindi (हिन्दी)** persisted across navigation and browser refreshes.
- **Air Quality & Weather Dashboard:** Live integration with Open-Meteo Air Quality & Weather APIs (US EPA AQI, PM2.5, PM10, CO, NO2, SO2, O3, temperature, humidity, wind speed, 24h interactive trend chart). Automatically falls back to clearly labeled demonstration data if live APIs are unreachable.
- **BreatheSafe AI Assistant (`POST /api/chat`):** Provider-abstracted backend LLM integration (`openai_compatible` or `gemini`), environment-variable key management, AQI & user-profile context injection, health safety guardrails, chat history in SQLite, suggested questions, clear chat, and a setup guide when `AI_API_KEY` is missing.
- **User Personalization (`GET/POST /api/preferences`):** Location, language, age group, lifestyle, family vulnerable categories, transport mode, and outdoor activity preferences stored in SQLite.
- **Community Pollution Watch & Eco Tracker (`GET/POST /api/reports`, `GET/POST /api/activities`):** Report local air incidents, upvote reports, and log sustainable habits with estimated CO2 savings in SQLite.

## Quick Start (Windows PowerShell)

1. Copy `.env.example` to `.env` and optionally add your `AI_API_KEY`:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Start the FastAPI backend:
   ```powershell
   cd backend
   .\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

3. Start the React frontend in a new PowerShell window:
   ```powershell
   cd frontend
   npm run dev
   ```

4. Open `http://127.0.0.1:5173` in your browser.
