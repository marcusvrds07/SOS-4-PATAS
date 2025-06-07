// Sessão: Controle responsivo do menu hambúrguer
document.addEventListener("DOMContentLoaded", () => {
  const menuToggle = document.getElementById("menu-toggle")
  const navMenu = document.getElementById("nav-menu")

    window.addEventListener("scroll", function() {
        const navbar = document.getElementById("navbar");
        if (window.scrollY > 50) {
            navbar.classList.add("scrolled");
        } else {
            navbar.classList.remove("scrolled");
        }
    });

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

  if (menuToggle && navMenu) {
    menuToggle.addEventListener("click", e => {
      e.stopPropagation()
      navMenu.classList.toggle("active")
      const spans = menuToggle.querySelectorAll("span")
      if (navMenu.classList.contains("active")) {
        spans[0].style.transform = "rotate(45deg) translate(5px, 5px)"
        spans[1].style.opacity = "0"
        spans[2].style.transform = "rotate(-45deg) translate(7px, -6px)"
      } else {
        resetHamburgerIcon(spans)
      }
    })

    navMenu.querySelectorAll("a").forEach(link => {
      link.addEventListener("click", closeHamburger)
    })
  }

  document.addEventListener("click", event => {
    if (
      menuToggle && navMenu &&
      !menuToggle.contains(event.target) &&
      !navMenu.contains(event.target)
    ) {
      closeHamburger()
    }
  })

  window.addEventListener("scroll", closeHamburger)
})
