# Generated by Django 3.2.16 on 2023-05-26 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hit_management', '0002_auto_20230526_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hit',
            name='assignee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignee', to='hit_management.hitman'),
        ),
    ]
