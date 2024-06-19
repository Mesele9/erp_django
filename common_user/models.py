# common_user/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
        ROLE_CHOICES = [
                ('hr_staff', 'HR Staff'),
                ('store_staff', 'Store Staff'),
                ('admin', 'Admin'),
                ]
        role = models.CharField(max_length=20, choices=ROLE_CHOICES)

