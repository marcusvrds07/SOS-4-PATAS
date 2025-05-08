document.addEventListener("DOMContentLoaded", () => {
  const menuToggle = document.getElementById("menu-toggle")
  const navMenu = document.getElementById("nav-menu")
  const selectedOption = document.querySelector(".selected-option")
  const options = document.querySelector(".options")
  const arrow = document.querySelector(".arrow")
  const navbar = document.getElementById("navbar")
  const carroussel = document.getElementById("carroussel")
  const slides = document.querySelectorAll(".slide")
  const carrousselContainer = document.querySelector(".carroussel-container")

  const contatoLink = document.getElementById("contato-link")
  const contatoModalOverlay = document.getElementById("contato-modal-overlay")
  const closeContatoModal = document.getElementById("close-contato-modal")

  if (contatoLink && contatoModalOverlay && closeContatoModal) {
    contatoLink.addEventListener("click", (e) => {
      e.preventDefault()
      contatoModalOverlay.style.display = "block"
      document.body.style.overflow = "hidden"
    })

    closeContatoModal.addEventListener("click", () => {
      contatoModalOverlay.style.display = "none"
      document.body.style.overflow = "auto"
    })

    contatoModalOverlay.addEventListener("click", (e) => {
      if (e.target === contatoModalOverlay) {
        contatoModalOverlay.style.display = "none"
        document.body.style.overflow = "auto"
      }
    })

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && contatoModalOverlay.style.display === "block") {
        contatoModalOverlay.style.display = "none"
        document.body.style.overflow = "auto"
      }
    })
  }

  let slideIndex = 0

  function resetHamburgerIcon(spans) {
    spans[0].style.transform = "none"
    spans[1].style.opacity = "1"
    spans[2].style.transform = "none"
  }

  function closeHamburger() {
    if (navMenu && navMenu.classList.contains("active")) {
      navMenu.classList.remove("active")
      const spans = menuToggle.querySelectorAll("span")
      resetHamburgerIcon(spans)
    }
  }

  function closeSelect() {
    if (options && options.classList.contains("open")) {
      options.classList.remove("open")
      if (arrow) arrow.classList.remove("rotate")
    }
  }

  if (menuToggle && navMenu) {
    menuToggle.addEventListener("click", function (e) {
      e.stopPropagation()
      navMenu.classList.toggle("active")
      const spans = this.querySelectorAll("span")

      if (navMenu.classList.contains("active")) {
        spans[0].style.transform = "rotate(45deg) translate(5px, 5px)"
        spans[1].style.opacity = "0"
        spans[2].style.transform = "rotate(-45deg) translate(7px, -6px)"
      } else {
        resetHamburgerIcon(spans)
      }
    })

    navMenu.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        closeHamburger()
      })
    })
  }

  if (selectedOption) {
    selectedOption.addEventListener("click", (e) => {
      e.stopPropagation()
      options.classList.toggle("open")
      arrow.classList.toggle("rotate")
    })
  }

  if (carroussel) {
    const originalSources = []
    slides.forEach((slide) => {
      const imgElement = slide.querySelector("img")
      if (imgElement) {
        originalSources.push(imgElement.getAttribute("src"))
      }
    })

    function updateCarouselImages() {
      const screenWidth = window.innerWidth

      if (!carrousselContainer.classList.contains("card-style")) {
        carrousselContainer.classList.add("card-style")
      }

      slides.forEach((slide, index) => {
        const imgElement = slide.querySelector("img")
        if (imgElement) {
          let sizePrefix

          if (screenWidth <= 320) {
            sizePrefix = "pequeno"
          } else if (screenWidth <= 375) {
            sizePrefix = "medio"
          } else if (screenWidth <= 430) {
            sizePrefix = "grande"
          } else if (screenWidth <= 768) {
            sizePrefix = "grande"
          } else {
            imgElement.setAttribute("src", originalSources[index])
            return
          }

          const newSrc = `/static/home/img/carrossel${index + 1}_${sizePrefix}.png`
          imgElement.setAttribute("src", newSrc)
        }
      })
    }

    updateCarouselImages()

    window.addEventListener("resize", updateCarouselImages)

    function showSlide(n) {
      slideIndex = n
      carroussel.style.transform = `translateX(-${slideIndex * 100}%)`
    }

    window.nextSlide = () => {
      slideIndex = (slideIndex + 1) % slides.length
      showSlide(slideIndex)
    }

    window.prevSlide = () => {
      slideIndex = (slideIndex - 1 + slides.length) % slides.length
      showSlide(slideIndex)
    }

    setInterval(window.nextSlide, 5000)
  }

  window.addEventListener("scroll", () => {
    if (navbar) {
      navbar.classList.toggle("scrolled", window.scrollY > 50)
    }

    closeHamburger()
    closeSelect()
  })

  document.addEventListener("click", (event) => {
    if (!menuToggle.contains(event.target) && !navMenu.contains(event.target)) {
      closeHamburger()
    }

    if (!selectedOption.contains(event.target) && !options.contains(event.target)) {
      closeSelect()
    }
  })
})

document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("pageInput")
  if (!input) return

  const prevBtn = document.getElementById("prevPage")
  const nextBtn = document.getElementById("nextPage")
  const form = document.getElementById("pageForm")

  const min = Number.parseInt(input.getAttribute("min"))
  const max = Number.parseInt(input.getAttribute("max"))
  const current = Number.parseInt(input.dataset.current)
  let clickedArrow = false

  input.addEventListener("input", () => {
    let value = input.value
    value = value.replace(/[^0-9]/g, "")
    if (value !== "") {
      const intVal = Number.parseInt(value)
      if (intVal < min) {
        input.value = ""
      } else if (intVal > max) {
        input.value = value.slice(0, -1)
      } else {
        input.value = intVal
      }
    }
  })

  input.addEventListener("keydown", (e) => {
    const val = Number.parseInt(input.value) || current
    if (e.key === "ArrowUp") {
      e.preventDefault()
      if (val < max) input.value = val + 1
    } else if (e.key === "ArrowDown") {
      e.preventDefault()
      if (val > min) input.value = val - 1
    } else if (e.key === "Enter") {
      e.preventDefault()
      const page = Number.parseInt(input.value)
      if (page >= min && page <= max) {
        goToPage(page)
      } else {
        input.value = input.dataset.current
      }
    }
  })

  input.addEventListener("blur", () => {
    if (clickedArrow) {
      clickedArrow = false
      return
    }

    const typedPage = Number.parseInt(input.value)
    const currentPage = Number.parseInt(input.dataset.current)

    if (!typedPage) {
      input.value = currentPage
      return
    }

    if (typedPage >= min && typedPage <= max) {
      if (typedPage !== currentPage) {
        goToPage(typedPage)
      }
    } else {
      input.value = currentPage
    }
  })

  if (prevBtn) {
    prevBtn.addEventListener("mousedown", () => {
      clickedArrow = true
    })
    prevBtn.addEventListener("click", () => {
      const current = Number.parseInt(input.dataset.current)
      if (current > min) goToPage(current - 1)
    })
  }

  if (nextBtn) {
    nextBtn.addEventListener("mousedown", () => {
      clickedArrow = true
    })
    nextBtn.addEventListener("click", () => {
      const current = Number.parseInt(input.dataset.current)
      if (current < max) goToPage(current + 1)
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
