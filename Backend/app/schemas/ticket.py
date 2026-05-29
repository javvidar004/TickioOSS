from pydantic import BaseModel
from datetime import datetime
from app.models.ticket import TicketStatus, TicketPriority, TicketCategory
from app.schemas.user import UserOut


class CommentCreate(BaseModel):
    content: str


class CommentOut(BaseModel):
    id: int
    content: str
    created_at: datetime
    author: UserOut

    model_config = {"from_attributes": True}


class TicketCreate(BaseModel):
    title: str
    description: str
    priority: TicketPriority = TicketPriority.medium
    category: TicketCategory = TicketCategory.other


class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TicketStatus | None = None
    priority: TicketPriority | None = None
    category: TicketCategory | None = None
    assigned_to_id: int | None = None


class TicketOut(BaseModel):
    id: int
    title: str
    description: str
    status: TicketStatus
    priority: TicketPriority
    category: TicketCategory
    created_at: datetime
    updated_at: datetime
    creator: UserOut
    assignee: UserOut | None = None

    model_config = {"from_attributes": True}


class DashboardStats(BaseModel):
    total: int
    open: int
    in_progress: int
    resolved: int
    closed: int
    by_priority: dict
    by_category: dict
