# Generated by Django 3.2.16 on 2023-05-26 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hit_management', '0003_alter_hit_assignee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='hit_management.hitman')),
            ],
        ),
        migrations.RemoveField(
            model_name='rol',
            name='permission',
        ),
        migrations.RenameField(
            model_name='hit',
            old_name='targetName',
            new_name='target_name',
        ),
        migrations.RemoveField(
            model_name='hitman',
            name='rol',
        ),
        migrations.DeleteModel(
            name='Permission',
        ),
        migrations.DeleteModel(
            name='Rol',
        ),
        migrations.AddField(
            model_name='manager',
            name='lackeys',
            field=models.ManyToManyField(blank=True, related_name='managers', to='hit_management.Hitman'),
        ),
    ]
