from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import CrearEstudio, ListaEstudios, EditarEstudio, \
    ListaPreguntas, CrearPregunta


# nombre de la url, view que respondera y el parametro name
urlpatterns = [

    # Urls modelo Estudio_entrevista
    url(r'^agregar_estudio/$', CrearEstudio.as_view(), name='estudio'),
    url(r'^lista_estudios', ListaEstudios.as_view(), name='lista_estudios'),
    url(r'^editar_estudio/(?P<pk>\d+)/$', EditarEstudio.as_view(), name='editar_estudio'),

    # Urls modelo Pregunta
    url(r'^lista_preguntas', ListaPreguntas.as_view(), name='lista_preguntas'),
    url(r'^crear_pregunta/$', CrearPregunta.as_view(), name='crear_pregunta'),

]