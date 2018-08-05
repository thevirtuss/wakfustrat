from django import forms
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

from wakfustrat.member.models import User


class SetPasswordBaseForm(forms.Form):
    """
    Based used to change password.
    """
    def clean_password(self):
        data = self.cleaned_data['password']
        validate_password(data)
        return data

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        password2 = cleaned_data['password2']

        if password != password2:
            raise forms.ValidationError(_('Les mots de passe doivent être identiques.'))

        return cleaned_data


class RegisterForm(SetPasswordBaseForm):
    """
    Form used for registration.
    """
    password = forms.CharField(label=_('Mot de passe'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Mot de passe (confirmation)'), widget=forms.PasswordInput)
    username = forms.CharField(label=_("Nom d'utilisateur"), min_length=3, max_length=30)
    email = forms.EmailField(label=_('Adresse mail'))

    def clean_username(self):
        data = self.cleaned_data['username']
        try:
            user = User.objects.get(username=data)
            raise forms.ValidationError(_("Le nom d'utilisateur {0} est déjà pris.").format(user.username))
        except User.DoesNotExist:
            return data


class UpdateMyPasswordForm(SetPasswordBaseForm):
    """
    Form to update password.
    """
    old_password = forms.CharField(label=_('Ancien mot de passe'), widget=forms.PasswordInput)
    password = forms.CharField(label=_('Nouveau mot de passe'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Nouveau mot de passe (confirmation)'), widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data['old_password']
        new_password = cleaned_data['password']

        if old_password == new_password:
            raise forms.ValidationError(_("Le nouveau mot de passe doit être différent de l'actuel."))

        return cleaned_data
