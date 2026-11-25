// Set date fields to today or later, and show a lightweight submit confirmation.
const dateField = document.getElementById("reportDate");
if (dateField) {
  const today = new Date();
  dateField.max = today.toISOString().slice(0, 10);
}
document.querySelectorAll("form").forEach(form => {
  form.addEventListener("submit", () => {
    const button = form.querySelector("button[type='submit'], button:not([type])");
    if (button && !button.disabled) {
      button.dataset.original = button.textContent;
      button.textContent = "Submitting…";
    }
  });
});