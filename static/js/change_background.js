document.addEventListener("DOMContentLoaded", function() {
        var backgroundImages = [
            "url('media/basic/background1.jpg')",
            "url('media/basic/background2.jpg')",
            "url('media/basic/background3.jpg')",
            "url('media/basic/background4.jpg')",
        ];

        var currentBackground = 0;
        setInterval(function() {
            currentBackground = (currentBackground + 1) % backgroundImages.length;
            document.body.style.backgroundImage = backgroundImages[currentBackground];
        }, 6500);
    });