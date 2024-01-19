document.getElementById('reservationForm').addEventListener('submit', function(event) {
        var startDate = new Date(document.getElementsByName('start_date')[0].value);
        var endDate = new Date(document.getElementsByName('end_date')[0].value);
        var today = new Date();
        today.setHours(0, 0, 0, 0);

        if (startDate < today) {
            event.preventDefault();
            alert('Start date must be after today.');
        } else if (endDate <= startDate) {
            event.preventDefault();
            alert('End date must be after start date.');
        }
    });

    document.addEventListener('DOMContentLoaded', function() {
        var rentalId = document.getElementById('reservationForm').getAttribute('data-rental-id');

        fetch('/get_booked_dates/' + rentalId)
            .then(response => response.json())
            .then(data => {
                let bookedDates = data.booked_dates;
                let datepickerOptions = {
                    beforeShowDay: function(date) {
                        var today = new Date();
                        today.setHours(0, 0, 0, 0);
                        var startDate = new Date(document.getElementsByName('start_date')[0].value);

                        for (let i = 0; i < bookedDates.length; i++) {
                            let start = new Date(bookedDates[i].start_date);
                            let end = new Date(bookedDates[i].end_date);
                            if (date >= start && date <= end) {
                                return [false];
                            }
                        }
                        if (date < today || date <= startDate){
                            return [false]
                        }
                        return [true];
                    },
                    onSelect: function() {
                        updateTotalCost();
                    }
                };
                $(".datepicker").datepicker(datepickerOptions);
            });
        function updateTotalCost() {
            var startDateInput = document.getElementsByName('start_date')[0];
            var endDateInput = document.getElementsByName('end_date')[0];
            var totalCostElement = document.getElementById('totalCost');
            var pricePerNight = parseFloat(document.getElementById('pricePerNight').value);
            console.log('upadte toto cost')

            if (startDateInput && endDateInput && totalCostElement && startDateInput.value && endDateInput.value) {
                console.log('if ok')
                var startDate = new Date(startDateInput.value);
                var endDate = new Date(endDateInput.value);
                var timeDiff = endDate - startDate;
                var days = timeDiff / (1000 * 3600 * 24);

                if (days > 0) {
                    var totalCost = pricePerNight * days;
                    totalCostElement.textContent = totalCost.toFixed(2);
                } else {
                    totalCostElement.textContent = '0';
                }
            }
        }

        updateTotalCost();
    });

