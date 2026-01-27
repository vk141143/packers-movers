from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.service_type import ServiceType

router = APIRouter()

@router.get("/service-types", tags=["Service Types"])
def get_service_types(db: Session = Depends(get_db)):
    service_types = db.query(ServiceType).filter(ServiceType.is_active == True).all()
    return service_types

@router.get("/service-types/{service_type_id}", tags=["Service Types"])
def get_service_type_by_id(service_type_id: int, db: Session = Depends(get_db)):
    service_type = db.query(ServiceType).filter(ServiceType.id == service_type_id).first()
    if not service_type:
        raise HTTPException(status_code=404, detail="Service type not found")
    return service_type
