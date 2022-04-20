# Views

> Auto-generated documentation for [account.views](..\..\account\views.py) module.

- [Coombboom](..\README.md#coombboom-index) / [Modules](..\MODULES.md#coombboom-modules) / [Account](index.md#account) / Views
    - [LoginView](#loginview)
        - [LoginView().form_valid](#loginviewform_valid)
    - [delete_user](#delete_user)
    - [forgot_password](#forgot_password)
    - [logout_view](#logout_view)
    - [profile](#profile)
    - [profile_changepassword](#profile_changepassword)
    - [profile_edit](#profile_edit)
    - [sign_up](#sign_up)

## LoginView

[[find in source code]](..\..\account\views.py#L132)

```python
class LoginView(generic.FormView):
```

View to handle user's login

### LoginView().form_valid

[[find in source code]](..\..\account\views.py#L141)

```python
def form_valid(form):
```

## delete_user

[[find in source code]](..\..\account\views.py#L186)

```python
def delete_user(request):
```

A method that lets you delete users. The data is transferred to another table, but it will no longer show up in the system.

#### Arguments

- `request` - POST-request, all user info will be deleted.

#### Returns

Returns a Http-response if delete was successful, returns a render of user deletion html-page if not.

## forgot_password

[[find in source code]](..\..\account\views.py#L161)

```python
def forgot_password(request):
```

A method that lets you change your password if you forgot it. You can reset your password by email.

#### Arguments

- `request` - POST request, used to check the email-address

#### Returns

Returns a Http-response if the email was found, returns a render of the password html-page if not.

## logout_view

[[find in source code]](..\..\account\views.py#L146)

```python
def logout_view(request):
```

A method that lets you log out of Coombboom

#### Arguments

- `request` - Logout request

#### Returns

Returns a render of the index html-page

## profile

[[find in source code]](..\..\account\views.py#L21)

```python
def profile(request):
```

A method that simply displays the profile page

#### Arguments

- `request` - Requests a redirection to the profile page

#### Returns

Render of the profile html-page

## profile_changepassword

[[find in source code]](..\..\account\views.py#L232)

```python
def profile_changepassword(request):
```

A method that lets you change your own password.

#### Arguments

- `request` - POST-request, checks if your old password is matching and the new ones are.

#### Returns

Returns a render of the profile page if successful, a Http-response if not.

## profile_edit

[[find in source code]](..\..\account\views.py#L30)

```python
def profile_edit(request):
```

A method that lets you edit your own personal details

#### Arguments

- `request` - Gets all the data from the form

#### Returns

render of the profile html-page, unless the edit fails.

## sign_up

[[find in source code]](..\..\account\views.py#L55)

```python
def sign_up(request):
```

A method that lets a user sign up for Coombboom. The method checks if an invitation link has been used.
If an invitation link has not been used, the user will not be able to sign up.

#### Arguments

- `request` - A POST request

#### Returns

returns a render of the register html-page if the user is invited. Http-response if not.
