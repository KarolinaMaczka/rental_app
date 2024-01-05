document.getElementById('rentalForm').addEventListener('submit', function(event) {
    var isValid = true;
    var messages = [];
    var maxGuests = document.getElementsByName('max_guests')[0].value;
    var numberOfRooms = document.getElementsByName('number_of_rooms')[0].value;
    var numberOfBathrooms = document.getElementsByName('number_of_bathrooms')[0].value;
    var numberOfBeds = document.getElementsByName('number_of_beds')[0].value;
    var pricePerNight = document.getElementsByName('price_per_night')[0].value;
    var name = document.getElementsByName('name')[0].value;
    var description = document.getElementsByName('description')[0].value;
    var addressCity = document.getElementsByName('address_city')[0].value;
    var addressStreet = document.getElementsByName('address_street')[0].value;

    if (!maxGuests || maxGuests < 1 || maxGuests > 20) messages.push('Max guests must be between 1 and 20.');
    if (!numberOfRooms || numberOfRooms < 1 || numberOfRooms > 50) messages.push('Number of rooms must be between 1 and 50.');
    if (!numberOfBathrooms || numberOfBathrooms < 1 || numberOfBathrooms > 50) messages.push('Number of bathrooms must be between 1 and 50.');
    if (!numberOfBeds || numberOfBeds < 1 || numberOfBeds > 50) messages.push('Number of beds must be between 1 and 50.');
    if (!pricePerNight || pricePerNight < 1 || pricePerNight > 10000) messages.push('Price per night must be reasonable.');
    if (!name.trim() || name.length > 50) messages.push('Name is required and must be less than 50 characters.');
    if (!description.trim() || description.length > 400) messages.push('Description is required and must be less than 400 characters.');
    if (!addressCity.trim() || addressCity.length > 50) messages.push('City is required and must be less than 50 characters.');
    if (!addressStreet.trim() || addressStreet.length > 50) messages.push('Street is required and must be less than 50 characters.');

    var imageInputs = document.querySelectorAll('#imageUploadContainer input[type="file"]');
    var imageAdded = Array.from(imageInputs).some(input => input.files.length > 0);

    if (!imageAdded) {
        messages.push('At least one image must be added.');
    }

    isValid = messages.length === 0;

    if (!isValid) {
        event.preventDefault();
        alert('Validation errors: \n' + messages.join('\n'));
    }
});