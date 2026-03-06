# Rayeva AI Systems — Internship Assignment

> **AI-powered sustainability intelligence platform** built with FastAPI, Groq LLM, SQLite, and a custom investment-grade frontend dashboard.

**Live Backend:** https://rayeva-ai-assignment-79v5.onrender.com/docs  
**Frontend:** Deploy via `npx vercel --prod` from `rayeva-dashboard/`

---

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Modules](#modules)
  - [Module 1 — Category & Tag Generator](#module-1--category--tag-generator)
  - [Module 2 — B2B Proposal Generator](#module-2--b2b-proposal-generator)
  - [Module 3 — Impact Report Generator](#module-3--impact-report-generator)
  - [Module 4 — WhatsApp Support Bot](#module-4--whatsapp-support-bot)
- [Authentication](#authentication)
- [Admin Dashboard](#admin-dashboard)
- [History & Search](#history--search)
- [Frontend Dashboard](#frontend-dashboard)
- [API Reference](#api-reference)
- [Setup & Deployment](#setup--deployment)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)

---

## Project Overview

Rayeva AI is a full-stack AI platform for sustainable ecommerce. It automates product categorization, generates B2B sustainability proposals, calculates environmental impact, and provides AI-powered customer support — all backed by a Groq LLM and a persistent SQLite database.

Built as part of an AI Engineer internship assignment for Rayeva AI Systems (Internshala).

### What's been implemented

| Feature | Status |
|---|---|
| Module 1: AI Category & Tag Generator | ✅ Complete |
| Module 2: AI B2B Proposal Generator | ✅ Complete |
| Module 3: AI Environmental Impact Report | ✅ Complete |
| Module 4: WhatsApp Support Bot (stub) | ✅ Complete |
| JWT Authentication (register / login) | ✅ Complete |
| Admin Stats Dashboard | ✅ Complete |
| History endpoints with search/filter | ✅ Complete |
| Sustainability Score (0–100) in Module 1 | ✅ Complete |
| Per-product cost breakdown in Module 2 | ✅ Complete |
| SQLite database with full ORM | ✅ Complete |
| Keep-alive scheduler (Render free tier) | ✅ Complete |
| Structured JSON logging | ✅ Complete |
| Input validation (Pydantic v2) | ✅ Complete |
| Frontend dashboard (single-file, no build) | ✅ Complete |

---

## Tech Stack

**Backend**
- Python 3.11+
- FastAPI — REST API framework
- Groq SDK — LLM inference (llama-3.1-8b-instant)
- SQLAlchemy — ORM with SQLite
- Pydantic v2 — request/response validation
- python-jose + passlib — JWT authentication (bcrypt)
- APScheduler — background keep-alive scheduler
- httpx — async HTTP for keep-alive pings

**Frontend**
- Vanilla HTML/CSS/JS (single file, no build step)
- Cormorant Garamond + Barlow Condensed + JetBrains Mono
- Investment-grade UI (Bloomberg Terminal aesthetic)

**Infrastructure**
- Render — backend hosting (free tier)
- Vercel — frontend hosting
- SQLite — persistent storage (file-based)

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (Vercel)                  │
│              index.html — single file app            │
│    Dashboard · M1 · M2 · M3 · M4 · Admin · History  │
└────────────────────────┬────────────────────────────┘
                         │ HTTPS API calls
┌────────────────────────▼────────────────────────────┐
│               FastAPI Backend (Render)               │
│                                                      │
│  /auth          JWT register · login · /me           │
│  /generate-*    AI modules 1, 2, 3                   │
│  /whatsapp      Module 4 webhook                     │
│  /admin/stats   Aggregate analytics                  │
│  /history/*     Persistent result history            │
│  /health        Keep-alive + health check            │
│                                                      │
│  ┌───────────────┐    ┌──────────────────────────┐  │
│  │  ai_client.py │    │     SQLite (rayeva.db)    │  │
│  │  Groq LLM     │    │  CategoryResult          │  │
│  │  + retry(2x)  │    │  ProposalResult          │  │
│  └───────────────┘    │  ImpactReport            │  │
│                       │  User                    │  │
│  APScheduler          └──────────────────────────┘  │
│  Pings /health every 10 min (prevents sleep)         │
└─────────────────────────────────────────────────────┘
```

### Module Data Flow

```
User Input → Pydantic Schema (validate) → AI Service (Groq prompt)
    → JSON parse → Validator (business rules) → SQLite (store)
    → Pydantic Response → JSON to client
```

---

## Modules

### Module 1 — Category & Tag Generator

**Endpoint:** `POST /generate-category`

Classifies any sustainable product into a predefined taxonomy, generates SEO keywords, sustainability attributes, and an ESG score.

**Input:**
```json
{
  "product_name": "Bamboo Toothbrush",
  "description": "Eco-friendly biodegradable toothbrush",
  "material": "bamboo",
  "use_case": "oral care"
}
```

**Output:**
```json
{
  "primary_category": "personal_care",
  "sub_category": "oral_care",
  "seo_tags": ["bamboo toothbrush", "eco friendly", "biodegradable", "plastic free", "sustainable oral care"],
  "sustainability_filters": ["biodegradable", "renewable resources", "plastic-free"],
  "sustainability_score": 88,
  "score_reasoning": "Bamboo is a fast-growing renewable material that is fully biodegradable and replaces single-use plastic."
}
```

**Valid categories:** `personal_care`, `kitchen`, `office_supplies`, `packaging`, `home_products`

**Validations:**
- `primary_category` must be one of the 5 valid values
- `seo_tags` must contain 5–10 tags
- `sustainability_score` must be 0–100 integer
- All required fields enforced

---

### Module 2 — B2B Proposal Generator

**Endpoint:** `POST /generate-proposal`

Generates a complete sustainable procurement proposal for corporate clients, including product mix, per-unit pricing, capital allocation breakdown, and ESG impact summary.

**Input:**
```json
{
  "client_type": "corporate office",
  "budget": 100000,
  "employee_count": 200,
  "sustainability_goal": "reduce plastic waste"
}
```

**Output:**
```json
{
  "product_mix": [
    {
      "product": "Stainless Steel Water Bottle",
      "quantity": 200,
      "unit_price": 350,
      "total_cost": 70000
    }
  ],
  "budget_allocation": {
    "products": 85000,
    "logistics": 10000,
    "buffer": 5000
  },
  "impact_summary": "This procurement will eliminate approximately 73,000 single-use plastic items annually across the organization."
}
```

**Validations:**
- Total budget allocation must not exceed client budget
- `unit_price` and `total_cost` must be positive numbers
- `impact_summary` must be meaningful text

---

### Module 3 — Impact Report Generator

**Endpoint:** `POST /generate-impact-report`

Calculates the environmental impact of a sustainability order — plastic diverted from landfill, carbon emissions avoided, and local sourcing analysis.

**Input:**
```json
{
  "order_id": "ORD-1023",
  "products": [
    {"product_name": "Steel Water Bottle", "quantity": 200, "material": "stainless steel"},
    {"product_name": "Bamboo Toothbrush", "quantity": 200, "material": "bamboo"}
  ]
}
```

**Output:**
```json
{
  "order_id": "ORD-1023",
  "plastic_saved_kg": 12.4,
  "carbon_avoided_kg": 8.2,
  "local_sourcing_summary": "Approximately 60% of selected materials are likely sourced within 500km based on material type.",
  "impact_statement": "This order prevented 12.4kg of plastic from entering landfill and avoided 8.2kg of CO₂ equivalent emissions."
}
```

**Logic:** AI estimates plastic saved by comparing eco materials to their single-use plastic equivalents (e.g. bamboo toothbrush saves ~15g plastic vs plastic equivalent × quantity).

**History endpoint:** `GET /history/impact-reports?limit=20`

---

### Module 4 — WhatsApp Support Bot

**Endpoint:** `POST /whatsapp/webhook`

Two-step AI pipeline: first classifies intent, then generates an appropriate reply. Escalation bypasses AI entirely and flags for human agent.

**Input:**
```json
{
  "phone_number": "+91-9999999999",
  "message": "My product arrived damaged, I want a refund!"
}
```

**Output:**
```json
{
  "intent": "escalation",
  "reply": "We've escalated your query to a human agent. Someone will contact you shortly.",
  "escalated": true
}
```

**Intent classes:** `order_status`, `return_policy`, `escalation`, `general`

**Production path:** Connect Twilio WhatsApp Business API to this webhook URL. Twilio sends POST requests on incoming messages; this endpoint handles classification, response generation, and escalation routing.

**Architecture for full implementation:**
```
WhatsApp User → Twilio → POST /whatsapp/webhook
    → Step 1: Groq classifies intent
    → Step 2: Groq generates reply (or escalation)
    → Twilio sends reply back to user
    → Escalations → notify human agent via Slack/email
```

---

## Authentication

JWT-based authentication using OAuth2 password flow.

### Register
```http
POST /auth/register
Content-Type: application/json

{
  "email": "analyst@firm.com",
  "password": "securepassword"
}
```

### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=analyst@firm.com&password=securepassword
```

Both return:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "email": "analyst@firm.com"
}
```

### Get current user
```http
GET /auth/me
Authorization: Bearer <token>
```

**Token:** 24-hour expiry, HS256 signed. Set `SECRET_KEY` in environment variables (minimum 32 characters, change in production).

---

## Admin Dashboard

**Endpoint:** `GET /admin/stats`

Returns platform-wide aggregate statistics across all AI modules.

**Response:**
```json
{
  "categories": {
    "total": 42,
    "avg_sustainability_score": 76.3,
    "most_common_category": "personal_care"
  },
  "proposals": {
    "total": 18,
    "total_budget_proposed_inr": 1850000
  },
  "impact_reports": {
    "total": 11,
    "total_plastic_saved_kg": 148.6,
    "total_carbon_avoided_kg": 92.4
  }
}
```

---

## History & Search

All AI outputs are stored persistently in SQLite and queryable via history endpoints.

| Endpoint | Filter params |
|---|---|
| `GET /history/categories` | `?category=personal_care&limit=20` |
| `GET /history/proposals` | `?client_type=office&limit=20` |
| `GET /history/impact-reports` | `?limit=20` |

All return `{ "count": N, "results": [...] }`.

---

## Frontend Dashboard

A single-file dashboard (`index.html`) with no build step required. Drop it into any static host.

**Design:** Investment-grade "ESG Terminal" aesthetic — white background, cobalt blue accents, gold prestige markers, Cormorant Garamond serif headings, JetBrains Mono for all data.

**Pages:**
- **Dashboard** — live stats from all 4 modules + recent activity feed
- **Module 1** — product classification form with ESG grade (A/B/C/D), score bar, SEO tags, sustainability filters
- **Module 2** — proposal form with product mix table, capital allocation bars, impact summary
- **Module 3** — order impact form with plastic/carbon metrics, local sourcing analysis
- **Module 4** — live WhatsApp chat simulation with intent badges
- **Admin** — aggregate ESG metrics, API reference
- **History** — tabbed audit trail for all 3 data types

**Auth:** JWT login/register modal, token stored in localStorage, persists across sessions.

---

## API Reference

```
Auth
  POST   /auth/register          Register new user
  POST   /auth/login             Login (OAuth2 form)
  GET    /auth/me                Get current user

AI Modules
  POST   /generate-category      Module 1: classify product
  POST   /generate-proposal      Module 2: generate B2B proposal
  POST   /generate-impact-report Module 3: calculate impact
  POST   /whatsapp/webhook       Module 4: support bot

History
  GET    /history/categories     Category results (filterable)
  GET    /history/proposals      Proposal results (filterable)
  GET    /history/impact-reports Impact report results

Analytics
  GET    /admin/stats            Platform-wide statistics

System
  GET    /health                 Health check + keep-alive target
  GET    /docs                   Swagger UI (auto-generated)
  GET    /redoc                  ReDoc documentation
```

---

## Setup & Deployment

### Local Development

```bash
# Clone and install
git clone <repo-url>
cd rayeva-ai-assignment
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your GROQ_API_KEY and SECRET_KEY

# Run
uvicorn app.main:app --reload

# API docs available at:
# http://localhost:8000/docs
```

### Deploy Backend to Render

1. Push code to GitHub
2. Create new **Web Service** on Render
3. Connect your GitHub repo
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables (see below)
7. Deploy

### Deploy Frontend to Vercel

```bash
cd rayeva-dashboard
npx vercel --prod
```

Or drag-and-drop `index.html` to vercel.com.

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ | Groq API key from console.groq.com |
| `SECRET_KEY` | ✅ | JWT signing secret (min 32 chars, change in production) |

**.env.example:**
```
GROQ_API_KEY=your_api_key_here
SECRET_KEY=your-secret-key-min-32-chars-change-this
```

---

## Project Structure

```
rayeva-ai-assignment/
│
├── app/
│   ├── main.py                    # FastAPI app, CORS, keep-alive scheduler
│   │
│   ├── database/
│   │   ├── db.py                  # SQLAlchemy engine, session, init_db()
│   │   └── models.py              # ORM models: CategoryResult, ProposalResult,
│   │                              #   ImpactReport, User
│   │
│   ├── routes/
│   │   ├── auth.py                # JWT register, login, /me
│   │   ├── category.py            # POST /generate-category + history
│   │   ├── proposal.py            # POST /generate-proposal + history
│   │   ├── impact.py              # POST /generate-impact-report + history
│   │   ├── whatsapp.py            # POST /whatsapp/webhook
│   │   └── admin.py               # GET /admin/stats
│   │
│   ├── services/
│   │   ├── ai_client.py           # Groq LLM client with retry logic
│   │   ├── auth_service.py        # JWT encode/decode, bcrypt hashing
│   │   ├── category_service.py    # Module 1 prompt engineering
│   │   ├── proposal_service.py    # Module 2 prompt engineering
│   │   └── impact_service.py      # Module 3 prompt engineering
│   │
│   ├── schemas/
│   │   ├── category_schema.py     # ProductInput, CategoryOutput (Pydantic v2)
│   │   ├── proposal_schema.py     # ProposalInput, ProposalOutput
│   │   └── impact_schema.py       # ImpactInput, ImpactOutput
│   │
│   ├── validators/
│   │   ├── category_validator.py  # Category whitelist, SEO tag count, score range
│   │   ├── proposal_validator.py  # Budget constraint, unit price, total cost
│   │   └── impact_validator.py    # Float validation, text quality checks
│   │
│   └── utils/
│       └── logger.py              # JSON file logger (ai_logs.json)
│
├── rayeva-dashboard/
│   └── index.html                 # Complete frontend (single file, no build)
│
├── requirements.txt               # All Python dependencies
├── .env.example                   # Environment variable template
└── README.md                      # This file
```

---

## Key Design Decisions

**Why SQLite over PostgreSQL?**  
Zero configuration, no external service required, perfectly adequate for demo scale. Easily swappable to PostgreSQL by changing `DATABASE_URL` in `db.py`.

**Why Groq over OpenAI?**  
Free tier, ultra-low latency (llama-3.1-8b-instant), and sufficient quality for structured JSON generation tasks.

**Why single-file frontend?**  
No build step, no Node.js required, instant deployment to any static host. The entire UI is one `index.html` — drop it anywhere.

**Why APScheduler for keep-alive?**  
Render's free tier spins down after 15 minutes of inactivity. The scheduler pings `/health` every 10 minutes from within the process itself, keeping the service warm during demos without an external cron.

**Why prompt-level JSON enforcement?**  
The AI is instructed to return only raw JSON with no markdown or explanation. This combined with the `ai_client.py` stripping of backtick fences ensures reliable parsing without fragile regex.

---

## Code Quality Highlights

- **Pydantic v2** syntax throughout (`model_config = ConfigDict(...)`, `@field_validator`)
- **Separation of concerns** — route → service → validator → schema → DB, no logic leakage
- **Retry logic** in `ai_client.py` — 2 attempts with 1s backoff before raising
- **Startup validation** — API key checked on import, fails fast with clear error
- **HTTP error preservation** — Groq error details passed through to client response
- **Type-safe budget checks** — explicit `isinstance()` guards before arithmetic
- **Searchable history** — query parameters on all history endpoints

---

*Submitted for Rayeva AI Systems internship assignment — Internshala*