document.addEventListener('DOMContentLoaded', () => {
  const tablesMenu = document.getElementById('tables');
  if (!tablesMenu) return;

  const items = tablesMenu.querySelectorAll('li.model-item');
  if (items.length === 0) {
    const msg = document.createElement('li');
    msg.className = 'model-item no-data';
    msg.innerHTML = '<span class="model-name">Você não pode ver nenhuma base de dados.</span>';
    tablesMenu.appendChild(msg);
  }
});
