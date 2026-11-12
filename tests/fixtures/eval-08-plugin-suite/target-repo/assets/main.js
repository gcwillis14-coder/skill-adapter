(function () {
  "use strict";
  const btn = document.getElementById("theme-toggle");
  if (btn) {
    btn.addEventListener("click", () => {
      document.documentElement.classList.toggle("dark");
    });
  }
})();
