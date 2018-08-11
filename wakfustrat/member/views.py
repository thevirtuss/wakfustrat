from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DetailView, FormView, UpdateView
from django.shortcuts import redirect, reverse
from django.utils.translation import gettext_lazy as _

from wakfustrat.member.forms import UpdateMyPasswordForm


class MyAccountView(LoginRequiredMixin, DetailView):
    """
    List my information view.
    """
    context_object_name = 'usr'
    template_name = 'member/my_account.html'

    def get_object(self, queryset=None):
        return self.request.user


class UpdateMyAccountView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Update my information.
    """
    fields = ('server',)
    success_message = _('Vos informations ont bien été mises à jour')  # TODO : check ortografffff
    template_name = 'member/update_my_account.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('my-account')


class UpdateMyPasswordView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    """
    Update my password view.
    """
    form_class = UpdateMyPasswordForm
    success_message = _('Votre mot de passe a été changé')
    template_name = 'member/update_password.html'

    def form_valid(self, form):
        if not self.request.user.check_password(form.cleaned_data.get('old_password')):
            form.add_error('old_password', _('Mot de passe invalide'))
            return self.form_invalid(form)

        self.request.user.set_password(form.cleaned_data.get('password'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('my-account')
