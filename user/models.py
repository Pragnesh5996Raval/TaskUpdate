from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models

class CustomUser(AbstractUser):
    phone_number = PhoneNumberField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)