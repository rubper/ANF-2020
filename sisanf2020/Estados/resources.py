from import_export import resources
from Empresa.models import SaldoDeCuentaResultado

class EstadoResource(resources.ModelResource):
    class Meta:
        model = SaldoDeCuentaResultado