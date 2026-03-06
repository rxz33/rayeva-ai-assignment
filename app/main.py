import httpx
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.db import init_db
from app.routes import admin, auth, category, impact, proposal, whatsapp

app = FastAPI(
    title="Rayeva AI Modules",
    description="AI-powered backend for sustainable product categorization and B2B proposal generation.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


def _keep_alive():
    try:
        httpx.get(
            "https://rayeva-ai-assignment-79v5.onrender.com/health",
            timeout=10,
        )
    except Exception:
        pass


scheduler = BackgroundScheduler()
scheduler.add_job(_keep_alive, "interval", minutes=10)
scheduler.start()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(category.router)
app.include_router(proposal.router)
app.include_router(impact.router)
app.include_router(whatsapp.router)
app.include_router(admin.router, prefix="/admin", tags=["Admin"])


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "Rayeva AI Modules", "version": "2.0.0"}
