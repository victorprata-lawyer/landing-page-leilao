const API_URL = "http://localhost:8000/api/wellness";

export const wellnessService = {
  // Buscar todos os lembretes
  getReminders: async () => {
    const response = await fetch(`${API_URL}/reminders`);
    return response.json();
  },

  // Registrar conclusão de um lembrete
  logReminder: async (reminderId) => {
    const response = await fetch(`${API_URL}/log`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ reminder_id: reminderId }),
    });
    return response.json();
  },

  // Buscar estatísticas
  getStats: async () => {
    const response = await fetch(`${API_URL}/stats`);
    return response.json();
  },

  // Buscar histórico de logs
  getLogs: async () => {
    const response = await fetch(`${API_URL}/logs`);
    return response.json();
  },
};