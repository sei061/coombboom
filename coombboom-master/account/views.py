from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, forms, update_session_auth_hash
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordResetForm
from django.http import HttpResponse
from django.shortcuts import render

from coombboom.decorators import authentication_required, project_access_control
from .models import User
from account.forms import AccountCreationForm, AccountAuthenticationForm
from account.models import User, DeletedUsers
from invitation.views import disable_token, get_email_through_token, verify_token


# Create your views here.

@authentication_required
def profile(request):
    """
    A method that simply displays the profile page

    :param request: Requests a redirection to the profile page
    :return: Render of the profile html-page
    """
    return render(request, 'account/profile.html')


@authentication_required
def profile_edit(request):
    """
    A method that lets you edit your own personal details

    :param request: Gets all the data from the form
    :return: render of the profile html-page, unless the edit fails.
    """
    if request.method == 'POST':
        button = request.POST['button']
        if button == "alter":
            user_id = request.POST['user_id']
            user = User.objects.get(pk=user_id)
            user.first_name = request.POST['profile_first_name']
            user.last_name = request.POST['profile_last_name']
            user.username = request.POST['profile_username']
            user.email = request.POST['profile_email']
            user.phone_number = request.POST['profile_phonenumber']
            user.save()
            return render(request, 'account/profile.html')
        else:
            return render(request, 'account/profile.html')

    else:
        return render(request, 'account/profile_edit.html')


def sign_up(request):
    """
    A method that lets a user sign up for Coombboom. The method checks if an invitation link has been used.
    If an invitation link has not been used, the user will not be able to sign up.

    :param request: A POST request
    :return: returns a render of the register html-page if the user is invited. Http-response if not.
    """
    # bool to decide whether user is invited or not
    invited_user = False
    token = None
    # get token from url if there is any
    if 'token' in request.GET:
        token = request.GET['token']  # TODO do we need to sanitize??
        if verify_token(token):
            invited_user = True
        else:
            return HttpResponse("<h1>You dont have access to this!<h1>")
    # if this is a POST request we need to process the form data. check whether user is invited or not
    if request.method == 'POST' and invited_user:
        print(request.POST)
        # create a form instance and populate it with data from the request:
        form = AccountCreationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()

            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=email, password=raw_password)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            # set token to be inactive
            disable_token(token)

            return HttpResponseRedirect(reverse_lazy('profile'))

    # if a GET (or any other method) we'll create a blank form as long as user is invited
    elif invited_user:
        form = AccountCreationForm()
        email = get_email_through_token(token)
        print(email)
        return render(request, 'account/register.html', {'form': form,
                                                         'email': email})
    # if user not invited generate error
    else:
        return HttpResponse("<h1>You dont have access to this!<h1>")


"""

def sign_in(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = AccountAuthenticationForm(data=request.POST)
        # check whether it's valid:

        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=email, password=password)

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return redirect('index')

     # if a GET (or any other method) we'll create a blank form
    else:
        form = AccountAuthenticationForm()

    return render(request, 'login.html', {'form': form})
    """


class LoginView(generic.FormView):
    """
    View to handle user's login
    """
    form_class = forms.AuthenticationForm
    success_url = reverse_lazy('index')
    template_name = 'account/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)


def logout_view(request):
    """
    A method that lets you log out of Coombboom

    :param request: Logout request
    :return: Returns a render of the index html-page
    """

    """
    View to handle logout
    """
    logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))


def forgot_password(request):
    """
    A method that lets you change your password if you forgot it. You can reset your password by email.

    :param request: POST request, used to check the email-address
    :return: Returns a Http-response if the email was found, returns a render of the password html-page if not.
    """
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PasswordResetForm(data=request.POST)
        # check whether it's valid:

        if form.is_valid():
            email = form.cleaned_data.get('email')

            return render(request, 'account/reset_password.html', {'toast': 'Link sent to " + str(email)', 'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AccountAuthenticationForm()

    return render(request, 'account/reset_password.html', {'form': form})


@authentication_required
@project_access_control('project.delete_user')
def delete_user(request, projects):
    """
    A method that lets you delete users. The data is transferred to another table, but it will no longer show up in the system.

    :param request: POST-request, all user info will be deleted.
    :return: Returns a Http-response if delete was successful, returns a render of user deletion html-page if not.
    """
    if request.method == 'POST':
        button = request.POST['button']
        if button == "delete":
            task_id = request.POST['task_id']
            data = User.objects.get(pk=task_id)

            user = {
                "user_data": data
            }
            return render(request, 'account/user_display.html', user)

        elif button == "confirm":
            user_id = request.POST['user_id']
            data = User.objects.get(pk=user_id)
            deleted = DeletedUsers()
            deleted.password = data.password
            deleted.email = data.email
            deleted.username = data.username
            deleted.date_joined = data.date_joined
            deleted.last_login = data.last_login
            deleted.first_name = data.first_name
            deleted.last_name = data.last_name
            deleted.employer_id = data.employer_id
            deleted.phone_number = data.phone_number
            deleted.why_deleted = request.POST['why_deleted']
            deleted.user_id = data.id
            deleted.save()
            data.delete()

            data = User.objects.all()
            return render(request, 'account/user_delete_profile.html', {'toast': 'Bruker slettet', 'user_data': data})

    else:
        data = User.objects.all()
        task = {
            "all_tasks": data
        }
        return render(request, 'account/user_delete_profile.html', task)


@authentication_required
def profile_changepassword(request):
    """
    A method that lets you change your own password.

    :param request: POST-request, checks if your old password is matching and the new ones are.
    :return: Returns a render of the profile page if successful, a Http-response if not.
    """
    if request.method == 'POST':

        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return render(request, 'account/profile_changepassword.html')
        else:
            return render(request, 'account/profile_changepassword.html', {'form': form, 'toast':
                'Sørg for at gammelt passord, og de to nye passordene samsvarer'})

    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'account/profile_changepassword.html', {'form': form})
