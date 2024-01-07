document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.standard-form').addEventListener('submit', function(event) {
        var username = document.getElementsByName('username')[0].value;
        var firstName = document.getElementsByName('first_name')[0].value;
        var surname = document.getElementsByName('surname')[0].value;
        var email = document.getElementsByName('email')[0].value;
        var password = document.getElementsByName('password')[0].value;
        var messages = [];

        if (!username.trim()) messages.push('Username is required.');
        if (!firstName.trim()) messages.push('Name is required.');
        if (!surname.trim()) messages.push('Surname is required.');

        if (!email.trim()) {
            messages.push('Email is required.');
        } else if (!/\S+@\S+\.\S+/.test(email)) {
            messages.push('Email is invalid.');
        }

        if (!password) {
            messages.push('Password is required.');
        } else {
            if (password.length < 8) messages.push('Password must be at least 8 characters long.');
            if (!/[A-Z]/.test(password)) messages.push('Password must contain at least one uppercase letter.');
            if (!/[0-9]/.test(password)) messages.push('Password must contain at least one digit.');
        }

        if (messages.length > 0) {
            event.preventDefault();
            alert('Validation errors:\n' + messages.join('\n'));
        }
    });
});