# Generated by Django 3.1.2 on 2020-11-05 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('nomUsuario', models.CharField(max_length=100, unique=True)),
                ('activo', models.BooleanField(default=True)),
                ('administrador', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
