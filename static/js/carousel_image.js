 document.addEventListener('DOMContentLoaded', function() {
                    const clickableImages = document.querySelectorAll('.clickable-image');

                    clickableImages.forEach(function(img) {
                        img.addEventListener('click', function() {
                            const clickedImageUrl = img.getAttribute('src');
                            const carouselImages = document.querySelectorAll('.carousel-image');
                            carouselImages.forEach(function(carouselImg) {
                                carouselImg.style.display = 'none';
                            });

                            const matchingCarouselImage = Array.from(carouselImages).find(function(carouselImg) {
                                return carouselImg.getAttribute('src') === clickedImageUrl;
                            });

                            if (matchingCarouselImage) {
                                matchingCarouselImage.style.display = '';
                            }
                        });
                    });
                });