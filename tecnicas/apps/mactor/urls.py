from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import listar_estudios, crear_estudio, editar_estudio, consultar_estudio,\
    crear_actor, listar_actores, editar_actor, consultar_actor, eliminar_actor, \
    crear_ficha, lista_fichas, editar_ficha, consultar_ficha, eliminar_ficha, consultar_ficha_mid, \
    crear_objetivo, listar_objetivos, editar_objetivo, consultar_objetivo, eliminar_objetivo, \
    crear_relacion_mid, generar_matriz_mid, generar_matriz_midi, generar_matriz_maxima, generar_matriz_ri, \
    generar_matriz_balance, generar_indicador_estabilidad, crear_1mao, crear_2mao, generar_matriz_mao,\
    generar_matrices_caa_daa, consultar_actores_faltantes, consultar_objetivos_faltantes, \
    crear_informe, exportar_estudio_xls, \
    histograma_mid, datos_histograma_mid, histograma_ri, datos_histograma_ri, \
    histograma_implicacion, histograma_movilizacion, datos_histogramas_mao,  \
    datos_histograma_caa_daa, histograma_caa_daa, \
    generar_mapa_midi, datos_mapa_midi, generar_mapa_caa_daa, datos_mapa_caa_daa, \
    generar_grafo_caa, datos_grafo_caa, generar_grafo_daa, datos_grafo_daa, \
    activar_consenso_influencias, activar_consenso_mao, activar_consenso_caa_daa

# nombre de la url, view que respondera y el parametro name
urlpatterns = [

    # Urls modelo Estudio_mactor
    url(r'^agregar_estudio/$', crear_estudio.as_view(), name='estudio'),
    url(r'^lista_estudios', login_required(listar_estudios), name='lista_estudios'),
    url(r'^editar_estudio/(?P<idEstudio>\d+)/$', login_required(editar_estudio), name='editar_estudio'),
    url(r'^consultar_estudio/$', login_required(consultar_estudio)),

    # Urls modelo Actor
    url(r'agregar_actor/$', login_required(crear_actor)),
    url(r'eliminar_actor/$', login_required(eliminar_actor)),
    url(r'editar_actor/$', login_required(editar_actor)),
    url(r'^lista_actores/(?P<idEstudio>\d+)/$', login_required(listar_actores), name='lista_actores'),
    url(r'consultar_actor', login_required(consultar_actor)),

    # Urls modelo Ficha
    url(r'^agregar_ficha/(?P<idEstudio>\d+)/$', login_required(crear_ficha), name='ficha'),
    url(r'eliminar_ficha/$', login_required(eliminar_ficha)),
    url(r'consultar_ficha/$', login_required(consultar_ficha)),
    url(r'^editar_ficha/(?P<idFicha>\d+)/$', login_required(editar_ficha), name='editar_ficha'),
    url(r'lista_fichas/(?P<idEstudio>\d+)/$', login_required(lista_fichas), name='lista_fichas'),
    url(r'consultar_ficha_mid/$', login_required(consultar_ficha_mid)),

    # Urls modelo Objetivo
    url(r'agregar_objetivo/$', login_required(crear_objetivo)),
    url(r'^lista_objetivos/(?P<idEstudio>\d+)/$', login_required(listar_objetivos), name='lista_objetivos'),
    url(r'eliminar_objetivo/$', login_required(eliminar_objetivo)),
    url(r'editar_objetivo/$', login_required(editar_objetivo)),
    url(r'consultar_objetivo', login_required(consultar_objetivo)),

    # Urls modelo Relacion_MID y matrices
    url(r'^agregar_influencia/(?P<idEstudio>\d+)/$', login_required(crear_relacion_mid), name='influencia'),
    url(r'^matriz_mid/(?P<idEstudio>\d+)/$', login_required(generar_matriz_mid), name='matriz_mid'),
    url(r'^matriz_midi/(?P<idEstudio>\d+)/$', login_required(generar_matriz_midi), name='matriz_midi'),
    url(r'^matriz_maxima/(?P<idEstudio>\d+)/$', login_required(generar_matriz_maxima), name='matriz_maxima'),
    url(r'^matriz_ri/(?P<idEstudio>\d+)/$', login_required(generar_matriz_ri), name='matriz_ri'),
    url(r'^matriz_balance/(?P<idEstudio>\d+)/$', login_required(generar_matriz_balance), name='matriz_balance'),
    url(r'^estabilidad/(?P<idEstudio>\d+)/$', login_required(generar_indicador_estabilidad), name='estabilidad'),

    # Urls modelo Relacion_MAO y matrices
    url(r'^1mao/(?P<idEstudio>\d+)/$', login_required(crear_1mao), name='1mao'),
    url(r'^2mao/(?P<idEstudio>\d+)/$', login_required(crear_2mao), name='2mao'),
    url(r'^matriz_mao/(?P<idEstudio>\d+)/(?P<numero_matriz>\d)/', login_required(generar_matriz_mao), name='matriz_mao'),
    url(r'^matriz_caa_daa/(?P<idEstudio>\d+)/(?P<numero_matriz>\d)/', login_required(generar_matrices_caa_daa), name='caa_daa'),

    # Urls consultas ajax
    url(r'mid-ajax/$', login_required(consultar_actores_faltantes)),  # obtiene lista actores X registrados en la mid
    url(r'mao-ajax/$', login_required(consultar_objetivos_faltantes)),  # obtiene lista objetivos X registrados en la mao

    # Urls histogramas de influencia
    url(r'^histograma_mid/(?P<idEstudio>\d+)/$', login_required(histograma_mid), name='histograma_mid'),
    url(r'datos_histograma_mid', login_required(datos_histograma_mid)),
    url(r'^histograma_ri/(?P<idEstudio>\d+)/$', login_required(histograma_ri), name='histograma_ri'),
    url(r'datos_histograma_ri', login_required(datos_histograma_ri)),

    # Urls histogramas mao
    url(r'^histograma_implicacion/(?P<idEstudio>\d+)/(?P<numero_matriz>\d)/$', login_required(histograma_implicacion),
        name='implicacion'),
    url(r'^histograma_movilizacion/(?P<idEstudio>\d+)/(?P<numero_matriz>\d)/$', login_required(histograma_movilizacion),
        name='movilizacion'),
    url(r'datos_histograma', login_required(datos_histogramas_mao)),

    # Urls mapa actores
    url(r'^mapa_actores/(?P<idEstudio>\d+)/$', login_required(generar_mapa_midi), name='mapa_actores'),
    url(r'datos_plano_midi', login_required(datos_mapa_midi)),

    # Urls graficos caa y daa
    url(r'^mapa_caa_daa/(?P<idEstudio>\d+)/(?P<numero_matriz>\d)/$', login_required(generar_mapa_caa_daa), name='mapa_caa_daa'),
    url(r'datos_mapa_caa_daa', login_required(datos_mapa_caa_daa)),
    url(r'^histograma_caa_daa/(?P<idEstudio>\d+)/(?P<numero_matriz>\d)/$', histograma_caa_daa, name='hist_caa_daa'),
    url(r'datos_caa_daa', login_required(datos_histograma_caa_daa)),
    url(r'^grafo_caa/(?P<idEstudio>\d+)/(?P<numero_matriz>\d)$', login_required(generar_grafo_caa), name='grafo_caa'),
    url(r'datos_grafo_caa', login_required(datos_grafo_caa)),
    url(r'^grafo_daa/(?P<idEstudio>\d+)/(?P<numero_matriz>\d)$', login_required(generar_grafo_daa), name='grafo_daa'),
    url(r'datos_grafo_daa', login_required(datos_grafo_daa)),

    # Urls exportar a excel
    url(r'exportar_estudios/xls/(?P<idEstudio>\d+)/$', login_required(exportar_estudio_xls), name='estudios_xls'),

    # Urls consensos
    url(r'^consenso_influencias/(?P<idEstudio>\d+)/(?P<tipo>\d)/', login_required(activar_consenso_influencias), name='consenso_influencias'),
    url(r'^consenso_mao/(?P<idEstudio>\d+)/(?P<matriz>\d)/(?P<tipo>\d)', login_required(activar_consenso_mao), name='consenso_mao'),
    url(r'^consenso_caa_daa/(?P<idEstudio>\d+)/(?P<matriz>\d)/(?P<tipo>\d)/', login_required(activar_consenso_caa_daa), name='consenso_caa_daa'),

    # Urls modelo informe final
    url(r'^informe_final/(?P<idEstudio>\d+)/$', login_required(crear_informe), name='informe_final'),

]