from datetime import datetime, timezone
from sqlalchemy import String, Text, Enum, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum


class TicketStatus(str, enum.Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"


class TicketPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class TicketCategory(str, enum.Enum):
    hardware = "hardware"
    software = "software"
    network = "network"
    access = "access"
    other = "other"


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[TicketStatus] = mapped_column(Enum(TicketStatus), default=TicketStatus.open)
    priority: Mapped[TicketPriority] = mapped_column(Enum(TicketPriority), default=TicketPriority.medium)
    category: Mapped[TicketCategory] = mapped_column(Enum(TicketCategory), default=TicketCategory.other)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    assigned_to_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    creator: Mapped["User"] = relationship("User", foreign_keys=[created_by_id], back_populates="created_tickets")
    assignee: Mapped["User | None"] = relationship("User", foreign_keys=[assigned_to_id], back_populates="assigned_tickets")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="ticket", cascade="all, delete-orphan")


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    ticket: Mapped["Ticket"] = relationship("Ticket", back_populates="comments")
    author: Mapped["User"] = relationship("User", back_populates="comments")
