from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.urgency_level import UrgencyLevel
from app.schemas.urgency_level import UrgencyLevelResponse
from typing import List

router = APIRouter()

@router.get("/urgency-levels", response_model=List[UrgencyLevelResponse], tags=["Urgency Levels"])
async def get_urgency_levels(db: Session = Depends(get_db)):
    urgency_levels = db.query(UrgencyLevel).filter(UrgencyLevel.is_active == True).all()
    return [UrgencyLevelResponse(
        id=str(ul.id),
        name=ul.name,
        sla_hours=ul.sla_hours,
        is_active=ul.is_active
    ) for ul in urgency_levels]
