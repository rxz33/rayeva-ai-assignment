from fastapi import FastAPI

from app.routes import category, proposal

app = FastAPI(title="Rayeva AI Modules")

app.include_router(category.router)
app.include_router(proposal.router)
