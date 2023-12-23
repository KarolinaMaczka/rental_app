(function() {
    var style = document.createElement('style');
    style.innerHTML = '* { opacity: 0 !important; }';
    document.head.appendChild(style);

    window.addEventListener('load', function() {
        style.innerHTML = '* { opacity: 1; transition: opacity 0.35s; }';
    });
})();

document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('a[href]'); // Select all links

    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault(); // Prevent the default link behavior
            const destination = this.href; // Store the URL to navigate to

            // Apply the fade-out effect to all elements
            fadeOutAllElements();

            // Wait for the fade-out to complete before navigating
            setTimeout(() => {
                window.location.href = destination;
            }, 250); // This timeout should be the duration of the fade-out
        });
    });
});

function fadeOutAllElements() {
    const elements = document.querySelectorAll('*');
    elements.forEach(el => {
        let opacity = 1; // initial opacity
        const fadeEffect = setInterval(() => {
            if (opacity <= 0.1) {
                clearInterval(fadeEffect);
                el.style.opacity = 0;
            } else {
                opacity -= 0.1;
                el.style.opacity = opacity;
            }
        }, 50); // adjust this value to control the speed of the fade-out
    });
}




