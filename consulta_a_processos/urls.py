from django.urls import path
from . import views

urlpatterns = [
    path('', views.cadastro_de_processos, name='cadastro_de_processos'),
]