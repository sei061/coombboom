from .forms import UserPasswordResetForm
from .views import LoginView, logout_view
from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

app_name = 'account'

urlpatterns = [
    path("profile", views.profile, name="profile"),
    path("profile_edit", views.profile_edit, name="profile_edit"),
    path("profile_changepassword", views.profile_changepassword, name="profile_changepassword"),
    path("register", views.sign_up, name="sign_up"),
    path("login", LoginView.as_view(), name='login'),
    path("logout/", logout_view, name='logout'),
    path("delete_user", views.delete_user, name="delete user"),
    #path("forgot-password", views.forgot_password, name="forgot_password"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="account/reset_password.html", form_class=UserPasswordResetForm), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_sent.html"), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_form.html"), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="account/password_reset_done.html"), name ='password_reset_complete'),
]
