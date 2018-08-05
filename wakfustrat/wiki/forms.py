from django import forms
from django.utils.translation import gettext_lazy as _

from wakfustrat.wiki.models import Dungeon


class DungeonForm(forms.ModelForm):
    """

    """
    content = forms.CharField(label=_('Contenu'), widget=forms.Textarea, required=False)

    class Meta:
        exclude = ('slug',)
        model = Dungeon
