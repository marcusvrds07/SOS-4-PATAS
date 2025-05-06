document.addEventListener("DOMContentLoaded", function () {
  const menuToggle = document.getElementById("menu-toggle");
  const navMenu = document.getElementById("nav-menu");
  const selectedOption = document.querySelector('.selected-option');
  const options = document.querySelector('.options');
  const arrow = document.querySelector('.arrow');
  const navbar = document.getElementById("navbar");
  const carroussel = document.getElementById('carroussel');
  const slides = document.querySelectorAll('.slide');

  let slideIndex = 0;

  function resetHamburgerIcon(spans) {
    spans[0].style.transform = "none";
    spans[1].style.opacity = "1";
    spans[2].style.transform = "none";
  }

  function closeHamburger() {
    if (navMenu && navMenu.classList.contains("active")) {
      navMenu.classList.remove("active");
      const spans = menuToggle.querySelectorAll("span");
      resetHamburgerIcon(spans);
    }
  }

  function closeSelect() {
    if (options && options.classList.contains('open')) {
      options.classList.remove('open');
      if (arrow) arrow.classList.remove('rotate');
    }
  }

  if (menuToggle && navMenu) {
    menuToggle.addEventListener("click", function (e) {
      e.stopPropagation();
      navMenu.classList.toggle("active");
      const spans = this.querySelectorAll("span");

      if (navMenu.classList.contains("active")) {
        spans[0].style.transform = "rotate(45deg) translate(5px, 5px)";
        spans[1].style.opacity = "0";
        spans[2].style.transform = "rotate(-45deg) translate(7px, -6px)";
      } else {
        resetHamburgerIcon(spans);
      }
    });

    navMenu.querySelectorAll("a").forEach(link => {
      link.addEventListener("click", () => {
        closeHamburger();
      });
    });
  }

  if (selectedOption) {
    selectedOption.addEventListener('click', function (e) {
      e.stopPropagation();
      options.classList.toggle('open');
      arrow.classList.toggle('rotate');
    });
  }

  if (carroussel) {
    function showSlide(n) {
      slideIndex = n;
      carroussel.style.transform = `translateX(-${slideIndex * 100}%)`;
    }

    window.nextSlide = function () {
      slideIndex = (slideIndex + 1) % slides.length;
      showSlide(slideIndex);
    };

    window.prevSlide = function () {
      slideIndex = (slideIndex - 1 + slides.length) % slides.length;
      showSlide(slideIndex);
    };

    setInterval(window.nextSlide, 5000);
  }

  window.addEventListener("scroll", function () {
    if (navbar) {
      navbar.classList.toggle("scrolled", window.scrollY > 50);
    }

    closeHamburger();
    closeSelect();
  });

  document.addEventListener("click", function (event) {
    if (!menuToggle.contains(event.target) && !navMenu.contains(event.target)) {
      closeHamburger();
    }

    if (!selectedOption.contains(event.target) && !options.contains(event.target)) {
      closeSelect();
    }
  });
});
