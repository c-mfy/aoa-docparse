from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
import datetime

from app.database import get_db
from app.models.work_order import WorkOrder
from app.permissions import CurrentUser, get_current_user, require

router = APIRouter()

class WorkOrderResponse(BaseModel):
    id: int
    parish_id: int
    display_number: str
    building_id: Optional[int]

    title: str
    description: Optional[str]
    priority: str
    due_date: Optional[datetime.date]

    status: str
    status_before_hold: Optional[str]

    requester_sub: str
    requester_name: Optional[str]
    technician_sub: Optional[str]
    technician_name: Optional[str]

    completion_notes: Optional[str]

    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    started_at: Optional[datetime.datetime]
    closed_at: Optional[datetime.datetime]

    class Config:
        from_attributes = True


@router.get("/{parish_id}/work-orders", response_model=List[WorkOrderResponse])
def list_work_orders(
    parish_id: int,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    # anyone logged in can view; no require() call here
    return (
        db.query(WorkOrder)
        .filter(WorkOrder.parish_id == parish_id)
        .order_by(WorkOrder.created_at.desc())
        .all()
    )