(function() {
    var style = document.createElement('style');
    style.innerHTML = '* { opacity: 0 !important; }';
    document.head.appendChild(style);

    window.addEventListener('load', function() {
        style.innerHTML = '* { opacity: 1; transition: opacity 0.35s; }';
    });
})();

document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('a[href]');

    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const destination = this.href;

            fadeOutAllElements();

            setTimeout(() => {
                window.location.href = destination;
            }, 250);
        });
    });
});

function fadeOutAllElements() {
    const elements = document.querySelectorAll('*');
    elements.forEach(el => {
        let opacity = 1;
        const fadeEffect = setInterval(() => {
            if (opacity <= 0.1) {
                clearInterval(fadeEffect);
                el.style.opacity = 0;
            } else {
                opacity -= 0.1;
                el.style.opacity = opacity;
            }
        }, 50);
    });
}




