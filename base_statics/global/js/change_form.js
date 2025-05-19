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

  var fotoInput = document.getElementById('id_foto');
  if (fotoInput) {
    fotoInput.addEventListener('change', function() {
      previewAvatar(this);
    });
  }
});

document.addEventListener('DOMContentLoaded', function() {
    // Encontrar o botão de adicionar (último item da galeria sem imagem)
    const addButton = document.querySelector('.gallery-item .file-input.add input[type="file"]');
    
    if (addButton) {
      addButton.addEventListener('change', function(e) {
        const files = e.target.files;
        if (files.length > 0) {
          // Criar URL para o arquivo selecionado
          const imageUrl = URL.createObjectURL(files[0]);
          
          // Obter o elemento pai (label.file-input.add)
          const fileInputLabel = this.parentElement;
          const galleryItem = fileInputLabel.parentElement;
          
          // Criar nova estrutura HTML para a imagem selecionada
          const newContent = document.createElement('div');
          newContent.innerHTML = `
            <label class="gallery-label" style="cursor:pointer;">
              <img src="${imageUrl}" class="gallery-img">
            </label>
            <button type="button" class="remove-btn" onclick="this.closest('.gallery-item').remove();">&times;</button>
          `;
          
          // Clonar o input de arquivo para a nova imagem
          const clonedInput = this.cloneNode(true);
          
          // Limpar o input original para permitir selecionar o mesmo arquivo novamente
          this.value = '';
          
          // Criar um novo item de galeria para a imagem selecionada
          const newGalleryItem = document.createElement('div');
          newGalleryItem.className = 'gallery-item';
          
          // Copiar campos ocultos do item original
          const hiddenFields = galleryItem.querySelectorAll('input[type="hidden"]');
          hiddenFields.forEach(function(field) {
            if (!field.name.includes('TOTAL_FORMS') && 
                !field.name.includes('INITIAL_FORMS') && 
                !field.name.includes('MIN_NUM_FORMS') && 
                !field.name.includes('MAX_NUM_FORMS')) {
              const clonedField = field.cloneNode(true);
              
              // Atualizar o índice no nome do campo
              const totalForms = document.querySelector('input[name$="TOTAL_FORMS"]');
              const newIndex = parseInt(totalForms.value);
              
              // Substituir o índice no nome do campo
              const oldIndex = field.name.match(/\d+/)[0];
              clonedField.name = field.name.replace(oldIndex, newIndex);
              clonedField.id = field.id.replace(oldIndex, newIndex);
              
              newGalleryItem.appendChild(clonedField);
            }
          });
          
          // Adicionar o input de arquivo clonado à nova label
          const newLabel = newContent.querySelector('.gallery-label');
          clonedInput.name = clonedInput.name.replace(/\d+/, document.querySelector('input[name$="TOTAL_FORMS"]').value);
          clonedInput.id = clonedInput.id.replace(/\d+/, document.querySelector('input[name$="TOTAL_FORMS"]').value);
          newLabel.appendChild(clonedInput);
          
          // Adicionar o novo conteúdo ao novo item de galeria
          while (newContent.firstChild) {
            newGalleryItem.appendChild(newContent.firstChild);
          }
          
          // Inserir o novo item de galeria antes do item com o botão de adicionar
          galleryItem.parentNode.insertBefore(newGalleryItem, galleryItem);
          
          // Incrementar o contador TOTAL_FORMS no management_form
          const totalForms = document.querySelector('input[name$="TOTAL_FORMS"]');
          totalForms.value = parseInt(totalForms.value) + 1;
        }
      });
    }


  });

  switchbutton = document.querySelector('.checkbox-field label');
  switchbutton.addEventListener('click', function(e) {
    console.log('Oi')
  });
