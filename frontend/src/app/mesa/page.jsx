import React, { useState, useEffect, useMemo } from 'react';

export default function MesaPage() {
  const [assets, setAssets] = useState([]);
  const [cityInput, setCityInput] = useState('');
  const [stateFilter, setStateFilter] = useState('');
  const [hideLowValue, setHideLowValue] = useState(true); 
  const [loading, setLoading] = useState(true);

  const [showModal, setShowModal] = useState(false);
  const [selectedAsset, setSelectedAsset] = useState(null);
  const [copied, setCopied] = useState(false);

  const normalize = (str) => {
    if (!str) return '';
    return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').trim().toLowerCase();
  };

  useEffect(() => {
    fetch('/api/oportunidades')
      .then(res => res.json())
      .then(data => {
        setAssets(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const filtered = useMemo(() => {
    if (assets.length === 0) return [];
    return assets.filter(asset => {
      const vgv = asset.estimated_vgv || 0;
      if (vgv <= 0) return false;
      if (hideLowValue && vgv < 300000) return false;
      const matchesState = !stateFilter || (asset.state && asset.state.toUpperCase().trim() === stateFilter.toUpperCase().trim());
      if (!matchesState) return false;
      const matchesCity = !cityInput.trim() || normalize(asset.city).includes(normalize(cityInput));
      return matchesCity;
    });
  }, [assets, cityInput, stateFilter, hideLowValue]);

  const formatCurrency = (val) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(val);
  const uniqueStates = Array.from(new Set(assets.map(asset => asset.state).filter(Boolean))).sort();

  const handleAnalyze = (asset) => {
    setSelectedAsset(asset);
    setCopied(false);
    setShowModal(true);
  };

  const copyToClipboard = () => {
    if (selectedAsset) {
      navigator.clipboard.writeText(selectedAsset.public_code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const goToZapSign = (e) => {
    e.preventDefault();
    const linkNda = "https://app.zapsign.com.br/verificar/doc/18154b67-464f-4cbe-a59f-a9f2549829b6";
    window.open(linkNda, '_blank');
    setShowModal(false);
  };

  return (
    <div style={{ padding: '40px 20px', backgroundColor: '#05070a', minHeight: '100vh', color: '#fff', fontFamily: 'Montserrat, sans-serif' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        
        <div style={{ marginBottom: '30px' }}>
          <a href="/" style={{ color: '#64748b', fontSize: '0.7rem', textDecoration: 'none', textTransform: 'uppercase', letterSpacing: '1px', display: 'flex', alignItems: 'center', gap: '5px' }}>
            ← Voltar para o Site Institucional
          </a>
        </div>

        <header style={{ marginBottom: '40px', borderLeft: '3px solid #c5a47e', paddingLeft: '25px' }}>
          <div style={{ fontSize: '0.75rem', color: '#c5a47e', letterSpacing: '3px', marginBottom: '10px', fontWeight: '600' }}>
            PRATA REAL ESTATE | SPECIAL SITUATIONS
          </div>
          <h2 style={{ fontSize: '2.8rem', margin: '0', fontWeight: '500', fontFamily: 'Playfair Display, serif' }}>
            Mesa de Originação
          </h2>
          <div style={{ color: '#64748b', fontSize: '0.8rem', marginTop: '10px' }}>
            Exibindo **{filtered.length}** ativos estruturados sob sigilo profissional.
          </div>
        </header>

        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '15px', marginBottom: '50px', padding: '20px', background: 'rgba(255, 255, 255, 0.02)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '2px', alignItems: 'center' }}>
          <input
            type="text" placeholder="Buscar por cidade..." value={cityInput}
            onChange={(e) => setCityInput(e.target.value)}
            style={{ flex: '2 1 250px', padding: '12px 15px', background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)', color: '#fff', outline: 'none' }}
          />
          <select
            value={stateFilter}
            onChange={(e) => setStateFilter(e.target.value)}
            style={{ flex: '1 1 120px', padding: '12px 15px', background: '#05070a', border: '1px solid rgba(255,255,255,0.1)', color: '#fff', cursor: 'pointer' }}
          >
            <option value="">Todos os Estados</option>
            {uniqueStates.map(uf => <option key={uf} value={uf}>{uf}</option>)}
          </select>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', padding: '0 15px', borderLeft: '1px solid rgba(255,255,255,0.1)' }}>
            <input type="checkbox" id="qualityFilter" checked={hideLowValue} onChange={(e) => setHideLowValue(e.target.checked)} style={{ cursor: 'pointer', accentColor: '#c5a47e' }} />
            <label htmlFor="qualityFilter" style={{ color: '#c5a47e', fontSize: '0.7rem', fontWeight: '700', cursor: 'pointer', textTransform: 'uppercase' }}>Filtro Qualificado (+300k)</label>
          </div>
        </div>

        {loading ? (
          <div style={{ color: '#c5a47e', textAlign: 'center', padding: '100px', letterSpacing: '2px' }}>SINCRONIZANDO BASE DE ATIVOS...</div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))', gap: '30px' }}>
            {filtered.slice(0, 40).map(asset => {
              const vgv = asset.estimated_vgv || 0;
              const lance = asset.min_bid || 0;
              const arbitragem = asset.discount_percentage || (vgv > 0 ? Math.round(((vgv - lance) / vgv) * 100) : 0);

              return (
                <div key={asset.public_code} style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.08)', padding: '40px', borderRadius: '2px', display: 'flex', flexDirection: 'column', position: 'relative' }}>
                  <div style={{ position: 'absolute', top: '20px', right: '20px', color: '#c5a47e', fontSize: '0.6rem', fontWeight: '800', border: '1px solid #c5a47e', padding: '3px 8px' }}>
                    {arbitragem}% ARBITRAGEM
                  </div>
                  <div style={{ color: '#64748b', fontSize: '0.7rem', fontWeight: '600', marginBottom: '8px' }}>{asset.public_code}</div>
                  <h3 style={{ fontSize: '1.5rem', margin: '0 0 5px 0', color: '#fff', fontFamily: 'Playfair Display, serif' }}>{asset.city.toUpperCase()} / {asset.state}</h3>
                  <p style={{ color: '#94a3b8', fontSize: '0.75rem', marginBottom: '25px', textTransform: 'uppercase' }}>{asset.typology}</p>
                  <div style={{ borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '20px', marginBottom: '30px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '15px' }}>
                      <span style={{ color: '#64748b', fontSize: '0.65rem', fontWeight: '700', textTransform: 'uppercase' }}>Avaliação de Mercado</span>
                      <span style={{ color: '#fff', fontWeight: '600' }}>{formatCurrency(vgv)}</span>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <span style={{ color: '#c5a47e', fontSize: '0.65rem', fontWeight: '800', textTransform: 'uppercase' }}>Lance Mínimo Estimado</span>
                      <span style={{ color: '#c5a47e', fontWeight: '700' }}>{formatCurrency(lance)}</span>
                    </div>
                  </div>
                  <button onClick={() => handleAnalyze(asset)} style={{ marginTop: 'auto', width: '100%', padding: '14px', background: 'transparent', border: '1px solid #c5a47e', color: '#c5a47e', fontWeight: '700', cursor: 'pointer', textTransform: 'uppercase', fontSize: '0.65rem', letterSpacing: '1px' }}>
                    Analisar Viabilidade
                  </button>
                </div>
              );
            })}
          </div>
        )}

        {showModal && (
          <div style={{ position: 'fixed', top: 0, left: 0, width: '100%', height: '100%', background: 'rgba(0,0,0,0.92)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
            <div style={{ background: '#0a0d12', padding: '40px', border: '1px solid #c5a47e', maxWidth: '500px', width: '90%', textAlign: 'center' }}>
              <h3 style={{ fontSize: '1.8rem', marginBottom: '15px', color: '#fff', fontFamily: 'Playfair Display' }}>Protocolo de Acesso</h3>
              <p style={{ color: '#94a3b8', fontSize: '0.85rem', marginBottom: '20px', textAlign: 'justify', lineHeight: '1.6' }}>
                Para garantir a <strong>exclusividade da tese jurídica</strong> e a proteção das partes, o acesso ao Data Room requer a assinatura de um NDA. Este protocolo assegura que o ativo permaneça restrito a investidores qualificados.
              </p>
              <div style={{ display: 'flex', gap: '10px', marginBottom: '30px', background: 'rgba(255,255,255,0.05)', padding: '10px', border: '1px solid rgba(255,255,255,0.1)' }}>
                <div style={{ flex: 1, color: '#fff', fontWeight: '700', textAlign: 'left', paddingLeft: '10px' }}>{selectedAsset?.public_code}</div>
                <button onClick={copyToClipboard} style={{ background: copied ? '#27ae60' : '#c5a47e', color: '#05070a', border: 'none', padding: '8px 15px', fontWeight: '700', cursor: 'pointer', fontSize: '0.7rem' }}>
                  {copied ? 'Copiado!' : 'Copiar'}
                </button>
              </div>
              <form onSubmit={goToZapSign}>
                <button type="submit" style={{ width: '100%', padding: '16px', background: '#c5a47e', color: '#05070a', border: 'none', fontWeight: '700', cursor: 'pointer', textTransform: 'uppercase', letterSpacing: '1px' }}>
                  Assinar NDA e Acessar Dados
                </button>
                <button onClick={() => setShowModal(false)} style={{ width: '100%', marginTop: '15px', background: 'transparent', color: '#64748b', border: 'none', cursor: 'pointer', fontSize: '0.75rem', textTransform: 'uppercase' }}>
                  Voltar para a Mesa
                </button>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}