# Generated by Django 3.1.2 on 2020-11-15 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresa', '0002_auto_20201113_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuenta',
            name='naturaleza_cuenta',
            field=models.CharField(choices=[('Acreedor', 'Acreedor'), ('Deudor', 'Deudor')], max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='cuenta',
            name='tipo_cuenta',
            field=models.CharField(choices=[('Activo Corrinte', 'Activo Corrinte'), ('Activo no Corrinte', 'Activo no Corrinte'), ('Pasivo Corriente', 'Pasivo Corrinte'), ('Pasivo no Corrinte', 'Pasivo no Corrinte'), ('Capital', 'Capital'), ('Estado de Resultado', 'Estado de Resultado')], max_length=25, null=True),
        ),
    ]
