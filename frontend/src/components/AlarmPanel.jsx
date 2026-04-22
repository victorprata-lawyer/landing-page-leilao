import React, { useState, useEffect } from "react";
import "../styles/AlarmPanel.css";

export const AlarmPanel = ({ reminders }) => {
  const [nextReminder, setNextReminder] = useState(null);
  const [timeUntil, setTimeUntil] = useState("");

  useEffect(() => {
    const updateNextReminder = () => {
      if (!reminders || reminders.length === 0) return;

      const now = new Date();
      const upcoming = reminders
        .map((r) => ({
          ...r,
          nextTime: new Date(r.next_reminder),
        }))
        .filter((r) => r.nextTime > now)
        .sort((a, b) => a.nextTime - b.nextTime)[0];

      if (upcoming) {
        setNextReminder(upcoming);
        
        // Calcular tempo até o próximo lembrete
        const diff = upcoming.nextTime - now;
        const hours = Math.floor(diff / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        
        setTimeUntil(`${hours}h ${minutes}m`);
      }
    };

    updateNextReminder();
    const interval = setInterval(updateNextReminder, 60000); // Atualizar a cada minuto
    return () => clearInterval(interval);
  }, [reminders]);

  if (!nextReminder) return null;

  return (
    <div className="alarm-panel">
      <div className="alarm-content">
        <span className="alarm-icon">🚨</span>
        <div className="alarm-text">
          <h3>{nextReminder.title}</h3>
          <p>Em {timeUntil}</p>
        </div>
      </div>
    </div>
  );
};