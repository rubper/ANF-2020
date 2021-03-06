from django.db import models
from Giro.models import Giro
from Estados.models import EstadoDeResultado, Balance
from Usuarios.models import User

# Información general de la empresa
class Empresa(models.Model):
    idEmpresa= models.AutoField(primary_key=True)
    gerente = models.OneToOneField(User, on_delete = models.CASCADE, null=False, blank=False)
    idGiro=models.ForeignKey(Giro, on_delete= models.CASCADE)
    rasonsocial =models.CharField(max_length= 50)
    telefono = models.CharField(max_length = 9)
    nrc= models.CharField(max_length =8)
    nit= models.CharField(max_length = 17)
    direccion= models.CharField(max_length = 100)
    EstadosDeEmpresa = models.ManyToManyField(EstadoDeResultado,through='EstadoEmpresa')
    BalancesDeEmpresa = models.ManyToManyField(Balance,through='BalanceEmpresa')

    def __str__(self):
     return  self.rasonsocial

#este modelo servira pera relacionar las cuentas con los ratios
class SobreNombre(models.Model):
    idSobreNombre = models.AutoField(primary_key=True)
    sobreNombre = models.CharField(max_length=100)

    def __str__(self):
     return  self.sobreNombre


#Cuentas de la empresa
class Cuenta(models.Model):
    tipo=(
        ('Activo Corriente','Activo Corriente'),
        ('Activo no Corriente','Activo no Corriente'),
        ('Pasivo Corriente','Pasivo Corriente'),
        ('Pasivo no Corriente','Pasivo no Corriente'),
        ('Capital','Capital'),
        ('Estado de Resultado','Estado de Resultado'),
    )
    naturaleza=(
        ('Acreedor','Acreedor'),
        ('Deudor','Deudor'),
    )
    idCuenta = models.AutoField(primary_key=True)
    idEmpresa = models.ForeignKey(Empresa,on_delete=models.CASCADE)
    codigo_cuenta = models.CharField(max_length=13)
    nombre_cuenta = models.CharField(max_length=100)
    tipo_cuenta = models.CharField(choices=tipo, max_length=25,null=True)
    naturaleza_cuenta = models.CharField(choices=naturaleza,max_length=12,null=True)
    idSobreNombre = models.ForeignKey(SobreNombre,on_delete=models.CASCADE,null=True)

    def __str__(self):
     return  self.nombre_cuenta

# Valores de cuentas necesarios para los estados

class SaldoDeCuentaBalace(models.Model):
    idSaldo = models.AutoField(primary_key=True)
    idCuenta = models.ForeignKey(Cuenta,on_delete=models.CASCADE)
    idbalance = models.ForeignKey(Balance,on_delete=models.CASCADE)
    year_saldo = models.DateField()
    monto_saldo = models.DecimalField(max_digits=15, decimal_places=2,null=True)

class SaldoDeCuentaResultado(models.Model):
    idSaldoResul = models.AutoField(primary_key=True)
    idCuenta = models.ForeignKey(Cuenta,on_delete=models.CASCADE)
    idResultado = models.ForeignKey(EstadoDeResultado,on_delete=models.CASCADE)
    year_saldo_Resul = models.DateField()
    monto_saldo_Resul = models.DecimalField(max_digits=15, decimal_places=2,null=True)



#Muchos a muchos, clase intermedia

class EstadoEmpresa(models.Model):
    idResultado = models.ForeignKey(EstadoDeResultado, on_delete=models.CASCADE)
    idEmpresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

class BalanceEmpresa(models.Model):
    idbalance = models.ForeignKey(Balance, on_delete=models.CASCADE)
    idEmpresa = models.ForeignKey(Empresa,on_delete=models.CASCADE)
