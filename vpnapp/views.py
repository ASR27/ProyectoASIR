from django.conf import settings
from django.shortcuts import HttpResponse, render, redirect, HttpResponseRedirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required,user_passes_test
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAdminUser
from vpnapp.serializers import PerfilSerializer, AulaSerializer, ConexionSerializer

from .models import *

##############################

# Vistas

##############################


class ConexionList(ListView):
	model = Conexion
	template_name = "conexionlist.html"

class ConexionDetail(DetailView):
	model = Conexion
	template_name = "conexionconf.html"
	fields = '__all__'

	def get_content_data(self, **kwargs):
 		context = super().get_content_data(**kwargs)
 		return

class AulaList(ListView):
 	model = Aula
 	template_name = "aulalist.html"

class AulaDetail(DetailView):
	model = Aula
	template_name = "auladetail.html"
	fields = '__all__'

	def get_content_data(self, **kwargs):
 		context = super().get_content_data(**kwargs)
 		return

	def get_context_data(self, *args, **kwargs):
		context = super(AulaDetail, self).get_context_data(*args, **kwargs)
		context["cperfil"] = Perfil.objects.all().values()
		context["cconexion"] = Conexion.objects.all().values()
		return context

###############################

# API

###############################

class PerfilAPI(viewsets.ModelViewSet):
	queryset = Perfil.objects.all()
	serializer_class = PerfilSerializer
	permission_classes = [permissions.IsAuthenticated]

class AulaAPI(viewsets.ModelViewSet):
	queryset = Aula.objects.all()
	serializer_class = AulaSerializer
	permission_classes = [permissions.IsAuthenticated]

class ConexionAPI(viewsets.ModelViewSet):
	queryset = Conexion.objects.all()
	serializer_class = ConexionSerializer
	permission_classes = [permissions.IsAuthenticated]