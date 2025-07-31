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