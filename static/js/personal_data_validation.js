document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.standard-form').addEventListener('submit', function(event) {
        var isValid = true;
        var messages = [];

        var address = document.getElementsByName('address')[0].value;
        var phoneNumber = document.getElementsByName('phone_number')[0].value;

        if (!address.trim()) {
            messages.push('Address is required.');
            isValid = false;
        }

        if (!phoneNumber.trim()) {
            messages.push('Phone number is required.');
            isValid = false;
        } else if (!/^\+\d{2} \d{3} \d{3} \d{3}$/.test(phoneNumber)) {
            messages.push('Phone number is invalid. Necessary format: +xx xxx xxx xxx');
            isValid = false;
        }

        if (!isValid) {
            event.preventDefault();
            alert('Validation errors:\n' + messages.join('\n'));
        }
    });
});