import React from "react";
import "../styles/ReminderCard.css";

export const ReminderCard = ({ reminder, onComplete }) => {
  const getCategoryLabel = (category) => {
    const labels = {
      hydration: "Hidratação",
      nutrition: "Nutrição",
      sunlight: "Luz Natural",
      movement: "Movimento",
      breathing: "Respiração",
      mindfulness: "Meditação",
      eyes: "Saúde Ocular",
      sleep: "Sono",
    };
    return labels[category] || category;
  };

  const getTimeUntilNext = (nextReminder) => {
    const now = new Date();
    const next = new Date(nextReminder);
    const diff = next - now;

    if (diff < 0) return "Vencido";

    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));

    if (hours > 0) return `${hours}h ${minutes}m`;
    return `${minutes}m`;
  };

  return (
    <div className="reminder-card">
      <div className="reminder-content">
        <div className="reminder-category">
          {getCategoryLabel(reminder.category)}
        </div>

        <h3 className="reminder-title">{reminder.title}</h3>

        <p className="reminder-description">{reminder.description}</p>

        <div className="reminder-meta">
          <span className="reminder-frequency">
            A cada {reminder.frequency_hours}h
          </span>
          <span className="reminder-time">
            {getTimeUntilNext(reminder.next_reminder)}
          </span>
        </div>
      </div>

      <button
        className="reminder-button"
        onClick={() => onComplete(reminder.id)}
      >
        Concluído
      </button>
    </div>
  );
};