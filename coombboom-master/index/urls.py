from django.urls import path

import account
from account.views import LoginView
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", LoginView.as_view(), name='login'),
    path("account/profile", account.views.profile, name="profile"),
]
