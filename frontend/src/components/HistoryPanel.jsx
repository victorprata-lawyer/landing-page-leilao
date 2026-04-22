import React from "react";
import "../styles/HistoryPanel.css";

export const HistoryPanel = ({ logs }) => {
  if (!logs || logs.length === 0) {
    return (
      <div className="history-panel">
        <h2>Histórico</h2>
        <div className="empty-history">Nenhum registro ainda</div>
      </div>
    );
  }

  const formatDate = (dateString) => {
    try {
      // Se for string ISO, converter para Date
      let date = new Date(dateString);
      
      // Se a data for inválida, tentar parse manual
      if (isNaN(date.getTime())) {
        // Tenta formato: "2026-04-16T10:30:00"
        const parts = dateString.split('T');
        if (parts.length === 2) {
          date = new Date(dateString);
        }
      }
      
      // Se ainda for inválida, retornar a string original
      if (isNaN(date.getTime())) {
        return dateString;
      }
      
      return date.toLocaleDateString("pt-BR", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch (e) {
      return dateString;
    }
  };

  const getReminderLabel = (reminderId) => {
    const labels = {
      1: "Hidratação",
      2: "Nutrição",
      3: "Luz Natural",
      4: "Movimento",
      5: "Respiração",
      6: "Meditação",
      7: "Saúde Ocular",
      8: "Sono",
    };
    return labels[reminderId] || `Lembrete ${reminderId}`;
  };

  return (
    <div className="history-panel">
      <h2>Histórico de Conclusões</h2>
      
      <div className="history-list">
        {logs.slice(0, 10).map((log, index) => (
          <div key={index} className="history-item">
            <div className="history-time">{formatDate(log.logged_at)}</div>
            <div className="history-reminder">
              {getReminderLabel(log.reminder_id)}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};