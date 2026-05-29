from datetime import datetime, timezone
from sqlalchemy import String, Boolean, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    agent = "agent"
    user = "user"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.user)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    created_tickets: Mapped[list["Ticket"]] = relationship(
        "Ticket", foreign_keys="Ticket.created_by_id", back_populates="creator"
    )
    assigned_tickets: Mapped[list["Ticket"]] = relationship(
        "Ticket", foreign_keys="Ticket.assigned_to_id", back_populates="assignee"
    )
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="author")
