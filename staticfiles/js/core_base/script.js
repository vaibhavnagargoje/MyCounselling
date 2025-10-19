// Batch Dropdown Functionality
const batchDropdown = document.getElementById("batchDropdown");
const batchMenu = document.getElementById("batchMenu");
const dropdownIcon = document.getElementById("dropdownIcon");
const selectedBatch = document.getElementById("selectedBatch");
const batchOptions = document.querySelectorAll(".batch-option");

batchDropdown.addEventListener("click", () => {
  batchMenu.classList.toggle("active");
  dropdownIcon.classList.toggle("rotate-180");
});

batchOptions.forEach((option) => {
  option.addEventListener("click", (e) => {
    e.preventDefault();
    const batchName = option.getAttribute("data-batch");
    selectedBatch.textContent = batchName;
    batchMenu.classList.remove("active");
    dropdownIcon.classList.remove("rotate-180");
  });
});

// Close dropdown when clicking outside
document.addEventListener("click", (e) => {
  if (!batchDropdown.contains(e.target)) {
    batchMenu.classList.remove("active");
    dropdownIcon.classList.remove("rotate-180");
  }
});
