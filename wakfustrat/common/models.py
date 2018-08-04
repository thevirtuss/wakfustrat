import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from wakfustrat.member.models import User


class Zone(models.Model):
    """
    A Zone on the game (example : Astrub).
    """
    name = models.CharField(_('nom'), max_length=128, unique=True)
    slug = models.SlugField(_('slug'), max_length=128, unique=True)

    class Meta:
        verbose_name = _('zone')
        verbose_name_plural = _('zones')

    def __str__(self):
        return self.name


class SubZone(models.Model):
    """
    A SubZone on the game (example : Cité d'Astrub).
    """
    name = models.CharField(_('nom'), max_length=128, unique=True)
    slug = models.SlugField(_('slug'), max_length=128, unique=True)

    class Meta:
        verbose_name = _('sous-zone')
        verbose_name_plural = _('sous-zones')

    def __str__(self):
        return self.name
