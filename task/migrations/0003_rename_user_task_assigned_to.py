# Generated by Django 5.1.7 on 2025-03-25 08:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_task_created_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='user',
            new_name='assigned_to',
        ),
    ]
