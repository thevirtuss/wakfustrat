from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, TemplateView, View

from wakfustrat.common.email import send_email
from wakfustrat.member.forms import RegisterForm, ResetPasswordRequestForm, ResetPasswordForm
from wakfustrat.member.models import User, PasswordToken
from wakfustrat.news.models import get_published_news
from wakfustrat.wiki.models import Boss, Dungeon, Content


class HomeView(TemplateView):
    """
    Home view.
    """
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorite'] = Dungeon.objects.filter(status='published').last()
        context['news_list'] = get_published_news()[:3]
        context['stats'] = {
            'dungeons': Dungeon.objects.exclude(status='empty').count(),
            'boss': Boss.objects.exclude(status='empty').count(),
            'users': User.objects.filter(is_active=True).count(),
            'editions': Content.objects.count(),
        }
        return context


class AboutView(TemplateView):
    """
    About view.
    """
    template_name = 'pages/about.html'


class ContactView(TemplateView):
    """
    Contact view.
    """
    template_name = 'pages/contact.html'


class RegisterView(FormView):
    """
    View for the registration of a new user.
    """
    # TODO : not logged view
    form_class = RegisterForm
    template_name = 'pages/register.html'

    def form_valid(self, form):
        data = form.cleaned_data

        # Ensure email is not in database (prevent enumeration of email in database)
        try:
            user = User.objects.get(email=data.get('email'))
        except User.DoesNotExist:
            user = None

        if user is None:
            user = User.objects.create_user(data.get('username'), data.get('email'), data.get('password'))
            user.is_active = False
            user.save()
            send_email("Confirmation d'inscription", user.email, 'email/member/register.html',
                       {'url': user.get_register_url()})
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('register-success')


class RegisterSuccessView(TemplateView):
    """
    View displayed after the register form.
    """
    # TODO : not logged view
    template_name = 'pages/register_success.html'


class RegisterValidationView(TemplateView):
    """
    View to valid the registration.
    """
    template_name = 'pages/register_validation_success.html'

    def get(self, request, *args, **kwargs):
        # message
        user = get_object_or_404(User, register_token=kwargs.get('token'), is_active=False)
        user.is_active = True
        user.save()
        return super().get(request, *args, **kwargs)


class LoginView(DjangoLoginView):
    """
    View for login.
    """
    def get_success_url(self):
        return reverse('home')


class LogoutView(LoginRequiredMixin, View):
    """
    View to logout an user.
    """
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('login'))


class ResetPasswordRequestView(SuccessMessageMixin, FormView):
    """
    View for password reset.
    """
    form_class = ResetPasswordRequestForm
    template_name = 'pages/password_reset/request.html'
    success_message = _("Si l'adresse existe vous allez recevoir un mail contenant les instructions pour réinitialiser "
                        "votre message.")

    def form_valid(self, form):
        try:
            user = User.objects.get(email=form.cleaned_data.get('email'))

            for old_token in PasswordToken.objects.filter(is_used=False, user=user).all():
                old_token.is_used = True
                old_token.save()

            token = PasswordToken(user=user)
            token.save()

            send_email(_('Réinitialisation du mot de passe'), user.email, 'email/member/password_reset.html',
                       {'url': token.get_absolute_url()})

        except User.DoesNotExist:
            pass

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('login')


class ResetPasswordView(SuccessMessageMixin, FormView):
    """
    View for reset a password.
    """
    form_class = ResetPasswordForm
    template_name = 'pages/password_reset/reset.html'
    success_message = _('Votre mot de passe a bien été changé, vous pouvez maintenant vous connecter.')

    token = None

    def dispatch(self, request, *args, **kwargs):
        self.token = get_object_or_404(PasswordToken, token=self.kwargs.get('token'), is_used=False)
        if self.token.is_expired():
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.token.is_used = True
        self.token.save()
        self.token.user.set_password(form.cleaned_data.get('password'))
        self.token.user.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('login')
