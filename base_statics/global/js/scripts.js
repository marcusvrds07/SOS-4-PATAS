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

  function menu_options() {
    menu = document.querySelector('.menu-options')

    menu.classList.toggle("active")
  }
  
  document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("pageInput")
    const prevBtn = document.getElementById("prevPage")
    const nextBtn = document.getElementById("nextPage")
    const form = document.getElementById("pageForm")
    const showAllBtn = document.getElementById("showAll")
    const backToPagedBtn = document.getElementById("backToPaged")
    
    if (backToPagedBtn) {
      backToPagedBtn.addEventListener("click", () => {
        const url = new URL(window.location.href)
        url.searchParams.delete("all")
        url.searchParams.set("p", "1")
        window.location.href = url.toString()
      })
    }    
  
    if (!input) return
  
    const min = Number(input.min)
    const max = Number(input.max)
    const current = Number(input.dataset.current)
    let clickedArrow = false
  
    input.addEventListener("input", () => {
      const val = input.value
      const numeric = val.replace(/[^0-9]/g, "")
      if (numeric === "") {
        input.value = ""
        return
      }
  
      const num = Number(numeric)
  
      if (num >= min && num <= max) {
        input.value = numeric
      } else {
        input.value = input.value.slice(0, -1)
      }
    })
  
    input.addEventListener("keydown", (e) => {
      const val = Number(input.value) || current
      if (e.key === "ArrowUp" && val < max) input.value = val + 1
      if (e.key === "ArrowDown" && val > min) input.value = val - 1
      if (e.key === "Enter") {
        e.preventDefault()
        const page = Number(input.value)
        if (page >= min && page <= max) {
          goToPage(page)
        } else {
          input.value = current
        }
      }
    })
  
    input.addEventListener("blur", () => {
      if (clickedArrow) {
        clickedArrow = false
        return
      }
      const page = Number(input.value)
      if (page && page !== current && page >= min && page <= max) {
        goToPage(page)
      } else {
        input.value = current
      }
    })
  
    if (prevBtn) {
      prevBtn.addEventListener("mousedown", () => (clickedArrow = true))
      prevBtn.addEventListener("click", () => {
        if (current > min) goToPage(current - 1)
      })
    }
  
    if (nextBtn) {
      nextBtn.addEventListener("mousedown", () => (clickedArrow = true))
      nextBtn.addEventListener("click", () => {
        if (current < max) goToPage(current + 1)
      })
    }
  
    if (showAllBtn) {
      showAllBtn.addEventListener("click", () => {
        const url = new URL(window.location.href)
        url.searchParams.delete("p")
        url.searchParams.set("all", "")
        window.location.href = url.toString()
      })
    }
  
    function goToPage(page) {
      const url = new URL(window.location.href)
      url.searchParams.set("p", page)
      url.searchParams.delete("all")
      window.location.href = url.toString()
    }
  })
  