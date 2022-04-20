from django.urls import path
from . import views
from .views import DeleteEntryView


app_name = 'workreg'

urlpatterns = [
    path('entry/add', views.new, name='entry-add'),
    path('entry/list', views.list, name='entry-list'),
    path('<int:pk>/', views.workreg_update_view, name='workreg_change'),
    path('entry/<int:pk>/delete', views.delete_entry, name='delete_workreg'),
    path('ajax/load-tasks/', views.load_tasks, name='ajax_load_tasks'),

]
