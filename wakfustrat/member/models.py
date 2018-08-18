import datetime
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    We extend Django's default model to add fields.
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
    username = models.CharField(
        _('pseudo'),
        max_length=32,
        unique=True,
        help_text=_('Obligatoire. 32 caractères max. Lettres, chiffres et @/./+/-/_ seulement.'),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    register_token = models.UUIDField(_("jeton d'inscription"), default=uuid.uuid4, editable=False, unique=True)
    server = models.CharField(_('serveur'), max_length=20, choices=SERVER_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.username

    def get_register_url(self):
        return reverse('register-validation', args=[self.register_token])


class PasswordToken(models.Model):
    """
    Model for password reset tokens.
    """
    token = models.UUIDField(_('jeton'), default=uuid.uuid4, editable=False, unique=True)
    date = models.DateTimeField(_('date et heure'), auto_now=True)
    is_used = models.BooleanField(_('utilisé'), default=False)
    user = models.ForeignKey(User, verbose_name=_('utilisateur'), on_delete=models.PROTECT)

    def is_expired(self):
        return self.date + datetime.timedelta(days=1) < datetime.datetime.now()

    class Meta:
        verbose_name = _('Jeton de réinitialisation de mot de passe')
        verbose_name_plural = _('Jetons de réinitialisation de mot de passe')

    def get_absolute_url(self):
        return reverse('password-reset-reset', args=[self.token])
