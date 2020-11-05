from import_export import resources
from Giro.models import Ratios

class RatiosResource(resources.ModelResource):
    class Meta:
        model = Ratios
