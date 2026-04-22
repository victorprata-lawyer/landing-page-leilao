from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float
from datetime import datetime
from app.database import Base

class WellnessReminder(Base):
    __tablename__ = "wellness_reminders"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    title = Column(String)
    description = Column(Text)
    frequency_hours = Column(Integer)
    last_reminder = Column(DateTime, default=datetime.utcnow)
    next_reminder = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # NOVOS CAMPOS PARA METAS INTELIGENTES
    daily_goal = Column(Integer, default=1)  # Meta diária (8 copos, 4 refeições, etc)
    unit = Column(String, default="vezes")  # copos, refeições, minutos, vezes, noites
    weight = Column(Float, default=12.5)  # Sempre 12.5% (8 atividades = 100%)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class WellnessLog(Base):
    __tablename__ = "wellness_logs"

    id = Column(Integer, primary_key=True, index=True)
    reminder_id = Column(Integer, index=True)
    category = Column(String)
    title = Column(String)
    completed_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class WellnessStats(Base):
    __tablename__ = "wellness_stats"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, unique=True, index=True)
    total_completed = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    last_completed = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)