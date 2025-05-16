function previewAvatar(input) {
  const avatar = document.getElementById('avatar');
  if (input.files && input.files[0]) {
    const reader = new FileReader();
    reader.onload = e => {
      avatar.style.backgroundImage = `url(${e.target.result})`;
      avatar.classList.add('image-set');
    };
    reader.readAsDataURL(input.files[0]);
  }
}

// Função utilitária para CSRF
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

// Função para abrir modal dinâmico
function openCrudModal({ title, contentHtml, buttons }) {
  document.getElementById('crud-modal-title').textContent = title;
  document.getElementById('crud-modal-content').innerHTML = contentHtml;

  var btnContainer = document.getElementById('crud-modal-buttons');
  btnContainer.innerHTML = '';
  buttons.forEach(function(btn) {
    var el = document.createElement('button');
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
  if(e.target === this) this.style.display = 'none';
};

// Adicionar Categoria
function abrirModalAdicionar() {
  openCrudModal({
    title: 'Adicionar Categoria',
    contentHtml: `
      <input type="text" id="nova-categoria" placeholder="Nome da nova categoria" style="width:100%;padding:12px;margin-bottom:16px;border-radius:6px;border:1px solid #ccc;">
    `,
    buttons: [
      {
        text: 'Adicionar',
        className: 'whatsapp-btn',
        onClick: adicionarCategoria
      }
    ]
  });
}

function adicionarCategoria() {
  var nome = document.getElementById('nova-categoria').value.trim();
  if(!nome) {
    document.getElementById('crud-modal-overlay').style.display = 'none';
    return;
  }
  fetch("/admin/animais/tipoanimal/add_ajax/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken
    },
    body: JSON.stringify({nome: nome}),
  })
  .then(resp => resp.json())
  .then(data => {
    if(data.success) {
      var select = document.querySelector('select[name="especie"]');
      var option = document.createElement('option');
      option.value = data.id;
      option.innerText = data.nome;
      option.selected = true;
      select.appendChild(option);
    }
    document.getElementById('crud-modal-overlay').style.display = 'none';
  })
  .catch(() => {
    document.getElementById('crud-modal-overlay').style.display = 'none';
  });
}

// Editar Categoria
function abrirModalEditar(valor, nomeAtual) {
  openCrudModal({
    title: 'Editar Categoria',
    contentHtml: `
      <input type="text" id="nova-categoria" value="${nomeAtual}" placeholder="Nome da categoria" style="width:100%;padding:12px;margin-bottom:16px;border-radius:6px;border:1px solid #ccc;">
    `,
    buttons: [
      {
        text: 'Salvar',
        className: 'whatsapp-btn',
        onClick: function() { editarCategoria(valor, document.getElementById('nova-categoria').value); }
      }
    ]
  });
}

function editarCategoria(id, novoNome) {
  if(!novoNome.trim()) {
    document.getElementById('crud-modal-overlay').style.display = 'none';
    return;
  }
  fetch("/admin/animais/tipoanimal/edit_ajax/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken
    },
    body: JSON.stringify({id: id, nome: novoNome}),
  })
  .then(resp => resp.json())
  .then(data => {
    if(data.success) {
      var select = document.querySelector('select[name="especie"]');
      select.options[select.selectedIndex].text = novoNome;
    }
    document.getElementById('crud-modal-overlay').style.display = 'none';
  })
  .catch(() => {
    document.getElementById('crud-modal-overlay').style.display = 'none';
  });
}

// Excluir Categoria
function abrirModalExcluir(valor, nomeAtual) {
  openCrudModal({
    title: 'Excluir Categoria',
    contentHtml: `
      <p style="margin: 18px 0; color:#C13584;">Tem certeza que deseja excluir <b>${nomeAtual}</b>?</p>
    `,
    buttons: [
      {
        text: 'Cancelar',
        className: 'instagram-btn',
        onClick: function() {
          document.getElementById('crud-modal-overlay').style.display = 'none';
        }
      },
      {
        text: 'Excluir',
        className: 'whatsapp-btn',
        onClick: function() { excluirCategoria(valor); }
      }
    ]
  });
}

function excluirCategoria(id) {
  fetch("/admin/animais/tipoanimal/delete_ajax/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken
    },
    body: JSON.stringify({id: id}),
  })
  .then(resp => resp.json())
  .then(data => {
    if(data.success) {
      var select = document.querySelector('select[name="especie"]');
      var opt = select.querySelector('option[value="'+id+'"]');
      if(opt) opt.remove();
    }
    document.getElementById('crud-modal-overlay').style.display = 'none';
  })
  .catch(() => {
    document.getElementById('crud-modal-overlay').style.display = 'none';
  });
}

// INTEGRAÇÃO: conecta os botões do admin ao modal CRUD custom
document.addEventListener('DOMContentLoaded', function() {
  var especieSelect = document.querySelector('select[name="especie"]');
  if (!especieSelect) return;

  // ADD
  var addBtn = document.getElementById('add_id_especie');
  if (addBtn) {
    addBtn.addEventListener('click', function(e) {
      e.preventDefault();
      abrirModalAdicionar();
    });
  }

  // EDIT
  var editBtn = document.getElementById('change_id_especie');
  if (editBtn) {
    editBtn.addEventListener('click', function(e) {
      e.preventDefault();
      var val = especieSelect.value;
      if (!val) return;
      var nomeAtual = especieSelect.options[especieSelect.selectedIndex].text;
      abrirModalEditar(val, nomeAtual);
    });
  }

  // DELETE
  var delBtn = document.getElementById('delete_id_especie');
  if (delBtn) {
    delBtn.addEventListener('click', function(e) {
      e.preventDefault();
      var val = especieSelect.value;
      if (!val) return;
      var nomeAtual = especieSelect.options[especieSelect.selectedIndex].text;
      abrirModalExcluir(val, nomeAtual);
    });
  }
});