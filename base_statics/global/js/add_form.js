document.addEventListener('DOMContentLoaded', function () {
  var fotoInput = document.getElementById('id_foto');
  var avatar = document.getElementById('avatar');
  if (fotoInput && avatar) {
    fotoInput.addEventListener('change', function () {
      if (this.files && this.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
          avatar.style.backgroundImage = 'url(' + e.target.result + ')';
          avatar.classList.add('image-set');
        };
        reader.readAsDataURL(this.files[0]);
      }
    });
  }
});
