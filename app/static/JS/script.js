// This function toggles the visibility of a password input field and changes the text content of a button to either "Show" or "Hide" based on the current input type.
function togglePasswordVisibility() {
  var passwordInput = document.getElementById("password");
  var toggleButton = passwordInput.nextElementSibling;
  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    toggleButton.textContent = "Hide";
  } else {
    passwordInput.type = "password";
    toggleButton.textContent = "Show";
  }
}
