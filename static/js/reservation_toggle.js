   document.querySelectorAll('.reservation-toggle').forEach(button => {
    button.addEventListener('click', function() {
        this.classList.toggle('active');
        var details = this.parentElement.nextElementSibling;
        if (details.style.display === "block") {
            details.style.display = "none";
            this.innerHTML = '<i class="fas fa-chevron-down"></i>';
        } else {
            details.style.display = "block";
            this.innerHTML = '<i class="fas fa-chevron-up"></i>';
        }
    });
});