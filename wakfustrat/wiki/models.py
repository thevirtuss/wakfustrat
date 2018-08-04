import uuid

from bs4 import BeautifulSoup
from model_utils.fields import StatusField

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from wakfustrat.common.models import SubZone, Zone


def upload_to_image(instance, filename):
    extension = filename.split('.')[-1].lower()
    return 'wiki/images/{0}.{1}'.format(uuid.uuid4().hex[:8], extension)


class Image(models.Model):
    """
    An image attached to an article.
    """

    image = models.ImageField(_('image'), upload_to=upload_to_image)
    date = models.DateTimeField(_('date'), auto_now_add=True)
    by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)


class Content(models.Model):
    """
    Represent the content of a wiki page.
    """
    markdown = models.TextField(_('contenu au format MarkDown'))
    html = models.TextField(_('contenu au format HTML'))
    toc = models.TextField(_('table des matières'))
    create_date = models.DateTimeField(_('date de création'), auto_now_add=True)
    version = models.PositiveIntegerField(_('version'), editable=False)
    uuid = models.UUIDField(_('UUID'), default=uuid.uuid4, editable=False, unique=True)
    by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('par'), on_delete=models.PROTECT)
    diff_count = models.IntegerField(_('quantité modifiée'), default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def _gen_menu_structure(self, values, tag):
        ignore_next = False
        looped = False
        for i in range(len(values)):
            if ignore_next:
                continue
            value = values[i]
            if value.name == tag:
                yield value.text
                looped = False
            elif value.name < tag:
                ignore_next = True
                looped = False
            else:
                if looped:
                    continue
                yield self._gen_menu_structure(values[i:], value.name)
                looped = True

    def _gen_menu_html(self, structure):
        menu = ''
        for value in structure:
            if isinstance(value, str):
                menu += '<li><a href="#">{0}</a></li>'.format(value)
            else:
                menu += '<li>{0}</li>'.format(self._gen_menu_html(value))
        return '<ul class="list-unstyled ml-4">{0}</ul>'.format(menu)

    @property
    def menu(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        structure = self._gen_menu_structure(soup.find_all(['h1', 'h2', 'h3']), 'h1')
        return self._gen_menu_html(structure)


def upload_dungeon_image(instance, filename):
    extension = filename.split('.')[-1].lower()
    return 'wiki/dungeons/{0}.{1}'.format(uuid.uuid4().hex, extension)


class Dungeon(models.Model):
    """
    An article about a dungeon in the game.
    """
    DIFFICULTY_0 = 0
    DIFFICULTY_1 = 1
    DIFFICULTY_2 = 2
    DIFFICULTY_3 = 3
    DIFFICULTY_4 = 4
    DIFFICULTY_CHOICES = (
        (DIFFICULTY_0, _('Très facile')),
        (DIFFICULTY_1, _('Facile')),
        (DIFFICULTY_2, _('Normal')),
        (DIFFICULTY_3, _('Difficile')),
        (DIFFICULTY_4, _('Très difficile')),
    )
    STATUS = (
        ('empty', _('Vide')),
        ('draft', _('Brouillon')),
        ('published', _('Terminé'))
    )

    name = models.CharField(_('nom'), max_length=64, unique=True)
    slug = models.SlugField(_('slug'), max_length=64, unique=True)
    status = StatusField()
    boss = models.CharField(_('boss'), max_length=64)
    level = models.PositiveSmallIntegerField(_('niveau'), validators=[MaxValueValidator(200)])
    difficulty = models.PositiveSmallIntegerField(
        _('difficulté'), choices=DIFFICULTY_CHOICES,
        help_text=_("Il s'agit d'une indication subjective à propos de la complexité de la stratégie du donjon"))
    zone = models.ForeignKey(Zone, verbose_name=_('zone'), on_delete=models.PROTECT)
    subzone = models.ForeignKey(SubZone, verbose_name=_('sous-zone'), on_delete=models.PROTECT, blank=True, null=True)
    contents = GenericRelation(Content)
    image = models.ImageField(_('image'), blank=True, null=True, upload_to=upload_dungeon_image)

    class Meta:
        verbose_name = _('Donjon')
        verbose_name_plural = _('Donjons')

    def __str__(self):
        return self.name

    @property
    def content(self):
        return self.contents.last()

    def get_absolute_url(self):
        return reverse('dungeon-detail', args=[self.slug])

    def get_difficulty_icons(self):
        color = {
            self.DIFFICULTY_0: 'text-success',
            self.DIFFICULTY_1: 'text-info',
            self.DIFFICULTY_2: '',
            self.DIFFICULTY_3: 'text-warning',
            self.DIFFICULTY_4: 'text-danger',
        }[self.difficulty]

        return (self.difficulty + 1) * '<i class="fas fa-star {0}"></i>'.format(color)
