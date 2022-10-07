# Generated by Django 3.2 on 2022-05-28 13:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TodoList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='untitled', max_length=128)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('secret_id_uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('secret_id_str', models.CharField(blank=True, max_length=50, null=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='todolists', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ranking', models.PositiveIntegerField(blank=True, null=True)),
                ('description', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
                ('is_finished', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='todos', to=settings.AUTH_USER_MODEL)),
                ('todolist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todos', to='lists.todolist')),
            ],
            options={
                'ordering': ('ranking',),
            },
        ),
    ]
