from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="3.0.0",
    description="Next-Generation AI Decision Operating System API"
)

# Configure CORS for Next.js Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {
        "status": "online",
        "intelligence_core": "active",
        "memory_graph": "connected"
    }

# Future Router Inclusions:
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
# app.include_router(decisions.router, prefix="/api/v1/decisions", tags=["Intelligence"])
# app.include_router(memory.router, prefix="/api/v1/memory", tags=["Memory"])
