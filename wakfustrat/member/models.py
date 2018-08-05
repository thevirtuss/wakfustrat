import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    We extend Django's default model to add fields.
    Check https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#extending-django-s-default-user
    for more information.
    """
    SERVER_CHOICES = (
        ('DAT', 'Dathura'),
        ('AER', 'Aerafal'),
        ('REM', 'Remington'),
        ('ELB', 'Elbor'),
        ('NOX', 'Nox'),
        ('EFR', 'Efrim'),
        ('PHA', 'Phaeris'),
    )

    register_token = models.UUIDField(_("jeton d'inscription"), default=uuid.uuid4, editable=False, unique=True)
    server = models.CharField(_('serveur'), max_length=20, choices=SERVER_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.username

    def get_register_url(self):
        return reverse('register-validation', args=[self.register_token])
