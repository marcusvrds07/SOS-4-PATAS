// Sessão: Definição da página anterior
document.addEventListener("DOMContentLoaded", function () {
    let previousPage = "{% url 'home:index' %}";
    try {
        if (document.referrer) {
            const urlObj = new URL(document.referrer, window.location.origin);
            urlObj.hash = "adoption";
            previousPage = urlObj.toString();
        }
    } catch (e) {
        console.warn("Referrer inválido. Usando index sem hash.");
    }

    // Sessão: Botões de navegação 
    const voltarBtn = document.getElementById("quero-adotar");
    
    if (voltarBtn) {
        voltarBtn.addEventListener("click", function(e) {
            e.preventDefault();
            window.location.href = previousPage;
        });
    }

    // Sessão: Carrossel e seleção de imagem da galeria
    const mainImage = document.getElementById("mainImage");
    const thumbnails = document.querySelectorAll(".thumbnail");
    const prevBtn = document.querySelector(".prev-btn");
    const nextBtn = document.querySelector(".next-btn");
    if (thumbnails.length > 0) {
        function swapWithThumbnail(idx) {
            if (idx >= 0 && idx < thumbnails.length) {
                const temp = mainImage.src;
                mainImage.src = thumbnails[idx].src;
                thumbnails[idx].src = temp;
            }
        }
        if (prevBtn) {
            prevBtn.addEventListener("click", function() {
                swapWithThumbnail(thumbnails.length - 1);
                const last = thumbnails[thumbnails.length - 1].src;
                for (let i = thumbnails.length - 1; i > 0; i--) {
                    thumbnails[i].src = thumbnails[i - 1].src;
                }
                thumbnails[0].src = last;
            });
        }
        if (nextBtn) {
            nextBtn.addEventListener("click", function() {
                swapWithThumbnail(0);
                const first = thumbnails[0].src;
                for (let i = 0; i < thumbnails.length - 1; i++) {
                    thumbnails[i].src = thumbnails[i + 1].src;
                }
                thumbnails[thumbnails.length - 1].src = first;
            });
        }
        thumbnails.forEach(thumb => {
            thumb.addEventListener("click", function() {
                const temp = mainImage.src;
                mainImage.src = this.src;
                this.src = temp;
            });
        });
    }

    // Sessão: Efeito de scroll
    window.addEventListener("scroll", function() {
        const navbar = document.getElementById("navbar");
        if (window.scrollY > 50) {
            navbar.classList.add("scrolled");
        } else {
            navbar.classList.remove("scrolled");
        }
    });
});

// Sessão: Ajuste responsividade do scroll da galeria
document.addEventListener("DOMContentLoaded", function () {
    const gallery = document.querySelector('.gallery');
    function updatePadding() {
        if (gallery.scrollWidth > gallery.clientWidth) {
            gallery.style.justifyContent = "flex-start";
        } else {
            gallery.style.justifyContent = "center";
        }
    }
    updatePadding();
    window.addEventListener("resize", updatePadding);
});
