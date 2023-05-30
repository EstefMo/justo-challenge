# Generated by Django 3.2.16 on 2023-05-25 22:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('permission', models.ManyToManyField(to='hit_management.Permission')),
            ],
        ),
        migrations.CreateModel(
            name='Hitman',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=45)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')], default='ACTIVE', max_length=8)),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hit_management.rol')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userId', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('targetName', models.CharField(max_length=45)),
                ('status', models.CharField(choices=[('OPENED', 'opened'), ('ASSIGNED', 'assigned'), ('COMPLETED', 'completed'), ('FAILED', 'failed')], max_length=15)),
                ('assignee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignee', to='hit_management.hitman')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to='hit_management.hitman')),
            ],
        ),
    ]