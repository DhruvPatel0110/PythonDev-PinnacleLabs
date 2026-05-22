document.addEventListener("DOMContentLoaded", () => {
  const roleInputs = Array.from(document.querySelectorAll("input[name='role']"));
  const roleSections = Array.from(document.querySelectorAll("[data-role-fields]"));

  const syncRoleFields = () => {
    const selectedRole = roleInputs.find((input) => input.checked)?.value || "customer";

    roleSections.forEach((section) => {
      const isActive = section.dataset.roleFields === selectedRole;
      section.classList.toggle("is-visible", isActive);
      section.hidden = !isActive;

      section.querySelectorAll("[data-role-required]").forEach((field) => {
        field.required = field.dataset.roleRequired === selectedRole;
      });
    });
  };

  roleInputs.forEach((input) => input.addEventListener("change", syncRoleFields));
  syncRoleFields();

  document.querySelectorAll("[data-toggle-password]").forEach((button) => {
    button.addEventListener("click", () => {
      const target = document.getElementById(button.dataset.togglePassword);
      if (!target) {
        return;
      }

      const shouldShow = target.type === "password";
      target.type = shouldShow ? "text" : "password";
      button.textContent = shouldShow ? "Hide" : "Show";
      button.setAttribute("aria-label", shouldShow ? "Hide password" : "Show password");
    });
  });

  const registerForm = document.querySelector("form[action$='/register']");
  if (registerForm) {
    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirm_password");

    const validatePasswords = () => {
      if (!password || !confirmPassword) {
        return;
      }

      const mismatch = password.value && confirmPassword.value && password.value !== confirmPassword.value;
      confirmPassword.setCustomValidity(mismatch ? "Passwords do not match." : "");
    };

    password?.addEventListener("input", validatePasswords);
    confirmPassword?.addEventListener("input", validatePasswords);
    registerForm.addEventListener("submit", validatePasswords);
  }
});
