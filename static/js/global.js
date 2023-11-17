window.addEventListener('scroll', function() {
    var header = document.getElementsByTagName('header')[0];
    var scrollPosition = window.scrollY;

    // Adjust this value based on when you want the navigation to become fixed
    var threshold = 100;

    if (scrollPosition > threshold) {
        header.classList.add('fixed');
    } else {
        header.classList.remove('fixed');
    }
});
