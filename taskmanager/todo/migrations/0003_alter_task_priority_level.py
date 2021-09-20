# Generated by Django 3.2.7 on 2021-09-19 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_task_priority_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority_level',
            field=models.CharField(blank=True, choices=[('low', 'LOW'), ('medium', 'MEDIUM'), ('high', 'HIGH')], default=('low', 'LOW'), max_length=20, null=True),
        ),
    ]
