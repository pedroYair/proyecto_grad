from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import Listar_estudios, Crear_estudio, Editar_estudio, Consultar_estudio,\
    Crear_actor, Listar_actores, Editar_actor, Consultar_actor, Eliminar_actor, \
    Crear_ficha, Lista_fichas, Editar_ficha, Consultar_ficha, Eliminar_ficha, Consultar_ficha_mid, \
    Crear_objetivo, Listar_objetivos, Editar_objetivo, Consultar_objetivo, Eliminar_objetivo, \
    Crear_relacion_mid, Generar_matriz_mid, Generar_matriz_midi, Generar_matriz_maxima, Generar_matriz_ri, \
    Generar_matriz_balance, Generar_indicador_estabilidad, Crear_1mao, Crear_2mao, Generar_matriz_mao,\
    Generar_matrices_caa_daa, Consultar_actores_faltantes, Consultar_objetivos_faltantes, \
    exportar_estudios_xls, exportar_actores_xls, exportar_fichas_xls, exportar_objetivos_xls, \
    histograma_mid, datos_histograma_mid, histograma_ri, datos_histograma_ri, \
    histograma_implicacion, obtener_datos_histograma, histograma_movilizacion,  \
    datos_histograma_caa_daa, histograma_caa_daa, \
    generar_mapa_midi, datos_mapa_midi, generar_mapa_caa_daa, datos_mapa_caa_daa, \
    generar_grafo_caa, datos_grafo_caa, generar_grafo_daa, datos_grafo_daa, \
    concenso_matriz_influencias, concenso_grafico_influencias, \
    activar_concenso_mao


# nombre de la url, view que respondera y el parametro name
urlpatterns = [

    # Urls modelo Estudio_mactor
    url(r'^agregar_estudio/$', Crear_estudio.as_view(), name='estudio'),
    url(r'^lista_estudios', login_required(Listar_estudios), name='lista_estudios'),
    url(r'^editar_estudio/(?P<pk>\d+)/$', Editar_estudio.as_view(), name='editar_estudio'),
    url(r'^consultar_estudio/$', login_required(Consultar_estudio)),

    # Urls modelo Actor
    url(r'agregar_actor/$', login_required(Crear_actor)),
    url(r'eliminar_actor/$', login_required(Eliminar_actor)),
    url(r'editar_actor/$', login_required(Editar_actor)),
    url(r'^lista_actores/(?P<idEstudio>\d+)/$', login_required(Listar_actores), name='lista_actores'),
    url(r'consultar_actor', login_required(Consultar_actor)),

    # Urls modelo Ficha_actor
    url(r'^agregar_ficha/(?P<idEstudio>\d+)/$', login_required(Crear_ficha), name='ficha'),
    url(r'eliminar_ficha/$', login_required(Eliminar_ficha)),
    url(r'consultar_ficha/$', login_required(Consultar_ficha)),
    url(r'^editar_ficha/(?P<idFicha>\d+)/$', login_required(Editar_ficha), name='editar_ficha'),
    url(r'lista_fichas/(?P<idEstudio>\d+)/$', login_required(Lista_fichas), name='lista_fichas'),
    url(r'consultar_ficha_mid/$', login_required(Consultar_ficha_mid)),

    # Urls modelo Objetivo
    url(r'agregar_objetivo/$', login_required(Crear_objetivo)),
    url(r'^lista_objetivos/(?P<idEstudio>\d+)/$', login_required(Listar_objetivos), name='lista_objetivos'),
    url(r'eliminar_objetivo/$', login_required(Eliminar_objetivo)),
    url(r'editar_objetivo/$', login_required(Editar_objetivo)),
    url(r'consultar_objetivo', login_required(Consultar_objetivo)),

    # Urls modelo Relacion_MID y matrices
    url(r'^agregar_influencia/(?P<idEstudio>\d+)/$', login_required(Crear_relacion_mid), name='influencia'),
    url(r'^matriz_mid/(?P<idEstudio>\d+)/$', login_required(Generar_matriz_mid), name='matriz_mid'),
    url(r'^matriz_midi/(?P<idEstudio>\d+)/$', login_required(Generar_matriz_midi), name='matriz_midi'),
    url(r'^matriz_maxima/(?P<idEstudio>\d+)/$', login_required(Generar_matriz_maxima), name='matriz_maxima'),
    url(r'^matriz_ri/(?P<idEstudio>\d+)/$', login_required(Generar_matriz_ri), name='matriz_ri'),
    url(r'^matriz_balance/(?P<idEstudio>\d+)/$', login_required(Generar_matriz_balance), name='matriz_balance'),
    url(r'^estabilidad/(?P<idEstudio>\d+)/$', login_required(Generar_indicador_estabilidad), name='estabilidad'),

    # Urls modelo Relacion_MAO y matrices
    url(r'^1mao/(?P<idEstudio>\d+)/$', login_required(Crear_1mao), name='1mao'),
    url(r'^2mao/(?P<idEstudio>\d+)/$', login_required(Crear_2mao), name='2mao'),
    url(r'^matriz_mao/(?P<idEstudio>\d+)/(?P<numero_matriz>\d)/', login_required(Generar_matriz_mao), name='matriz_mao'),
    url(r'^matriz_caa_daa/(?P<idEstudio>\d+)/(?P<numero_matriz>\d)/', login_required(Generar_matrices_caa_daa), name='caa_daa'),

    # Urls consultas ajax
    url(r'mid-ajax/$', login_required(Consultar_actores_faltantes)),  # obtiene lista actores X registrados en la mid
    url(r'mao-ajax/$', login_required(Consultar_objetivos_faltantes)),  # obtiene lista objetivos X registrados en la mao

    # Urls histogramas de influencia
    url(r'^histograma_mid/(?P<idEstudio>\d+)/$', login_required(histograma_mid), name='histograma_mid'),
    url(r'datos_histograma_mid', login_required(datos_histograma_mid)),
    url(r'^histograma_ri/(?P<idEstudio>\d+)/$', login_required(histograma_ri), name='histograma_ri'),
    url(r'datos_histograma_ri', login_required(datos_histograma_ri)),

    # Urls exportar a excel
    url(r'exportar_estudios/xls/(?P<idEstudio>\d+)/$', login_required(exportar_estudios_xls), name='estudios_xls'),

    # Urls histogramas mao
    url(r'^histograma_implicacion/(?P<idEstudio>\d+)/(?P<numero_matriz>\d)/$', login_required(histograma_implicacion),
        name='implicacion'),
    url(r'^histograma_movilizacion/(?P<idEstudio>\d+)/(?P<numero_matriz>\d)/$', login_required(histograma_movilizacion),
        name='movilizacion'),
    url(r'datos_histograma', login_required(obtener_datos_histograma)),

    # Urls mapa actores
    url(r'^mapa_actores/(?P<idEstudio>\d+)/$', login_required(generar_mapa_midi), name='mapa_actores'),
    url(r'datos_plano_midi', login_required(datos_mapa_midi)),

    # Urls graficos caa y daa
    url(r'^mapa_caa_daa/(?P<idEstudio>\d+)/(?P<numero_matriz>\d)/$', login_required(generar_mapa_caa_daa), name='mapa_caa_daa'),
    url(r'datos_mapa_caa_daa', login_required(datos_mapa_caa_daa)),
    url(r'^histograma_caa_daa/(?P<idEstudio>\d+)/(?P<numero_matriz>\d)/$', histograma_caa_daa, name='hist_caa_daa'),
    url(r'datos_caa_daa', login_required(datos_histograma_caa_daa)),

    # Urls grafos
    url(r'^grafo_caa/(?P<idEstudio>\d+)/(?P<numero_matriz>\d)$', login_required(generar_grafo_caa), name='grafo_caa'),
    url(r'datos_grafo_caa', login_required(datos_grafo_caa)),
    url(r'^grafo_daa/(?P<idEstudio>\d+)/(?P<numero_matriz>\d)$', login_required(generar_grafo_daa), name='grafo_daa'),
    url(r'datos_grafo_daa', login_required(datos_grafo_daa)),

    # Urls concensos
    url(r'^concenso_influencias/(?P<idEstudio>\d+)/(?P<matriz>\d)/', login_required(concenso_matriz_influencias), name='concenso_influencias'),
    url(r'^concenso_grafico_influencias/(?P<idEstudio>\d+)/(?P<grafico>\d)/', login_required(concenso_grafico_influencias), name='concenso_inf_graficos'),
    url(r'^concenso_mao/(?P<idEstudio>\d+)/(?P<matriz>\d)/', login_required(activar_concenso_mao), name='concenso_mao'),

]