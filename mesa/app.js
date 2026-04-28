document.addEventListener('DOMContentLoaded', function() {
  const grid = document.getElementById('grid');
  const loading = document.getElementById('loading');
  const empty = document.getElementById('empty');
  const modal = document.getElementById('modal');
  const overlay = document.getElementById('overlay');
  const modalCode = document.getElementById('modalCode');
  const copyCodeBtn = document.getElementById('copyCode');
  const zapsignBtn = document.getElementById('zapsign');
  const closeModalBtn = document.getElementById('closeModal');
  const estadoFilter = document.getElementById('estadoFilter');
  const cidadeFilter = document.getElementById('cidadeFilter');
  const hideLowValue = document.getElementById('hideLowValue');
  const clearFilters = document.getElementById('clearFilters');
  const resultsCounter = document.getElementById('resultsCounter'); // Novo elemento

  let oportunidades = [];
  let filteredOportunidades = [];

  function normalizeCity(city) {
    return city
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase()
      .replace(/[^\w\s]/g, '');
  }

  async function carregarOportunidades() {
    try {
      const response = await fetch('/api/oportunidades');
      oportunidades = await response.json();

      oportunidades.forEach(item => {
        if (!item.discount_percentage) {
          item.discount_percentage = Math.round((1 - item.min_bid / item.estimated_vgv) * 100);
        }
        item.normCity = normalizeCity(item.city);
      });

      oportunidades.sort((a, b) => b.discount_percentage - a.discount_percentage);

      atualizarFiltros();
      filtrarEExibir();
      loading.style.display = 'none';
    } catch (error) {
      console.error('Erro ao carregar:', error);
      loading.textContent = 'Erro ao carregar oportunidades.';
    }
  }

  function atualizarFiltros() {
    const estadosUnicos = [...new Set(oportunidades.map(o => o.state))].sort();
    estadoFilter.innerHTML = '<option value="">Todos os Estados</option>';
    estadosUnicos.forEach(estado => {
      const option = document.createElement('option');
      option.value = estado;
      option.textContent = estado;
      estadoFilter.appendChild(option);
    });
    atualizarCidades();
  }

  function atualizarCidades(estadoSelecionado = '') {
    const cidadesNorm = [...new Set(
      oportunidades
        .filter(o => !estadoSelecionado || o.state === estadoSelecionado)
        .map(o => o.normCity)
    )].sort();

    cidadeFilter.innerHTML = '<option value="">Todas as Cidades</option>';
    cidadesNorm.forEach(normCity => {
      const match = oportunidades.find(o => o.normCity === normCity);
      if (match) {
        const option = document.createElement('option');
        option.value = normCity;
        option.textContent = match.city;
        cidadeFilter.appendChild(option);
      }
    });
  }

  function filtrarEExibir() {
    const estado = estadoFilter.value;
    const cidadeNorm = cidadeFilter.value;
    const hideLow = hideLowValue.checked;

    // Filtra a lista completa
    const fullFilteredList = oportunidades.filter(item => {
      if (estado && item.state !== estado) return false;
      if (cidadeNorm && item.normCity !== cidadeNorm) return false;
      if (hideLow && item.estimated_vgv < 300000) return false;
      return true;
    });

    // Atualiza o contador com o poder da mesa (X de Y)
    if (resultsCounter) {
      const exibidos = fullFilteredList.length;
      const total = oportunidades.length;
      resultsCounter.textContent = `Exibindo ${exibidos} de ${total} teses estruturadas`;
    }

    // Limita a exibição no grid para performance (opcional, mantido conforme seu original)
    filteredOportunidades = fullFilteredList.slice(0, 40);

    exibirGrid();

    if (fullFilteredList.length === 0) {
      empty.style.display = 'block';
      grid.style.display = 'none';
    } else {
      empty.style.display = 'none';
      grid.style.display = 'grid';
    }
  }

  function exibirGrid() {
    grid.innerHTML = '';
    filteredOportunidades.forEach(item => {
      const card = document.createElement('div');
      card.className = 'card';
      card.innerHTML = `
        <h3>${item.public_code}</h3>
        <p><strong>${item.typology}</strong></p>
        <p>${item.city} - ${item.state}</p>
        <p><strong>VGV Estimado:</strong> R$ ${Math.round(item.estimated_vgv).toLocaleString('pt-BR')}</p>
        <p><strong>Lance Mínimo:</strong> R$ ${Math.round(item.min_bid).toLocaleString('pt-BR')}</p>
        <div class="arbitragem">Arbitragem: ${item.discount_percentage}%</div>
      `;
      card.addEventListener('click', () => abrirModal(item));
      grid.appendChild(card);
    });
  }

  function abrirModal(item) {
    modalCode.textContent = item.public_code;
    overlay.style.display = 'block';
    modal.style.display = 'block';
  }

  function fecharModal() {
    modal.style.display = 'none';
    overlay.style.display = 'none';
  }

  copyCodeBtn.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(modalCode.textContent);
      const originalText = copyCodeBtn.textContent;
      copyCodeBtn.textContent = 'Copiado!';
      setTimeout(() => {
        copyCodeBtn.textContent = originalText;
      }, 2000);
    } catch (err) {
      console.error('Erro ao copiar:', err);
    }
  });

  zapsignBtn.addEventListener('click', () => {
    window.open('https://app.zapsign.com.br/verificar/doc/18154b67-464f-4cbe-a59f-a9f2549829b6', '_blank');
  });

  closeModalBtn.addEventListener('click', fecharModal);
  overlay.addEventListener('click', fecharModal);

  estadoFilter.addEventListener('change', () => {
    atualizarCidades(estadoFilter.value);
    filtrarEExibir();
  });

  cidadeFilter.addEventListener('change', filtrarEExibir);
  hideLowValue.addEventListener('change', filtrarEExibir);

  clearFilters.addEventListener('click', () => {
    estadoFilter.value = '';
    cidadeFilter.value = '';
    hideLowValue.checked = false;
    atualizarCidades();
    filtrarEExibir();
  });

  carregarOportunidades();
}); 