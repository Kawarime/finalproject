# Generated by Django 5.0.6 on 2024-07-05 08:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0009_remove_task_dead_line_remove_task_priority_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='created_at',
        ),
    ]
