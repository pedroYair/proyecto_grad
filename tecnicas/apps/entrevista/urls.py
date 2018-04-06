from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import CrearEstudio, ListaEstudios, EditarEstudio, \
    ListaPreguntas, CrearPregunta, \
    ListaValoresEscala, CrearValorEscala, \
    ListaRondas, CrearRonda, \
    ListaJuicios, CrearJuicio


# nombre de la url, view que respondera y el parametro name
urlpatterns = [

    # Urls modelo Estudio_entrevista
    url(r'^agregar_estudio/$', CrearEstudio.as_view(), name='estudio'),
    url(r'^lista_estudios', ListaEstudios.as_view(), name='lista_estudios'),
    url(r'^editar_estudio/(?P<pk>\d+)/$', EditarEstudio.as_view(), name='editar_estudio'),

    # Urls modelo Pregunta
    url(r'^lista_preguntas', ListaPreguntas.as_view(), name='lista_preguntas'),
    url(r'^crear_pregunta/$', CrearPregunta.as_view(), name='crear_pregunta'),

    # Urls modelo Valor escala
    url(r'^lista_valores_escala', ListaValoresEscala.as_view(), name='escala'),
    url(r'^registrar_valor/$', CrearValorEscala.as_view(), name='registrar_valor'),

    # Urls modelo Valor escala
    url(r'^lista_rondas', ListaRondas.as_view(), name='rondas'),
    url(r'^registrar_ronda/$', CrearRonda.as_view(), name='registrar_ronda'),

    # Urls modelo Juicio
    url(r'^lista_juicios', ListaJuicios.as_view(), name='juicios'),
    url(r'^registrar_juicio/$', CrearJuicio.as_view(), name='registrar_juicio'),

]