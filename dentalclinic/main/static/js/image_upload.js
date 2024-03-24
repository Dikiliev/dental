document.addEventListener('DOMContentLoaded', function() {
  const fileInput = document.getElementById('file-upload');
  const imageShow = document.getElementById('image-show');

  fileInput.addEventListener('change', function() {
    if (this.files && this.files[0]) {
      const src = URL.createObjectURL(this.files[0]);
      imageShow.src = src;
    }
  });
});
