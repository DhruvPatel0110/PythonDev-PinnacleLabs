(function () {
  const TOAST_DURATION_MS = 2800;

  function getContainer() {
    let container = document.getElementById("toastContainer");
    if (!container) {
      container = document.createElement("div");
      container.id = "toastContainer";
      container.className = "toast-container";
      container.setAttribute("aria-live", "polite");
      container.setAttribute("aria-atomic", "true");
      document.body.appendChild(container);
    }
    return container;
  }

  window.showToast = function (message, category) {
    const type = category || "success";
    const container = getContainer();
    const toast = document.createElement("div");
    toast.className = `toast-alert toast-alert--${type}`;
    toast.setAttribute("role", "alert");
    toast.textContent = message;
    container.appendChild(toast);

    requestAnimationFrame(function () {
      toast.classList.add("toast-alert--visible");
    });

    window.setTimeout(function () {
      toast.classList.remove("toast-alert--visible");
      window.setTimeout(function () {
        toast.remove();
      }, 300);
    }, TOAST_DURATION_MS);
  };
})();
