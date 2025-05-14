document.addEventListener('DOMContentLoaded', () => {
  /* seção sidebar */
  const sidebarMenu = document.querySelector('.sidebar');
  const sidebarTop = document.querySelector('.sidebar-top');
  const hamburgerBtn = document.getElementById('sidebar-hamburger');

  function fecharSidebarMenu() {
    sidebarMenu.classList.remove('open');
    sidebarTop.classList.remove('show');
  }

  /* seção filtro */
  const sidebarFilters = document.getElementById('filters-sidebar');
  const filterOpenBtn = document.getElementById('open-filters');
  const filterCloseBtn = document.getElementById('close-filters');

  function fecharSidebarFiltro() {
    if (sidebarFilters) sidebarFilters.classList.remove('open');
  }

  /* seção overlay */
  const overlay = document.getElementById('filters-overlay');
  function updateOverlay() {
    const algumaAberta =
      sidebarMenu.classList.contains('open') ||
      (sidebarFilters && sidebarFilters.classList.contains('open'));
    if (overlay) {
      overlay.classList[algumaAberta ? 'add' : 'remove']('open');
    }
  }

  function fecharTodos() {
    fecharSidebarMenu();
    fecharSidebarFiltro();
    updateOverlay();
  }

  /* toggle sidebar principal */
  if (hamburgerBtn) {
    hamburgerBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const abrindoMenu = !sidebarMenu.classList.contains('open');
      fecharSidebarFiltro();
      if (abrindoMenu) {
        sidebarMenu.classList.add('open');
        sidebarTop.classList.add('show');
      } else {
        fecharSidebarMenu();
      }
      updateOverlay();
    });
  }

  /* open filter sidebar */
  if (filterOpenBtn) {
    filterOpenBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      fecharSidebarMenu();
      if (sidebarFilters) sidebarFilters.classList.add('open');
      updateOverlay();
    });
  }

  /* close filter sidebar */
  if (filterCloseBtn) {
    filterCloseBtn.addEventListener('click', () => {
      fecharSidebarFiltro();
      updateOverlay();
    });
  }

  /* click fora fecha */
  document.addEventListener('click', (e) => {
    const clicouForaSidebar =
      sidebarMenu && !sidebarMenu.contains(e.target) &&
      hamburgerBtn && !hamburgerBtn.contains(e.target);
    const clicouForaFiltro =
      sidebarFilters && !sidebarFilters.contains(e.target) &&
      filterOpenBtn && !filterOpenBtn.contains(e.target);

    if (
      (sidebarMenu.classList.contains('open') && clicouForaSidebar) ||
      (sidebarFilters && sidebarFilters.classList.contains('open') && clicouForaFiltro)
    ) {
      fecharTodos();
    }
  });

  /* scroll fecha */
  window.addEventListener('scroll', () => {
    if (
      sidebarMenu.classList.contains('open') ||
      (sidebarFilters && sidebarFilters.classList.contains('open'))
    ) {
      fecharTodos();
    }
  });

  const tabela = document.querySelector('#result_list');
  if (tabela) {
    const linhas = tabela.querySelectorAll('tbody tr');
    const cabecalho = tabela.querySelector('.table-wrapper thead');
  
    if (linhas.length > 5 && cabecalho) {
      cabecalho.style.paddingRight = '13px';
    }
  }

});
