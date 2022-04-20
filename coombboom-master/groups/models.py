from django.contrib.contenttypes.models import ContentType
from django.db import models
from account.models import User
from django.contrib.auth.models import Group, Permission


# Create your models here.

# add author field to auth_group table
class CustomGroupField(models.Model):
    Group.add_to_class('author', models.ForeignKey(User, on_delete=models.CASCADE, null=True))
    Group.add_to_class('is_perm_group', models.BooleanField(blank=True, null=True))

    class Meta:
        permissions = {
            ('add_perm_group', 'Can add permission group'),
            ('handout_add_perm_group', 'Can give permission to add permission group'),  # Perm to give out perm

            ('edit_members_group', 'Can Add or remove members of group'),
            ('handout_edit_members_group', 'Can give permission to Add or remove members of group'),

            ('report_generation_group', 'Can generate reports for group'),
            ('handout_report_generation_group', 'Can give permission to generate reports for group'),
            # Perm to give out perm

            # Standard Perms handout:
            ('handout_view_group', 'Can give permission to view group'),
            ('handout_change_group', 'Can give permission to change group information'),
            ('handout_delete_group', 'Can give permission to delete group'),
            ('handout_add_group', 'Can give permission to add group'),
        }


class Project(models.Model):

    name = models.CharField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # Teams will receive permission 'member' linking to the project they are a member of
    class Meta:
        permissions = {
            ('add_task_perm', 'Can add tasks to project'),
            ('update_estimate', 'Can update time estimate in tasks within a project'),

            ('edit_group_project', 'Can Add or remove groups from project'),
            ('generate_report', 'Can generate reports for projects'),
            ('edit_project', 'Can edit project. name, description etc'),
            ('read_project', 'Can read project'),
            ('generate_report', 'Can generate reports for projects'),
            ('give_perm', 'can give permissions regarding project'),
            ('add_perm_project', 'Can add permission project'),

            ('member', 'team membership'),
        }

    def __str__(self):
        return self.name
