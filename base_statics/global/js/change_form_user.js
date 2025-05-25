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

// --- CSRF Token Utility ---
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// --- CRUD Modal Functions ---
function openCrudModal({ title, contentHtml, buttons }) {
  document.getElementById('crud-modal-title').textContent = title;
  document.getElementById('crud-modal-content').innerHTML = contentHtml;
  const btnContainer = document.getElementById('crud-modal-buttons');
  btnContainer.innerHTML = '';
  buttons.forEach(function(btn) {
    const el = document.createElement('button');
    el.type = 'button';
    el.className = btn.className || '';
    el.innerHTML = btn.text;
    el.onclick = btn.onClick;
    btnContainer.appendChild(el);
  });
  document.getElementById('crud-modal-overlay').style.display = 'block';
}
document.getElementById('close-crud-modal').onclick = function() {
  document.getElementById('crud-modal-overlay').style.display = 'none';
};
document.getElementById('crud-modal-overlay').onclick = function(e) {
  if (e.target === this) this.style.display = 'none';
};

// --- Botão de Excluir no formulário de User ---
document.addEventListener('DOMContentLoaded', function () {
  const excluirBtn = document.getElementById('btn-excluir-form');
  if (excluirBtn) {
    excluirBtn.addEventListener('click', function (e) {
      e.preventDefault();
      const url = excluirBtn.getAttribute('data-delete-url');
      openCrudModal({
        title: 'Excluir usuário',
        contentHtml: `<p style="margin:18px 0; color:#C13584;">Tem certeza que deseja excluir este usuário?</p>`,
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
              fetch(url, {
                method: 'POST',
                headers: {
                  'X-CSRFToken': csrftoken,
                  'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: 'post=yes'
              }).then(res => {
                if (res.redirected) {
                  window.location.href = res.url;
                } else {
                  location.reload();
                }
              }).catch(() => alert('Erro ao tentar excluir o usuário.'));
            }
          }
        ]
      });
    });
  }
});

// --------- VALIDADORES FRONT ---------
function validatePassword() {
    const password = document.getElementById("id_new_password1").value;

    const length = password.length >= 8;
    const hasNumber = /\d/.test(password);
    const hasLower = /[a-z]/.test(password);
    const hasUpper = /[A-Z]/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

    document.getElementById("length").className = length ? "valid" : "invalid";
    document.getElementById("number").className = hasNumber ? "valid" : "invalid";
    document.getElementById("lowercase").className = hasLower ? "valid" : "invalid";
    document.getElementById("uppercase").className = hasUpper ? "valid" : "invalid";
    document.getElementById("special").className = hasSpecialChar ? "valid" : "invalid";
    isSamePassword();
}

function isSamePassword() {
    const password = document.getElementById("id_new_password1").value;
    const password2 = document.getElementById("id_new_password2").value;
    let isSame = password && password === password2;
    document.getElementById("isSame").className = isSame ? "valid" : "invalid";
}

// --------- OLHO DA SENHA ---------
function togglePasswordVisibility(inputId, toggleId) {
    const input = document.getElementById(inputId);
    const toggle = document.getElementById(toggleId);
    if (input.type === "password") {
        input.type = "text";
        toggle.src = toggle.getAttribute('data-hide');
    } else {
        input.type = "password";
        toggle.src = toggle.getAttribute('data-show');
    }
}

// --------- ABRIR MODAL (CHAMAR ISSO NO CLIQUE DO BOTÃO) ---------
function abrirModalTrocarSenha(userId) {
    var modal = document.getElementById('modal-change-password');
    if (!modal) return;
    modal.style.display = 'block';
    document.getElementById('change-password-form').reset();
    document.getElementById('password-error').innerText = '';
    document.getElementById('modal-password-user-id').value = userId || '';
    // Resetar visual das regras
    ['length', 'number', 'lowercase', 'uppercase', 'special', 'isSame'].forEach(id => {
        document.getElementById(id).className = 'invalid';
    });
}

// --------- INTERCEPTA CLIQUE NO "Reconfigurar senha" DO DJANGO ---------
document.addEventListener('DOMContentLoaded', function () {
    var btns = document.querySelectorAll('a.button');
    btns.forEach(function(btn) {
        if (
            btn.textContent.trim() === "Reconfigurar senha" ||
            btn.textContent.trim() === "Change password"
        ) {
            btn.addEventListener('click', function(e) {
                e.preventDefault();
                var parts = window.location.pathname.split('/');
                var userIndex = parts.indexOf('user');
                var userId = (userIndex !== -1 && parts.length > userIndex+1) ? parts[userIndex+1] : '';
                abrirModalTrocarSenha(userId);
            });
        }
    });

    // --------- FECHAR MODAL ---------
    var modal = document.getElementById('modal-change-password');
    var closeBtn = document.getElementById('close-change-password-modal');
    if (closeBtn && modal) {
        closeBtn.onclick = function() { modal.style.display = 'none'; };
    }
    if (modal) {
        modal.onclick = function(e) {
            if (e.target === modal) modal.style.display = 'none';
        };
    }

    // --------- ENVIO AJAX ---------
    var form = document.getElementById('change-password-form');
    if (form) {
        form.onsubmit = function(e) {
            e.preventDefault();
            var newPassword = document.getElementById('id_new_password1').value;
            var confirmPassword = document.getElementById('id_new_password2').value;
            var errorBox = document.getElementById('password-error');
            var userId = document.getElementById('modal-password-user-id').value;

            // Checagem rápida no front
            if (newPassword !== confirmPassword) {
                errorBox.innerText = 'As senhas precisam ser iguais.';
                return;
            }
            // Aqui você pode bloquear envio se quiser que todas as regras estejam válidas no front
            // MAS: quem valida oficialmente é o backend Django

            fetch('/admin/auth/user/' + userId + '/change_password_ajax/', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ password: newPassword })
            }).then(resp => resp.json())
              .then(res => {
                if (res.success) {
                    modal.style.display = 'none';
                    alert('Senha alterada com sucesso!');
                } else {
                    errorBox.innerText = res.error;
                }
              }).catch(() => errorBox.innerText = 'Erro de conexão.');
        };
    }
});
