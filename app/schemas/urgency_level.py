from pydantic import BaseModel

class UrgencyLevelResponse(BaseModel):
    id: str
    name: str
    sla_hours: int
    is_active: bool

    class Config:
        from_attributes = True
