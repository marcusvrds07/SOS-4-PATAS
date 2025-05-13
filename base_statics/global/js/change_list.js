  document.addEventListener('DOMContentLoaded', () => {

    // Checkbox da tabela
    const toggle = document.getElementById('action-toggle');
    const checks = Array.from(document.querySelectorAll('input.action-select'));
    const countEl = document.getElementById('selected-count');
    const btnRemove = document.getElementById('btn-remove');

    function refreshActions() {
      const checkedCount = checks.filter(c => c.checked).length;
      countEl.textContent = checkedCount
        ? `${checkedCount} selecionado${checkedCount > 1 ? 's' : ''}`
        : '0 selecionados';
      btnRemove.disabled = checkedCount === 0;
    }

    if (toggle) {
      toggle.addEventListener('change', () => {
        checks.forEach(c => c.checked = toggle.checked);
        refreshActions();
      });
    }

    checks.forEach(c => c.addEventListener('change', refreshActions));
    refreshActions();

    document.querySelectorAll('.grp-filter-choice').forEach(select => {
      select.addEventListener('change', function () {
        if (this.value) {
          window.location.href = this.value;
        }
      });
    });

    const form = document.querySelector('.search-container');
    const input = form.querySelector('input[name="q"]');
    form.addEventListener('submit', e => {
      if (input.value.trim() === '') {
        e.preventDefault();
        window.location.href = window.location.pathname;
      }
    });
});