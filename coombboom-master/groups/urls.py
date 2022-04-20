from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path("new_team/", views.add_new_group, name="new_team"),
    path("new_project/", views.add_new_project, name="new_project"),
    path("add_perm_user/", views.add_perm_user, name="assign_perm_user"),
    path("add_perm_group/", views.add_perm_group, name="add permission group"),
    path("view_groups", views.view_groups, name="view group objects"),
    path("change_group", views.change_group, name="Modify group object"),
    path("view_projects/", views.view_projects, name="view projects objects"),
    path("perm_to_group/", views.add_perm_to_group, name="Add perm to group"),
    path('perm_to_group/ajax/load-group-info/', views.ajax_load_group_info, name='ajax_group_info'),
    path("view_projects/change_project", views.change_project, name="modify project object"),
]
