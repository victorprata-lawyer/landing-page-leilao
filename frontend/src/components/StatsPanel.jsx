import React from "react";
import "../styles/StatsPanel.css";

export const StatsPanel = ({ stats }) => {
  if (!stats) return null;

  return (
    <div className="stats-panel">
      <h2>Suas Estatísticas</h2>
      
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-label">Hoje</div>
          <div className="stat-value">{stats.today || 0}</div>
          <div className="stat-unit">concluídos</div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Esta Semana</div>
          <div className="stat-value">{stats.week || 0}</div>
          <div className="stat-unit">concluídos</div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Taxa de Conclusão</div>
          <div className="stat-value">{stats.completion_rate || 0}%</div>
          <div className="stat-unit">hoje</div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Sequência</div>
          <div className="stat-value">{stats.streak || 0}</div>
          <div className="stat-unit">dias</div>
        </div>
      </div>
    </div>
  );
};