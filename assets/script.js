document.addEventListener('DOMContentLoaded', function() {

    setTimeout(function() {
        const header = document.getElementById('app-header');
        const logo = document.getElementById('app-logo');

        //check if elements exist 
        if (header && logo) {
            
            //check for scroll on page
            window.onscroll = function() {
                
                //check if the user has scrolled more than 50 pixels down
                if (window.scrollY > 50 || document.documentElement.scrollTop > 50) {
                    //if scrolled at scrolled class
                    header.classList.add('scrolled');
                    logo.classList.add('scrolled');
                } else {
                    // If at the top, remove scrolled class
                    header.classList.remove('scrolled');
                    logo.classList.remove('scrolled');
                }
            };
        } else {
            //if the script runs but can't find the elements
            console.error("Header (app-header) or Logo (app-logo) elements not found. Dash might still be loading.");
        }
    }, 100); 
});
