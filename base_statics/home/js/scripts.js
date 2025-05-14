  // Sessão: Dropdown customizado
  const selectedOption = document.querySelector(".selected-option")
  const options = document.querySelector(".options")
  const arrow = document.querySelector(".arrow")

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

  // Sessão: Carrossel responsivo
  const carroussel = document.getElementById("carroussel")
  const slides = document.querySelectorAll(".slide")
  const carrousselContainer = document.querySelector(".carroussel-container")

  if (carroussel) {
    const originalSources = []
    slides.forEach(slide => {
      const img = slide.querySelector("img")
      if (img) originalSources.push(img.getAttribute("src"))
    })

    function updateCarouselImages() {
      const w = window.innerWidth
      if (!carrousselContainer.classList.contains("card-style")) {
        carrousselContainer.classList.add("card-style")
      }
      slides.forEach((slide, i) => {
        const img = slide.querySelector("img")
        if (!img) return
        let prefix
        if (w <= 320) prefix = "pequeno"
        else if (w <= 375) prefix = "medio"
        else if (w <= 430) prefix = "grande"
        else if (w <= 768) prefix = "grande"
        else {
          img.src = originalSources[i]
          return
        }
        img.src = `/static/home/img/carrossel${i+1}_${prefix}.png`
      })
    }

    updateCarouselImages()
    window.addEventListener("resize", updateCarouselImages)

    let slideIndex = 0
    function showSlide(n) {
      slideIndex = n
      carroussel.style.transform = `translateX(-${n*100}%)`
    }
    window.nextSlide = () => showSlide((slideIndex+1) % slides.length)
    window.prevSlide = () => showSlide((slideIndex-1+slides.length) % slides.length)
    setInterval(window.nextSlide, 5000)
  }

  
  // Sessão: Efeito de scroll
  const navbar = document.getElementById("navbar")
  window.addEventListener("scroll", () => {
    if (navbar) navbar.classList.toggle("scrolled", window.scrollY > 50)
    closeSelect()
  })

// Sessão: Paginação
document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("pageInput")
  if (!input) return

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
})
