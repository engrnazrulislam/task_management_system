# Generated by Django 5.2.3 on 2025-07-17 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_remove_taskdetail_assigned_to_alter_task_assigned_to_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='is_completed',
        ),
    ]
