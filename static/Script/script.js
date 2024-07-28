const hamburger = document.querySelector(".hamburger");
const navMenu = document.querySelector("nav ul");
const dropdowns = document.querySelectorAll(".dropdown");

hamburger.addEventListener("click", () => {
  hamburger.classList.toggle("active");
  navMenu.classList.toggle("active");
});

dropdowns.forEach((dropdown) => {
  const dropdownLink = dropdown.querySelector("a");
  const dropdownContent = dropdown.querySelector(".dropdown-content");

  dropdownLink.addEventListener("click", (e) => {
    if (window.innerWidth <= 968) {
      e.preventDefault();

      // Close all other dropdowns
      dropdowns.forEach((otherDropdown) => {
        if (otherDropdown !== dropdown) {
          otherDropdown
            .querySelector(".dropdown-content")
            .classList.remove("active");
        }
      });

      // Toggle the clicked dropdown
      dropdownContent.classList.toggle("active");
    }
  });
});

// Close dropdowns when clicking outside
document.addEventListener("click", (e) => {
  if (window.innerWidth <= 968 && !e.target.closest(".dropdown")) {
    dropdowns.forEach((dropdown) => {
      dropdown.querySelector(".dropdown-content").classList.remove("active");
    });
  }
});
document.querySelectorAll("nav ul li a").forEach((n) =>
  n.addEventListener("click", () => {
    if (!n.parentElement.classList.contains("dropdown")) {
      hamburger.classList.remove("active");
      navMenu.classList.remove("active");
    }
  })
);

// Scroll functionality
let lastScrollTop = 0;
const navbar = document.getElementById("navbar");
const scrollThreshold = 100;

window.addEventListener("scroll", function () {
  let scrollTop = window.pageYOffset || document.documentElement.scrollTop;

  if (scrollTop > lastScrollTop && scrollTop > scrollThreshold) {
    // Scrolling down
    navbar.style.top = `-${navbar.offsetHeight}px`;
  } else {
    // Scrolling up
    navbar.style.top = "0";
  }

  lastScrollTop = scrollTop;
});


const searchBar = document.getElementById("mainSearchBar");
      const suggestionsBox = document.getElementById("suggestions");
      const searchForm = document.getElementById("searchForm");

      searchBar.addEventListener("input", async (e) => {
        const query = e.target.value;
        if (query.length > 2) {
          const response = await fetch(
            `/api/suggestions?query=${encodeURIComponent(query)}`
          );
          const suggestions = await response.json();
          displaySuggestions(suggestions);
        } else {
          suggestionsBox.innerHTML = "";
        }
      });

      function displaySuggestions(suggestions) {
        suggestionsBox.innerHTML = "";
        suggestions.forEach((item) => {
          const div = document.createElement("div");
          div.textContent = `${item.name} (${item.type})`;
          div.setAttribute("data-type", item.type.toLowerCase());
          div.addEventListener("click", () => {
            searchBar.value = item.name;
            suggestionsBox.innerHTML = "";
            searchForm.submit();
          });
          suggestionsBox.appendChild(div);
        });
      }

      searchForm.addEventListener("submit", (e) => {
        e.preventDefault();
        if (searchBar.value.trim()) {
          searchForm.submit();
        }
      });