// document.addEventListener('DOMContentLoaded', function () {
//     document.body.addEventListener('click', function (event) {
//         const btn = event.target.closest('.mark-adopted-btn');
//         if (!btn) return;
//
//         console.log('Botão "Marcar como Adotado" clicado.');
//
//         const modalId = btn.getAttribute('data-modal-id');
//         const animalId = btn.getAttribute('data-id');
//         const modal = document.getElementById(modalId);
//         const modalAnimalId = document.getElementById('modal-animal-id');
//         const confirmarBtn = document.getElementById('confirmar-adocao-btn');
//
//         if (modal && modalAnimalId && confirmarBtn) {
//             modal.classList.remove('hidden');
//             modalAnimalId.value = animalId;
//
//             confirmarBtn.onclick = function () {
//                 document.getElementById('adocao-form').submit();
//             };
//         } else {
//             console.warn('Modal ou elementos não encontrados.');
//         }
//     });
// });