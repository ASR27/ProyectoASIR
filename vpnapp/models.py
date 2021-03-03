from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

import os
# Create your models here.

class Perfil(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	pubkey = models.CharField(max_length=200)

	def __str__(self):
		return str(self.user.username)

@receiver(post_save, sender=User)
def create_user_perfil(sender, instance, created, **kwargs):
	if created:
		Perfil.objects.create(user=instance)

@receiver(post_save, sender=User)
def sace_user_perfil(sender, instance, **kwargs):
	instance.perfil.save()

class Aula(models.Model):
	nombre = models.CharField(max_length=10)
	serverip = models.GenericIPAddressField(protocol='IPv4')
	serverpubkey = models.CharField(max_length=200)
	serverprivkey = models.CharField(max_length=200)
	endpoint = models.CharField(max_length=200)
	port = models.IntegerField()
	subred = models.GenericIPAddressField(protocol='IPv4')
	clientes = models.ManyToManyField(Perfil, through='Conexion')

	def __str__(self):
		return str(self.nombre)


class Conexion(models.Model):
	alumno = models.ForeignKey(Perfil, on_delete=models.CASCADE)
	interfaz = models.ForeignKey(Aula, on_delete=models.CASCADE)
	ip = models.GenericIPAddressField(protocol='IPv4')

	class Meta:
		unique_together = [['alumno','interfaz']]

	def __str__(self):
		return str(self.ip + " - " + self.alumno.user.username + " - " + self.interfaz.nombre)


###########################################################################################
#Ruta del fichero actualizado.py temporal
###########################################################################################

@receiver(signals.post_save, sender=Perfil)
def actualizar(sender, instance, created, **kwargs):
	os.system("python3 /home/asr/actualizado.py")