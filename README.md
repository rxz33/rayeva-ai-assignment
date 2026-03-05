# Rayeva AI Systems Assignment

AI-powered backend services for sustainable product categorization and B2B proposal generation.

## Overview

This project implements two AI-powered backend modules for an ecommerce sustainability platform.

Module 1: Product Categorization  
Automatically classifies products into sustainability-focused categories and generates SEO tags.

Module 2: AI B2B Proposal Generator  
Generates sustainable product recommendations and budget allocation plans for corporate clients.

The system ensures structured AI outputs, logging, validation, and clear separation of AI and business logic.

## Tech Stack

- Python
- FastAPI
- Groq / LLM API
- Pydantic
- Uvicorn

## Features

- AI-powered product categorization
- B2B sustainability proposal generation
- Structured JSON outputs
- Prompt and response logging
- Modular backend architecture
- Validation and error handling

## Project Architecture
```
app/
├── routes/            # API endpoints
│   ├── category.py
│   └── proposal.py
│
├── services/          # AI interaction layer
│   ├── ai_client.py
│   ├── category_service.py
│   └── proposal_service.py
│
├── validators/        # AI output validation
│   ├── category_validator.py
│   └── proposal_validator.py
│
├── schemas/           # Request and response models
│   ├── category_schema.py
│   └── proposal_schema.py
│
└── utils/
    └── logger.py      # prompt + response logging
```

### Architecture Explanation

- **Routes** handle API endpoints and request processing.
- **Services** interact with the AI model and construct prompts.
- **Validators** ensure AI responses follow the expected JSON schema.
- **Schemas** define request and response models using Pydantic.
- **Logger** stores prompts and responses for debugging and observability.

## API Modules

## Module 1: Product Categorization

This module classifies a product into sustainability-focused categories and generates SEO tags.

Endpoint:
`POST /generate-category`

Example request:
```json
{
 "product_name": "Bamboo Toothbrush",
 "description": "Eco friendly toothbrush",
 "material": "bamboo",
 "use_case": "oral care"
}
```

Example response:
```json
{
 "primary_category": "personal_care",
 "sub_category": "oral_care",
 "seo_tags": ["bamboo", "eco friendly", "sustainable"],
 "sustainability_filters": ["biodegradable", "renewable resources"]
}
```

## Module 2: B2B Proposal Generator

This module generates sustainable product proposals for corporate clients based on budget, employee count, and sustainability goals.

Endpoint:
`POST /generate-proposal`

Example request:
```json
{
 "client_type": "corporate office",
 "budget": 100000,
 "employee_count": 200,
 "sustainability_goal": "reduce plastic waste"
}
```

Example response:
```json
{
 "product_mix": [
  {"product": "steel water bottle", "quantity": 200},
  {"product": "bamboo toothbrush", "quantity": 200}
 ],
 "budget_allocation": {
  "products": 85000,
  "logistics": 10000,
  "buffer": 5000
 },
 "impact_summary": "Reusable products reduce single-use plastic waste."
}
```

## Technical Requirements Implementation

### Structured JSON Outputs
AI responses are constrained using explicit JSON schemas and validated before returning responses.

### Prompt + Response Logging
All prompts and AI responses are logged using a custom logging utility.

### Environment-based API Key Management
API keys are stored in environment variables using `.env` and loaded via `python-dotenv`.

### Clear Separation of AI and Business Logic
AI interactions are isolated in the service layer while API logic remains in routes.

### Error Handling and Validation
The system includes structured error handling for:
- AI failures
- invalid JSON responses
- missing or incorrect fields
- business rule violations

## Setup and Run

Clone the project from GitHub

```bash
git clone https://github.com/rxz33/rayeva-ai-assignment.git
cd rayeva-ai-assignment
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Set environment variables
Copy the example environment file:
```
cp .env.example .env
```

Then open .env and add your API key:
```
GROQ_API_KEY=your_api_key_here
```

Run the server
```
uvicorn app.main:app --reload
```

Open Swagger API documentation:
```
http://127.0.0.1:8000/docs
```

## AI Logging

All AI prompts and responses are stored in ai_logs.json.

Example log entry:
```json
{
 "timestamp": "...",
 "module": "category_generator",
 "prompt": "...",
 "response": "..."
}
```

## Future Improvements

- Add database storage for logs
- Improve prompt optimization
- Add response caching
- Implement monitoring and analytics for AI outputs