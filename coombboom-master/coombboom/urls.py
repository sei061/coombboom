from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("index.urls")),
    path("account/", include("account.urls")),
    path('invitation/', include('invitation.urls')),
    path('tasks/', include('tasks.url')),
    path('log/', include('workreg.urls')),
    path("group/", include("groups.urls")),
    path("dashboard/", include("dashboard.urls")),
    path('', include('django.contrib.auth.urls')),
]
