 document.addEventListener('DOMContentLoaded', function() {
        var resetPasswordForm = document.querySelector('form');

        resetPasswordForm.addEventListener('submit', function(event) {
            var newPassword = document.querySelector('input[name="new_password"]').value;
            var confirmPassword = document.querySelector('input[name="confirm_password"]').value;
            var errorMessage = '';
            if (newPassword !== confirmPassword) {
                errorMessage += 'Passwords do not match.\n';
            }
            if (newPassword.length < 8) {
                errorMessage += 'Password must be at least 8 characters long.\n';
            }
            if (!/[A-Z]/.test(newPassword)) {
                errorMessage += 'Password must contain at least one uppercase letter.\n';
            }
            if (!/\d/.test(newPassword)) {
                errorMessage += 'Password must contain at least one digit.\n';
            }
            if (errorMessage.length > 0) {
                event.preventDefault();
                alert(errorMessage);
            }
        });
    });