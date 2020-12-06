from django.contrib.auth.models import User, Group
from rest_framework import serializers
from vpnapp.models import *


class PerfilSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Perfil
		fields = ['id','pubkey']

class AulaSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Aula
		fields = ['id','nombre','serverpubkey','endpoint','clientes']

class ConexionSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Conexion
		fields = ['ip','alumno','interfaz']