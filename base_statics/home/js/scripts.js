var customSelect = document.getElementById("customSelect");
if (customSelect) {
  var selectedOption = customSelect.querySelector(".selected-option");
  var selectText = customSelect.querySelector("#select-text");
  var arrow = customSelect.querySelector(".arrow");
  var options = customSelect.querySelector(".options");
  var optionItems = options.querySelectorAll(".option");
  
  selectedOption.addEventListener("click", function () {
    options.classList.toggle("open");
    arrow.classList.toggle("rotate");
  });
  
  optionItems.forEach(function (item) {
    item.addEventListener("click", function (event) {
      selectText.firstChild.textContent = event.target.textContent;
    });   
  });
  
  document.addEventListener("click", function (event) {
    if (!customSelect.contains(event.target)) {
      options.classList.remove("open");
      arrow.classList.remove("rotate");
    }
  });
}

const carroussel = document.getElementById("carroussel");
const slides = carroussel.querySelectorAll(".slide");

let index = 0;

function updateCarroussel() {
  const width = carroussel.clientWidth;
  carroussel.style.transform = `translateX(-${index * width}px)`;
}

function nextSlide() {
  index = (index + 1) % slides.length;
  updateCarroussel();
}

function prevSlide() {
  index = (index - 1 + slides.length) % slides.length;
  updateCarroussel();
}

setInterval(nextSlide, Listener("resize", updateCarroussel));


const navbar = document.getElementById('navbar');
    const trigger = document.getElementById('carroussel');

    window.addEventListener('scroll', () => {
      const triggerBottom = trigger.getBoundingClientRect().bottom;

      if (triggerBottom <= 90) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    });