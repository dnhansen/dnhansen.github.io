const tocLinks = document.querySelectorAll(".table-of-contents a");
const headingIds = Array.from(tocLinks).map(link => decodeURIComponent(link.getAttribute("href").slice(1)));
const headings = headingIds
  .map(id => document.getElementById(id))
  .filter(Boolean);

const observerOptions = {
  rootMargin: "0px 0px -70% 0px",
  threshold: 0
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    const id = entry.target.id;
    const link = document.querySelector(`.table-of-contents a[href="#${id}"]`);

    if (entry.isIntersecting && link) {
      tocLinks.forEach(l => l.classList.remove("active"));
      link.classList.add("active");

      // Auto-scroll the active link into view if needed
      const container = document.querySelector("nav");
      const linkTop = link.offsetTop;
      const linkBottom = linkTop + link.offsetHeight;
      const containerScrollTop = container.scrollTop;
      const containerHeight = container.clientHeight;

      if (linkTop < containerScrollTop || linkBottom > containerScrollTop + containerHeight) {
        link.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
    }
  });
}, observerOptions);

headings.forEach(h => observer.observe(h));