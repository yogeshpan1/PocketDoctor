from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model. We extend Django's built-in AbstractUser
    instead of building our own auth from scratch (which is what
    the original project did with a JSON file — insecure and fragile).
    Django gives us: hashed passwords, sessions, login attempt handling.
    """
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    phone_number = models.CharField(max_length=20, blank=True)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.role})"