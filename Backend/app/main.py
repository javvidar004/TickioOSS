from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine, SessionLocal
from app.routers import auth, tickets, users
import app.models  # noqa: F401 — ensure models are registered before create_all
from app.models.user import User, UserRole

Base.metadata.create_all(bind=engine)


def _seed_admin() -> None:
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.username == "admin").first():
            db.add(User(
                username="admin",
                email="admin@tickio.local",
                # bcrypt hash of "admin123" (rounds=12)
                password_hash="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TiGPB.mKZKnDHfyOEMhm8y3gvmsi",
                role=UserRole.admin,
                is_active=True,
            ))
            db.commit()
    finally:
        db.close()


_seed_admin()

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
