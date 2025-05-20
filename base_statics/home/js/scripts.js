const selectedOption = document.querySelector(".selected-option")
const options = document.querySelector(".options")
const arrow = document.querySelector(".arrow")
const buttons = document.querySelectorAll('.donation-amount');

function closeSelect() {
  if (options && options.classList.contains("open")) {
    options.classList.remove("open")
    if (arrow) arrow.classList.remove("rotate")
  }
}

if (selectedOption) {
  selectedOption.addEventListener("click", e => {
    e.stopPropagation()
    options.classList.toggle("open")
    arrow.classList.toggle("rotate")
  })
}

document.addEventListener("click", event => {
  if (
    selectedOption && options &&
    !selectedOption.contains(event.target) &&
    !options.contains(event.target)
  ) {
    closeSelect()
  }
})

const navbar = document.getElementById("navbar")
window.addEventListener("scroll", () => {
  if (navbar) navbar.classList.toggle("scrolled", window.scrollY > 0)
  closeSelect()
})

document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("pageInput")
  if (input) {
    const prevBtn = document.getElementById("prevPage")
    const nextBtn = document.getElementById("nextPage")
    const form = document.getElementById("pageForm")
    const min = parseInt(input.min)
    const max = parseInt(input.max)
    const current = parseInt(input.dataset.current)
    let clickedArrow = false

    input.addEventListener("input", () => {
      let v = input.value.replace(/[^0-9]/g, "")
      if (v !== "") {
        const n = parseInt(v)
        if (n < min) input.value = ""
        else if (n > max) input.value = v.slice(0, -1)
        else input.value = n
      }
    })

    input.addEventListener("keydown", e => {
      const val = parseInt(input.value) || current
      if (e.key === "ArrowUp" && val < max) {
        e.preventDefault(); input.value = val+1
      }
      if (e.key === "ArrowDown" && val > min) {
        e.preventDefault(); input.value = val-1
      }
      if (e.key === "Enter") {
        e.preventDefault()
        const p = parseInt(input.value)
        if (p >= min && p <= max) goToPage(p)
        else input.value = current
      }
    })

    input.addEventListener("blur", () => {
      if (clickedArrow) { clickedArrow = false; return }
      const typed = parseInt(input.value)
      if (!typed) input.value = current
      else if (typed !== current && typed >= min && typed <= max) {
        goToPage(typed)
      } else input.value = current
    })

    if (prevBtn) {
      prevBtn.addEventListener("mousedown", () => { clickedArrow = true })
      prevBtn.addEventListener("click", () => {
        const c = parseInt(input.dataset.current)
        if (c > min) goToPage(c-1)
      })
    }
    if (nextBtn) {
      nextBtn.addEventListener("mousedown", () => { clickedArrow = true })
      nextBtn.addEventListener("click", () => {
        const c = parseInt(input.dataset.current)
        if (c < max) goToPage(c+1)
      })
    }

    function goToPage(page) {
      const url = new URL(window.location.href)
      url.searchParams.set("page", page)
      url.hash = "adoption"
      form.querySelector("input[name='page']").value = page
      window.location.href = url.toString()
    }
  }
  
  setupDonationSystem();
  setupContactModal();
})

function setupDonationSystem() {
  const doarBtn = document.getElementById("doar-btn");
  const doacaoModal = document.getElementById("doacao-modal-overlay");
  const closeDoacaoModal = document.getElementById("close-doacao-modal");
  const copyPixBtn = document.getElementById("copy-pix-btn");
  const pixKey = "21968049191";
  
  if (doarBtn) {
    doarBtn.addEventListener("click", function() {
      doacaoModal.style.display = "block";
    });
  }
  
  if (closeDoacaoModal) {
    closeDoacaoModal.addEventListener("click", function() {
      doacaoModal.style.display = "none";
    });
  }
  
  if (copyPixBtn) {
    copyPixBtn.addEventListener("click", function() {
      navigator.clipboard.writeText(pixKey).then(() => {
        this.textContent = "Chave copiada!";
        setTimeout(() => {
          this.textContent = "Copiar chave PIX";
        }, 2000);
      });
    });
  }
  
  window.addEventListener("click", function(event) {
    if (event.target === doacaoModal) {
      doacaoModal.style.display = "none";
    }
  });
}

function setupContactModal() {
  const contatoLink = document.getElementById("contato-link");
  const contatoModal = document.getElementById("contato-modal-overlay");
  const closeContatoModal = document.getElementById("close-contato-modal");
  
  if (contatoLink) {
    contatoLink.addEventListener("click", function(e) {
      e.preventDefault();
      contatoModal.style.display = "block";
    });
  }
  
  if (closeContatoModal) {
    closeContatoModal.addEventListener("click", function() {
      contatoModal.style.display = "none";
    });
  }
  
  window.addEventListener("click", function(event) {
    if (event.target === contatoModal) {
      contatoModal.style.display = "none";
    }
  });
}