from django.urls import path
from tasks import views

app_name = 'task'

urlpatterns = [
    path("", views.task, name="task_index"),
    path("create", views.create_task, name="create_task"),
    path("display", views.display_task, name="display_task"),
    path("update_estimate", views.display_task_get, name="dashboard_link_to_edit_task")
]