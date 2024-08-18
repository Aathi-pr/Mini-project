document.querySelector(".toggle-button").addEventListener("click", function () {
  var navLinks = document.querySelector(".nvLinks ul");
  navLinks.style.display =
    navLinks.style.display === "block" ? "none" : "block";
});
