from rest_framework import generics, permissions
from ..models.task import Task
from ..serializers.task import TaskSerializer

class MonthlyTaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # ログインユーザーの「monthly」タイプのみ取得
        return Task.objects.filter(user=self.request.user, type='monthly')

    def perform_create(self, serializer):
        # 作成時にuserとtypeをセット
        serializer.save(user=self.request.user, type='monthly')


class MonthlyTaskRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Task.objects.all()

    def get_queryset(self):
        # ログインユーザーの「monthly」タイプのタスクのみ対象
        return Task.objects.filter(user=self.request.user, type='monthly')
