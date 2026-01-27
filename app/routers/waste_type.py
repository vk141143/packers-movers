from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.waste_type import WasteType

router = APIRouter()

@router.get("/waste-types", tags=["Waste Types"])
def get_waste_types(db: Session = Depends(get_db)):
    waste_types = db.query(WasteType).filter(WasteType.is_active == True).all()
    return waste_types

@router.get("/waste-types/{waste_type_id}", tags=["Waste Types"])
def get_waste_type_by_id(waste_type_id: int, db: Session = Depends(get_db)):
    waste_type = db.query(WasteType).filter(WasteType.id == waste_type_id).first()
    if not waste_type:
        raise HTTPException(status_code=404, detail="Waste type not found")
    return waste_type
