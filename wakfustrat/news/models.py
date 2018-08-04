import datetime

from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _

from wakfustrat.common.md import generate_html


class News(models.Model):
    """
    A simple news model.
    """
    name = models.CharField(_('nom'), max_length=100, unique=True)
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    publish_date = models.DateTimeField(_('date et heure de publication'), blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('auteur'), on_delete=models.PROTECT)
    description = models.CharField(_('description/accroche'), max_length=512)
    markdown = models.TextField(_('markdown'))
    html = models.TextField(_('HTML'))

    class Meta:
        verbose_name = _('News')
        verbose_name_plural = _('News')

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        self.html, toc = generate_html(self.markdown)
        super().save(**kwargs)

    def get_absolute_url(self):
        return '{0}#news-{1}'.format(reverse('news-list'), self.slug)


def get_published_news():
    return News\
        .objects\
        .exclude(publish_date=None)\
        .filter(publish_date__lte=datetime.datetime.now())\
        .order_by('-publish_date')\
        .all()