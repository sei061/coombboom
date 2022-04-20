from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError("User must have email!")

        if not username:
            raise ValueError("User must have username!")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# change from AbstractBaseUser to AbstractUser for guardian compatibility
class User(AbstractUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(verbose_name="username", max_length=45)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last sign_in", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    employer_id = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=45)

    objects = MyAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # TODO implement perm checks here

        return self.is_admin

    def has_module_perms(self, app_label):
        # TODO has module perms
        return True

    class Meta:
        permissions = {
            ('assign_create_group',     'Can assign permission to create groups'),
            ('assign_create_project',   'Can assign permission to create Projects'),
        }


class DeletedUsers(models.Model):
    password = models.CharField(max_length=128)
    email = models.EmailField(verbose_name="email", max_length=60)
    username = models.CharField(verbose_name="username", max_length=45)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last sign_in", auto_now=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    employer_id = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=45)
    why_deleted = models.CharField(max_length=100)
    user_id = models.IntegerField(10)
    date_deleted = models.DateTimeField(verbose_name="date_deleted", auto_now_add=True)
