from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('technicien', 'Technicien'),
        ('utilisateur', 'Utilisateur'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='utilisateur')
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
