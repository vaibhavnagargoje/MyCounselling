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

// Announcement Banner Close
const closeBanner = document.getElementById("closeBanner");
const announcementBanner = document.getElementById("announcementBanner");

closeBanner.addEventListener("click", () => {
  announcementBanner.style.animation = "slideUp 0.3s ease-out";
  setTimeout(() => {
    announcementBanner.style.display = "none";
  }, 300);
});

// Sidebar Active State
const sidebarItems = document.querySelectorAll(".sidebar-item");
sidebarItems.forEach((item) => {
  item.addEventListener("click", function (e) {
    // Only handle the active state, don't prevent default navigation
    sidebarItems.forEach((i) => i.classList.remove("active"));
    item.classList.add("active");

    // Allow the default navigation to proceed
    // No preventDefault() here
  });
});

// Animation on Scroll
const observerOptions = {
  threshold: 0.1,
  rootMargin: "0px 0px -50px 0px",
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = "1";
      entry.target.style.transform = "translateY(0)";
    }
  });
}, observerOptions);

// Observe animated elements
document
  .querySelectorAll(
    ".animate-fade-in-up, .animate-fade-in-left, .animate-fade-in-right"
  )
  .forEach((el) => {
    el.style.opacity = "0";
    el.style.transform = "translateY(30px)";
    observer.observe(el);
  });

// Initialize animations
document.addEventListener("DOMContentLoaded", function () {
  // Trigger animations after a short delay
  setTimeout(() => {
    document
      .querySelectorAll(
        ".animate-fade-in-up, .animate-fade-in-left, .animate-fade-in-right"
      )
      .forEach((el) => {
        el.style.opacity = "1";
        el.style.transform = "translateY(0)";
      });
  }, 100);
});
