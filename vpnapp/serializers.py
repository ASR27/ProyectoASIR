from django.contrib.auth.models import User, Group
from rest_framework import serializers
from vpnapp.models import *


class PerfilSerializer(serializers.ModelSerializer):
	class Meta:
		model = Perfil
		fields = ['id','pubkey']

class AulaSerializer(serializers.ModelSerializer):
	class Meta:
		model = Aula
		fields = ['id','nombre','serverpubkey','endpoint','clientes']

class ConexionSerializer(serializers.ModelSerializer):
	alumno = PerfilSerializer()
	interfaz = AulaSerializer()

	class Meta:
		model = Conexion
		fields = ['ip','alumno','interfaz']
