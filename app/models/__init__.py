# Models package - Import all models to register with SQLAlchemy Base
from app.models.client import Client
from app.models.urgency_level import UrgencyLevel
from app.models.service_type import ServiceType
from app.models.waste_type import WasteType
from app.models.access_difficulty import AccessDifficulty
from app.models.job import Job
from app.models.invoice import Invoice

__all__ = ["Client", "UrgencyLevel", "ServiceType", "WasteType", "AccessDifficulty", "Job", "Invoice"]
