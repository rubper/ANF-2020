# Generated by Django 3.1.2 on 2020-11-15 05:06

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Giro',
            fields=[
                ('idGiro', models.PositiveIntegerField(primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)])),
                ('nombreGiro', models.CharField(max_length=100)),
                ('sector', models.CharField(choices=[('SP', 'Sector primario'), ('SS', 'Sector secundario'), ('ST', 'Sector terciario')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Ratios',
            fields=[
                ('idRatio', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('categoria', models.CharField(max_length=50)),
                ('nomRatio', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='DatoGiro',
            fields=[
                ('idDato', models.AutoField(primary_key=True, serialize=False)),
                ('valorParametro', models.FloatField(default=0)),
                ('valorPromedio', models.FloatField(default=0)),
                ('idGiro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Giro.giro')),
                ('idRatio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Giro.ratios')),
            ],
            options={
                'unique_together': {('idGiro', 'idRatio')},
            },
        ),
    ]
