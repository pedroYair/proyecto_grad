from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import CrearEstudio, ListaEstudios

# nombre de la url, view que respondera y el parametro name
urlpatterns = [

    # Urls modelo Estudio_entrevista
    url(r'^agregar_estudio/$', CrearEstudio.as_view(), name='estudio'),
    url(r'^lista_estudios/$', ListaEstudios.as_view(), name='lista_estudios'),

]