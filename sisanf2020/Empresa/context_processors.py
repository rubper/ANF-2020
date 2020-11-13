from .models import Empresa

def ContextoGlobal(request):
    emp = Empresa.objects.all().values('idEmpresa', 'rasonsocial')
    return {'emp':emp}
