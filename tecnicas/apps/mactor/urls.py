from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import Listar_estudios, Editar_estudio, Consultar_estudio,\
    Crear_actor, Listar_actores, Editar_actor, Consultar_actor, Eliminar_actor, \
    Crear_ficha, Lista_fichas, Editar_ficha, Consultar_ficha, Eliminar_ficha, \
    Crear_objetivo, Listar_objetivos, Editar_objetivo, Consultar_objetivo, Eliminar_objetivo, \
    Crear_relacion_mid, Generar_matriz_mid, Crear_auto_influencia, \
    Crear_1mao, Crear_2mao, Generar_matriz_mao, \
    Consultar_actores_faltantes, Consultar_objetivos_faltantes

# nombre de la url, view que respondera y el parametro name
urlpatterns = [

    # Urls modelo Estudio_mactor
    url(r'^lista_estudios', login_required(Listar_estudios), name='lista_estudios'),
    url(r'^editar_estudio/(?P<pk>\d+)/$', Editar_estudio.as_view(), name='editar_estudio'),
    url(r'^consultar_estudio/$', login_required(Consultar_estudio)),

    # Urls modelo Actor
    url(r'agregar_actor/$', login_required(Crear_actor)),
    url(r'eliminar_actor/$', login_required(Eliminar_actor)),
    url(r'editar_actor/$', login_required(Editar_actor)),
    url(r'^lista_actores/(?P<idEstudio>\d+)/$', login_required(Listar_actores), name='lista_actores'),
    url(r'consultar_actor/$', login_required(Consultar_actor)),

    # Urls modelo Ficha_actor
    url(r'^agregar_ficha/(?P<idEstudio>\d+)/$', login_required(Crear_ficha), name='ficha'),
    url(r'eliminar_ficha/$', login_required(Eliminar_ficha)),
    url(r'consultar_ficha/$', login_required(Consultar_ficha)),
    url(r'^editar_ficha/(?P<idFicha>\d+)/$', login_required(Editar_ficha), name='editar_ficha'),
    url(r'lista_fichas/(?P<idEstudio>\d+)/$', login_required(Lista_fichas), name='lista_fichas'),

    # Urls modelo Objetivo
    url(r'agregar_objetivo/$', login_required(Crear_objetivo)),
    url(r'^lista_objetivos/(?P<idEstudio>\d+)/$', login_required(Listar_objetivos), name='lista_objetivos'),
    url(r'eliminar_objetivo/$', login_required(Eliminar_objetivo)),
    url(r'editar_objetivo/$', login_required(Editar_objetivo)),
    url(r'consultar_objetivo/$', login_required(Consultar_objetivo)),

    # Urls modelo Relacion_MID y matrices
    url(r'^agregar_influencia/(?P<idEstudio>\d+)/$', Crear_relacion_mid, name='influencia'),
    url(r'^matriz_mid/(?P<idEstudio>\d+)/$', Generar_matriz_mid, name='matriz_mid'),
    url(r'^auto-influencia/$', Crear_auto_influencia),

    # Urls modelo Relacion_MAO y matrices
    url(r'^1mao/(?P<idEstudio>\d+)/$', Crear_1mao, name='1mao'),
    url(r'^2mao$', Crear_2mao.as_view(), name='2mao'),
    url(r'^matriz_mao/(?P<idEstudio>\d+)/(?P<numero_matriz>\d)/', Generar_matriz_mao, name='matriz_mao'),

    # Urls consultas ajax
    url(r'mid-ajax/$', Consultar_actores_faltantes),  # obtiene lista actores X registrados en la mid
    url(r'mao-ajax/$', Consultar_objetivos_faltantes) # obtiene lista objetivos X registrados en la mao
]