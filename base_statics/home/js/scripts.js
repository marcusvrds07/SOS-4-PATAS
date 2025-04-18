var customSelect = document.getElementById("customSelect");
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