from django.shortcuts import render
from .models import *
from .forms import FormEstudio
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import CreateView


class crearEstudio(CreateView):
    model = EstudioEntrevista
    form_class = FormEstudio
    template_name = 'estudio/crear_estudio_entrevista.html'
    success_url = reverse_lazy('entrevista:estudio')

