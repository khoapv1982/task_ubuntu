# Generated by Django 5.1.7 on 2025-03-28 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0018_alter_task_model_urgent_old'),
    ]

    operations = [
        migrations.AddField(
            model_name='task_model2',
            name='date_alarm',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
