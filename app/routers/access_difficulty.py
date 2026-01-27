from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.access_difficulty import AccessDifficulty

router = APIRouter()

@router.get("/access-difficulties", tags=["Access Difficulty"])
def get_access_difficulties(db: Session = Depends(get_db)):
    access_difficulties = db.query(AccessDifficulty).filter(AccessDifficulty.is_active == True).all()
    return access_difficulties

@router.get("/access-difficulties/{access_difficulty_id}", tags=["Access Difficulty"])
def get_access_difficulty_by_id(access_difficulty_id: int, db: Session = Depends(get_db)):
    access_difficulty = db.query(AccessDifficulty).filter(AccessDifficulty.id == access_difficulty_id).first()
    if not access_difficulty:
        raise HTTPException(status_code=404, detail="Access difficulty not found")
    return access_difficulty
