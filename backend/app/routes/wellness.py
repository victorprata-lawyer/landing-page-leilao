from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.database import get_db
from pydantic import BaseModel

# AJUSTE DE IMPORTAÇÃO: Apontando para o local exato dos modelos
from app.models.models import WellnessReminder, WellnessLog, WellnessStats

from app.wellness_schemas import (
    WellnessReminderCreate,
    WellnessReminderUpdate,
    WellnessReminderResponse,
    WellnessLogCreate,
    WellnessLogResponse,
    WellnessStatsResponse
)

class LogWellnessRequest(BaseModel):
    reminder_id: int

router = APIRouter(prefix="/api/wellness", tags=["wellness"])

# ===== GET REMINDERS =====
@router.get("/reminders")
def get_wellness_reminders(db: Session = Depends(get_db)):
    """Retorna todos os lembretes de bem-estar ativos"""
    reminders = db.query(WellnessReminder).filter(WellnessReminder.is_active == True).all()
    return reminders

@router.get("/reminders/{reminder_id}")
def get_wellness_reminder(reminder_id: int, db: Session = Depends(get_db)):
    """Retorna um lembrete específico"""
    reminder = db.query(WellnessReminder).filter(WellnessReminder.id == reminder_id).first()
    if not reminder:
        raise HTTPException(status_code=404, detail="Lembrete não encontrado")
    return reminder

# ===== CREATE REMINDER =====
@router.post("/reminders")
def create_wellness_reminder(reminder: WellnessReminderCreate, db: Session = Depends(get_db)):
    """Cria um novo lembrete de bem-estar"""
    next_reminder = datetime.utcnow() + timedelta(hours=reminder.frequency_hours)
    
    db_reminder = WellnessReminder(
        category=reminder.category,
        title=reminder.title,
        description=reminder.description,
        frequency_hours=reminder.frequency_hours,
        next_reminder=next_reminder,
        is_active=reminder.is_active
    )
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder

# ===== UPDATE REMINDER =====
@router.put("/reminders/{reminder_id}")
def update_wellness_reminder(reminder_id: int, reminder: WellnessReminderUpdate, db: Session = Depends(get_db)):
    """Atualiza um lembrete de bem-estar"""
    db_reminder = db.query(WellnessReminder).filter(WellnessReminder.id == reminder_id).first()
    if not db_reminder:
        raise HTTPException(status_code=404, detail="Lembrete não encontrado")
    
    if reminder.title:
        db_reminder.title = reminder.title
    if reminder.description:
        db_reminder.description = reminder.description
    if reminder.frequency_hours:
        db_reminder.frequency_hours = reminder.frequency_hours
    if reminder.is_active is not None:
        db_reminder.is_active = reminder.is_active
    
    db.commit()
    db.refresh(db_reminder)
    return db_reminder

# ===== LOG COMPLETION =====
@router.post("/log")
def log_wellness_completion(request: LogWellnessRequest, db: Session = Depends(get_db)):
    try:
        reminder = db.query(WellnessReminder).filter(WellnessReminder.id == request.reminder_id).first()
        if not reminder:
            raise HTTPException(status_code=404, detail="Lembrete não encontrado")
        
        log_entry = WellnessLog(
            reminder_id=request.reminder_id,
            category=reminder.category,
            title=reminder.title,
            completed_at=datetime.utcnow()
        )
        db.add(log_entry)
        db.commit()
        
        stats = db.query(WellnessStats).filter(WellnessStats.category == reminder.category).first()
        if not stats:
            stats = WellnessStats(
                category=reminder.category,
                total_completed=1,
                current_streak=1,
                last_completed=datetime.utcnow()
            )
            db.add(stats)
        else:
            stats.total_completed = (stats.total_completed or 0) + 1
            stats.last_completed = datetime.utcnow()
        
        db.commit()
        
        return {"message": "Lembrete registrado com sucesso", "log_id": log_entry.id}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# ===== GET STATS =====
@router.get("/stats")
def get_wellness_stats(db: Session = Depends(get_db)):
    """Retorna estatísticas de bem-estar com cálculo inteligente de metas"""
    today = datetime.utcnow().date()
    reminders = db.query(WellnessReminder).filter(WellnessReminder.is_active == True).all()
    
    total_completion_percentage = 0.0
    today_logs_count = 0
    week_logs_count = 0
    
    for reminder in reminders:
        today_logs = db.query(WellnessLog).filter(
            WellnessLog.reminder_id == reminder.id,
            WellnessLog.completed_at >= datetime.combine(today, datetime.min.time())
        ).count()
        
        week_ago = datetime.utcnow() - timedelta(days=7)
        week_logs = db.query(WellnessLog).filter(
            WellnessLog.reminder_id == reminder.id,
            WellnessLog.completed_at >= week_ago
        ).count()
        
        today_logs_count += today_logs
        week_logs_count += week_logs
        
        daily_goal = reminder.daily_goal or 1
        weight = reminder.weight or 12.5
        
        if daily_goal > 0:
            activity_completion = min((today_logs / daily_goal) * weight, weight)
            total_completion_percentage += activity_completion
    
    completion_rate = min(int(total_completion_percentage), 100)
    
    # Cálculo de streak simplificado
    streak = 0
    current_date = datetime.utcnow().date()
    while True:
        logs_on_date = db.query(WellnessLog).filter(
            WellnessLog.completed_at >= datetime.combine(current_date, datetime.min.time()),
            WellnessLog.completed_at < datetime.combine(current_date + timedelta(days=1), datetime.min.time())
        ).count()
        if logs_on_date > 0:
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break
    
    return {
        "today": today_logs_count,
        "week": week_logs_count,
        "completion_rate": completion_rate,
        "streak": streak
    }

# ===== GET LOGS =====
@router.get("/logs")
def get_wellness_logs(days: int = 7, db: Session = Depends(get_db)):
    """Retorna logs dos últimos N dias"""
    since = datetime.utcnow() - timedelta(days=days)
    logs = db.query(WellnessLog).filter(WellnessLog.completed_at >= since).order_by(WellnessLog.completed_at.desc()).all()
    
    result = []
    for log in logs:
        result.append({
            "id": log.id,
            "reminder_id": log.reminder_id,
            "title": log.title,
            "category": log.category,
            "logged_at": log.completed_at.isoformat() if log.completed_at else None
        })
    return result

# ===== INITIALIZE REMINDERS =====
@router.post("/init")
def initialize_wellness_reminders(db: Session = Depends(get_db)):
    """Inicializa lembretes padrão de bem-estar"""
    reminders_data = [
        {"category": "hydration", "title": "💧 Beber água", "description": "200ml de água.", "frequency_hours": 1, "daily_goal": 13, "unit": "copos", "weight": 12.5},
        {"category": "nutrition", "title": "🍽️ Se alimentar", "description": "Pausa para refeição.", "frequency_hours": 4, "daily_goal": 4, "unit": "refeições", "weight": 12.5},
        {"category": "sunlight", "title": "☀️ Tomar sol", "description": "Luz natural.", "frequency_hours": 24, "daily_goal": 1, "unit": "vezes", "weight": 12.5},
        {"category": "movement", "title": "🚶 Caminhar", "description": "30 minutos de movimento.", "frequency_hours": 24, "daily_goal": 30, "unit": "minutos", "weight": 12.5},
        {"category": "breathing", "title": "🫁 Respirar", "description": "Respire fundo.", "frequency_hours": 8, "daily_goal": 3, "unit": "vezes", "weight": 12.5},
        {"category": "mindfulness", "title": "🧘 Meditação", "description": "Pausa mental.", "frequency_hours": 8, "daily_goal": 3, "unit": "sessões", "weight": 12.5},
        {"category": "eyes", "title": "👁️ Descanso de tela", "description": "Olhe para longe.", "frequency_hours": 1, "daily_goal": 12, "unit": "vezes", "weight": 12.5},
        {"category": "sleep", "title": "😴 Hora de dormir", "description": "Período de sono.", "frequency_hours": 8, "daily_goal": 3, "unit": "períodos", "weight": 12.5},
    ]
    
    for data in reminders_data:
        existing = db.query(WellnessReminder).filter(WellnessReminder.category == data["category"]).first()
        if not existing:
            next_reminder = datetime.utcnow() + timedelta(hours=data["frequency_hours"])
            reminder = WellnessReminder(
                category=data["category"], title=data["title"], description=data["description"],
                frequency_hours=data["frequency_hours"], next_reminder=next_reminder,
                is_active=True, daily_goal=data["daily_goal"], unit=data["unit"], weight=data["weight"]
            )
            db.add(reminder)
    
    db.commit()
    return {"message": "Lembretes de bem-estar inicializados com sucesso!"}