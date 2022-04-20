import hashlib
import secrets
from django.shortcuts import render
from coombboom.settings import EMAIL_HOST_USER
from . import forms
from django.core.mail import send_mail
from .models import Invitations
from django.http import HttpResponse


def get_email_through_token(token):
    i = Invitations.objects.get(referred_token=token)
    return i.referred_email


# disable token by matching token in DB
def disable_token(token):
    """

    :param token:
    :return:
    """
    i = Invitations.objects.get(referred_token=token)
    i.referral_active = False
    i.save()


# Enable token by matching email
def enable_token(email):
    """

    :param email:
    :return:
    """
    i = Invitations.objects.get(referred_email=email)  # get row
    i.referral_active = True  # set referral_active to True
    i.save()  # commit to database


# check token | check token is active
def verify_token(token):
    """

    :param token:
    :return:
    """
    token_exists = bool(Invitations.objects.filter(
        referred_token__icontains=token))  # check if token matches any in DB
    if token_exists:  # check if token is active
        i = Invitations.objects.get(referred_token=token)
        return i.referral_active  # true if token is active, false if not
    else:
        return False  # token is inactive


# check if invite exists or not
def invite_exists(email):
    """

    :param email:
    :return:
    """
    return bool(Invitations.objects.filter(referred_email__icontains=email))


# encode token from email
def encode_token(email):
    """

    :param email:
    :return:
    """
    salt = secrets.token_hex(8) + email
    referral_token = hashlib.sha256(salt.encode('utf-8')).hexdigest()
    return referral_token


# calls encode_token() pushes to db and returns referral_token for use.
def create_token(referer_id, recipient):
    """

    :param referer_id:
    :param recipient:
    :return:
    """
    referral_token = encode_token(recipient)
    Invitations.objects.create(
        referer_id=referer_id,
        referred_email=recipient,
        referred_token=referral_token)
    return referral_token


def invitation(request):
    """

    :param request:
    :return:
    """
    sub = forms.Invitation()
    sufficient_permissions = request.user.is_superuser  # see if user is allowed to invite
    if request.method == 'POST' and sufficient_permissions:
        sub = forms.Invitation(request.POST)
        # set referer_id and recipient/referral email
        referer_id = request.user.id
        recipient = str(sub['Email'].value())
        # if email is found in database, set referral_active to True instead of creating a duplicate invite
        if invite_exists(recipient):
            enable_token(recipient)
            return render(request, 'invitation/invite-link-send.html', {'recepient': recipient, 'toast': 'Det har allerede blitt sendt en '
                                                                                                         'link til denne brukeren. Linken er re-aktivert'})  # render success
        else:  # if there is no duplicate, create new invite
            # save referer_id, referral_email and token to DB
            referral_token = create_token(referer_id, recipient)
            # start email message
            subject = 'Velkommen til Coombboom'
            message = 'Her er din link for å registrere deg: http://127.0.0.1:8000/account/register?token={}'.format(
                referral_token)
            send_mail(subject,
                      message, EMAIL_HOST_USER, [recipient], fail_silently=False)  # send email
            return render(request, 'invitation/invite-link-send.html', {'recepient': recipient, 'toast': 'Invitasjonslink sendt!'})  # render success

    elif sufficient_permissions:
        return render(request, 'invitation/invite-link-send.html', {'form': sub})  # if you are superuser load form

    else:
        return HttpResponse("<h1>You dont have access to this!<h1>")  # if you are not superuser, return err
