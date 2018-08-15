from django import forms
from django.utils.translation import gettext_lazy as _

from wakfustrat.wiki.models import Boss, Dungeon


class DungeonForm(forms.ModelForm):
    """
    Form for Dungeon objects.
    """
    content = forms.CharField(label=_('Contenu'), widget=forms.HiddenInput, required=False)

    class Meta:
        exclude = ('slug', 'images')
        model = Dungeon


class BossForm(forms.ModelForm):
    """
    Form for Boss objects.
    """
    content = forms.CharField(label=_('Contenu'), widget=forms.HiddenInput, required=False)

    class Meta:
        exclude = ('slug', 'images')
        model = Boss
