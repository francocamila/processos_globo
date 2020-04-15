from django.urls import path
from . import views

urlpatterns = [
    path('cadastro_de_processos/', views.cadastro_de_processos, name='cadastro_de_processos'),
    path('processos_list/', views.processos_list, name='processos_list'),
    path('', views.login_user, name='login_user'),
    path('submit', views.submit_login, name='submit_login'),
    path('processos_list/delete/<process_id>', views.delete_process),
]