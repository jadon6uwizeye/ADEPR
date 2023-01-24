# Generated by Django 4.1.5 on 2023-01-24 07:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LocalChurch',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
            ],
            options={
                'verbose_name': 'Local church',
                'verbose_name_plural': 'Amatorero',
            },
        ),
        migrations.CreateModel(
            name='Parish',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
            ],
            options={
                'verbose_name': 'Parish',
                'verbose_name_plural': 'Parishes',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
            ],
            options={
                'verbose_name': 'Region',
                'verbose_name_plural': 'Regions',
            },
        ),
        migrations.CreateModel(
            name='Ururembo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
            ],
            options={
                'verbose_name': 'Ururembo',
                'verbose_name_plural': 'Indembo',
            },
        ),
    ]
