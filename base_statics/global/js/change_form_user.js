document.addEventListener('DOMContentLoaded', function() {
  // Seleciona todos os campos checkbox-field dentro do #superuser-toggle
  document.querySelectorAll('#superuser-toggle .checkbox-field').forEach(function(box) {
    // Ao clicar na área do campo (exceto no input diretamente)
    box.addEventListener('click', function(e) {
      const input = box.querySelector('input[type="checkbox"]');
      // Evita toggle duplo se clicou no input diretamente
      if (input && !input.disabled && e.target !== input) {
        input.checked = !input.checked;
        input.dispatchEvent(new Event('change', { bubbles: true }));
      }
    });
  });
});
