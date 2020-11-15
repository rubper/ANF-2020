# Generated by Django 3.1.2 on 2020-11-15 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Empresa', '0001_initial'),
        ('Estados', '0001_initial'),
        ('Giro', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analisis',
            fields=[
                ('idAnalisis', models.AutoField(primary_key=True, serialize=False)),
                ('year_analisis', models.PositiveSmallIntegerField(default=2020)),
                ('year_previos', models.PositiveSmallIntegerField()),
                ('conclusion_horizontal', models.TextField(max_length=1500, null=True)),
                ('conclusion_vertical', models.TextField(max_length=1500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RatiosAnalisis',
            fields=[
                ('idRatioAnalisis', models.AutoField(primary_key=True, serialize=False)),
                ('valorRatiosAnalisis', models.DecimalField(decimal_places=4, max_digits=8)),
                ('conclusion', models.TextField(max_length=1500, null=True)),
                ('idAnalisis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Analisis.analisis')),
                ('idRatios', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Giro.ratios')),
            ],
        ),
        migrations.CreateModel(
            name='LineaDeInforme',
            fields=[
                ('idLineaInfo', models.AutoField(primary_key=True, serialize=False)),
                ('variacion_horizontal', models.DecimalField(decimal_places=2, max_digits=11)),
                ('porcentaje_horizontal', models.DecimalField(decimal_places=4, max_digits=5)),
                ('porcentaje_vertical', models.DecimalField(decimal_places=4, max_digits=5, null=True)),
                ('idAnalisis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Analisis.analisis')),
                ('idCuenta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresa.cuenta')),
            ],
        ),
        migrations.CreateModel(
            name='EstadoAnalisis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idAnalisis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Analisis.analisis')),
                ('idResultado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Estados.estadoderesultado')),
            ],
        ),
        migrations.CreateModel(
            name='BalanceAnalisis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idAnalisis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Analisis.analisis')),
                ('idbalance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Estados.balance')),
            ],
        ),
        migrations.AddField(
            model_name='analisis',
            name='balancesParaAnalisis',
            field=models.ManyToManyField(through='Analisis.BalanceAnalisis', to='Estados.Balance'),
        ),
        migrations.AddField(
            model_name='analisis',
            name='estadosParaAnalisis',
            field=models.ManyToManyField(through='Analisis.EstadoAnalisis', to='Estados.EstadoDeResultado'),
        ),
        migrations.AddField(
            model_name='analisis',
            name='idEmpresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Empresa.empresa'),
        ),
    ]
