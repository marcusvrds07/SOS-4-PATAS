document.addEventListener('DOMContentLoaded', () => {
  // Código abaixo trata da sidebar
  const sidebarMenu = document.querySelector('.sidebar');
  const sidebarTop = document.querySelector('.sidebar-top');
  const hamburgerBtn = document.getElementById('sidebar-hamburger');

  function fecharSidebarMenu() {
    sidebarMenu.classList.remove('open');
    sidebarTop.classList.remove('show');
  }

  // Código abaixo trata da filter sidebar
  const sidebarFilters = document.getElementById('filters-sidebar');
  const filterOpenBtn = document.getElementById('open-filters');
  const filterCloseBtn = document.getElementById('close-filters');

  function fecharSidebarFiltro() {
    sidebarFilters.classList.remove('open');
  }

  // Código abaixo trata do overlay 
  const overlay = document.getElementById('filters-overlay');

  function updateOverlay() {
    const algumaAberta =
      sidebarMenu.classList.contains('open') ||
      sidebarFilters.classList.contains('open');

    if (algumaAberta) {
      overlay.classList.add('open');
    } else {
      overlay.classList.remove('open');
    }
  }

  function fecharTodos() {
    fecharSidebarMenu();
    fecharSidebarFiltro();
    updateOverlay();
  }

  // Código abaixo trata da sidebar
  hamburgerBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    const abrindo = !sidebarMenu.classList.contains('open');

    fecharSidebarFiltro();
    if (abrindo) {
      sidebarMenu.classList.add('open');
      sidebarTop.classList.add('show');
    } else {
      fecharSidebarMenu();
    }

    updateOverlay();
  });

  // Código abaixo trata da filter sidebar
  filterOpenBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    fecharSidebarMenu();
    sidebarFilters.classList.add('open');
    updateOverlay();
  });

  // Código abaixo trata da filter sidebar
  filterCloseBtn.addEventListener('click', () => {
    fecharSidebarFiltro();
    updateOverlay();
  });

  // Código abaixo trata de ambos
  document.addEventListener('click', (e) => {
    const clicouForaSidebar = !sidebarMenu.contains(e.target) && !hamburgerBtn.contains(e.target);
    const clicouForaFiltro = !sidebarFilters.contains(e.target) && !filterOpenBtn.contains(e.target);

    if (
      (sidebarMenu.classList.contains('open') && clicouForaSidebar) ||
      (sidebarFilters.classList.contains('open') && clicouForaFiltro)
    ) {
      fecharTodos();
    }
  });

  // Código abaixo trata de ambos
  window.addEventListener('scroll', () => {
    if (sidebarMenu.classList.contains('open') || sidebarFilters.classList.contains('open')) {
      fecharTodos();
    }
  });
});
