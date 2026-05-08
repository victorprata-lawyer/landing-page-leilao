from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

# --- MESA DE ORIGINAÇÃO (Prata Real Estate) ---
class Asset(Base):
    __tablename__ = 'assets'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    internal_code = Column(String, nullable=False)
    public_code = Column(String, nullable=False)
    process_number = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    typology = Column(String, nullable=False)
    estimated_vgv = Column(Float, nullable=False)
    leilao_percent = Column(Float, nullable=False)
    is_public = Column(Boolean, default=True)
    metragem = Column(Float, default=0.0)
    
    @hybrid_property
    def minimum_bid(self):
        return self.estimated_vgv * (self.leilao_percent / 100)

# --- SISTEMA DE GESTÃO (Wellness/Advocacia Hub) ---
class WellnessReminder(Base):
    __tablename__ = "wellness_reminders"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    title = Column(String)
    description = Column(String)
    frequency_hours = Column(Integer)
    next_reminder = Column(DateTime)
    is_active = Column(Boolean, default=True)
    daily_goal = Column(Integer)
    unit = Column(String)
    weight = Column(Float)

class WellnessLog(Base):
    __tablename__ = "wellness_logs"
    id = Column(Integer, primary_key=True, index=True)
    reminder_id = Column(Integer)
    category = Column(String)
    title = Column(String)
    completed_at = Column(DateTime, default=datetime.utcnow)

class WellnessStats(Base):
    __tablename__ = "wellness_stats"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    total_completed = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    last_completed = Column(DateTime)