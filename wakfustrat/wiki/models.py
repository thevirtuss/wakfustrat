import uuid

from model_utils.fields import StatusField

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from wakfustrat.common.models import SubZone, Zone


# Generic


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


def upload_to_wiki_page_image(instance, filename):
    extension = filename.split('.')[-1].lower()
    return 'wiki/{0}.{1}'.format(uuid.uuid4().hex, extension)


class WikiCategoryBase(models.Model):
    """
    Base used for all types in the wiki.
    """
    STATUS = (
        ('draft', _('Brouillon')),
        ('published', _('Terminé'))
    )

    name = models.CharField(_('nom'), max_length=64, unique=True)
    slug = models.SlugField(_('slug'), max_length=64, unique=True)
    status = StatusField()
    contents = GenericRelation(Content)

    class Meta:
        abstract = True

    @property
    def content(self):
        return self.contents.last()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.name)
        super().save()


# Per type


class WikiDungeonBase(WikiCategoryBase):
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

    boss = models.CharField(_('boss'), max_length=64)
    level = models.PositiveSmallIntegerField(_('niveau'), validators=[MaxValueValidator(200)])
    difficulty = models.PositiveSmallIntegerField(
        _('difficulté'), choices=DIFFICULTY_CHOICES,
        help_text=_("Il s'agit d'une indication subjective à propos de la complexité de la stratégie du donjon"))
    zone = models.ForeignKey(Zone, verbose_name=_('zone'), on_delete=models.PROTECT)
    subzone = models.ForeignKey(SubZone, verbose_name=_('sous-zone'), on_delete=models.PROTECT, blank=True, null=True)
    image = models.ImageField(_('image'), blank=True, null=True, upload_to=upload_to_wiki_page_image)

    class Meta:
        abstract = True

    def get_difficulty_icons(self):
        color = {
            self.DIFFICULTY_0: 'text-success',
            self.DIFFICULTY_1: 'text-info',
            self.DIFFICULTY_2: '',
            self.DIFFICULTY_3: 'text-warning',
            self.DIFFICULTY_4: 'text-danger',
        }[self.difficulty]

        return (self.difficulty + 1) * '<i class="fas fa-star {0}"></i>'.format(color)


class Dungeon(WikiDungeonBase):
    """
    An article about a dungeon in the game.
    """
    class Meta:
        verbose_name = _('Donjon')
        verbose_name_plural = _('Donjons')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wiki:page-detail', args=['donjons', self.slug])


class Boss(WikiDungeonBase):
    """
    An article about a ultimate boss in the game.
    """
    class Meta:
        verbose_name = _('Boss ultime')
        verbose_name_plural = _('Boss ultimes')

    def __str__(self):
        return self.boss

    def get_absolute_url(self):
        return reverse('wiki:page-detail', args=['boss-ultimes', self.slug])
