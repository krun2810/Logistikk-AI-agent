# 🚛 Logistikk AI-Agent

> **An AI-powered logistics inquiry processing agent built with FastAPI, LangChain, and OpenAI.**

[![CI](https://github.com/Logistikk-AI-agent/Logistikk-AI-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/Logistikk-AI-agent/Logistikk-AI-agent/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green)
![LangChain](https://img.shields.io/badge/LangChain-0.2+-yellow)
![Docker](https://img.shields.io/badge/Docker-ready-blue)

---

## 📋 Beskrivelse / Description

Logistikk AI-Agent er en intelligent backend-tjeneste som automatisk behandler kundehenvendelser for et norsk fraktselskap. Agenten kategoriserer henvendelser, trekker ut sporingsnumre og foreslår passende svar – alt ved hjelp av LangChain og OpenAI GPT-4o-mini.

**Logistikk AI-Agent** is an intelligent backend service that automatically processes customer inquiries for a Norwegian shipping company. The agent categorizes inquiries, extracts tracking numbers, and suggests appropriate responses – all powered by LangChain and OpenAI GPT-4o-mini.

---

## 🛠 Teknologistabel / Tech Stack

| Teknologi      | Versjon  | Formål                        |
|----------------|----------|-------------------------------|
| Python         | 3.11     | Kjøretidsmiljø                |
| FastAPI        | ≥0.110   | REST API-rammeverk            |
| LangChain      | ≥0.2     | Agent-orkestreringsrammeverk  |
| OpenAI         | ≥1.30    | LLM (GPT-4o-mini)             |
| AgentOps       | ≥0.3     | Agent-overvåking              |
| Pydantic       | ≥2.0     | Datavalidering                |
| Docker         | —        | Containerisering              |
| GitHub Actions | —        | CI/CD                         |

---

## 🏗 Arkitektur / Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Application                   │
│                                                         │
│  POST /inquiries                GET /health             │
│        │                              │                 │
│        ▼                              ▼                 │
│  InquiryRequest              HealthResponse             │
│  (Pydantic model)                                       │
│        │                                                │
│        ▼                                                │
│  process_inquiry()                                      │
│        │                                                │
│        ▼                                                │
│  ┌─────────────────────────────────┐                    │
│  │       LangChain AgentExecutor   │                    │
│  │                                 │                    │
│  │  Tools:                         │                    │
│  │  • categorize_inquiry()         │                    │
│  │  • get_tracking_info()          │                    │
│  │                                 │                    │
│  │  LLM: OpenAI GPT-4o-mini        │                    │
│  └─────────────────────────────────┘                    │
│        │                                                │
│        ▼                                                │
│  InquiryResponse (JSON)                                 │
│  • category                                             │
│  • summary                                              │
│  • suggested_action                                     │
│  • confidence                                           │
│  • processing_time_ms                                   │
└─────────────────────────────────────────────────────────┘
         │
         ▼
   AgentOps Dashboard (overvåking / monitoring)
```

---

## 🚀 Oppsett / Setup

### Forutsetninger / Prerequisites
- Python 3.11+
- Docker & Docker Compose (valgfritt / optional)
- OpenAI API-nøkkel

### Lokal installasjon / Local Installation

```bash
# 1. Klon repositoriet / Clone the repository
git clone https://github.com/your-username/Logistikk-AI-agent.git
cd Logistikk-AI-agent

# 2. Kopier miljøvariabelfilen / Copy env file
cp .env.example .env

# 3. Legg til API-nøkler i .env / Add API keys in .env
# OPENAI_API_KEY=sk-...
# AGENTOPS_API_KEY=...

# 4. Installer avhengigheter / Install dependencies
pip install -r requirements.txt

# 5. Start serveren / Start the server
uvicorn app.main:app --reload
```

### Docker

```bash
# Bygg og start / Build and start
docker-compose up --build

# API tilgjengelig på / API available at:
# http://localhost:8000
```

---

## 📡 API-endepunkter / API Endpoints

| Metode | Endepunkt    | Beskrivelse                        |
|--------|--------------|-------------------------------------|
| GET    | `/health`    | Helsesjekk / Health check           |
| POST   | `/inquiries` | Behandle henvendelse / Process inquiry |
| GET    | `/docs`      | Swagger UI (automatisk / auto)      |

---

## 💡 Eksempel / Example

### Forespørsel / Request

```bash
curl -X POST http://localhost:8000/inquiries \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Pakken min med nummer NO12345678901234567 er ikke kommet frem etter 5 dager.",
    "language": "no"
  }'
```

### Svar / Response

```json
{
  "category": "pakke_sporing",
  "summary": "Kunde rapporterer at pakke med sporingsnummer NO12345678901234567 ikke er levert etter 5 dager.",
  "suggested_action": "Sjekk sporingsstatus for NO12345678901234567 og kontakt transportør om forsinkelse.",
  "confidence": 0.95,
  "processing_time_ms": 842.31
}
```

---

## 📊 Overvåking med AgentOps / Monitoring with AgentOps

Agenten integrerer med [AgentOps](https://agentops.ai) for sanntidsovervåking av alle agent-kjøringer.

- Hver henvendelse oppretter en AgentOps-sesjon tagget med `["logistics", "inquiry"]`
- Du kan se alle kjøringer, kostnader og feil i AgentOps-dashbordet
- Sett `AGENTOPS_API_KEY` i `.env` for å aktivere

*AgentOps integration tracks every agent run in real-time, including tool calls, LLM costs, and errors.*

---

## ⚙️ CI/CD med GitHub Actions / CI/CD with GitHub Actions

Repositoriet bruker GitHub Actions for automatisk testing og linting på hvert push.

```
Push til main / PR til main
        │
        ▼
  GitHub Actions (ubuntu-latest)
        │
        ├── pip install -r requirements.txt
        ├── ruff check app/ tests/    ← Linting
        └── pytest tests/ -v          ← Alle tester
```

Workflow-filen: [`.github/workflows/ci.yml`](.github/workflows/ci.yml)

---

## 🧪 Testing

```bash
# Kjør alle tester / Run all tests
pytest tests/ -v

# Kjør linter / Run linter
ruff check app/ tests/
```

Testene bruker mocke-data og krever **ingen** OpenAI API-nøkkel.
*Tests use mocked data and require **no** OpenAI API key.*

---

## 📁 Prosjektstruktur / Project Structure

```
Logistikk-AI-agent/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI-applikasjon
│   ├── agent.py         # LangChain agent-logikk
│   ├── models.py        # Pydantic-modeller
│   └── tools.py         # Agent-verktøy (kategorisering, sporingsnummer)
├── tests/
│   ├── __init__.py
│   ├── test_main.py     # API-endepunkttester
│   └── test_agent.py    # Enhetstester for verktøy
├── .github/
│   └── workflows/
│       └── ci.yml       # GitHub Actions CI
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 📄 Lisens / License

MIT © 2024
