# Forms

> Auto-generated documentation for [account.forms](..\..\account\forms.py) module.

- [Coombboom](..\README.md#coombboom-index) / [Modules](..\MODULES.md#coombboom-modules) / [Account](index.md#account) / Forms
    - [AccountAuthenticationForm](#accountauthenticationform)
    - [AccountCreationForm](#accountcreationform)
    - [CustomUserChangeForm](#customuserchangeform)
    - [UserPasswordResetForm](#userpasswordresetform)

## AccountAuthenticationForm

[[find in source code]](..\..\account\forms.py#L19)

```python
class AccountAuthenticationForm(AuthenticationForm, UserCreationForm.Meta):
```

## AccountCreationForm

[[find in source code]](..\..\account\forms.py#L7)

```python
class AccountCreationForm(UserCreationForm, UserCreationForm.Meta):
```

## CustomUserChangeForm

[[find in source code]](..\..\account\forms.py#L27)

```python
class CustomUserChangeForm(UserChangeForm):
```

## UserPasswordResetForm

[[find in source code]](..\..\account\forms.py#L33)

```python
class UserPasswordResetForm(PasswordResetForm):
    def __init__(*args, **kwargs):
```
