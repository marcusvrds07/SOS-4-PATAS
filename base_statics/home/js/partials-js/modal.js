// Sessão: Modais
document.addEventListener("DOMContentLoaded", () => {
  // Sessão: Modal de Contato
  const contatoLink = document.getElementById("contato-link")
  const contatoModalOverlay = document.getElementById("contato-modal-overlay")
  const closeContatoModal = document.getElementById("close-contato-modal")

  if (contatoLink && contatoModalOverlay && closeContatoModal) {
    contatoLink.addEventListener("click", e => {
      e.preventDefault()
      contatoModalOverlay.style.display = "block"
      document.body.style.overflow = "hidden"
    })
    closeContatoModal.addEventListener("click", () => {
      contatoModalOverlay.style.display = "none"
      document.body.style.overflow = "auto"
    })
    contatoModalOverlay.addEventListener("click", e => {
      if (e.target === contatoModalOverlay) {
        contatoModalOverlay.style.display = "none"
        document.body.style.overflow = "auto"
      }
    })
    document.addEventListener("keydown", e => {
      if (e.key === "Escape" && contatoModalOverlay.style.display === "block") {
        contatoModalOverlay.style.display = "none"
        document.body.style.overflow = "auto"
      }
    })
  }

  const adotarBtn = document.getElementById("adotar-btn")
  const adotarModalOverlay = document.getElementById("modal-overlay")
  const closeAdotarModal = document.getElementById("close-modal")

  if (adotarBtn && adotarModalOverlay && closeAdotarModal) {
    adotarBtn.addEventListener("click", e => {
      e.preventDefault()
      adotarModalOverlay.style.display = "block"
      document.body.style.overflow = "hidden"
    })
    closeAdotarModal.addEventListener("click", () => {
      adotarModalOverlay.style.display = "none"
      document.body.style.overflow = "auto"
    })
    adotarModalOverlay.addEventListener("click", e => {
      if (e.target === adotarModalOverlay) {
        adotarModalOverlay.style.display = "none"
        document.body.style.overflow = "auto"
      }
    })
    document.addEventListener("keydown", e => {
      if (e.key === "Escape" && adotarModalOverlay.style.display === "block") {
        adotarModalOverlay.style.display = "none"
        document.body.style.overflow = "auto"
      }
    })
  }
})
