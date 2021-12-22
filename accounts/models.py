from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):

    email = models.EmailField(blank=False, max_length=255, verbose_name="email")
    phone = PhoneNumberField(null=True, blank=False, unique=True)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
