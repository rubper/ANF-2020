# Generated by Django 3.1.2 on 2020-11-19 05:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


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
                ('rol', models.SmallIntegerField(choices=[(1, 'Administrador'), (2, 'Analista'), (3, 'Gerente')], default=1)),
                ('is_administrador', models.BooleanField(default=False)),
                ('is_analista', models.BooleanField(default=False)),
                ('is_gerente', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OpcionForm',
            fields=[
                ('idOpcion', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('descOpcion', models.CharField(max_length=100)),
                ('numForm', models.PositiveIntegerField()),
            ],
            options={
                'unique_together': {('idOpcion', 'descOpcion', 'numForm')},
            },
        ),
        migrations.CreateModel(
            name='AccesoUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idOpcion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Usuarios.opcionform')),
                ('idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('idUsuario', 'idOpcion')},
            },
        ),
    ]
