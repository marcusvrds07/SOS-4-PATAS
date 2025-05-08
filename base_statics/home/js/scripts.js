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

    const style = document.createElement("style")
    style.textContent = `
      body {
        padding-top: 80px;
      }

      .card-style {
        max-width: 90%;
        margin: 0 auto 40px;
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 
          0 10px 25px rgba(9, 45, 115, 0.2),
          0 6px 12px rgba(9, 45, 115, 0.15),
          0 4px 6px rgba(247, 214, 71, 0.1),
          0 0 0 1px rgba(9, 45, 115, 0.05);
        background-color: white;
        transition: box-shadow 0.3s ease, transform 0.3s ease;
        position: relative;
      }

      .card-style::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(to bottom, rgba(255, 255, 255, 0.4), transparent);
        border-top-left-radius: 14px;
        border-top-right-radius: 14px;
        pointer-events: none;
      }

      .card-style .carroussel {
        width: 100%;
        display: flex;
      }

      .card-style .slide {
        flex: 0 0 100%;
        min-width: 100%;
      }
      
      @media (min-width: 1367px) {
        .card-style {
          max-width: 80%;
          margin: 0 auto 40px;
          box-shadow: 
            0 15px 30px rgba(9, 45, 115, 0.2),
            0 8px 16px rgba(9, 45, 115, 0.15),
            0 4px 8px rgba(247, 214, 71, 0.1),
            0 0 0 1px rgba(9, 45, 115, 0.05);
        }
        
        .card-style .slide-content img {
          max-height: 450px;
          width: auto;
          max-width: 100%;
        }
      }
      
      @media (min-width: 769px) and (max-width: 1366px) {
        .card-style {
          max-width: 85%;
          margin: 0 auto 40px;
        }
        
        .card-style .slide-content img {
          max-height: 380px;
          width: auto;
          max-width: 100%;
        }
      }

      @media (max-width: 768px) {
        .card-style {
          margin: 0 auto 40px;
          box-shadow: 
            0 8px 20px rgba(9, 45, 115, 0.18),
            0 4px 10px rgba(9, 45, 115, 0.12),
            0 2px 4px rgba(247, 214, 71, 0.08),
            0 0 0 1px rgba(9, 45, 115, 0.05);
        }
      
        .card-style .slide-content img {
          border-radius: 0;
          width: 100%;
          height: auto;
          object-fit: cover;
        }

        .card-style .seta {
          width: 30px;
          height: 30px;
          font-size: 1.2rem;
          box-shadow: 0 4px 8px rgba(0, 0, 0, 0.25);
        }
      }
    `

    document.head.appendChild(style)

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