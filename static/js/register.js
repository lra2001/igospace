document.getElementById('registerForm').addEventListener('submit', function (e) {
    e.preventDefault(); // prevent default submission

    // Clear previous errors
    const errorElems = this.querySelectorAll('.error-message');
    errorElems.forEach(el => el.remove());

    const errorBox = document.getElementById("form-errors");
    errorBox.innerHTML = ''; // clear previous top error box

    let isValid = true;
    let errors = [];

    function showError(input, message) {
        isValid = false;
        errors.push(message);

        const error = document.createElement('div');
        error.className = 'error-message';
        error.textContent = message;
        input.parentNode.insertBefore(error, input.nextSibling);
        input.classList.add('input-error'); // highlight field
    }

    // Get form fields
    const { username, password, email, fname, lname, address, phone } = this;

    // Clear old highlights
    [username, password, email, fname, lname, address, phone].forEach(input => {
        input.classList.remove('input-error');
    });

    // Required check
    const fieldLabels = {
        username: "Username",
        password: "Password",
        email: "Email",
        fname: "First name",
        lname: "Last name",
        address: "Address",
        phone: "Phone number"
    };

    // Required check with specific messages
    [username, password, email, fname, lname, address, phone].forEach(field => {
        if (!field.value.trim()) {
            const label = fieldLabels[field.name] || "This field";
            showError(field, `${label} is a required field`);
        }
    });

    // Email format
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (email.value && !emailPattern.test(email.value)) {
        showError(email, 'Please enter a valid email address');
    }

    // Phone: exactly 10 digits
    const phonePattern = /^\d{10}$/;
    if (phone.value && !phonePattern.test(phone.value)) {
        showError(phone, 'Phone number must be exactly 10 digits');
    }

    // Password: strong
    const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;
    if (password.value && !passwordPattern.test(password.value)) {
        showError(password, 'Password must be at least 8 characters long and include uppercase, lowercase, number, and special character');
    }

    // Show error summary at top
    if (!isValid) {
        errorBox.innerHTML = errors.map(err => `<p>${err}</p>`).join("");
        return;
    }

    // All good
    this.submit();
});