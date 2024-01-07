
    document.getElementById('city-input').addEventListener('change', function() {
        var optionFound = false,
            datalist = this.list;

        if (this.value === '') {
            this.setCustomValidity('');
            return;
        }

        for (var j = 0; j < datalist.options.length; j++) {
            if (this.value == datalist.options[j].value) {
                optionFound = true;
                break;
            }
        }
        if (optionFound) {
            this.setCustomValidity('');
        } else {
            this.setCustomValidity('Please select a valid city');
        }
    });

    function updateCarousel(rentalId) {
        var images = document.querySelectorAll('#' + rentalId + ' .carousel-image');
        images.forEach((img, index) => {
            img.style.display = index === window['currentImageIndex_' + rentalId] ? 'block' : 'none';
        });
    }

    function nextImage(rentalId) {
        if (window['currentImageIndex_' + rentalId] === undefined) window['currentImageIndex_' + rentalId] = 0;
        var images = document.querySelectorAll('#' + rentalId + ' .carousel-image');
        window['currentImageIndex_' + rentalId] = (window['currentImageIndex_' + rentalId] + 1) % images.length;
        updateCarousel(rentalId);
    }

    function prevImage(rentalId) {
        if (window['currentImageIndex_' + rentalId] === undefined) window['currentImageIndex_' + rentalId] = 0;
        var images = document.querySelectorAll('#' + rentalId + ' .carousel-image');
        window['currentImageIndex_' + rentalId] = (window['currentImageIndex_' + rentalId] - 1 + images.length) % images.length;
        updateCarousel(rentalId);
    }
