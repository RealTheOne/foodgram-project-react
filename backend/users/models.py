from django.contrib.auth.models import AbstractUser
from django.db import models

TEXT_LENGTH = 29


class User(AbstractUser):
    '''Custom user model.'''

    username = models.CharField(
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        max_length=150,
    )
    last_name = models.CharField(
        max_length=150,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = 'username', 'first_name', 'last_name'

    class Meta:
        ordering = ['username']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username[:TEXT_LENGTH]
