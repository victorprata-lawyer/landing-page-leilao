from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WellnessReminderCreate(BaseModel):
    category: str
    title: str
    description: str
    frequency_hours: int
    is_active: bool = True

class WellnessReminderUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    frequency_hours: Optional[int] = None
    is_active: Optional[bool] = None

class WellnessReminderResponse(BaseModel):
    id: int
    category: str
    title: str
    description: str
    frequency_hours: int
    last_reminder: datetime
    next_reminder: datetime
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class WellnessLogCreate(BaseModel):
    reminder_id: int
    notes: Optional[str] = None

class WellnessLogResponse(BaseModel):
    id: int
    reminder_id: int
    category: str
    title: str
    completed_at: datetime
    notes: Optional[str]

    class Config:
        from_attributes = True

class WellnessStatsResponse(BaseModel):
    category: str
    total_completed: int
    current_streak: int
    last_completed: Optional[datetime]

    class Config:
        from_attributes = True