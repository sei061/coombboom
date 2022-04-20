from django import template

from account.models import User
from tasks.models import Task

register = template.Library()


@register.filter(name='user_name')
def user_name(value):  # Only one argument.
    """Converts a string into all lowercase"""
    return User.objects.get(pk=value)

@register.filter(name='task_name')
def task_name(value):  # Only one argument.
    """Converts a string into all lowercase"""
    return Task.objects.get(pk=value)
