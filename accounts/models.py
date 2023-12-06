from django.contrib.auth.models import User
from django.db import models
import uuid


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_token = models.UUIDField(default=uuid.uuid4)


class PersonalData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='personal_data')
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.surname} - {self.address}"
