import uuid
from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractUser, Group, Permission


class Event(models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    thumbnail = models.ImageField(upload_to='event_thumbnails/')

    def __str__(self):
        return self.title


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Change this to a unique name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # Change this to a unique name
        blank=True,
    )

class Registration(models.Model):
    event = models.ForeignKey(Event, related_name='registrations', on_delete=models.CASCADE)
    client_email = models.EmailField()
    manage_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def save(self, *args, **kwargs):
        if not self.manage_code:
            self.manage_code = get_random_string(length=12)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.client_email} registered for {self.event}'
        