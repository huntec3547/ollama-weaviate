# ============================================================================
# Pydantic Models
# ============================================================================

from pydantic import BaseModel
from typing import Dict
from enum import Enum
from datetime import datetime

class RagRequest(BaseModel):
    question: str
    context: str

class RagResponse(BaseModel):
    question: str
    context: str
    answer: str

class HealthStatus(BaseModel):
    status: str
    timestamp: datetime
    version: str
    external_services: Dict[str, str]

class ServiceStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    ERROR = "error"    