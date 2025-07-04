# Generated by Django 4.2.9 on 2025-06-18 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(blank=True, choices=[('high', '高'), ('medium', '中'), ('low', '低')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(blank=True, choices=[('not_started', '未着手'), ('in_progress', '進行中'), ('completed', '完了')], max_length=15, null=True),
        ),
    ]
