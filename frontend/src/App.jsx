import React, { useState } from "react";
import { WellnessDashboard } from "./pages/WellnessDashboard";
import AssetShowcase from "./AssetShowcase";
import "./App.css";

function App() {
  const [activeTab, setActiveTab] = useState("wellness");

  return (
    <div className="App">
      {/* Menu de Navegação - Estilizado manualmente para não conflitar */}
      <nav style={{ 
        backgroundColor: '#0f172a', 
        padding: '1rem', 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        color: 'white',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
      }}>
        <span style={{ fontWeight: 'bold', fontSize: '1.2rem' }}>ADVOCACIA HUB</span>
        
        <div style={{ display: 'flex', gap: '10px' }}>
          <button
            onClick={() => setActiveTab("wellness")}
            style={{
              padding: '8px 16px',
              borderRadius: '4px',
              border: 'none',
              cursor: 'pointer',
              backgroundColor: activeTab === "wellness" ? '#2563eb' : 'transparent',
              color: 'white',
              fontWeight: 'bold'
            }}
          >
            🌿 Gestão Wellness
          </button>
          
          <button
            onClick={() => setActiveTab("assets")}
            style={{
              padding: '8px 16px',
              borderRadius: '4px',
              border: 'none',
              cursor: 'pointer',
              backgroundColor: activeTab === "assets" ? '#2563eb' : 'transparent',
              color: 'white',
              fontWeight: 'bold'
            }}
          >
            💎 Mesa de Originação
          </button>
        </div>
      </nav>

      {/* Área de Conteúdo Dinâmico */}
      <div className="content-area">
        {activeTab === "wellness" ? (
          /* Seu Wellness original sem interferência do Tailwind */
          <WellnessDashboard />
        ) : (
          /* Mesa de Originação usando Tailwind de forma isolada */
          <div className="tailwind-scope">
            <AssetShowcase />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;