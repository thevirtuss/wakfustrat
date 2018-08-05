from django.urls import path

from wakfustrat.member.views import MyAccountView, UpdateMyPasswordView, UpdateMyAccountView


urlpatterns = [
    path('mon-compte/', MyAccountView.as_view(), name='my-account'),
    path('mon-compte/mot-de-passe/', UpdateMyPasswordView.as_view(), name='my-account-password'),
    path('mon-compte/mot-profil/', UpdateMyAccountView.as_view(), name='my-account-update'),

]
