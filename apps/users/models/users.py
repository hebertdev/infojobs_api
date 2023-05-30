#  Django
from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    infojobs_id = models.IntegerField('infojobs_profile_id', null=True)
    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email already exists.'
        }
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    def __str__(self):
        """Return username."""
        return self.username

    def get_short_name(self):
        """Return username."""
        return self.username
