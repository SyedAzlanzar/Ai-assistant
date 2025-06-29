from fastapi import FastAPI
from app.api.v1.routes import auth, ai

app = FastAPI(title="AI Writing Assistant")


app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["ai"])
