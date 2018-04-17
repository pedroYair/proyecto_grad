from django.shortcuts import render
from .models import *
from .forms import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string

"""------------------------------------VIEWS MODELO ESTUDIOENTREVISTA------------------------------------"""


class CrearEstudio(CreateView):
    model = EstudioEntrevista
    form_class = FormEstudioE
    template_name = 'estudio/crear_estudio_entrevista.html'
    success_url = reverse_lazy('entrevista:lista_estudios')


class ListaEstudios(ListView):
    model = EstudioEntrevista
    template_name = 'estudio/lista_estudios_entrevista.html'
    context_object_name = 'estudios'
    paginate_by = 15

    def get_queryset(self):
        return EstudioEntrevista.objects.all().order_by('titulo')


class EditarEstudio(UpdateView):   # por arreglar template
    model = EstudioEntrevista
    template_name = 'estudio/editar_estudio_entrevista.html'
    form_class = FormEstudioE
    success_url = reverse_lazy('entrevista:lista_estudios')

"""------------------------------------VIEWS MODELO PREGUNTA------------------------------------"""


class ListaPreguntas(ListView):
    model = Pregunta
    template_name = 'pregunta/lista_preguntas.html'
    context_object_name = 'preguntas'
    paginate_by = 15


    def get_queryset(self):
        self.estudio = get_object_or_404(EstudioEntrevista, id=self.args[0])
        return Pregunta.objects.filter(idEstudio=self.estudio.id).order_by('texto_pregunta')

    def get_context_data(self, **kwargs):
        context = super(ListaPreguntas, self).get_context_data(**kwargs)
        context['estudio'] = self.estudio
        context['usuario'] = obtener_tipo_usuario(self, self.estudio.id)
        return context


class CrearPregunta(CreateView):
    model = Pregunta
    form_class = FormPregunta
    template_name = 'pregunta/crear_pregunta.html'

    def get_context_data(self, **kwargs):
        context = super(CrearPregunta, self).get_context_data(**kwargs)
        self.estudio = get_object_or_404(EstudioEntrevista, id=self.args[0])
        context['estudio'] = self.estudio
        return context

"""------------------------------------VIEWS MODELO VALOR ESCALA------------------------------------"""


class ListaValoresEscala(ListView):
    model = ValorEscalaLikert
    template_name = 'escala/lista_valores.html'
    context_object_name = 'valores'
    paginate_by = 10

    def get_queryset(self):
        self.estudio = get_object_or_404(EstudioEntrevista, id=self.args[0])
        return ValorEscalaLikert.objects.filter(idEstudio=self.estudio.id).order_by('valor')

    def get_context_data(self, **kwargs):
        context = super(ListaValoresEscala, self).get_context_data(**kwargs)
        context['estudio'] = self.estudio
        context['usuario'] = obtener_tipo_usuario(self, self.estudio.id)
        return context


class CrearValorEscala(CreateView):
    model = ValorEscalaLikert
    form_class = FormValorEscala
    template_name = 'escala/registrar_valor_escala.html'

    def get_context_data(self, **kwargs):
        context = super(CrearValorEscala, self).get_context_data(**kwargs)
        self.estudio = get_object_or_404(EstudioEntrevista, id=self.args[0])
        context['estudio'] = self.estudio
        return context

"""------------------------------------VIEWS MODELO RONDA-----------------------------------------"""


class ListaRondas(ListView):
    model = RondaJuicio
    template_name = 'ronda/lista_rondas.html'
    context_object_name = 'rondas'
    paginate_by = 10

    def get_queryset(self):
        self.estudio = get_object_or_404(EstudioEntrevista, id=self.args[0])
        return RondaJuicio.objects.filter(idEstudio=self.estudio.id).order_by('numero_ronda')

    def get_context_data(self, **kwargs):
        context = super(ListaRondas, self).get_context_data(**kwargs)
        context['estudio'] = self.estudio
        context['usuario'] = obtener_tipo_usuario(self, self.estudio.id)
        return context


class CrearRonda(CreateView):
    model = ValorEscalaLikert
    form_class = FormRonda
    template_name = 'ronda/crear_ronda.html'

    def get_context_data(self, **kwargs):
        context = super(CrearRonda, self).get_context_data(**kwargs)
        self.estudio = get_object_or_404(EstudioEntrevista, id=self.args[0])
        context['estudio'] = self.estudio
        return context


"""------------------------------------VIEWS MODELO JUICIO-----------------------------------------"""


class ListaJuicios(ListView):
    model = Juicio
    template_name = 'juicio/lista_juicios.html'
    context_object_name = 'juicios'
    paginate_by = 10

    def get_queryset(self):
        self.estudio = get_object_or_404(EstudioEntrevista, id=self.args[0])
        return Juicio.objects.filter(idPregunta__idEstudio=self.estudio.id).order_by('idPregunta')

    def get_context_data(self, **kwargs):
        context = super(ListaJuicios, self).get_context_data(**kwargs)
        context['estudio'] = self.estudio
        context['usuario'] = obtener_tipo_usuario(self, self.estudio.id)
        return context


class CrearJuicio(CreateView):
    model = Juicio
    form_class = FormJuicio
    template_name = 'juicio/crear_juicio.html'

    def get_context_data(self, **kwargs):
        context = super(CrearJuicio, self).get_context_data(**kwargs)
        self.estudio = get_object_or_404(EstudioEntrevista, id=self.args[0])
        context['estudio'] = self.estudio
        return context


"""----------------------------------------------------FUNCIONES AUXILIARES------------------------------"""


def obtener_tipo_usuario(self, idEstudio):

    estudio = EstudioEntrevista.objects.get(id=idEstudio)
    lista_expertos = estudio.idExpertos.all()
    tipo = ""

    if self.request.user == estudio.idAdministrador or self.request.user == estudio.idCoordinador:
        tipo = "COORDINADOR"
    elif self.request.user in lista_expertos:
        tipo = "EXPERTO"
    print(tipo, "-------")
    return tipo





