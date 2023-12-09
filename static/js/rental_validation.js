document.getElementById('rentalForm').addEventListener('submit', function(event) {
        var isValid = true;
        var maxGuests = document.getElementsByName('max_guests')[0].value;
        var numberOfRooms = document.getElementsByName('number_of_rooms')[0].value;
        var numberOfBathrooms = document.getElementsByName('number_of_bathrooms')[0].value;
        var numberOfBeds = document.getElementsByName('number_of_beds')[0].value;
        var pricePerNight = document.getElementsByName('price_per_night')[0].value;

        if (maxGuests < 1 || maxGuests >= 10) isValid = false;
        if (numberOfRooms < 0 || numberOfRooms >= 100) isValid = false;
        if (numberOfBathrooms < 0 || numberOfBathrooms >= 100) isValid = false;
        if (numberOfBeds < 0 || numberOfBeds >= 100) isValid = false;
        if (pricePerNight < 0 || pricePerNight >= 100000) isValid = false;

        if (!isValid) {
            event.preventDefault();
            alert('Validation errors. Please check your inputs.');
        }
    });