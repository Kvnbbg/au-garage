// This function toggles the visibility of a password input field and changes the text content of a button to either "Show" or "Hide" based on the current input type.
function togglePasswordVisibility() {
  var passwordInput = document.getElementById("password");
  var toggleIcon = passwordInput.nextElementSibling;
  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    toggleIcon.classList.remove("fa-eye");
    toggleIcon.classList.add("fa-eye-slash");
  } else {
    passwordInput.type = "password";
    toggleIcon.classList.remove("fa-eye-slash");
    toggleIcon.classList.add("fa-eye");
  }
}
