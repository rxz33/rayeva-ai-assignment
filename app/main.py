from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.db import init_db
from app.routes import category, proposal, whatsapp

app = FastAPI(
    title="Rayeva AI Modules",
    description="AI-powered backend services for sustainable product categorization and B2B proposal generation.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialise database tables on startup
init_db()

app.include_router(category.router)
app.include_router(proposal.router)
app.include_router(whatsapp.router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "Rayeva AI Modules"}
