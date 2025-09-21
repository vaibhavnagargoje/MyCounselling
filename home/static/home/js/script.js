// Announcement Banner Close
const closeBanner = document.getElementById("closeBanner");
const announcementBanner = document.getElementById("announcementBanner");

if (closeBanner && announcementBanner) {
  closeBanner.addEventListener("click", () => {
    announcementBanner.style.animation = "slideUp 0.3s ease-out";
    setTimeout(() => {
      announcementBanner.style.display = "none";
    }, 300);
  });
}

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
