from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    TYPE_CHOICES = [
        ('normal', '通常'),
        ('daily', '日次'),
        ('weekly', '週次'),
        ('monthly', '月次'),
    ]

    PRIORITY_CHOICES = [
        ('high', '高'),
        ('medium', '中'),
        ('low', '低'),
    ]

    STATUS_CHOICES = [
        ('not_started', '未着手'),
        ('in_progress', '進行中'),
        ('completed', '完了'),
    ]

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    deadline = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES,null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES,null=True, blank=True)
    
    description = models.TextField(blank=True)
    repeat_rule = models.JSONField(null=True, blank=True)  # 例: {"frequency": "weekly", "day": "monday"}
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
