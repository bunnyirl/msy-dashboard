// This file goes in the 'assets' folder.
// It adds the 'scrolled' class to the header and logo when you scroll down.

// Wait for the window to load before running the script
window.onload = function() {
    
    // Get the header and logo elements by their IDs
    const header = document.getElementById('app-header');
    const logo = document.getElementById('app-logo');

    // Check if elements exist (good practice)
    if (header && logo) {
        
        // Listen for the 'scroll' event on the window
        window.onscroll = function() {
            
            // Check if the user has scrolled more than 50 pixels down
            // document.documentElement.scrollTop is for cross-browser compatibility
            if (window.scrollY > 50 || document.documentElement.scrollTop > 50) {
                // If scrolled, add the 'scrolled' class
                header.classList.add('scrolled');
                logo.classList.add('scrolled');
            } else {
                // If at the top, remove the 'scrolled' class
                header.classList.remove('scrolled');
                logo.classList.remove('scrolled');
            }
        };
    }
};
