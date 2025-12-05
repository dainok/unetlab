/**
* This script enables closing Bootstrap dropdowns by clicking on a close button inside them.
* It supports multiple dropdowns on the same page and ensures that only the correct dropdown is closed.
*
* Usage requirements:
* - Each dropdown toggle must have the attribute: data-bs-toggle="dropdown"
* - Each close button must have the attribute: data-bs-dismiss="dropdown"
* - The close button must be inside a .dropdown container
*/

document.addEventListener("DOMContentLoaded", function () {
    // Select all close buttons that should dismiss a dropdown
    const closeButtons = document.querySelectorAll('.btn[data-bs-dismiss="dropdown"]');

    closeButtons.forEach(closeBtn => {
        closeBtn.addEventListener("click", function () {
            // Find the nearest parent dropdown container
            const dropdown = closeBtn.closest(".dropdown");

            if (!dropdown) return; // Exit if no dropdown parent is found

            // Find the toggle element that controls this dropdown (usually an <a> with data-bs-toggle)
            const toggle = dropdown.querySelector('[data-bs-toggle="dropdown"]');

            if (!toggle) return; // Exit if toggle is not found

            // Get the Bootstrap Dropdown instance or create one if it doesn't exist
            const dropdownInstance = bootstrap.Dropdown.getOrCreateInstance(toggle);

            // Programmatically hide the dropdown
            dropdownInstance.hide();
        });
    });
});


/**
 * Switch between light and dark theme.
 *
 * Usage requirements:
 * - Switch A tag must have onclick=toggleTheme()
 */

function toggleTheme() {
    // Switch between light and dark theme.

    const root = document.documentElement;
    const current = root.getAttribute("data-bs-theme");
    const next = current === "dark" ? "light" : "dark";

    // Switch theme
    root.setAttribute("data-bs-theme", next);

    // Save the current theme in the browser
    localStorage.setItem("theme", next);
}

(function() {
    // Load saved theme
    const saved = localStorage.getItem("theme");
    if (saved) {
        // Apply saved theme
        document.documentElement.setAttribute("data-bs-theme", saved);
    }
})();
