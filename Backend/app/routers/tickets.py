from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.ticket import Ticket, Comment, TicketStatus, TicketPriority, TicketCategory
from app.models.user import User, UserRole
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketOut, CommentCreate, CommentOut, DashboardStats
from app.auth.jwt import get_current_user

router = APIRouter(prefix="/tickets", tags=["tickets"])


def _can_edit(user: User, ticket: Ticket) -> bool:
    return user.role in (UserRole.admin, UserRole.agent) or ticket.created_by_id == user.id


@router.get("/", response_model=list[TicketOut])
def list_tickets(
    status: TicketStatus | None = None,
    priority: TicketPriority | None = None,
    category: TicketCategory | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(Ticket)
    if current_user.role == UserRole.user:
        q = q.filter(Ticket.created_by_id == current_user.id)
    if status:
        q = q.filter(Ticket.status == status)
    if priority:
        q = q.filter(Ticket.priority == priority)
    if category:
        q = q.filter(Ticket.category == category)
    return q.order_by(Ticket.created_at.desc()).all()


@router.post("/", response_model=TicketOut, status_code=201)
def create_ticket(data: TicketCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ticket = Ticket(**data.model_dump(), created_by_id=current_user.id)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.get("/dashboard", response_model=DashboardStats)
def dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role == UserRole.user:
        base = db.query(Ticket).filter(Ticket.created_by_id == current_user.id)
    else:
        base = db.query(Ticket)

    total = base.count()
    by_status = {
        s.value: base.filter(Ticket.status == s).count()
        for s in TicketStatus
    }
    by_priority = {
        p.value: base.filter(Ticket.priority == p).count()
        for p in TicketPriority
    }
    by_category = {
        c.value: base.filter(Ticket.category == c).count()
        for c in TicketCategory
    }

    return DashboardStats(
        total=total,
        open=by_status["open"],
        in_progress=by_status["in_progress"],
        resolved=by_status["resolved"],
        closed=by_status["closed"],
        by_priority=by_priority,
        by_category=by_category,
    )


@router.get("/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if current_user.role == UserRole.user and ticket.created_by_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return ticket


@router.put("/{ticket_id}", response_model=TicketOut)
def update_ticket(
    ticket_id: int,
    data: TicketUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if not _can_edit(current_user, ticket):
        raise HTTPException(status_code=403, detail="Access denied")

    if current_user.role == UserRole.user:
        allowed = {"title", "description"}
        update_data = {k: v for k, v in data.model_dump(exclude_none=True).items() if k in allowed}
    else:
        update_data = data.model_dump(exclude_none=True)

    if "assigned_to_id" in update_data:
        agent = db.query(User).filter(User.id == update_data["assigned_to_id"]).first()
        if not agent:
            raise HTTPException(status_code=404, detail="Assignee not found")

    for k, v in update_data.items():
        setattr(ticket, k, v)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.delete("/{ticket_id}", status_code=204)
def delete_ticket(ticket_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if current_user.role not in (UserRole.admin,) and ticket.created_by_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    db.delete(ticket)
    db.commit()


@router.get("/{ticket_id}/comments", response_model=list[CommentOut])
def list_comments(ticket_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket.comments


@router.post("/{ticket_id}/comments", response_model=CommentOut, status_code=201)
def add_comment(
    ticket_id: int,
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    comment = Comment(content=data.content, ticket_id=ticket_id, user_id=current_user.id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment
