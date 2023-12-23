from django.db import models
from django.contrib.auth.models import User

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    number_of_rooms = models.IntegerField()
    number_of_bathrooms = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=6, decimal_places=2)
    max_guests = models.IntegerField()
    number_of_beds = models.IntegerField()
    address_city = models.CharField(max_length=100)
    address_street = models.CharField(max_length=100)
    images = models.ImageField(upload_to='rentals/')


class Reservation(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.rental} reserved by {self.user}'

