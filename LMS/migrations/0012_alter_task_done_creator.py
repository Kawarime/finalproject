# Generated by Django 5.0.6 on 2024-07-05 14:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0011_alter_lesson_creator'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='task_done',
            name='creator',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]