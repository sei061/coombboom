from django import forms
from django.contrib.postgres.forms import SimpleArrayField


# add_new_group()
class ValidateGroupForm(forms.Form):
    name = forms.CharField()
    users = SimpleArrayField(forms.IntegerField())


# add_new_project()
class ValidateProjectForm(forms.Form):
    name = forms.CharField()
    teams = SimpleArrayField(forms.IntegerField())


# add_new_permissions()
class ValidateAddPermForm(forms.Form):
    perms = SimpleArrayField(forms.IntegerField())
    users = SimpleArrayField(forms.IntegerField())


# add_perm_group()
class ValidatePermGroupForm(forms.Form):
    team_name = forms.CharField()
    perms = SimpleArrayField(forms.IntegerField())
    users = SimpleArrayField(forms.IntegerField())


class ValidatePermToGroupForm(forms.Form):
    group_to_edit = forms.IntegerField()
