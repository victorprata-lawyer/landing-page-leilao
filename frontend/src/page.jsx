'use client';

import React from 'react';

export default function HomePage() {
  return (
    <div style={{ backgroundColor: '#05070a', minHeight: '100vh', color: '#fff', fontFamily: 'Montserrat, sans-serif' }}>
      
      {/* NAVBAR PROFISSIONAL */}
      <nav style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center', 
        padding: '25px 50px', 
        backgroundColor: 'rgba(5, 7, 10, 0.98)',
        borderBottom: '1px solid rgba(197, 164, 126, 0.2)',
        position: 'sticky',
        top: 0,
        zIndex: 100
      }}>
        <div style={{ fontFamily: 'Playfair Display, serif', fontSize: '1.6rem', color: '#c5a47e', fontWeight: '700', letterSpacing: '1px' }}>
          PRATA REAL ESTATE
        </div>
        
        <a href="/mesa" style={{
          padding: '12px 30px',
          border: '1px solid #c5a47e',
          color: '#c5a47e',
          textDecoration: 'none',
          fontSize: '0.75rem',
          fontWeight: '700',
          textTransform: 'uppercase',
          letterSpacing: '2px',
          transition: '0.3s ease'
        }}
        onMouseOver={(e) => { e.target.style.background = '#c5a47e'; e.target.style.color = '#05070a'; }}
        onMouseOut={(e) => { e.target.style.background = 'transparent'; e.target.style.color = '#c5a47e'; }}
        >
          Mesa de Originação
        </a>
      </nav>

      {/* CONTEÚDO HERO */}
      <main style={{ maxWidth: '1100px', margin: '0 auto', padding: '120px 20px', textAlign: 'center' }}>
        <header style={{ marginBottom: '80px' }}>
          <h1 style={{ fontFamily: 'Playfair Display, serif', fontSize: '4rem', marginBottom: '30px', fontWeight: '500', lineHeight: '1.1' }}>
            Special Situations em <br/> <span style={{ color: '#c5a47e' }}>Real Estate</span>
          </h1>
          <p style={{ color: '#64748b', fontSize: '1.3rem', lineHeight: '1.6', maxWidth: '800px', margin: '0 auto' }}>
            Originação estruturada e inteligência jurídica de alta performance para investidores institucionais, family offices e parceiros estratégicos.
          </p>
        </header>

        {/* DIFERENCIAIS */}
        <section style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '40px', textAlign: 'left', marginTop: '100px' }}>
          <div style={{ padding: '40px', border: '1px solid rgba(197, 164, 126, 0.1)', background: 'rgba(255,255,255,0.01)' }}>
            <h3 style={{ color: '#c5a47e', marginBottom: '20px', fontSize: '1.2rem', textTransform: 'uppercase', letterSpacing: '1px' }}>Originação Proprietária</h3>
            <p style={{ color: '#94a3b8', fontSize: '0.95rem', lineHeight: '1.7' }}>
              Varredura industrial de mais de 30 mil editais anuais. Nossa tecnologia identifica ativos ocultos com alto potencial de arbitragem antes do mercado comum.
            </p>
          </div>
          <div style={{ padding: '40px', border: '1px solid rgba(197, 164, 126, 0.1)', background: 'rgba(255,255,255,0.01)' }}>
            <h3 style={{ color: '#c5a47e', marginBottom: '20px', fontSize: '1.2rem', textTransform: 'uppercase', letterSpacing: '1px' }}>Segurança Jurídica</h3>
            <p style={{ color: '#94a3b8', fontSize: '0.95rem', lineHeight: '1.7' }}>
              Transformamos complexidade em viabilidade. Teses jurídicas robustas focadas em aquisição originária e blindagem patrimonial de ativos distressed.
            </p>
          </div>
        </section>

        <footer style={{ marginTop: '120px', borderTop: '1px solid rgba(255,255,255,0.05)', paddingTop: '50px', color: '#475569', fontSize: '0.8rem', letterSpacing: '1px' }}>
          © {new Date().getFullYear()} PRATA REAL ESTATE | ADVOCACIA HUB. TODOS OS DIREITOS RESERVADOS.
        </footer>
      </main>
    </div>
  );
}