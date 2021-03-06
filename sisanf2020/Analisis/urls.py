from django.urls import path
from .views import *
from . import views

app_name = 'Analisis'

urlpatterns = [

    #URL para  Ratios
    path('Ratios', MostrarRatios.as_view(), name = 'ListaRatios'),
    path('Importar', views.uploadRatios, name='ImportarRatios'),
    #URL analisis horizontal
    path('AnalisisHorizontal/<int:idempresadmin>/<int:anio>', views.indexAnalisisHorizontal, name='AnalisisHorizontal'),
    path('AnalisisHorizontal/<int:anio>', views.indexAnalisisHorizontal, name='AnalisisHorizontal'),
    path('AnalisisVertical/<int:idempresadmin>/<int:anio>', views.indexAnalisisVertical, name='AnalisisVertical'),
    path('AnalisisVertical/<int:anio>', views.indexAnalisisVertical, name='AnalisisVertical'),
    path('Analisis/', views.VerOverView, name='VerAnalisis'),
    path('OverView/', views.OverView, name='OverView'),
    path('Razones/<int:idempresadmin>/<int:anio>',views.Analisis_razones,name='Razones'),
    path('Razones/<int:anio>',views.Analisis_razones,name='Razones'),
    path('Editar/<int:anali>/<int:anio>/<int:idempresadmin>',views.editar_conclusion,name='Editar_Conclusion')
]
