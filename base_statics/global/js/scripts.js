function validatePassword() {
    const password = document.getElementById("id_new_password1").value;
  
    const length = password.length >= 8;
    const hasNumber = /\d/.test(password);
    const hasLower = /[a-z]/.test(password);
    const hasUpper = /[A-Z]/.test(password);
    const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

    document.getElementById("length").className = length ? "valid" : "invalid";
    document.getElementById("number").className = hasNumber ? "valid" : "invalid";
    document.getElementById("lowercase").className = hasLower ? "valid" : "invalid";
    document.getElementById("uppercase").className = hasUpper ? "valid" : "invalid";
    document.getElementById("special").className = hasSpecialChar ? "valid" : "invalid";
    isSamePassword()
}

function isSamePassword() {
    const password = document.getElementById("id_new_password1").value;
    const password2 = document.getElementById("id_new_password2").value;
    let isSame = false

    if (password == password2) {
        isSame = true
    }

    document.getElementById("isSame").className = isSame ? "valid" : "invalid";
}


  function togglePasswordVisibility(id, idImg) {
    const input = document.getElementById(id);
    const icon = document.getElementById(idImg);

    if (input.type === "password") {
      input.type = "text";
      icon.src = icon.dataset.hide;
    } else {
      input.type = "password";
      icon.src = icon.dataset.show;
    }
  }

  function activate_adopted_area() {
    // document.body.style.overflow = "hidden";
    modal = document.querySelector('.adopters-modal')
    modal.style.display = 'block'
  }

  function toggleMenu(id, button) {
    var arrow = document.querySelector(".arrow");
    const menu = document.getElementById(id);
    menu.classList.toggle('show');
    button.classList.toggle('open');
    arrow.classList.toggle("rotate");
  }

  function setActive(element) {
    const allItems = document.querySelectorAll('.submenu li');
    allItems.forEach(item => item.classList.remove('active'));
    element.classList.add('active');
  }