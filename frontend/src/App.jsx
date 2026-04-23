import React from "react";
import { Routes, Route, Link, useLocation } from "react-router-dom";
import { WellnessDashboard } from "./pages/WellnessDashboard";
import AssetShowcase from "./AssetShowcase";
import "./App.css";

function App() {
  const location = useLocation();

  return (
    <div className="App">
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
          <Link to="/">
            <button style={{
              padding: '8px 16px',
              borderRadius: '4px',
              border: 'none',
              cursor: 'pointer',
              backgroundColor: location.pathname === "/" ? '#2563eb' : 'transparent',
              color: 'white',
              fontWeight: 'bold'
            }}>
              🌿 Gestão Wellness
            </button>
          </Link>
          
          <Link to="/mesa">
            <button style={{
              padding: '8px 16px',
              borderRadius: '4px',
              border: 'none',
              cursor: 'pointer',
              backgroundColor: location.pathname === "/mesa" ? '#2563eb' : 'transparent',
              color: 'white',
              fontWeight: 'bold'
            }}>
              💎 Mesa de Originação
            </button>
          </Link>
        </div>
      </nav>

      <div className="content-area">
        <Routes>
          <Route path="/" element={<WellnessDashboard />} />
          <Route path="/mesa" element={
            <div className="tailwind-scope">
              <AssetShowcase />
            </div>
          } />
        </Routes>
      </div>
    </div>
  );
}

export default App;