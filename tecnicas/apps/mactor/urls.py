from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import Listar_estudio, Editar_estudio, Consultar_estudio,\
    Crear_actor, Listar_actor, Editar_actor, Consultar_actor, Eliminar_actor_ajax, \
    Crear_ficha, Listar_ficha, Editar_ficha, Consultar_ficha, Eliminar_ficha_ajax, \
    Crear_objetivo, Listar_objetivo, Editar_objetivo, Consultar_objetivo, Eliminar_objetivo_ajax, \
    Crear_relacion_mid, Generar_matriz_mid, Crear_auto_influencia, \
    Crear_1mao, Crear_2mao, Generar_matriz_mao, \
    Consultar_actores_faltantes, Consultar_objetivos_faltantes, probar, actores

# nombre de la url, view que respondera y el parametro name
urlpatterns = [

    # Urls modelo Estudio_mactor
    url(r'^lista_estudios', login_required(Listar_estudio.as_view()), name='lista_estudios'),
    url(r'^editar_estudio/(?P<pk>\d+)/$', Editar_estudio.as_view(), name='editar_estudio'),
    url(r'^consultar_estudio/$', Consultar_estudio),

    # Urls modelo Actor
    url(r'new-actor$', Crear_actor),
    url(r'eliminar_actor-ajax/$', Eliminar_actor_ajax),
    url(r'update_actor-ajax$', Editar_actor),
    url(r'^lista_actores/(\d+)/$', actores, name='lista_actores'),
    url(r'consultar_actor/$', login_required(Consultar_actor)),

    #url(r'actores/(\d+)/$', login_required(actores), name='actores'),

    # Urls modelo ficha_actor
    url(r'^ficha$', Crear_ficha.as_view(), name='ficha'),
    url(r'^lista_fichas', Listar_ficha.as_view(), name='lista_fichas'),
    url(r'^eliminar_ficha-ajax/$', Eliminar_ficha_ajax),
    url(r'^ficha-editar/(?P<pk>\d+)/$', Editar_ficha.as_view(), name='editar_ficha'),
    url(r'^ficha-ajax/$', Consultar_ficha),

    # Urls modelo Objetivo
    url(r'^objetivo$', Crear_objetivo),
    url(r'^lista_objetivos', Listar_objetivo.as_view(), name='lista_objetivos'),
    url(r'^eliminar_objetivo-ajax/$', Eliminar_objetivo_ajax),
    url(r'^objetivo-editar$', Editar_objetivo),
    url(r'^consultar_objetivo/$', Consultar_objetivo),

    # Urls modelo Relacion_MID y matrices
    url(r'^influencia$', Crear_relacion_mid.as_view(), name='influencia'),
    url(r'^matriz_mid', Generar_matriz_mid, name='matriz_mid'),
    url(r'^auto-influencia/$', Crear_auto_influencia),

    # Urls modelo Relacion_MAO y matrices
    url(r'^1mao$', Crear_1mao.as_view(), name='1mao'),
    url(r'^2mao$', Crear_2mao.as_view(), name='2mao'),
    url(r'^matriz_mao/(\d)/', Generar_matriz_mao, name='matriz_mao'),

    # Urls consultas ajax
    url(r'^mid-ajax/$', Consultar_actores_faltantes),  # obtiene lista actores X registrados en la mid
    url(r'^mao-ajax/$', Consultar_objetivos_faltantes) # obtiene lista objetivos X registrados en la mao
]