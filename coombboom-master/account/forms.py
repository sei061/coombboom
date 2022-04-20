from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordResetForm
from django import forms

from account.models import User


class AccountCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "email",
            "employer_id",
            "first_name",
            "last_name",
            "phone_number",
        )


class AccountAuthenticationForm(AuthenticationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'email',
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = 'email',


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'form-control form-control-user bg-gradient-dark-highlight' 'text-center',
        'placeholder': 'Din e-post...',
        'type': 'email',
        'name': 'email'
        }))
