from django.urls import path
from ..views.monthly import MonthlyTaskListCreateAPIView, MonthlyTaskRetrieveUpdateAPIView

urlpatterns = [
    path('monthly_task/', MonthlyTaskListCreateAPIView.as_view(), name='monthly-task-list-create'),
    path('monthly_task_lists/', MonthlyTaskListCreateAPIView.as_view(), name='monthly-task-lists'),
    path('monthly_task/<int:pk>/', MonthlyTaskRetrieveUpdateAPIView.as_view(), name='monthly-task-retrieve-update'),
]
