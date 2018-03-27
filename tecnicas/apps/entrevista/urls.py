from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import crearEstudio

# nombre de la url, view que respondera y el parametro name
urlpatterns = [

    # Urls modelo Estudio_entrevista
    url(r'^agregar_estudio/$', crearEstudio.as_view(), name='estudio'),

]