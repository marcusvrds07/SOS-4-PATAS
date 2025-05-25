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

document.addEventListener('DOMContentLoaded', function() {
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
});


function openCrudModal({ title, contentHtml, buttons }) {
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
}

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


document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.delete-btn').forEach(button => {
    button.addEventListener('click', function () {
      const id = this.dataset.id;
      const nome = this.dataset.name;

      openCrudModal({
        title: 'Excluir Animal',
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
              fetch(`/admin/auth/user/${id}/delete/`, {
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

      let contentHtml;
      if (window.location.pathname.startsWith('/admin/auth/user/')) {
          let nomes = Array.from(checked)
            .map(el => el.closest('tr').querySelector('th.field-username')?.innerText.trim() || '')
            .filter(Boolean);

          let nomesHtml = nomes.length
            ? `<ul style="margin: 8px 0 0 0; padding-left: 18px; color:#1941a0;">${nomes.map(nome => `<li>${nome}</li>`).join('')}</ul>`
            : '';
          
          contentHtml = `<p>Tem certeza que deseja excluir os usuários abaixo?</p>${nomesHtml}`
        } 
        else if (window.location.pathname.startsWith('/admin/auth/group/')) {
          let nomes = Array.from(checked)
            .map(el => el.closest('tr').querySelector('th.field-name')?.innerText.trim() || '')
            .filter(Boolean);

          let nomesHtml = nomes.length
            ? `<ul style="margin: 8px 0 0 0; padding-left: 18px; color:#1941a0;">${nomes.map(nome => `<li>${nome}</li>`).join('')}</ul>`
            : '';
          
          contentHtml = `<p>Tem certeza que deseja excluir os grupos abaixo?</p>${nomesHtml}`
        }
        else {
          let nomes = Array.from(checked)
            .map(el => el.closest('tr').querySelector('td.field-nome')?.innerText.trim() || '')
            .filter(Boolean);

          let nomesHtml = nomes.length
            ? `<ul style="margin: 8px 0 0 0; padding-left: 18px; color:#1941a0;">${nomes.map(nome => `<li>${nome}</li>`).join('')}</ul>`
            : '';

          contentHtml = `<p>Tem certeza que deseja excluir os registros abaixo?</p>${nomesHtml}`
      }

      openCrudModal({
        title: 'Excluir selecionados',
        contentHtml: contentHtml,
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
