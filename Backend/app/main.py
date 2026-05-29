from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import auth, tickets, users
import app.models  # noqa: F401 — ensure models are registered before create_all

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TickioOSS API", version="1.0.0", description="Open-source IT support ticket system")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tickets.router)
app.include_router(users.router)


@app.get("/health")
def health():
    return {"status": "ok", "service": "TickioOSS"}
