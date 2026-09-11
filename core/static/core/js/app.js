const root = document.documentElement;
const themeToggle = document.getElementById("theme-toggle");

const savedTheme = localStorage.getItem("lixdex-theme");
if (savedTheme === "light" || savedTheme === "dark") {
    root.setAttribute("data-theme", savedTheme);
}

if (themeToggle) {
    themeToggle.addEventListener("click", () => {
        const current = root.getAttribute("data-theme") || "dark";
        const next = current === "dark" ? "light" : "dark";
        root.setAttribute("data-theme", next);
        localStorage.setItem("lixdex-theme", next);
    });
}
