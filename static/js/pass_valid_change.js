document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('form').addEventListener('submit', function(event) {
        var newPassword = document.getElementsByName('new_password')[0].value;
        var messages = [];

        if (newPassword.length < 8) {
            messages.push('Password must be at least 8 characters long.');
        }
        if (!/[A-Z]/.test(newPassword)) {
            messages.push('Password must contain at least one uppercase letter.');
        }
        if (!/[0-9]/.test(newPassword)) {
            messages.push('Password must contain at least one digit.');
        }

        if (messages.length > 0) {
            event.preventDefault();
            alert('Validation errors: \n' + messages.join('\n'));
        }
    });
});