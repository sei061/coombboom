from django.db import models

# Create your models here.
from django.db import models
from django.utils.timezone import now


# Create your models here.
class Invitations(models.Model):
    id = models.AutoField(primary_key=True)
    referer_id = models.CharField(max_length=45)
    referred_email = models.CharField(max_length=300)
    referred_token = models.CharField(max_length=300)
    referred_time = models.DateTimeField(default=now, editable=False)
    referral_active = models.BooleanField(default=True)
