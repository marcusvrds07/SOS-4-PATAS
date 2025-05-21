// modal.js

document.addEventListener('DOMContentLoaded', function() {
  // Fecha modal ao clicar no X ou fora do modal
  var closeBtn = document.getElementById('close-crud-modal');
  var overlay = document.getElementById('crud-modal-overlay');
  if (closeBtn && overlay) {
    closeBtn.onclick = function() {
      overlay.style.display = 'none';
    };
  }
  if (overlay) {
    overlay.onclick = function(e) {
      if (e.target === overlay) overlay.style.display = 'none';
    };
  }

  // Função para abrir modal CRUD
  window.openCrudModal = function({ title, contentHtml, buttons }) {
    document.getElementById('crud-modal-title').textContent = title;
    document.getElementById('crud-modal-content').innerHTML = contentHtml;

    const btnContainer = document.getElementById('crud-modal-buttons');
    btnContainer.innerHTML = '';
    buttons.forEach(({ text, className, onClick }) => {
      const btn = document.createElement('button');
      btn.textContent = text;
      btn.className = className;
      btn.type = 'button';
      btn.onclick = onClick;
      btnContainer.appendChild(btn);
    });

    document.getElementById('crud-modal-overlay').style.display = 'block';
  };

  // Utilitário para CSRF
  function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          let cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
              let cookie = cookies[i].trim();
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
  const csrftoken = getCookie('csrftoken');

  // Botões de deletar lista de TipoAnimal
  document.querySelectorAll('.delete-btn').forEach(button => {
    button.addEventListener('click', function () {
      const id = this.dataset.id;
      const nome = this.dataset.name;

      openCrudModal({
        title: 'Excluir Categoria de Animal',
        contentHtml: `<p>Tem certeza que deseja excluir <b>${nome}</b>?</p>`,
        buttons: [
          {
            text: 'Cancelar',
            className: 'instagram-btn',
            onClick: () => document.getElementById('crud-modal-overlay').style.display = 'none'
          },
          {
            text: 'Excluir',
            className: 'whatsapp-btn',
            onClick: () => {
              fetch(`/admin/animais/tipoanimal/${id}/delete/`, {
                method: 'POST',
                headers: {
                  'X-CSRFToken': csrftoken,
                  'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: 'post=yes'
              })
              .then(res => {
                if (res.redirected) {
                  window.location.href = res.url;
                } else {
                  location.reload();
                }
              })
              .catch(() => alert('Erro ao tentar excluir o registro.'));
            }
          }
        ]
      });
    });
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('changelist-form');
  const btnRemove = document.getElementById('btn-remove');

  if (form && btnRemove) {
    btnRemove.addEventListener('click', function (e) {
      e.preventDefault();

      const checked = form.querySelectorAll('input.action-select:checked');
      if (!checked.length) return;

      let nomes = Array.from(checked)
        .map(el => el.closest('tr').querySelector('th.field-nome')?.innerText.trim() || '')
        .filter(Boolean);

      let nomesHtml = nomes.length
        ? `<ul style="margin: 8px 0 0 0; padding-left: 18px; color:#1941a0;">${nomes.map(nome => `<li>${nome}</li>`).join('')}</ul>`
        : '';

      openCrudModal({
        title: 'Excluir Categoria(s) de Animal',
        contentHtml: `<p>Tem certeza que deseja excluir os registros abaixo?</p>${nomesHtml}`,
        buttons: [
          {
            text: 'Cancelar',
            className: 'instagram-btn',
            onClick: () => document.getElementById('crud-modal-overlay').style.display = 'none'
          },
          {
            text: 'Excluir',
            className: 'whatsapp-btn',
            onClick: () => {
              let inputAction = document.createElement('input');
              inputAction.type = 'hidden';
              inputAction.name = 'action';
              inputAction.value = 'delete_selected';

              let inputPost = document.createElement('input');
              inputPost.type = 'hidden';
              inputPost.name = 'post';
              inputPost.value = 'yes';

              form.appendChild(inputAction);
              form.appendChild(inputPost);

              form.submit();
            }
          }
        ]
      });
    });
  }
});
