from django.contrib import admin
from .models import PersonalData, UserProfile

# Register your models here.
admin.site.register(PersonalData)
admin.site.register(UserProfile)
