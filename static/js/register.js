const registerForm = document.getElementById('registerForm');

if (registerForm) {
  registerForm.addEventListener('submit', function(e) {
    e.preventDefault(); // Only load on the register page

  // Clear previous error messages and styles
  const errorElems = this.querySelectorAll('.error-message');
  errorElems.forEach(el => el.remove());
  const inputs = [this.username, this.password, this.email, this.fname, this.lname, this.address, this.phone];
  inputs.forEach(input => input.classList.remove('input-error'));

  let isValid = true;

  function getLabelText(input) {
      const label = document.querySelector(`label[for="${input.id}"]`);
      return label ? label.textContent : input.name;
    }

  function showError(input, message) {
    isValid = false;
    input.classList.add('input-error');
    const error = document.createElement('div');
    error.className = 'error-message';
    error.style.color = '#ff4c4c';
    error.style.fontSize = '0.9em';
    error.textContent = message;
    input.parentNode.insertBefore(error, input.nextSibling);
  }

  // Required fields check
  inputs.forEach(field => {
    if (!field.value.trim()) {
      showError(field, `${getLabelText(field)} is required`);
    }
  });

  // Email format check
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (this.email.value && !emailPattern.test(this.email.value)) {
    showError(this.email, 'Please enter a valid email address');
  }

  // Phone number check: exactly 10 digits only
  const phonePattern = /^\d{10}$/;
  if (this.phone.value && !phonePattern.test(this.phone.value)) {
    showError(this.phone, 'Phone number must be exactly 10 digits');
  }

  // Password strength check
  const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_\-+=\[\]{};:'",.<>?/\\|`~]).{8,}$/;
  if (this.password.value && !passwordPattern.test(this.password.value)) {
    showError(this.password, 'Password must be at least 8 characters long and include uppercase, lowercase, number, and special character.');
  }

  if (isValid) {
    this.submit();
  }
 });
}