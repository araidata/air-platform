from datetime import datetime
from typing import Optional

from app.schemas.base import ApiModel, StrictApiModel


class OwnerCreate(StrictApiModel):
    display_name: str
    email: str
    department: str
    role: str


class OwnerRead(ApiModel):
    id: str
    display_name: str
    email: str
    department: str
    role: str
    created_at: datetime
    updated_at: datetime


class OwnerUpdate(StrictApiModel):
    display_name: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    role: Optional[str] = None
