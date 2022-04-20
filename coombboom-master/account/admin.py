from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from tasks.models import Task
from .forms import UserCreationForm, CustomUserChangeForm


# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email']


admin.site.register(User, CustomUserAdmin)
admin.site.register(Task)
