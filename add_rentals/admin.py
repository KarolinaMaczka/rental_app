from django.contrib import admin
from .models import Rental, Reservation, Image

admin.site.register(Rental)
admin.site.register(Reservation)
admin.site.register(Image)

