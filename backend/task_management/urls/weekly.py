from django.urls import path
from ..views.weekly import WeeklyTaskListCreateAPIView, WeeklyTaskRetrieveUpdateAPIView

urlpatterns = [
    path('weekly_task/', WeeklyTaskListCreateAPIView.as_view(), name='weekly-task-list-create'),
    path('weekly_task_lists/', WeeklyTaskListCreateAPIView.as_view(), name='weekly-task-lists'),
    path('weekly_task/<int:pk>/', WeeklyTaskRetrieveUpdateAPIView.as_view(), name='weekly-task-retrieve-update'),
]
