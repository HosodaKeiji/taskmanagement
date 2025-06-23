from django.urls import path
from ..views.task import TaskListCreateAPIView, TaskRetrieveUpdateAPIView, TaskDestroyAPIView

urlpatterns = [
    path('task_create/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    path('task_lists/', TaskListCreateAPIView.as_view(), name='task-lists'),
    path('task_update/<int:pk>/', TaskRetrieveUpdateAPIView.as_view(), name='task-detail-update'),
    path('task/<int:pk>/delete/', TaskDestroyAPIView.as_view(), name='task-destroy'),
]
