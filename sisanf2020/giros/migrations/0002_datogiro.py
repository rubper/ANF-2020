# Generated by Django 3.1.2 on 2020-10-27 01:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ratios', '0001_initial'),
        ('giros', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatoGiro',
            fields=[
                ('idDato', models.AutoField(primary_key=True, serialize=False)),
                ('valorParametro', models.FloatField(default=0)),
                ('valorPromedio', models.FloatField(default=0)),
                ('idGiro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='giros.giro')),
                ('idRatio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ratios.ratios')),
            ],
        ),
    ]