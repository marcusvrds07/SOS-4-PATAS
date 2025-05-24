document.addEventListener('DOMContentLoaded', function() {

  document.querySelectorAll('#superuser-toggle .checkbox-field').forEach(function(box) {

    box.addEventListener('click', function(e) {
      const input = box.querySelector('input[type="checkbox"]');

      if (input && !input.disabled && e.target !== input) {
        input.checked = !input.checked;
        input.dispatchEvent(new Event('change', { bubbles: true }));
      }
    });
  });
});


