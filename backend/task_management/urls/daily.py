from django.urls import path
from ..views.daily import DailyTaskListCreateAPIView, DailyTaskRetrieveUpdateAPIView

urlpatterns = [
    path('daily_task/', DailyTaskListCreateAPIView.as_view(), name='daily-task-list-create'),
    path('daily_task_lists/', DailyTaskListCreateAPIView.as_view(), name='daily-task-lists'),
    path('daily_task/<int:pk>/', DailyTaskRetrieveUpdateAPIView.as_view(), name='daily-task-retrieve-update'),
]
