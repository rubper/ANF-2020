from import_export import resources
from .models import Cuenta
class CuentaResouce(resources.ModelResource):
    class Meta:
        model:Cuenta