"""wakfustrat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from wakfustrat.pages.views import HomeView, RegisterView, RegisterSuccessView, RegisterValidationView, LoginView, \
    LogoutView, AboutView, ContactView, ResetPasswordRequestView, ResetPasswordView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('membre/', include('wakfustrat.member.urls')),
    path('news/', include('wakfustrat.news.urls')),
    path('wiki/', include('wakfustrat.wiki.urls')),

    path('a-propos/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('connexion/', LoginView.as_view(), name='login'),
    path('déconnexion/', LogoutView.as_view(), name='logout'),
    path('inscription/', RegisterView.as_view(), name='register'),
    path('inscription/succès/', RegisterSuccessView.as_view(), name='register-success'),
    path('inscription/validation/<uuid:token>/', RegisterValidationView.as_view(), name='register-validation'),
    path('réiitialiser-mon-mot-de-passe/', ResetPasswordRequestView.as_view(), name='password-reset-request'),
    path('réiitialiser-mon-mot-de-passe/<uuid:token>/', ResetPasswordView.as_view(), name='password-reset-reset'),

    path('', HomeView.as_view(), name='home'),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
