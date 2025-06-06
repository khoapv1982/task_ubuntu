# Generated by Django 5.1.2 on 2024-10-31 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='department',
            fields=[
                ('department_id', models.CharField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('manager_dep', models.CharField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_id', models.CharField(default=None)),
                ('department_id', models.CharField(default=None)),
                ('name', models.CharField(max_length=50)),
                ('team_leader', models.CharField()),
                ('manager_dep', models.CharField(default=None)),
            ],
        ),
    ]
