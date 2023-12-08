function togglePasswordVisibility(id) {
    console.log('togglePasswordVisibility called with id:', id);
    var passwordInput = document.getElementById(id);
    console.log('passwordInput:', passwordInput);

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
    console.log('passwordInput.type after toggle:', passwordInput.type);
}