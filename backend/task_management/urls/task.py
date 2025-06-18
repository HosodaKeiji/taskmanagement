from django.urls import path
from ..views.task import TaskListCreateAPIView

urlpatterns = [
    path('task_create/', TaskListCreateAPIView.as_view(), name='task-list-create'),
]
