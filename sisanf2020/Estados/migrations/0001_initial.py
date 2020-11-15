# Generated by Django 3.1.2 on 2020-11-15 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('idBalance', models.AutoField(primary_key=True, serialize=False)),
                ('fechaInicioBalance', models.DateField()),
                ('fechaFinBalance', models.DateField()),
                ('yearEstado', models.PositiveSmallIntegerField()),
                ('moneda_balance', models.CharField(max_length=40)),
                ('moneda_codigo_balance', models.CharField(choices=[('USD', 'Dolares estadounodense'), ('SVC', 'Colón salvadoreño'), ('EUR', 'Euro')], default='USD', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='EstadoDeResultado',
            fields=[
                ('idResultado', models.AutoField(primary_key=True, serialize=False)),
                ('fechaInicioEstado', models.DateField()),
                ('fechaFinEstado', models.DateField()),
                ('yearEstado', models.PositiveSmallIntegerField()),
                ('moneda_estado', models.CharField(max_length=40)),
                ('moneda_codigo_estado', models.CharField(choices=[('USD', 'Dolares estadounodense'), ('SVC', 'Colón salvadoreño'), ('EUR', 'Euro')], default='USD', max_length=3)),
            ],
        ),
    ]
