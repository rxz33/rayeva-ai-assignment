# Rayeva AI Systems Assignment

AI-powered backend services for sustainable product categorization and B2B proposal generation.

## Overview

This project implements four AI-powered backend modules for an ecommerce sustainability platform.

- **Module 1:** AI Auto-Category & Tag Generator — Classifies products and generates SEO tags
- **Module 2:** AI B2B Proposal Generator — Generates sustainable product proposals for corporate clients
- **Module 3:** AI Impact Reporting Generator *(Architecture outlined)*
- **Module 4:** AI WhatsApp Support Bot *(Stub implemented + Architecture outlined)*

The system ensures structured AI outputs, logging, validation, database storage, and clear separation of AI and business logic.

---

## Tech Stack

- Python 3.11
- FastAPI
- Groq (LLaMA 3.1 via API)
- Pydantic v2
- SQLAlchemy + SQLite
- Uvicorn

---

## Features

- AI-powered product categorization with validated category enforcement
- B2B sustainability proposal generation with per-product cost breakdown
- Structured JSON outputs with strict schema validation
- SQLite database storage for all AI outputs
- Prompt and response logging to `ai_logs.json`
- `/history` endpoints to retrieve past results
- Retry logic for resilient AI responses
- WhatsApp bot stub (Module 4)
- Modular backend architecture
- Error handling and validation

---

## Project Architecture

```
app/
├── main.py
├── database/
│   ├── db.py              # SQLAlchemy engine and session
│   └── models.py          # ORM models for categories and proposals
│
├── routes/
│   ├── category.py        # POST /generate-category, GET /history/categories
│   ├── proposal.py        # POST /generate-proposal, GET /history/proposals
│   └── whatsapp.py        # POST /whatsapp/webhook (Module 4 stub)
│
├── services/
│   ├── ai_client.py       # Groq API wrapper with retry logic
│   ├── category_service.py
│   └── proposal_service.py
│
├── validators/
│   ├── category_validator.py
│   └── proposal_validator.py
│
├── schemas/
│   ├── category_schema.py
│   └── proposal_schema.py
│
└── utils/
    └── logger.py          # Prompt + response logging
```

### Architecture Explanation

- **Routes** handle API endpoints and HTTP request/response processing.
- **Services** interact with the AI model and construct prompts — all AI logic lives here.
- **Validators** enforce that AI responses match expected JSON schemas and business rules.
- **Schemas** define request and response models using Pydantic v2.
- **Database** stores all AI outputs persistently via SQLAlchemy ORM.
- **Logger** writes raw prompts and responses to `ai_logs.json` for debugging.

---

## API Modules

---

## Module 1: AI Auto-Category & Tag Generator

Classifies a product into sustainability-focused categories and generates SEO tags.

**Endpoint:** `POST /generate-category`

**Example request:**
```json
{
  "product_name": "Bamboo Toothbrush",
  "description": "Eco friendly toothbrush",
  "material": "bamboo",
  "use_case": "oral care"
}
```

**Example response:**
```json
{
  "primary_category": "personal_care",
  "sub_category": "oral_care",
  "seo_tags": ["bamboo", "eco friendly", "sustainable", "plastic free", "oral care"],
  "sustainability_filters": ["biodegradable", "renewable resources"]
}
```

**Retrieve history:** `GET /history/categories`

---

## Module 2: AI B2B Proposal Generator

Generates sustainable product proposals for corporate clients based on budget, employee count, and sustainability goals.

**Endpoint:** `POST /generate-proposal`

**Example request:**
```json
{
  "client_type": "corporate office",
  "budget": 100000,
  "employee_count": 200,
  "sustainability_goal": "reduce plastic waste"
}
```

**Example response:**
```json
{
  "product_mix": [
    {"product": "steel water bottle", "quantity": 200, "unit_price": 300, "total_cost": 60000},
    {"product": "bamboo toothbrush", "quantity": 200, "unit_price": 50, "total_cost": 10000}
  ],
  "budget_allocation": {
    "products": 85000,
    "logistics": 10000,
    "buffer": 5000
  },
  "impact_summary": "Reusable products reduce single-use plastic waste."
}
```

**Retrieve history:** `GET /history/proposals`

---

## Module 3: AI Impact Reporting Generator *(Architecture)*

This module generates an impact report for a completed order, estimating environmental metrics.

**Planned Endpoint:** `POST /generate-impact-report`

**Planned Request:**
```json
{
  "order_id": "ORD-1023",
  "products": [
    {"product_name": "Steel Water Bottle", "quantity": 200, "material": "stainless steel"},
    {"product_name": "Bamboo Toothbrush", "quantity": 200, "material": "bamboo"}
  ]
}
```

**Planned Response:**
```json
{
  "order_id": "ORD-1023",
  "plastic_saved_kg": 12.4,
  "carbon_avoided_kg": 8.2,
  "local_sourcing_summary": "60% of products sourced from within 500km",
  "impact_statement": "This order prevented approximately 12.4kg of plastic from entering landfill and avoided 8.2kg of CO2 equivalent emissions."
}
```

**Planned Architecture:**

```
routes/impact.py
  └── POST /generate-impact-report
        └── services/impact_service.py
              ├── Builds prompt with product list and material data
              ├── Calls generate_ai_response()
              └── Logs and stores result

validators/impact_validator.py
  └── Validates plastic_saved_kg, carbon_avoided_kg > 0
  └── Validates impact_statement is meaningful text

database/models.py
  └── ImpactReport model (order_id, plastic_saved_kg, carbon_avoided_kg, impact_statement, created_at)
```

**Prompt Design for Module 3:**

The prompt will provide product names, quantities, and materials, then instruct the AI to apply logic-based estimations (e.g., average plastic saved per bamboo toothbrush vs. plastic equivalent). The AI is instructed to return only numeric fields and a human-readable summary — no markdown, no explanations.

---

## Module 4: AI WhatsApp Support Bot *(Stub + Architecture)*

This module handles WhatsApp messages via a webhook, routing queries to the AI for order status, return policy, and escalation.

**Implemented Stub Endpoint:** `POST /whatsapp/webhook`

The stub accepts an incoming WhatsApp message body, sends it to the AI with a sustainability support context, and returns a structured response. In production, this would integrate with Twilio's WhatsApp API.

**Planned Architecture:**

```
routes/whatsapp.py
  └── POST /whatsapp/webhook
        ├── Parses incoming Twilio WhatsApp payload
        └── services/whatsapp_service.py
              ├── Classifies intent: order_status | return_policy | escalation | general
              ├── For order_status: queries database for real order data
              ├── For escalation: flags message and alerts human agent
              └── Logs full AI conversation

validators/whatsapp_validator.py
  └── Validates intent is one of known types
  └── Validates response text is non-empty

database/models.py
  └── WhatsAppConversation model (phone_number, intent, user_message, ai_response, escalated, created_at)
```

**Intent Classification Prompt Design:**

The AI is first asked to classify the user's message into one of four intents: `order_status`, `return_policy`, `escalation`, or `general`. Based on the classified intent, a second prompt is generated with relevant context (e.g., injecting real order data for order_status queries). This two-step prompting ensures the AI always has the right context before generating a response.

**Escalation Logic:**

If the AI classifies intent as `escalation`, the system skips the AI response and instead triggers a human agent alert (email/Slack notification) and logs the conversation with `escalated: true`.

**Production Integration:**

In production, Twilio's WhatsApp sandbox sends POST requests to this webhook. The response is formatted as TwiML and sent back to the user's WhatsApp number. A Twilio account SID and auth token would be stored as environment variables.

---

## AI Prompt Design Explanation

### Design Philosophy

All prompts in this system follow three principles:

1. **Strict output constraints** — Every prompt instructs the AI to return *only* valid JSON with an exact schema provided inline. This eliminates the need to parse natural language.

2. **Enumerated valid values** — Where applicable (e.g., `primary_category`), the prompt lists all valid options explicitly. This reduces hallucination and makes validation deterministic.

3. **Low temperature (0.2)** — All AI calls use `temperature=0.2` to favour consistent, predictable outputs over creative variation. This is critical for structured data generation.

### Module 1 Prompt Design

The prompt provides product details (name, description, material, use case) and instructs the AI to classify into one of five predefined categories. The category list is embedded directly in the prompt to prevent out-of-scope outputs. SEO tags are constrained to 5–10 keywords to match the spec.

### Module 2 Prompt Design

The prompt embeds the exact JSON schema the AI must return, including the new `unit_price` and `total_cost` fields per product. The client budget is passed explicitly, and the AI is instructed that total budget allocation must not exceed it. The impact summary is scoped to sustainability language to maintain brand consistency.

### Retry Logic

If the AI returns invalid JSON (e.g., due to a rare hallucination), `ai_client.py` retries the call once before raising an error. This is implemented with a configurable `max_retries` parameter.

---

## Technical Requirements Implementation

| Requirement | Implementation |
|---|---|
| Structured JSON Outputs | Explicit schema in every prompt + Pydantic validation |
| Prompt + Response Logging | `utils/logger.py` → `ai_logs.json` |
| Environment-based API Key Management | `.env` + `python-dotenv` |
| Clear Separation of AI and Business Logic | Services handle AI; Routes handle HTTP |
| Error Handling and Validation | Validators + HTTPException with detailed errors |
| Database Storage | SQLAlchemy + SQLite for all module outputs |

---

## Setup and Run

**Clone the repository:**
```bash
git clone https://github.com/rxz33/rayeva-ai-assignment.git
cd rayeva-ai-assignment
```

**Create and activate a virtual environment:**
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Set environment variables:**
```bash
cp .env.example .env
# Open .env and add your API key:
# GROQ_API_KEY=your_api_key_here
```

**Run the server:**
```bash
uvicorn app.main:app --reload
```

**Open Swagger docs:**
```
http://127.0.0.1:8000/docs
```

---

## AI Logging

All AI prompts and responses are stored in `ai_logs.json`.

Example log entry:
```json
{
  "timestamp": "2024-01-01T12:00:00",
  "module": "category_generator",
  "prompt": "...",
  "response": "..."
}
```

---

## Future Improvements

- Full Twilio WhatsApp integration for Module 4
- Full implementation of Module 3 impact reporting
- Improve prompt optimization with few-shot examples
- Add response caching with Redis
- Implement monitoring and analytics for AI outputs
- PostgreSQL migration for production deployments