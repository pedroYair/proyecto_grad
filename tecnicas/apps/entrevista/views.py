from django.shortcuts import render
from .models import *
from .forms import FormEstudio
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView

"""------------------------------------VIEWS MODELO ESTUDIOENTREVISTA------------------------------------"""


class CrearEstudio(CreateView):
    model = EstudioEntrevista
    form_class = FormEstudio
    template_name = 'estudio/crear_estudio_entrevista.html'
    success_url = reverse_lazy('entrevista:lista_estudios')


class ListaEstudios(ListView):
    model = EstudioEntrevista
    template_name = 'estudio/lista_estudios_entrevista.html'
    context_object_name = 'estudios'
    paginate_by = 20


class EditarEstudio(UpdateView):
    model = EstudioEntrevista
    template_name = 'estudio/editar_estudio_entrevista.html'
    form_class = FormEstudio
    success_url = reverse_lazy('entrevista:lista_estudios')


class ListaPreguntas(ListView):
    model = Pregunta
    template_name = 'pregunta/lista_preguntas.html'
    context_object_name = 'preguntas'
    paginate_by = 20



