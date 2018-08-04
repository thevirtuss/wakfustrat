from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.shortcuts import get_object_or_404, redirect, reverse
from django.views.generic import FormView, TemplateView, View

from wakfustrat.common.email import send_email
from wakfustrat.member.forms import RegisterForm
from wakfustrat.member.models import User
from wakfustrat.news.models import get_published_news
from wakfustrat.wiki.models import Dungeon


class HomeView(TemplateView):
    """
    Home view.
    """
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorite'] = Dungeon.objects.filter(status='published').last()
        context['news_list'] = get_published_news()[:5]
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
