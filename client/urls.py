from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('generate/', views.generar_identidad, name='generar_identidad'),
    path('download/', views.descargar_credenciales, name='descargar_credenciales'),
    path('login/', views.login_anonimo, name='login_anonimo'),
    path('dashboard/', views.dashboard_anonimo, name='dashboard_anonimo'),
    
     path('crear/', views.crear_secreto, name='crear_secreto'),
]


