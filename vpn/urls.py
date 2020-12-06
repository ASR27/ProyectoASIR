"""vpn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from vpnapp import views
from vpnapp.views import *

router = routers.DefaultRouter()
router.register(r'perfiles', views.PerfilAPI)
router.register(r'aulas', views.AulaAPI)
router.register(r'conexiones', views.ConexionAPI)



urlpatterns = [
	path('', include(router.urls)),
    path('admin/', admin.site.urls),
    # path('perfillist/', PerfilList.as_view(), name="usuarios"),
    # path('configuracion/<int:pk>', Configuracion.as_view(), name="configuracion"),
    path('conexionlist/', ConexionList.as_view(), name="conexiones"),
    path('conexiondetail/<int:pk>/', ConexionDetail.as_view(), name="detalles"),
    path('aulalist/', AulaList.as_view(), name="aulas"),
    path('auladetail/<int:pk>/', AulaDetail.as_view(), name="aula_detalles"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
