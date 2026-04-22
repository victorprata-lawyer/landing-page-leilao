import React, { useState, useEffect } from "react";
import { ReminderCard } from "../components/ReminderCard";
import { StatsPanel } from "../components/StatsPanel";
import { HistoryPanel } from "../components/HistoryPanel";
import { AlarmPanel } from "../components/AlarmPanel";
import { wellnessService } from "../services/wellnessService";
import "../styles/WellnessDashboard.css";

export const WellnessDashboard = () => {
  const [reminders, setReminders] = useState([]);
  const [stats, setStats] = useState(null);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState("");

  // Buscar dados ao carregar
  useEffect(() => {
    loadData();
    // Atualizar a cada 30 segundos
    const interval = setInterval(loadData, 30000);
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [remindersData, statsData, logsData] = await Promise.all([
        wellnessService.getReminders(),
        wellnessService.getStats(),
        wellnessService.getLogs(),
      ]);
      setReminders(remindersData);
      setStats(statsData);
      setLogs(logsData);
      setError(null);
    } catch (err) {
      setError("Erro ao carregar dados. Verifique se o backend está rodando.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleComplete = async (reminderId) => {
    try {
      await wellnessService.logReminder(reminderId);
      setSuccessMessage("✓ Lembrete registrado com sucesso!");
      setTimeout(() => setSuccessMessage(""), 3000);
      loadData(); // Recarregar dados
    } catch (err) {
      setError("Erro ao registrar lembrete.");
      console.error(err);
    }
  };

  return (
    <div className="wellness-dashboard">
      {/* Painel de Alarme */}
      <AlarmPanel reminders={reminders} />

      {/* Header */}
      <header className="dashboard-header">
        <h1>Bem-Estar</h1>
        <p>Cuide de você enquanto cuida dos seus clientes</p>
      </header>

      {/* Mensagens */}
      {error && <div className="alert alert-error">{error}</div>}
      {successMessage && (
        <div className="alert alert-success">{successMessage}</div>
      )}

      {/* Estatísticas */}
      {!loading && stats && <StatsPanel stats={stats} />}

      {/* Lembretes */}
      <div className="reminders-section">
        <h2>Lembretes</h2>
        {loading ? (
          <div className="loading">Carregando lembretes...</div>
        ) : reminders.length > 0 ? (
          <div className="reminders-grid">
            {reminders.map((reminder) => (
              <ReminderCard
                key={reminder.id}
                reminder={reminder}
                onComplete={handleComplete}
              />
            ))}
          </div>
        ) : (
          <div className="empty-state">
            Nenhum lembrete encontrado.
          </div>
        )}
      </div>

      {/* Histórico */}
      {!loading && logs && <HistoryPanel logs={logs} />}

      {/* Botão de Atualizar */}
      {!loading && (
        <button className="refresh-button" onClick={loadData}>
          🔄 Atualizar
        </button>
      )}
    </div>
  );
};