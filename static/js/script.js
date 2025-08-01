document.querySelectorAll('.remove-icon').forEach(function(btn) {
  btn.addEventListener('click', function() {
    var itemId = btn.getAttribute('data-item-id');
    var checkbox = document.getElementById('remove-' + itemId);
    if (checkbox) {
      checkbox.checked = true;

      btn.closest('form').submit();
    }
  });
});

// Get elements for thumbnail and modal
if (document.querySelector('.thumbnail')) {
const modal = document.getElementById("imageModal");
const modalImg = document.getElementById("modalImage");
const closeBtn = document.querySelector(".close");

document.querySelectorAll('.thumbnail').forEach((img) => {
  img.addEventListener('click', () => {
    const fullSrc = img.getAttribute('data-full');
    modalImg.src = fullSrc;
    modal.style.display = "block";
  });
});

closeBtn.onclick = () => {
  modal.style.display = "none";
};

window.onclick = (event) => {
  if (event.target === modal) {
    modal.style.display = "none";
  }
};
}