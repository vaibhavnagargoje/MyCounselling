// Batch Dropdown Functionality
const batchDropdown = document.getElementById("batchDropdown");
const batchMenu = document.getElementById("batchMenu");
const dropdownIcon = document.getElementById("dropdownIcon");
const selectedBatch = document.getElementById("selectedBatch");
const batchOptions = document.querySelectorAll(".batch-option");

if (batchDropdown) {
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
}

// Mobile Menu Functionality
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const mobileMenu = document.getElementById('mobile-menu');
const mobileMenuClose = document.getElementById('mobile-menu-close');

if (mobileMenuBtn && mobileMenu && mobileMenuClose) {
    mobileMenuBtn.addEventListener('click', () => {
        mobileMenu.classList.add('active');
    });

    mobileMenuClose.addEventListener('click', () => {
        mobileMenu.classList.remove('active');
    });

    // Close mobile menu when clicking on links
    const mobileLinks = mobileMenu.querySelectorAll('a');
    mobileLinks.forEach(link => {
        link.addEventListener('click', () => {
            mobileMenu.classList.remove('active');
        });
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!mobileMenu.contains(e.target) && !mobileMenuBtn.contains(e.target) && mobileMenu.classList.contains('active')) {
            mobileMenu.classList.remove('active');
        }
    });
}
