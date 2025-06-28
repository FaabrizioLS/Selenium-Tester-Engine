document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("formulario-completo");

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    const data = new FormData(form);
    console.log("Formulario enviado:");
    for (let [name, value] of data.entries()) {
      console.log(`${name}: ${value}`);
    }
    alert("Formulario enviado (ver consola para datos)");
  });

  const toggleButton = document.getElementById("toggle-dark-mode");

  toggleButton.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    toggleButton.textContent = document.body.classList.contains("dark-mode")
      ? "Desactivar modo oscuro"
      : "Activar modo oscuro";
  });
});
