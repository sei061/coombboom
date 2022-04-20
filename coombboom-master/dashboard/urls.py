from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path("project", views.project, name="project dashboard"),
    path("team", views.team, name="team dashboard"),
    path("all", views.load_grps_proj, name="all"),
    path("", views.load_dash_user, name=""),
    path("ajax_load_project", views.csv_ajax_get_project, name="get_json_formatted_project_data"),
    path("ajax_load_team", views.csv_ajax_get_team, name="Get_json_formatted_team_data")
]