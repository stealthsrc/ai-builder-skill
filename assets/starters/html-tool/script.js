const input = document.querySelector("#input-text");
const output = document.querySelector("#output-text");
const button = document.querySelector("#run-button");

button.addEventListener("click", () => {
  const value = input.value.trim();
  output.textContent = value ? `Processed input:\n\n${value}` : "Nothing to process yet.";
});
