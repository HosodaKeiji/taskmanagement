# task_management/urls/__init__.py
from django.urls import path, include

urlpatterns = [
    path("tasks/", include("task_management.urls.task")),
    path("daily/", include("task_management.urls.daily")),
    path("weekly/", include("task_management.urls.weekly")),
    path("monthly/", include("task_management.urls.monthly")),
]