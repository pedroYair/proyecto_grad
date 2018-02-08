import xlwt
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .constants import VALOR_RELACION_NO_REGISTRADA, COLUMNAS_EXTRAS_MATRIZ_MAO, MATRIZ_COMPLETA, MATRIZ_INCOMPLETA
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponse, request, Http404
from django.views.generic import CreateView, UpdateView
from .models import Estudio_Mactor, Actor, Ficha, Objetivo, Relacion_MID, Relacion_MAO, Informe_Final
from .forms import Form_Estudio, Form_Ficha, Form_MID, Form_1mao, Form_2mao, Form_Informe


# ----------------------------------------VIEWS MODELO ESTUDIO MACTOR--------------------------------->


class Crear_estudio(CreateView):
    model = Estudio_Mactor
    form_class = Form_Estudio
    template_name = 'estudio/crear_estudio_mactor.html'
    success_url = reverse_lazy('mactor:lista_estudios')


def Listar_estudios(request):

    estudios = Estudio_Mactor.objects.all().order_by('-estado', 'titulo')
    estudios_usuario = []

    for i in estudios:
        estudio = Estudio_Mactor.objects.get(id=i.id)
        lista_expertos = estudio.idExpertos.all()
        if request.user in lista_expertos or request.user == i.idCoordinador:
            estudios_usuario.append(i)

    page = request.GET.get('page', 1)
    paginator = Paginator(estudios_usuario, 10)
    try:
        estudio_contexto = paginator.page(page)
    except PageNotAnInteger:
        estudio_contexto = paginator.page(1)
    except EmptyPage:
        estudio_contexto = paginator.page(paginator.num_pages)

    contexto = {'lista_estudios': estudio_contexto}
    return render(request, 'estudio/lista_estudios.html', contexto)


def Consultar_estudio(request):

    if request.is_ajax():
        id = request.GET['id']
        if id.count("est"):
            id = id.lstrip("est")
        estudio = get_object_or_404(Estudio_Mactor, id=id)
        response = JsonResponse({'titulo': estudio.titulo, 'descripcion': estudio.descripcion})
        return HttpResponse(response.content)
    else:
        return redirect('/')


def Editar_estudio(request, idEstudio):

    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    informes = Informe_Final.objects.all().order_by('idEstudio')
    tipo_usuario = obtener_tipo_usuario(request, estudio.id)
    flag = False

    for i in informes:
        if i.idEstudio.id == int(idEstudio) and i.estado is True:
            flag = True
           
    if request.method == 'GET':
        form = Form_Estudio(instance=estudio)
    else:
        form = Form_Estudio(request.POST, instance=estudio)
        if form.is_valid():
            form.save()
            return redirect('mactor:lista_estudios')
    return render(request, 'estudio/editar_estudio.html', {'form': form, 'informe': flag,
                                                             'estudio': estudio, 'usuario':tipo_usuario})

# -------------------------------------------VIEWS MODELO ACTOR--------------------------------------->


def Crear_actor(request):

    nombreLargo = request.GET['nombreLargo']
    nombreCorto = request.GET['nombreCorto']
    descripcion = request.GET['descripcion']
    estudio = get_object_or_404(Estudio_Mactor, id=int(request.GET['codigo_Estudio']))
    mensaje = "El actor " + nombreLargo + " se ha registrado con exito"
    actores = Actor.objects.filter(idEstudio=estudio.id)
    flag = False

    for i in actores:
        if i.nombreCorto == nombreCorto:
            flag = True

    if flag is False:
        try:
            actor = Actor(nombreLargo=nombreLargo,
                          nombreCorto=nombreCorto,
                          descripcion=descripcion,
                          idEstudio=estudio)
            actor.save()
            response = JsonResponse({'info': mensaje})
            return HttpResponse(response.content)
        except:
            mensaje = "ERROR"
            response = JsonResponse({'info': mensaje})
            return HttpResponse(response.content)
    else:
       mensaje = "Ya existe un actor con el nombre corto " + nombreCorto
       response = JsonResponse({'info': mensaje})
       return HttpResponse(response.content)


def Editar_actor(request):

    if request.is_ajax():
        # se obtienen los datos modificados
        id = request.GET.get('id')
        nombreLargo = request.GET.get('nombreLargo')
        nombreCorto = request.GET.get('nombreCorto')
        descripcion = request.GET.get('descripcion')
        idEstudio = int(request.GET.get('idEstudio'))

        # se elimina del id obtenido la subcadena "act"
        if id.count("act"):
            id = id.lstrip("act")

        # se obtiene de los actores exceptuando el que se va a modificar para comparar
        lista_actor = Actor.objects.all().exclude(id=id)
        flag = False

        # se verifica que el nombre corto modificado no coincida con el de otros actores
        for i in lista_actor:
            if i.nombreCorto == nombreCorto:
                flag = True

        # se realiza la modificacion de los datos y se envia la respuesta
        if flag is False:
            try:
                actor = get_object_or_404(Actor, id=id, idEstudio=idEstudio)
                actor.nombreLargo = nombreLargo
                actor.nombreCorto = nombreCorto
                actor.descripcion = descripcion
                actor.save()
                mensaje = "El registro del actor " + nombreLargo + " se ha actualizado con exito"
                response = JsonResponse({'info': mensaje})
                return HttpResponse(response.content)
            except:
                mensaje = "Error: no se pudo modificar"
                response = JsonResponse({'info': mensaje})
                return HttpResponse(response.content)
        else:
            mensaje = "Ya existe un actor con el nombre corto " + nombreCorto
            response = JsonResponse({'info': mensaje})
            return HttpResponse(response.content)


def Consultar_actor(request):

    if request.is_ajax():
        id = request.GET.get('id')
        idEstudio = request.GET['idEstudio']

        if id.count("str"):
            id = id.lstrip("str")
        elif id.count("daa"):
            id = id.lstrip("daa")
        elif id.count("ver"):
            id = int(id.lstrip("ver"))
        elif id.count("act"):
            id = int(id.lstrip("act"))
        else:
            id = int(id)

        if type(id) == int:
            actor = get_object_or_404(Actor, id=id)
        else:
            actor = get_object_or_404(Actor, nombreCorto=id, idEstudio=int(idEstudio))

        response = JsonResponse(
            {'nombreCorto': actor.nombreCorto,
             'nombreLargo': actor.nombreLargo,
             'descripcion': actor.descripcion})
        return HttpResponse(response.content)
    else:
        return redirect('/')        # redirecciona a la misma pagina


def Listar_actores(request, idEstudio):

    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    actores = Actor.objects.filter(idEstudio=estudio.id).order_by('nombreLargo')
    tipo_usuario = obtener_tipo_usuario(request, idEstudio)
    contexto = {'estudio': estudio,
                'usuario': tipo_usuario,
                'lista_actores': actores,
                'cantidad_registrados': len(actores)}
    return render(request, 'actor/lista_actores.html', contexto)


def Eliminar_actor(request):

    if request.is_ajax():
        actor = Actor.objects.get(id=request.GET.get('id'))
        mensaje = "Actor "+actor.nombreLargo + " eliminado con exito"
        try:
            actor.delete()
            response = JsonResponse({'info': mensaje})
            return HttpResponse(response.content)
        except:
            mensaje = "El actor "+actor.nombreLargo + "no pudo ser eliminado"
            response = JsonResponse({'info': mensaje})
            return HttpResponse(response.content)


# -------------------------------------------VIEWS MODELO FICHA ACTOR----------------------------------->

def Crear_ficha(request, idEstudio):

    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    tipo_usuario = obtener_tipo_usuario(request, estudio.id)
    if request.method == 'POST':
        form = Form_Ficha(request.POST)
        if form.is_valid():
            form.save()
        return redirect('mactor:lista_fichas', estudio.id)
    else:
        actores = Actor.objects.filter(idEstudio=estudio.id).order_by('nombreLargo')
        form = Form_Ficha()
    return render(request, 'ficha/crear_ficha.html', {'form': form,
                                                      'estudio': estudio,
                                                      'usuario': tipo_usuario,
                                                      'actores': actores})


def Lista_fichas(request, idEstudio):

    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    fichas = Ficha.objects.filter(idActorY__idEstudio=estudio.id).order_by('idActorY', 'idActorX')

    # lista = fichas_estudio.filter(idActorY=estudio.id)
    tipo_usuario = obtener_tipo_usuario(request, estudio.id)

    page = request.GET.get('page', 1)
    paginator = Paginator(fichas, 15)
    try:
        fichas_contexto = paginator.page(page)
    except PageNotAnInteger:
        fichas_contexto = paginator.page(1)
    except EmptyPage:
        fichas_contexto = paginator.page(paginator.num_pages)

    contexto = {'estudio': estudio, 'usuario': tipo_usuario, 'lista_fichas': fichas_contexto}
    return render(request, 'ficha/lista_fichas.html', contexto)


def Editar_ficha(request, idFicha):

    ficha = get_object_or_404(Ficha, id=int(idFicha))
    estudio = get_object_or_404(Estudio_Mactor, id=ficha.idEstudio.id)
    tipo_usuario = obtener_tipo_usuario(request, estudio.id)

    if request.method == 'GET':
        form = Form_Ficha(instance=ficha)
    else:
        form = Form_Ficha(request.POST, instance=ficha)
        if form.is_valid():
            form.save()
            return redirect('mactor:lista_fichas', estudio.id)
    return render(request, 'ficha/editar_ficha.html', {'form': form, 'estudio': estudio, 'usuario': tipo_usuario})


def Consultar_ficha(request):

    if request.is_ajax():
        id = request.GET['id']

        if id.count("ver"):
            id = id.lstrip("ver")

        ficha = get_object_or_404(Ficha, id=int(id))
        actorY = ficha.idActorY.nombreLargo
        actorX = ficha.idActorX.nombreLargo
        response = JsonResponse({'actorY': actorY, 'actorX': actorX, 'estrategia': ficha.estrategia})
        return HttpResponse(response.content)
    else:
        return redirect('/')


def Eliminar_ficha(request):
    if request.is_ajax():
        ficha = Ficha.objects.get(id=request.GET['id'])
        mensaje = "Registro de estrategias eliminado con exito"
        try:
            ficha.delete()
            response = JsonResponse({'info': mensaje})
            return HttpResponse(response.content)
        except:
            mensaje = "El registro no pudo ser eliminado"
            response = JsonResponse({'info': mensaje})
            return HttpResponse(response.content)


            # VIEWS MODELO OBJETIVO------------------------------------------------------------------------------------->


# Obtiene la ficha de influencias del par de actores seleccionado en el formulario de influencias mid
def Consultar_ficha_mid(request):

    if request.is_ajax():
        if request.GET['id'] == "" or request.GET['id2'] == "":
            response = JsonResponse({'info': "Seleccione el par de actores a consultar"})
            return HttpResponse(response.content)
        else:
            actorX = int(request.GET['id'])
            actorY = int(request.GET['id2'])
            idEstudio = int(request.GET['idEstudio'])
            ficha = get_object_or_404(Ficha, idActorX=actorX, idActorY=actorY, idActorY__idEstudio=idEstudio)
            response = JsonResponse({'actorY': ficha.idActorY.nombreLargo,
                                     'actorX': ficha.idActorX.nombreLargo,
                                     'estrategia': ficha.estrategia})
            return HttpResponse(response.content)
    else:
        return redirect('/')


# ------------------------------------------VIEWS MODELO OBJETIVO------------------------------------>

def Crear_objetivo(request):

    nombreLargo = request.GET['nombreLargo']
    nombreCorto = request.GET['nombreCorto']
    descripcion = request.GET['descripcion']
    estudio = get_object_or_404(Estudio_Mactor, id=int(request.GET['codigo_Estudio']))
    mensaje = "El objetivo " + nombreLargo + " se ha registrado con exito"
    lista_objetivo = Objetivo.objects.filter(idEstudio=estudio.id)
    flag = False

    for i in lista_objetivo:
        if i.nombreCorto == nombreCorto:
            flag = True

    if flag is False:
        try:
            objetivo = Objetivo(nombreLargo=nombreLargo,
                                nombreCorto=nombreCorto,
                                descripcion=descripcion,
                                idEstudio=estudio)
            objetivo.save()
            response = JsonResponse({'info': mensaje})
            return HttpResponse(response.content)
        except:
            mensaje = "ERROR"
            response = JsonResponse({'info': mensaje})
            return HttpResponse(response.content)
    else:
        mensaje = "Ya existe un objetivo con el nombre corto " + nombreCorto
        response = JsonResponse({'info': mensaje})
        return HttpResponse(response.content)


def Listar_objetivos(request, idEstudio):

    estudio_mactor = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    objetivos = Objetivo.objects.filter(idEstudio=estudio_mactor.id).order_by('nombreLargo')
    tipo_usuario = obtener_tipo_usuario(request, idEstudio)
    contexto = {'estudio': estudio_mactor,
                'usuario': tipo_usuario,
                'lista_objetivos': objetivos,
                'cantidad_registrados': len(objetivos)}

    return render(request, 'objetivo/lista_objetivos.html', contexto)


def Editar_objetivo(request):

    if request.is_ajax():
        id = request.GET.get('id')
        nombreLargo = request.GET['nombreLargo']
        nombreCorto = request.GET['nombreCorto']
        descripcion = request.GET['descripcion']

        # se elimina del id obtenido la subcadena "id"
        if id.count("obj"):
            id = id.lstrip("obj")

        # se obtiene el registro del actor a modificar
        lista_objetivo = Objetivo.objects.all().exclude(id=id)
        flag = False

        # se verifica que el nombre corto modificado no coincida con el de otros actores
        for i in lista_objetivo:
            if i.nombreCorto == nombreCorto:
                flag = True

        # se realiza la modificacion de los datos y se envia la respuesta
        if flag is False:
            try:
                objetivo = get_object_or_404(Objetivo, id=id)
                objetivo.nombreLargo = nombreLargo
                objetivo.nombreCorto = nombreCorto
                objetivo.descripcion = descripcion
                objetivo.save()
                mensaje = "El registro del objetivo " + nombreLargo + " se ha actualizado con exito"
                response = JsonResponse({'info': mensaje})
                return HttpResponse(response.content)
            except:
                mensaje = "Error: no se pudo modificar"
                response = JsonResponse({'info': mensaje})
                return HttpResponse(response.content)
        else:
            mensaje = "Ya existe un objetivo con el nombre corto " + nombreCorto
            response = JsonResponse({'info': mensaje})
            return HttpResponse(response.content)


def Consultar_objetivo(request):

    if request.is_ajax():
        id = request.GET.get('id')

        if id.count("obj"):
            id = id.lstrip("obj")
        elif id.count("ver"):
            id = id.lstrip("ver")

        objetivo = get_object_or_404(Objetivo, id=int(id))
        response = JsonResponse(
            {'nombreCorto': objetivo.nombreCorto,
             'nombreLargo': objetivo.nombreLargo,
             'descripcion': objetivo.descripcion})
        return HttpResponse(response.content)
    else:
        return redirect('/')


def Eliminar_objetivo(request):

    if request.is_ajax():
        objetivo = Objetivo.objects.get(id=request.GET['id'])
        mensaje = "Objetivo " + objetivo.nombreLargo + " eliminado con exito"
        try:
            objetivo.delete()
            response = JsonResponse({'info': mensaje})
            return HttpResponse(response.content)
        except:
            mensaje = "El objetivo " + objetivo.nombreLargo + "no pudo ser eliminado"
            response = JsonResponse({'info': mensaje})
            return HttpResponse(response.content)


# -----------------------------------------VIEWS MODELO RELACION_MID--------------------------------->

def Crear_relacion_mid(request, idEstudio):

    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    if request.method == 'POST':
        form = Form_MID(request.POST)
        if form.is_valid():
            form.save()
            Crear_auto_influencia(request, idEstudio)
        return redirect('mactor:influencia', estudio.id)
    else:
        tipo_usuario = obtener_tipo_usuario(request, idEstudio)
        actores = Actor.objects.filter(idEstudio=estudio.id).order_by('nombreLargo')
        form = Form_MID()
    return render(request, 'influencia/crear_influencia.html', {'form': form,
                                                                'estudio': estudio,
                                                                'usuario': tipo_usuario,
                                                                'actores': actores})


# View generadora de la matriz MID
def Generar_matriz_mid(request, idEstudio):

    concenso = verificar_concenso(request, idEstudio)
    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    lista_actores = Actor.objects.filter(idEstudio=estudio.id).order_by('id')
    tipo_usuario = obtener_tipo_usuario(request, estudio.id)
    tamano_matriz_completa = len(lista_actores) * len(lista_actores)
    posicion_salto_linea = lista_actores.count() + 1
    lista_influencias = []
    cantidad_expertos = 0  # cantidad de expertos que han finalizado la matriz y por tanto estan en el concenso

    # muestra la matriz grupal
    if concenso is True:
        lista_influencias = calcular_concenso_mid(estudio.id)
        cantidad_expertos = lista_influencias['num_expertos']
        lista_influencias = lista_influencias['concenso']
    # muestra la matriz diligenciada por el usuario en sesion
    elif tipo_usuario != "COORDINADOR":
        lista_influencias = Relacion_MID.objects.filter(idActorY__idEstudio=estudio.id,
                                                        idExperto=request.user.id).order_by('idActorY', 'idActorX')

    if len(lista_influencias) == tamano_matriz_completa and tamano_matriz_completa > 0 or concenso is True:
        valores_mid = establecer_valores_mid(estudio.id, lista_influencias)

        contexto = {'actores': lista_actores,
                    'posicion_salto': posicion_salto_linea,
                    'valores': valores_mid,
                    'expertos': cantidad_expertos,
                    'estudio': estudio,
                    'usuario': tipo_usuario}

    elif len(lista_influencias) != tamano_matriz_completa and tamano_matriz_completa != 0:
        valores_mid = generar_mid_incompleta(request, estudio.id)

        contexto = {'actores': lista_actores, 'posicion_salto': posicion_salto_linea,
                    'valores': valores_mid, 'estudio': estudio, 'usuario': tipo_usuario}
    # si no se han registrado actores
    else:
        contexto = {'estudio': estudio, 'usuario': tipo_usuario}

    if concenso is False:
        return render(request, 'influencia/matriz_mid.html', contexto)
    else:
        return render(request, 'influencia/concenso/mid_concenso.html', contexto)


# View generadora de la matriz MIDI
def Generar_matriz_midi(request, idEstudio):

    concenso = verificar_concenso(request, idEstudio)
    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    lista_actores = Actor.objects.filter(idEstudio=estudio.id).order_by('id')
    lista_influencias = Relacion_MID.objects.filter(idActorY__idEstudio=estudio.id,
                                                    idExperto=request.user.id).order_by('idActorY', 'idActorX')
    tamano_matriz_completa = len(lista_actores) * len(lista_actores)
    posicion_salto_linea = lista_actores.count() + 1
    tipo_usuario = obtener_tipo_usuario(request, estudio.id)

    if len(lista_influencias) == tamano_matriz_completa and tamano_matriz_completa > 0 or concenso is True:
        valores_midi = calcular_midi(request, idEstudio)
        cantidad_expertos = 0
        if concenso is True:
            influencias_mid = calcular_concenso_mid(estudio.id)
            cantidad_expertos = influencias_mid['num_expertos']

        contexto = {'actores': lista_actores,
                    'posicion_salto': posicion_salto_linea,
                    'valores_midi': valores_midi,
                    'expertos': cantidad_expertos,
                    'estudio': estudio,
                    'usuario': tipo_usuario}
    else:
        contexto = {'estudio': estudio, 'usuario': tipo_usuario}

    if concenso is False:
        return render(request, 'influencia/matriz_midi.html', contexto)
    else:
        return render(request, 'influencia/concenso/midi_concenso.html', contexto)


# View generadora de la matriz MIDI
def Generar_matriz_maxima(request, idEstudio):

    concenso = verificar_concenso(request, idEstudio)
    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    lista_actores = Actor.objects.filter(idEstudio=estudio.id).order_by('id')
    lista_influencias = Relacion_MID.objects.filter(idActorY__idEstudio=estudio.id,
                                                    idExperto=request.user.id).order_by('idActorY', 'idActorX')
    tamano_matriz_completa = len(lista_actores) * len(lista_actores)
    posicion_salto_linea = lista_actores.count() + 1
    tipo_usuario = obtener_tipo_usuario(request, idEstudio)

    if len(lista_influencias) == tamano_matriz_completa and tamano_matriz_completa > 0 or concenso is True:
        valores_maximos = calcular_maxima_influencia(request, idEstudio)
        cantidad_expertos = 0
        if concenso is True:
            influencias_mid = calcular_concenso_mid(estudio.id)
            cantidad_expertos = influencias_mid['num_expertos']

        contexto = {'actores': lista_actores,
                    'posicion_salto': posicion_salto_linea,
                    'valores_maximos': valores_maximos,
                    'expertos': cantidad_expertos,
                    'estudio': estudio,
                    'usuario': tipo_usuario}
    else:
        contexto = {'estudio': estudio, 'usuario': tipo_usuario}

    if concenso is False:
        return render(request, 'influencia/matriz_maxima.html', contexto)
    else:
        return render(request, 'influencia/concenso/maxima_concenso.html', contexto)


# Genera la matriz de coeficientes de fuerza ri de cada actor
def Generar_matriz_ri(request, idEstudio):

    concenso = verificar_concenso(request, idEstudio)
    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    valores_ri = calcular_ri(request, idEstudio)
    actores = Actor.objects.filter(idEstudio=estudio.id).order_by('id')
    lista_contexto = []
    tipo_usuario = obtener_tipo_usuario(request, estudio.id)

    for i in range(len(actores)):
        lista_contexto.append(Valor_posicion(posicion=0, valor=actores[i].nombreCorto, descripcion=actores[i].nombreLargo))
        lista_contexto.append(Valor_posicion(posicion=1, valor=round(valores_ri[i], 2), descripcion=round(valores_ri[i], 2)))

    lista_contexto[len(lista_contexto)-1].posicion = ""

    cantidad_expertos = 0
    if concenso is True:
        influencias_mid = calcular_concenso_mid(estudio.id)
        cantidad_expertos = influencias_mid['num_expertos']
    contexto = {'lista_contexto': lista_contexto, 'expertos': cantidad_expertos,
                'estudio': estudio, 'usuario': tipo_usuario}

    if concenso is False:
        return render(request, 'influencia/matriz_ri.html', contexto)
    else:
        return render(request, 'influencia/concenso/ri_concenso.html', contexto)


# Genera la matriz de balance liquido
def Generar_matriz_balance(request, idEstudio):

    concenso = verificar_concenso(request, idEstudio)
    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    actores = Actor.objects.filter(idEstudio=estudio.id).order_by('id')
    lista_influencias = Relacion_MID.objects.filter(idActorY__idEstudio=estudio.id,
                                                    idExperto=request.user.id).order_by('idActorY', 'idActorX')
    tamano_matriz_completa = len(actores) * len(actores)
    tipo_usuario = obtener_tipo_usuario(request, estudio.id)

    if len(lista_influencias) == tamano_matriz_completa and tamano_matriz_completa > 0 or concenso is True:
        valores_balance = calcular_balance_liquido(request, idEstudio)
        cantidad_expertos = 0
        if concenso is True:
            influencias_mid = calcular_concenso_mid(estudio.id)
            cantidad_expertos = influencias_mid['num_expertos']
        contexto = {'actores': actores, 'valores_balance': valores_balance, 'posicion_salto': actores.count()+1,
                    'expertos': cantidad_expertos, 'estudio': estudio, 'usuario': tipo_usuario}
    else:
        contexto = {'estudio': estudio, 'usuario': tipo_usuario}

    if concenso is False:
        return render(request, 'influencia/matriz_balance.html', contexto)
    else:
        return render(request, 'influencia/concenso/balance_concenso.html', contexto)


# Genera la matriz de balance liquido
def Generar_indicador_estabilidad(request, idEstudio):

    concenso = verificar_concenso(request, idEstudio)
    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    indicador = calcular_estabilidad(request, idEstudio)
    tipo_usuario = obtener_tipo_usuario(request, estudio.id)

    cantidad_expertos = 0
    if concenso is True:
        influencias_mid = calcular_concenso_mid(estudio.id)
        cantidad_expertos = influencias_mid['num_expertos']

    contexto = {'indicador': indicador, 'expertos': cantidad_expertos, 'estudio': estudio, 'usuario': tipo_usuario}

    if concenso is False:
        return render(request, 'influencia/indicador_estabilidad.html', contexto)
    else:
        return render(request, 'influencia/concenso/indicador_estabilidad_concenso.html', contexto)


# -----------------------------------------VIEWS MODELO RELACION_MAO---------------------------------->

# Agrega la relacion 1mao
def Crear_1mao(request, idEstudio):

    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    tipo_usuario = obtener_tipo_usuario(request, estudio.id)
    if request.method == 'POST':
        form = Form_1mao(request.POST)
        if form.is_valid():
            form.save()
        return redirect('mactor:1mao', estudio.id)
    else:
        actores = Actor.objects.filter(idEstudio=estudio.id).order_by('nombreLargo')
        objetivos = Objetivo.objects.filter(idEstudio=estudio.id).order_by('nombreLargo')
        form = Form_1mao()
    return render(request, 'mao/crear_1mao.html', {'form': form,
                                                   'estudio': estudio,
                                                   'usuario': tipo_usuario,
                                                   'actores': actores,
                                                   'objetivos': objetivos})


# Agrega la relacion 2mao
def Crear_2mao(request, idEstudio):

    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    tipo_usuario = obtener_tipo_usuario(request, estudio.id)
    if request.method == 'POST':
        form = Form_2mao(request.POST)
        if form.is_valid():
            form.save()
        return redirect('mactor:2mao', estudio.id)
    else:
        actores = Actor.objects.filter(idEstudio=estudio.id).order_by('nombreLargo')
        objetivos = Objetivo.objects.filter(idEstudio=estudio.id).order_by('nombreLargo')
        form = Form_2mao()
    return render(request, 'mao/crear_2mao.html', {'form': form,
                                                   'estudio': estudio,
                                                   'usuario': tipo_usuario,
                                                   'actores': actores,
                                                   'objetivos': objetivos})


# Genera las matrices mao
def Generar_matriz_mao(request, idEstudio, numero_matriz):

    concenso = verificar_concenso(request, idEstudio)
    contexto = crear_contexto_mao(request, idEstudio, int(numero_matriz))

    if int(numero_matriz) == 1:
        if concenso is True:
            return render(request, 'mao/concenso/concenso_1mao.html', contexto)
        else:
            return render(request, 'mao/matriz_1mao.html', contexto)
    elif int(numero_matriz) == 2:
        if concenso is True:
            return render(request, 'mao/concenso/concenso_2mao.html', contexto)
        else:
            return render(request, 'mao/matriz_2mao.html', contexto)
    elif int(numero_matriz) == 3:
        if concenso is True:
            return render(request, 'mao/concenso/concenso_3mao.html', contexto)
        else:
            return render(request, 'mao/matriz_3mao.html', contexto)
    else:
        raise Http404("Error: Esta vista no existe")


# Genera las matrices de convergencia y divergencia
def Generar_matrices_caa_daa(request, idEstudio, numero_matriz):

    concenso = verificar_concenso(request, idEstudio)
    numero_matriz = int(numero_matriz)
    if numero_matriz in [1, 2, 3]:
        estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
        actores = Actor.objects.filter(idEstudio=estudio.id).order_by('id')
        tipo_usuario = obtener_tipo_usuario(request, estudio.id)
        contexto_mao = crear_contexto_mao(request, idEstudio, numero_matriz)

        num_expertos = 0
        if concenso is True:
            if numero_matriz == 3:
                numero_matriz = 2  # porque 3mao se calcula apartir de 2mao
            num_expertos = calcular_concenso_mao(request, estudio.id, numero_matriz)
            num_expertos = num_expertos['expertos']

        if contexto_mao['estado_matriz'] == MATRIZ_COMPLETA:
            contexto = {
                'actores': actores,
                'valores_caa': contexto_mao['valores_caa'],
                'posicion_salto_caa_daa': actores.count(),
                'valores_daa': contexto_mao['valores_daa'],
                'estudio': estudio,
                'numero_matriz': numero_matriz,
                'usuario': tipo_usuario,
                'expertos': num_expertos}
        else:
            if int(numero_matriz) in [1, 2]:
                mensaje = "Finalice el registro de las posiciones " + numero_matriz + "MAO para visualizar esta matriz."
            else:
                mensaje = "Finalice el registro de las posiciones MID y 2MAO para visualizar esta matriz."

            contexto = {
                'estudio': estudio,
                'numero_matriz': numero_matriz,
                'mensaje': mensaje,
                'usuario': tipo_usuario}

        if concenso is True:
            return render(request, 'mao/concenso/concenso_caa_daa.html', contexto)
        else:
            return render(request, 'mao/matrices_caa_daa.html', contexto)
    else:
        raise Http404("Error: Esta vista no existe")


# ---------------------------------------------CLASES AUXILIARES-------------------------------------->


# Clase auxiliar para la generacion de matrices, se asigna una posicion a un respectivo valor
class Valor_posicion:
    def __init__(self, posicion, valor, descripcion):
        self.posicion = posicion
        self.valor = valor
        self.descripcion = descripcion


# Clase auxiliar para la generacion de matrices, se asigna una posicion a un respectivo valor
class Valor_xy:
    def __init__(self, x, y, valor):
        self.x = x
        self.y = y
        self.valor = valor

# -------------------------------------FUNCIONES AUXILIARES------------------------------------------------------------>


# <<<<FUNCIONES RELACIONES MID>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def Crear_auto_influencia(request, idEstudio):

        estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
        actor = Actor.objects.filter(idEstudio=estudio.id).order_by('id')
        inf = Relacion_MID.objects.filter(idActorY__idEstudio=estudio.id, idExperto=request.user.id).order_by('idActorY',
                                                                                                        'idActorX')
        lista_registrados = []

        # se verifica si estas influencias ya existen
        for i in actor:
            for j in inf:
                if len(inf) > 0 and j.idActorX.id == i.id and j.idActorY.id == i.id:
                    lista_registrados.append(i.id)

        # se agregan las autoinfluencias restantes
        for i in actor:
            if i.id not in lista_registrados:
                a = Relacion_MID()
                a.idActorY = i
                a.idActorX = i
                a.valor = 0
                a.justificacion = "auto_influencia"
                a.idExperto = request.user
                a.save()


# Establece la lista de valores mid enviandos por contexto a la matriz
def establecer_valores_mid(idEstudio, influencias):

    actores = Actor.objects.filter(idEstudio=idEstudio).order_by('id')
    lista_valores_mid = []
    posicion = 0               # controla y asignar la posicion de acuerdo al numero de actores e influencias
    indice = 0                 # representa el indice del nombreCorto que se ha de colocar en valores
    suma_fila_influencias = 0
    suma_columna_dependencia = 0

    for i in range(len(influencias)):

        posicion += 1
        # se asigna a las influencias registradas una posicion para facilitar su visualizacion y manejo
        lista_valores_mid.append(Valor_posicion(posicion=posicion, valor=influencias[i].valor, descripcion=""))

        # Se calcula el valor de influencia directa I.D
        if influencias[i].valor != VALOR_RELACION_NO_REGISTRADA:
            suma_fila_influencias += influencias[i].valor

        # Si posicion (representa el numero de la columna) es igual a la cantidad de actores agrega total de influencias
        if posicion == actores.count():
            lista_valores_mid.append(Valor_posicion(posicion=posicion + 1,
                                                    valor=suma_fila_influencias,
                                                    descripcion=suma_fila_influencias))
            # Se determina la posicion donde se va a colocar el nombre corto de la nueva fila
            pos_nombre = (actores.count() + 2) * indice
            lista_valores_mid.insert(pos_nombre, Valor_posicion(posicion=0,
                                                                valor=actores[indice].nombreCorto,
                                                                descripcion=actores[indice].nombreLargo))
            posicion = 0               # reinicio de la posicion (nueva fila)
            indice += 1                # indice hace referencia al siguiente actor
            suma_fila_influencias = 0  # reinicio del valor de suma_fila_influencias

    # Se calculan las dependencias directas D.D (suma de columnas)
    lista_valores_mid.append(Valor_posicion(posicion=0, valor="D.D", descripcion="DEPENDENCIA DIRECTA"))
    posicion = 1
    suma_dependencia_total = 0

    while posicion <= actores.count():
        for i in lista_valores_mid:
            # si posicion es igual al numero de la columna que se esta sumando
            if i.posicion == posicion:
                # si se trata de un valor no valido (matriz incompleta)
                if i.valor != VALOR_RELACION_NO_REGISTRADA:
                    suma_columna_dependencia += i.valor
                    suma_dependencia_total += i.valor
        # Se ingresa a la lista de valores_mid la sumatoria de la columna
        lista_valores_mid.append(Valor_posicion(posicion="",
                                                valor=suma_columna_dependencia,
                                                descripcion=suma_columna_dependencia))
        posicion += 1                 # iteracion de las posiciones
        suma_columna_dependencia = 0  # reinicio a o del valor movilizacion
    lista_valores_mid.append(Valor_posicion(posicion="", valor=suma_dependencia_total, descripcion=suma_dependencia_total))

    lista_valores_mid = agregar_descripcion_mid(idEstudio, lista_valores_mid)

    return lista_valores_mid


# Establece como se mostrara la matriz mid en caso de que no este completamente diligenciada
def generar_mid_incompleta(request, idEstudio):

    lista_actores = Actor.objects.filter(idEstudio=idEstudio).order_by('id')
    mid = Relacion_MID.objects.filter(idActorY__idEstudio=idEstudio, idExperto=request.user.id).order_by('idActorY', 'idActorX')
    lista_ejes_incompletos = []
    lista_ejes_ordenados = []

    # se llena la lista de ejes ordenados con los orden en que deben ir los actores en la matriz (ejes Y y X)
    for i in lista_actores:
        for j in lista_actores:
            lista_ejes_ordenados.append(Valor_xy(y=i.id, x=j.id, valor=""))

    # se obtienen las parejas de ejes, actualmente registradas y su valor correspondiente
    for i in mid:
        lista_ejes_incompletos.append(Valor_xy(y=i.idActorY.id, x=i.idActorX.id, valor=i.valor))

    # se ingresan a la lista de ejes incompletos, valores relleno que facilitan la comparacion con la de ejes ordenados
    cont = 0
    while len(lista_ejes_incompletos) != len(lista_ejes_ordenados):
        lista_ejes_incompletos.append(Valor_xy(y=0, x=0, valor=0))
        cont += 1

    # se detectan los ejes faltantes y se ingresan en esas posiciones con valor 100 para indicar la falta del registro
    for j in range(len(lista_ejes_ordenados)):
            eje_y = lista_ejes_ordenados[j].y
            eje_x = lista_ejes_ordenados[j].x
            if lista_ejes_incompletos[j].y != eje_y or lista_ejes_incompletos[j].x != eje_x:
                lista_ejes_incompletos.insert(j, Valor_xy(y=eje_y, x=eje_x, valor=VALOR_RELACION_NO_REGISTRADA))

    # se eliminan de la lista de ejes incompletos los valores relleno inicialmente ingresados para comparar
    while cont != 0:
        lista_ejes_incompletos.pop()
        cont -= 1

    lista_contexto = establecer_valores_mid(idEstudio, lista_ejes_incompletos)

    return lista_contexto


# Agrega a la lista de valores mid y midi la descripcion del valor
def agregar_descripcion_mid(idEstudio, lista):

    actores = Actor.objects.filter(idEstudio=idEstudio).order_by('id')

    for i in lista:
        if i.posicion in range(actores.count() + 1):
            if i.valor == 0:
                i.descripcion = "Sin influencia"
            elif i.valor == 1:
                i.descripcion = "Procesos"
            elif i.valor == 2:
                i.descripcion = "Proyectos"
            elif i.valor == 3:
                i.descripcion = "Misión"
            elif i.valor == 4:
                i.descripcion = "Existencia"
    return lista


# Calcula los valores de la matriz de MIDIij = MIDij + Sum(Minimo[(MID ik, MID ik])
def calcular_midi(request, idEstudio):

    estudio = int(idEstudio)
    actores = Actor.objects.filter(idEstudio=estudio).order_by('id')
    lista_comparacion_minimo = []   # contiene las sublistas de valores minimos por cada actores Y
    lista_total = []                # contiene lista_comparacion_minimo concatenado
    valores_midi = []               # contiene los valores correspondientes a MIDI

    if verificar_concenso(request, idEstudio):
        influencias_mid = calcular_concenso_mid(estudio)
        influencias_mid = influencias_mid['concenso']
    else:
        influencias_mid = Relacion_MID.objects.filter(idActorY__idEstudio=estudio, idExperto=request.user.id).order_by(
            'idActorY', 'idActorX')

    # se agrega la sublista de valores minimos correspondiente al actorY a lista_comparacion_minimo
    for i in range(len(influencias_mid)):
        if influencias_mid[i].idActorY == influencias_mid[i].idActorX:
            # cada valor i que representa a un actor permite el calculo de una fila de la matriz
            lista_comparacion_minimo.append(sumar_valores_minimos(request, actorY=i, idEstudio=estudio))

    # concatenacion de lista_minimo para facilitar la suma con las influencias correspondientes (igual longitud)
    for i in lista_comparacion_minimo:
        lista_total += i
    # se realiza la suma MID ij + Sum(Minimo [(MID ik, MID ik])
    indice = 0
    posicion = 0
    influencia = 0  # valor de la ultima columna
    for i in range(len(influencias_mid)):
        indice += 1
        valor = influencias_mid[i].valor + lista_total[i]
        valores_midi.append(Valor_posicion(posicion=indice, valor=valor, descripcion=valor))

        # se calcula el valor influencia, no se incluye la influencia sobre si mismo
        if influencias_mid[i].idActorY != influencias_mid[i].idActorX and indice <= actores.count():
            influencia += valor

        # se determina la posicion donde se va a colocar el nombre corto de la nueva fila
        if indice == actores.count():
            # se determina la posicion del nombre corto se suma 2 debido a las columna extras (nombre e influencia)
            posicion_nombre = (actores.count() + 2) * posicion
            valores_midi.insert(posicion_nombre, Valor_posicion(posicion=0,
                                                                valor=actores[posicion].nombreCorto,
                                                                descripcion=actores[posicion].nombreLargo))
            # se determina la posición de la columna influencia y se inserta en la posicion establecida
            posicion_li = posicion_nombre + actores.count() + 1
            valores_midi.insert(posicion_li, Valor_posicion(posicion=actores.count()+1, valor=influencia, descripcion=influencia))

            indice = 0
            posicion += 1
            influencia = 0

    # se calculan los valores di (ultima fila)
    valores_midi.append(Valor_posicion(posicion=0, valor="D.DI", descripcion="DEPENDENCIA DIRECTA E INDIRECTA"))
    valores_midi = establecer_dependencias(valores_midi, actores.count(), "MIDI")

    return valores_midi


# Suma de valores minimos (lado derecho formula midi)
def sumar_valores_minimos(request, actorY, idEstudio):

    estudio = int(idEstudio)
    actores = Actor.objects.filter(idEstudio=estudio).order_by('id')
    lista_suma = []  # contiene la suma de los valores minimos establecidos al comparar

    # mayor_valores_minimos(request, actorY, idEstudio)
    # si se accede al concenso midi (en este caso idEstudio = str)
    if verificar_concenso(request, idEstudio):
        mid = calcular_concenso_mid(estudio)
        mid = mid['concenso']
    else:
        mid = Relacion_MID.objects.filter(idActorY__idEstudio=estudio, idExperto=request.user.id).order_by('idActorY', 'idActorX')

    for i in range(len(mid)):
        lista_suma.append(0)

    valores_minimos = obtener_valores_minimos(request, idEstudio, actorY)

    inicio_sublista = 0             # indica el punto inicial de la sublista
    fin_sublista = actores.count()  # indica el punto final de la sublista

    # la lista valores_minimos es divida y sumada
    for i in range(fin_sublista):
        if i < actores.count() - 1:
            lista_suma = map(sum, zip(lista_suma, valores_minimos[inicio_sublista:fin_sublista]))
            inicio_sublista = fin_sublista
            fin_sublista = fin_sublista + actores.count()

    return lista_suma


# Calcula la maxima influencia directa e indirecta idEstudio = str
def calcular_maxima_influencia(request, idEstudio):

    concenso = verificar_concenso(request, idEstudio)
    estudio = int(idEstudio)
    actores = Actor.objects.filter(idEstudio=estudio).order_by('id')
    lista_comparacion_minimo = []  # contiene las sublistas de valores minimos por cada actores Y
    lista_maximos = []  # contiene lista_comparacion_minimo concatenado (sin sublista)
    valores_maximos = []  # contiene los valores que se muestran a la matriz luego de comparar

    # muestra la matriz grupal
    if concenso is True:
        influencias_mid = calcular_concenso_mid(estudio)
        influencias_mid = influencias_mid['concenso']
    # muestra la matriz diligenciada por el usuario en sesion
    else:
        influencias_mid = Relacion_MID.objects.filter(idActorY__idEstudio=estudio,
                                                        idExperto=request.user.id).order_by('idActorY', 'idActorX')

    # se agrega la sublista de valores minimos correspondiente al actorY a lista_comparacion_minimo
    for i in range(len(influencias_mid)):
        if influencias_mid[i].idActorY == influencias_mid[i].idActorX:
            # cada valor de actorY permite el calculo de una fila de la matriz
            lista_comparacion_minimo.append(mayor_valores_minimos(request, actorY=i, idEstudio=idEstudio))

    # concatenacion de lista_minimo para facilitar la suma con las influencias correspondientes (igual longitud)
    for i in lista_comparacion_minimo:
        lista_maximos += i

    # se realiza la comparacion para determinar cual valor es mayor
    indice = 0
    posicion = 0
    influencia = 0  # valor de la ultima columna
    for i in range(len(influencias_mid)):
        indice += 1
        maximo = max(influencias_mid[i].valor, lista_maximos[i])
        valores_maximos.append(Valor_posicion(posicion=indice, valor=maximo, descripcion=maximo))

        # se calcula el valor de influencia (ultima columna), no se incluye la influencia sobre si mismo
        if influencias_mid[i].idActorY != influencias_mid[i].idActorX and indice <= actores.count():
            influencia += maximo

        # se determina la posicion donde se va a colocar el nombre corto de la nueva fila
        if indice == actores.count():
            # se determina la posicion del nombre corto se suma 2 debido a las columna extras (nombreCorto y li)
            posicion_nombre = (actores.count() + 2) * posicion
            valores_maximos.insert(posicion_nombre, Valor_posicion(posicion=0,
                                                                   valor=actores[posicion].nombreCorto,
                                                                   descripcion=actores[posicion].nombreLargo))
            # se determina la posición de la columna li y se inserta en la posicion establecida
            posicion_li = posicion_nombre + actores.count() + 1
            valores_maximos.insert(posicion_li, Valor_posicion(posicion=actores.count() + 1,
                                                               valor=influencia, descripcion=influencia))
            # se reinician los parametros para recalcular
            indice = 0
            posicion += 1
            influencia = 0

    valores_maximos.append(
        Valor_posicion(posicion=0, valor="DDI.M", descripcion="DEPENDENCIA DIRECTA E INDIRECTA MAXIMA"))
    valores_maximos = establecer_dependencias(valores_maximos, actores.count(), "MAXIMA")

    return valores_maximos


# Determinacion de valores minimos mayores, (lado derecho formula maxima)
def mayor_valores_minimos(request, actorY, idEstudio):

    actores = Actor.objects.filter(idEstudio=int(idEstudio)).order_by('id')
    lista_minimos = obtener_valores_minimos(request, idEstudio, actorY)
    lista_comparar = []
    lista_mayores = []

    # Se asigna una posicion a los valores minimos para facilitar la comparacion y posterior visualizacion
    contador = 0
    for i in lista_minimos:
        if contador <= actores.count():
            lista_comparar.append(Valor_posicion(posicion=contador, valor=i, descripcion=""))
            contador += 1
        if contador + 1 > actores.count():
            contador = 0

    # Se determinan el valor mayor dentro de la lista de valores minimos por cada pareja ij
    posicion = 0
    while posicion < actores.count():
        mayor = 0
        for i in lista_comparar:
            if i.posicion == posicion and i.valor > mayor:
                mayor = i.valor
        lista_mayores.append(mayor)
        posicion += 1

    return lista_mayores


# Obtencion de valores minimos, necesarios para midi y maxima
def obtener_valores_minimos(request, idEstudio, actorY):

    estudio = int(idEstudio)
    actores = Actor.objects.filter(idEstudio=estudio).order_by('id')
    valores_izquierdos = []  # contiene los valores izquierdos a comparar
    valores_derechos = []  # contiene los valores derechos a comparar
    valores_minimos = []  # contiene los valores minimos establecidos al comparar valores_izquierdos vs derechos

    if verificar_concenso(request, idEstudio):
        mid = calcular_concenso_mid(estudio)
        mid = mid['concenso']
    else:
        mid = Relacion_MID.objects.filter(idActorY__idEstudio=estudio, idExperto=request.user.id).order_by('idActorY',
                                                                                                   'idActorX')

    # Valores_derechos: influencias de los actores influenciados por Y sobre el actor X excepto Y
    indice = 1
    aux = 0
    for i in range(len(mid)):
        # se verifica si en el registro actual (i), el campo idActorY no corresponde al actorY recibido
        if mid[i].idActorY != mid[actorY].idActorY:
            valores_derechos.append(Valor_posicion(posicion=indice, valor=mid[i].valor, descripcion=""))
            aux += 1
            if aux == actores.count():
                indice += 1
                aux = 0

    # Valores_izquierdos: influencias del actorY recibido, sobre los demas.
    indice = 0
    for i in range(len(mid)):
        longitud = len(valores_izquierdos)
        cantidad_actores = actores.count() - 1
        eje_y = mid[i].idActorY
        eje_x = mid[i].idActorX

        if mid[actorY].idActorY != eje_x and eje_y == mid[actorY].idActorY and longitud < cantidad_actores:
            valores_izquierdos.append(Valor_posicion(posicion=indice + 1, valor=mid[i].valor, descripcion=""))
            indice += 1

    # determinacion del valor minimo entre cada pareja izquierdo[i] - derecho[i]
    indice = 0
    for i in range(len(valores_derechos)):
        if valores_izquierdos[indice].posicion == valores_derechos[i].posicion and indice < actores.count():
            minimo = min(valores_izquierdos[indice].valor, valores_derechos[i].valor)
            valores_minimos.append(minimo)
        else:
            indice += 1
            if valores_izquierdos[indice].posicion == valores_derechos[i].posicion:
                minimo = min(valores_izquierdos[indice].valor, valores_derechos[i].valor)
                valores_minimos.append(minimo)
    return valores_minimos


# Calcular balance liquido
def calcular_balance_liquido(request, idEstudio):

    valores_midi = calcular_midi(request, idEstudio)
    actores = Actor.objects.filter(idEstudio=int(idEstudio)).order_by('id')
    lista_inversa = []
    lista_balance = []
    suma_fila = 0

    indice = 0
    for i in range(len(valores_midi)):
        if valores_midi[i].valor == "D.DI":
            indice = i

    columna = 0
    lista_inversa.append("nombre")
    while columna < actores.count():
        for i in valores_midi[0:indice]:
            if i.posicion == columna+1:
                lista_inversa.append(i.valor)
        if columna + 1 != actores.count():
            lista_inversa.append("influencia")
            lista_inversa.append("nombre")
        columna += 1
    lista_inversa.append("influencia")

    for i in range(len(valores_midi[0:indice])):
        if valores_midi[i].posicion == 0:
            lista_balance.append(valores_midi[i])
        elif valores_midi[i].posicion > 0 and valores_midi[i].posicion < actores.count()+1:
            balance = valores_midi[i].valor - lista_inversa[i]
            suma_fila += balance
            lista_balance.append(Valor_posicion(posicion=valores_midi[i].posicion, valor=balance, descripcion=balance))
        elif valores_midi[i].posicion == actores.count()+1:
            lista_balance.append(Valor_posicion(posicion=valores_midi[i].posicion, valor=suma_fila, descripcion=suma_fila))
            suma_fila = 0

    lista_balance[len(lista_balance)-1].posicion = ""  # para que no realize el salto despues de la ultima fila
    return lista_balance


# Establece los valores de dependencias de las matrices midi y maxima
def establecer_dependencias(lista, cant_actores, tipo):

    indice = 1
    dependencia = 0
    suma_di = 0
    while indice <= cant_actores:
        for i in lista:
            if i.posicion == indice:
                dependencia += i.valor
        # se obtiene el valor de influecia sobre si mismo para restarlo a dependencia
        valor_auto_influencia = lista[((cant_actores + 2) * (indice - 1)) + indice].valor
        dependencia = dependencia - valor_auto_influencia

        if tipo == "MAXIMA":
            # se colocan en 0 los valores de la diagonal
            lista[((cant_actores + 2) * (indice - 1)) + indice].valor = 0
            lista[((cant_actores + 2) * (indice - 1)) + indice].descripcion = 0

        # se inserta el valor dependencia a la lista de valores midi
        lista.append(Valor_posicion(posicion="", valor=dependencia, descripcion=dependencia))
        # se actualizan los parametros de iteracion
        suma_di += dependencia  # sumatoria total de dependencia
        indice += 1
        dependencia = 0
    # se inserta la sumatoria total dependencia donde di_total = li_total, ultima celda
    lista.append(Valor_posicion(posicion="", valor=suma_di, descripcion=suma_di))

    return lista


# Calcula el indicador de estabilidad del estudio
def calcular_estabilidad(request, idEstudio):

    actores = Actor.objects.filter(idEstudio=int(idEstudio))
    valores_midi = calcular_midi(request, idEstudio)
    lista_influencias = []
    lista_dependencias = []
    total = valores_midi[len(valores_midi) - 1].valor
    estabilidad = 0

    for i in valores_midi:
        if i.posicion == actores.count() + 1:
            lista_influencias.append(i.valor)

        elif i.posicion == "" and len(lista_dependencias) < actores.count():
            lista_dependencias.append(i.valor)

    for i in range(len(lista_influencias)):
        estabilidad += abs(lista_influencias[i] - lista_dependencias[i])

    estabilidad = round((estabilidad / (2 * total)) * 100, 2)
    return estabilidad


# <<<<FUNCIONES RELACIONES MAO>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Establece el diccionario correspondiente al contexto a enviar al template de la matriz mao correspondiente
def crear_contexto_mao(request, idEstudio, numero_matriz):

    concenso = verificar_concenso(request, idEstudio)
    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    tipo_usuario = obtener_tipo_usuario(request, estudio.id)
    lista_objetivos = Objetivo.objects.filter(idEstudio=estudio.id).order_by('id')
    lista_actores = Actor.objects.filter(idEstudio=estudio.id).order_by('id')
    tamano_matriz_completa = (len(lista_actores)*len(lista_objetivos))
    lista_mao = []
    num_expertos = []

    if numero_matriz < 3:
        if concenso is True:
            lista_mao = calcular_concenso_mao(request, estudio.id, numero_matriz)
            num_expertos = lista_mao['expertos']
            lista_mao = lista_mao['concenso']
        else:
            lista_mao = Relacion_MAO.objects.filter(idEstudio=estudio.id, tipo=numero_matriz,
                                                idExperto=request.user.id).order_by('idActorY', 'idObjetivoX')
    else:
        if concenso is True:
            lista_mao = calcular_concenso_mao(request, estudio.id, numero_matriz)
            num_expertos = calcular_concenso_mao(request, estudio.id, 2)
            num_expertos = num_expertos['expertos']
            lista_mao = lista_mao['concenso']
        else:
            estado_mao3 = verificar_mid_mao2(request, estudio.id)
            if estado_mao3:
                lista_mao = calcular_valores_3mao(request, estudio.id)

    # Si la matriz esta completa
    if len(lista_mao) == tamano_matriz_completa and tamano_matriz_completa > 0:
        lista_contexto = calcular_valores_mao(estudio.id, lista_mao, MATRIZ_COMPLETA)
        valores_mao = agregar_descripcion_mao(estudio.id, numero_matriz, lista_contexto[0])
        valores_caa = agregar_descripcion_caa_daa(estudio.id, lista_contexto[1])
        valores_daa = agregar_descripcion_caa_daa(estudio.id, lista_contexto[2])

        contexto = {'objetivos': lista_objetivos,
                    'actores': lista_actores,
                    'valores_mao': valores_mao,
                    'posicion_salto': lista_objetivos.count() + COLUMNAS_EXTRAS_MATRIZ_MAO,
                    'posicion_salto_movilizacion': (lista_objetivos.count() * 2) + 4,
                    'valores_caa': valores_caa,
                    'posicion_salto_caa_daa': lista_actores.count(),
                    'valores_daa': valores_daa,
                    'estado_matriz': MATRIZ_COMPLETA,
                    'estudio': estudio,
                    'usuario': tipo_usuario,
                    'expertos': num_expertos}
    # Si la matriz es 1mao o 2mao y esta incompleta
    elif len(lista_mao) != tamano_matriz_completa and numero_matriz != 3 or len(lista_mao) == 0 and numero_matriz != 3:

        valores_mao = generar_mao_incompleta(estudio.id, lista_mao)
        valores_mao = agregar_descripcion_mao(estudio.id, numero_matriz, valores_mao)
        contexto = {'objetivos': lista_objetivos,
                    'actores': lista_actores,
                    'valores_mao': valores_mao,
                    'valores_caa': [],
                    'valores_daa': [],
                    'posicion_salto': lista_objetivos.count() + COLUMNAS_EXTRAS_MATRIZ_MAO,
                    'posicion_salto_movilizacion': (lista_objetivos.count() * 2) + 4,
                    'estado_matriz': MATRIZ_INCOMPLETA,
                    'estudio': estudio,
                    'usuario': tipo_usuario}
    else:
        contexto = {'estudio': estudio, 'usuario': tipo_usuario, 'estado_matriz': MATRIZ_INCOMPLETA}

    return contexto


# Establece los valores de la matriz que se muestran en la matriz mao
def calcular_valores_mao(idEstudio, mao, estado_matriz):

    objetivos = Objetivo.objects.filter(idEstudio=idEstudio).order_by('id')
    actores = Actor.objects.filter(idEstudio=idEstudio).order_by('id')
    lista_valores_mao = []
    list_valores_caa = []
    lista_valores_daa = []
    posicion = 0        # referencia a la lista de valores mao
    indice = 0          # referencia a las lista de actores y objetivos
    suma_positivos = 0  # sumatoria de los valores positivos de implicacion
    suma_negativos = 0  # sumatoria de los valores negativos de implicacion

    # se agregan las relaciones mao a la lista de valores que sera enviada como contexto
    for i in range(len(mao)):
        posicion += 1
        # se agregan las relaciones mao registradas asignandoles una posicion para facilitar su impresion
        lista_valores_mao.append(Valor_posicion(posicion=posicion, valor=mao[i].valor, descripcion=""))

        # se determinan las implicaciones positivas, negativas y totales (columnas +, - , Imp)
        if mao[i].valor == abs(mao[i].valor) and mao[i].valor != VALOR_RELACION_NO_REGISTRADA:
            suma_positivos += mao[i].valor
        elif mao[i].valor != abs(mao[i].valor) and mao[i].valor != VALOR_RELACION_NO_REGISTRADA:
            suma_negativos += abs(mao[i].valor)

        # cuando el numero de registros alcanza la cantidad de objetivos se tiene una fila de la matriz
        # se agregan entonces las sumatorias de implicacion (ultimas 3 columnas)
        if posicion == objetivos.count():
            positivo = round(suma_positivos, 1)
            negativo = round(suma_negativos, 1)
            total = round(suma_positivos + suma_negativos, 1)
            lista_valores_mao.extend([
                Valor_posicion(posicion=posicion + 1, valor=positivo, descripcion=positivo),
                Valor_posicion(posicion=posicion + 2, valor=negativo, descripcion=negativo),
                Valor_posicion(posicion=posicion + 3, valor=total, descripcion=total)])

            # Agregada la fila se determina la posicion donde se va a colocar el nombre corto de fila (primera columna)
            posicion_nombre = (objetivos.count() + 4) * indice
            lista_valores_mao.insert(posicion_nombre, Valor_posicion(posicion=0,
                                                                     valor=actores[indice].nombreCorto,
                                                                     descripcion=actores[indice].nombreLargo))
            # se reinician los valores para crear la nueva fila
            posicion = 0
            indice += 1
            suma_positivos = 0
            suma_negativos = 0

    # si la matriz esta totalmente diligenciada
    if estado_matriz == MATRIZ_COMPLETA:
        list_valores_caa = calcular_caa_daa(idEstudio, lista_valores_mao, 1)
        lista_valores_daa = calcular_caa_daa(idEstudio, lista_valores_mao, 2)

    # se agrega a lista los valores de movilizacion
    valores_mao = []
    if objetivos.count() > 0:
        valores_mao = establecer_valores_movilizacion(objetivos, lista_valores_mao)

    if estado_matriz == MATRIZ_COMPLETA:
        lista= []
        lista.append(valores_mao)
        lista.append(list_valores_caa)
        lista.append(lista_valores_daa)
        return lista
    else:
        return valores_mao


# <<<<FUNCIONES RELACIONES CAA Y DAA>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Generacion de matriz de convergencias Y divergencias
def calcular_caa_daa(idEstudio, lista_mao, tipo):

    cant_objetivos = Objetivo.objects.filter(idEstudio=idEstudio).order_by('id').count()
    actores = Actor.objects.filter(idEstudio=idEstudio).order_by('id')
    valores_mao = []
    cont = 1
    cont2 = 0

    # filtrado del contenido de la matriz 2mao (solo lo valores de relacion actor x objetivo)
    # al conjunto de valores de una fila se le asigna el una misma posicion para facilitar
    # los filtros y la posterior comparacion
    for i in lista_mao:
        if i.posicion > 0 and i.posicion <= cant_objetivos:
            valores_mao.append(Valor_posicion(posicion=cont, valor=i.valor, descripcion=""))
            cont2 += 1
            if cont2 == cant_objetivos:
                cont += 1
                cont2 = 0

    # Devuelve una lista con los valores que poseen la posicion pasada como parametro
    def filtrar_posicion(pos):
        sublista_aux = []
        for x in valores_mao:
            if x.posicion == pos:
                sublista_aux.append(x.valor)

        # a la sublista se ingresan los mismos n valores que contiene, hasta que tenga...
        # la misma longitud de la lista que contiene los otros valores con que se ha de comparar
        b = 0
        while len(sublista_aux) < len(valores_mao) - cant_objetivos:
            sublista_aux.append(sublista_aux[b])
            b += 1
            if b == cant_objetivos:
                b = 0
        return sublista_aux

    # devuelve una lista con los valores con que se ha de comparar la lista retornada por filtrar_posicion
    def filtrar_comparacion(pos):
        sublista_aux = []
        for q in valores_mao:
            if q.posicion != pos:
                sublista_aux.append(q.valor)
        return sublista_aux

    # Se lleva a cabo el calculo de las convergencias o divergencias de acuerdo al tipo de matriz
    # if tipo == 1 convergencias
    # if tipo == 2 divergencias
    valores = []  # contiene los valores de las convergencias o divergencias calculadas
    pos = 1
    if tipo == 1:
        # Se realiza la comparacion para identificar las convergencias (Signos iguales)
        while pos <= actores.count():
            aux = filtrar_posicion(pos)
            aux2 = filtrar_comparacion(pos)
            cont = 0
            cont2 = 0
            suma = 0
            for i in range(len(aux)):
                # compara si ambos valores son positivos
                if (aux[i] == abs(aux[i])) and (aux2[i] == abs(aux2[i])) and (aux[i] != 0) and (aux2[i] != 0):
                    suma += (aux[i] + aux2[i]) / 2.0
                    cont += 1
                # compara si ambos valores son negativos
                elif (aux[i] != abs(aux[i])) and (aux2[i] != abs(aux2[i])) and (aux[i] != 0) and (aux2[i] != 0):
                    suma += (abs(aux[i]) + abs(aux2[i])) / 2.0
                    cont += 1
                else:
                    cont2 += 1
                if cont + cont2 == cant_objetivos:
                    cont = 0
                    cont2 = 0
                    valores.append(round(suma, 1))
                    suma = 0
            pos += 1

    else:
        # Se realiza la comparacion para identificar las divergencias (Signos diferentes)
        while pos <= actores.count():
            aux = filtrar_posicion(pos)
            aux2 = filtrar_comparacion(pos)
            cont = 0
            cont2 = 0
            suma = 0
            for i in range(len(aux)):
                # compara si el primero es positivo y el segundo negativo
                if (aux[i] == abs(aux[i])) and (aux2[i] != abs(aux2[i])) and (aux[i] != 0) and (aux2[i] != 0):
                    suma += (aux[i] + abs(aux2[i])) / 2.0
                    cont += 1
                # compara si el primero es negativo y el segundo positivo
                elif (aux[i] != abs(aux[i])) and (aux2[i] == abs(aux2[i])) and (aux[i] != 0) and (aux2[i] != 0):
                    suma += (abs(aux[i]) + aux2[i]) / 2.0
                    cont += 1
                else:
                    cont2 += 1
                if cont + cont2 == cant_objetivos:
                    cont = 0
                    cont2 = 0
                    valores.append(round(suma, 1))
                    suma = 0
            pos += 1

# posible corte-----------------------------------------------------------------------------
    # Agregado a la lista de los nombres cortos y de los ceros de la diagonal
    cont = 0
    pos_list = 1

    for i in range(actores.count()):
        # agregado de los nombres cortos de los actores
        valores.insert(cont, actores[i].nombreCorto)
        cont2 = cont + pos_list
        # agregado de los valores 0 de la diagonal
        valores.insert(cont2, 0)
        pos_list += 1
        cont += actores.count() + 1

    # Asignacion de una posicion a cada valor para facilitar la visualizacion de la matriz
    cont = 0
    valores_posicion = []
    for i in valores:
        valores_posicion.append(Valor_posicion(posicion=cont, valor=i, descripcion=i))
        if cont == actores.count():
            cont = 0
        else:
            cont += 1

    if tipo == 1:
        valores_posicion.append(Valor_posicion(posicion=0, valor="Ci", descripcion="Convergencia"))
    else:
        valores_posicion.append(Valor_posicion(posicion=0, valor="Di", descripcion="Divergencia"))

    # Calculo del numero de convergencias o divergencias totales de cada actor
    cont = 1
    suma = 0
    while cont <= actores.count():
        for i in valores_posicion:
            if i.posicion == cont:
                suma += i.valor
        valores_posicion.append(
            Valor_posicion(posicion="", valor="{0:.1f}".format(suma), descripcion="{0:.1f}".format(suma)))
        cont += 1
        suma = 0

    return valores_posicion


# Agrega a la lista de valores mao, los valores de movilizacion (ultimas 3 filas)
def establecer_valores_movilizacion(objetivos, valores):

    lista_positivos = []
    lista_negativos = []
    lista_movilizacion = []
    suma_positivos = 0
    suma_negativos = 0
    posicion_movilizacion = objetivos.count() + 4  # +4 por las cuatro columnas extras (nombresCortos y sumatorias)
    indice = 1

    # Determinacion de sumatorias de movilizacion (ultima fila) suma de columnas
    while indice <= objetivos.count():
        for i in valores:
            if i.posicion == indice:
                if i.valor == abs(i.valor) and i.valor != VALOR_RELACION_NO_REGISTRADA:
                    suma_positivos += i.valor
                elif i.valor != abs(i.valor) and i.valor != VALOR_RELACION_NO_REGISTRADA:
                    suma_negativos += abs(i.valor)
        negativo = round(suma_negativos, 1)
        positivo = round(suma_positivos, 1)
        total = positivo + negativo
        # se agregan a la lista los valores de movilizacion
        lista_negativos.append(Valor_posicion(posicion=0, valor=negativo, descripcion=negativo))
        lista_positivos.append(Valor_posicion(posicion=0, valor=positivo, descripcion=positivo))
        lista_movilizacion.append(Valor_posicion(posicion=0, valor=total, descripcion=total))
        indice += 1         # iteracion de las posiciones
        suma_positivos = 0  # reinicio de la suma positiva
        suma_negativos = 0  # reinicio de la suma negativa

    # Se agregan las sumatorias de movilizacion positiva
    valores.append(Valor_posicion(posicion=0, valor="+", descripcion="MOVILIZACIÓN POSITIVA"))
    for i in range(len(lista_positivos)):
        valores.append(Valor_posicion(posicion=posicion_movilizacion + i + 1,
                                      valor=lista_positivos[i].valor,
                                      descripcion=lista_positivos[i].valor))

    # Se agregan las sumatorias de movilizacion negativa
    valores.append(Valor_posicion(posicion=0, valor="-", descripcion="MOVILIZACIÓN NEGATIVA"))
    for i in range(len(lista_negativos)):
        valores.append(Valor_posicion(posicion=posicion_movilizacion + i + 1,
                                      valor=lista_negativos[i].valor,
                                      descripcion=lista_negativos[i].valor))

    # Se agregan la sumatoria de movilizacion total (Suma absoluta)
    valores.append(Valor_posicion(posicion=0, valor="Mov.", descripcion="MOVILIZACIÓN"))
    for i in range(len(lista_movilizacion)):
        valores.append(Valor_posicion(posicion="",
                                      valor=lista_movilizacion[i].valor,
                                      descripcion=lista_movilizacion[i].valor))

    return valores


# Verifica si las matrices MID y 2MAO estan totalmente diligenciadas para proceder al calculo de la matriz 3mao
def verificar_mid_mao2(request, idEstudio):

    objetivos = Objetivo.objects.filter(idEstudio=idEstudio).order_by('id')
    actores = Actor.objects.filter(idEstudio=idEstudio).order_by('id')
    mid = Relacion_MID.objects.filter(idActorY__idEstudio=idEstudio, idExperto=request.user.id).order_by('idActorY', 'idActorX')
    mao2 = Relacion_MAO.objects.filter(tipo=2, idEstudio=idEstudio, idExperto=request.user.id).order_by('idActorY', 'idObjetivoX')
    tamano_mid = len(actores) * len(actores)
    tamano_2mao = len(actores) * len(objetivos)
    estado_3mao = False

    if len(mid) == tamano_mid and len(mao2) == tamano_2mao:
        estado_3mao = True

    return estado_3mao


# Calculo de los valores 3mao = 2mao * ri
def calcular_valores_3mao(request, idEstudio):

    concenso = verificar_concenso(request, idEstudio)
    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    cant_objetivos = len(Objetivo.objects.filter(idEstudio=estudio.id).order_by('id'))
    valores_ri = calcular_ri(request, idEstudio)
    valores_3mao = []

    if concenso is True:
        mao = calcular_concenso_mao(request, estudio.id, 2)
        mao = mao['concenso']
    else:
        mao = Relacion_MAO.objects.filter(idEstudio=estudio.id, tipo=2, idExperto=request.user.id).order_by('idActorY',
                                                                                                            'idObjetivoX')
    # Multiplicacion de los valores 2mao por los valores ri para hallar los valores 3mao
    cont = 0
    cont2 = 0
    for i in mao:
        if cont2 < cant_objetivos:
            valor = i.valor * valores_ri[cont]
            valores_3mao.append(Valor_posicion(posicion=cont2 + 1, valor=round(valor, 1), descripcion=round(valor, 1)))
            cont2 += 1
            if cont2 == cant_objetivos:
                cont2 = 0
                cont += 1

    return valores_3mao


# Calculo del valor ri para la matriz 3mao
def calcular_ri(request, idEstudio):

    cant_actor = len(Actor.objects.filter(idEstudio=int(idEstudio)).order_by('id'))
    valores_midi = calcular_midi(request, idEstudio)
    valores_diagonal = []  # valores de la diagonal de la matriz midi
    valores_Ii = []        # valores Ii de midi
    valores_Di = []        # valores Di de midi
    valores_ri = []        # valores ri calculados

    # se obtienen los valores de la diagonal en la matriz midi
    cont = 0
    cont2 = 0
    for i in valores_midi:
        a = i.posicion
        # se obtienen los valores de la diagonal de la matriz midi
        # mediante este if no se incluye la columna de nombrecorto, Ii y Di
        if a != "" and (a > 0 and a <= cant_actor):
            if len(valores_diagonal) == 0 or cont2 + cant_actor == cont:
                valores_diagonal.append(i.valor)
                cont += 1
                cont2 = cont
            else:
                cont += 1
        # se obtienen los valores de Ii de la matriz midi
        elif i.posicion == cant_actor+1:
            valores_Ii.append(i.valor)
        # se obtienen los valores Di de la matriz midi
        elif i.posicion == "":
            valores_Di.append(i.valor)

    # se calcula el valor ri de cada actor
    suma_ri = 0
    for i in range(len(valores_diagonal)):
        a = valores_Ii[i]
        b = valores_diagonal[i]
        c = valores_Di[cant_actor]
        d = valores_Di[i]
        ri = ((a - b) / (c * 1.0))*(a / ((a + d)*1.0))
        # el valor calculado es guardado en una lista
        valores_ri.append(ri)
        suma_ri += ri
    # se calcula el promedio de los valores ri
    ri_prom = suma_ri / cant_actor

    # se obtiene el valor ri promedio de cada actor
    for i in range(len(valores_ri)):
        res = valores_ri[i]/ri_prom
        valores_ri[i] = res

    return valores_ri


# Genera la matriz mao en caso de que este incompleta, solo 1mao y 2mao
def generar_mao_incompleta(idEstudio, mao):

    lista_objetivos = Objetivo.objects.filter(idEstudio=idEstudio).order_by('id')
    lista_actores = Actor.objects.filter(idEstudio=idEstudio).order_by('id')
    lista_mao_incompleta = []               # contendra los valores de la matriz mao incompleta
    lista_actores_objetivos = []            # establece el orden de los ejes de la matriz

    # se obtiene el orden de los ejes
    for i in lista_actores:
        for j in lista_objetivos:
            lista_actores_objetivos.append(Valor_xy(y=i.id, x=j.id, valor=""))

    # se obtienen las influencias mao actualmente registradas
    for i in mao:
        lista_mao_incompleta.append(Valor_xy(y=i.idActorY.id, x=i.idObjetivoX.id, valor=i.valor))

    # ingreso de valores de relleno en la matriz mao para permitir la comparacion con el orden ideal (igual longitud)
    registros_relleno = 0
    while len(lista_mao_incompleta) != len(lista_actores_objetivos):
        lista_mao_incompleta.append(Valor_xy(y=0, x=0, valor=0))
        registros_relleno += 1

    # al detectar ejes diferentes al ideal se inserta en esa posicion un registro de relleno con los ejes adecucados
    for j in range(len(lista_actores_objetivos)):
            eje_y = lista_actores_objetivos[j].y
            eje_x = lista_actores_objetivos[j].x
            if lista_mao_incompleta[j].y != eje_y or lista_mao_incompleta[j].x != eje_x:
                lista_mao_incompleta.insert(j, Valor_xy(y=eje_y, x=eje_x, valor=VALOR_RELACION_NO_REGISTRADA))

    # se eliminan los registros de relleno con ejes de relleno
    while registros_relleno != 0:
        lista_mao_incompleta.pop()
        registros_relleno -= 1

    lista_contexto = calcular_valores_mao(idEstudio, lista_mao_incompleta, MATRIZ_INCOMPLETA)

    return lista_contexto


# Agrega a la lista de valores mid y midi la descripcion del valor
def agregar_descripcion_mao(idEstudio, tipo_matriz, lista):

    objetivos = Objetivo.objects.filter(idEstudio=idEstudio).order_by('id')

    if tipo_matriz == 1:
        for i in lista:
            if i.posicion in range(objetivos.count() + 1):
                if i.valor == 0:
                    i.descripcion = "Neutro"
                elif i.valor == 1:
                    i.descripcion = "A favor"
                elif i.valor == -1:
                    i.descripcion = "En contra"

    elif tipo_matriz == 2:
        for i in lista:
            if i.posicion in range(objetivos.count()+1) and i.descripcion == "":
                if i.valor == abs(i.valor):
                    i.descripcion = "Acuerdo"
                else:
                    i.descripcion = "Desacuerdo"

    elif tipo_matriz == 3:
        for i in lista:
            if i.posicion in range(objetivos.count() + 1) and i.descripcion == "":
                i.descripcion = i.valor
    return lista


# Agrega a la lista de valores mid y midi la descripcion del valor
def agregar_descripcion_caa_daa(idEstudio, lista):

    actores = Actor.objects.filter(idEstudio=idEstudio).order_by('id')
    indice = 0

    for i in lista:
        if i.posicion == 0 and indice < actores.count():
                i.descripcion = actores[indice].nombreLargo
                indice += 1
        elif i.valor != "Ci" and i.valor != "Di":
            i.descripcion = i.valor

    return lista


# ------------------------------------VIEWS AJAX----------------------------------------------------

# Devuelve la lista de actores que no se han registrado en determina matriz
def Consultar_actores_faltantes(request):

    if request.is_ajax():
        id = request.GET['id']
        idEstudio = int(request.GET['estudio'])
        tipo = request.GET['tipo']
        actores = Actor.objects.filter(idEstudio=idEstudio).order_by('id')
        lista_registrados = []
        lista_id = []
        lista_valores = []

        # si se esta registrando una influencia mid
        if tipo == "form_mid":
            # para desactivar la opcion correspondiente a autoinfluencia se agrega el id como registrado

            # se obtiene la lista de relaciones mid registradas
            mid = Relacion_MID.objects.filter(idActorY__idEstudio=idEstudio).order_by('idActorY', 'idActorX')
            # se obtienen los id de los actores ya registrados en la matriz mid
            for i in mid:
                if i.idActorY.id == int(id) and i.idExperto == request.user:
                    lista_registrados.append(i.idActorX.id)
                    lista_valores.append(i.valor)

            # el actor seleccionado debe mostrarse desactivado en caso de no estarlo mediante la funcion
            # de auto_influencia
            if id not in lista_registrados:
                lista_registrados.append(id)
                lista_valores.append(0)

        # si se esta registrando una ficha de estrategias
        if tipo == "form_ficha":
            fichas = Ficha.objects.filter(idActorY__idEstudio=idEstudio).order_by('idActorY', 'idActorX')
            for i in fichas:
                if i.idActorY.id == int(id):
                    lista_registrados.append(i.idActorX.id)

        # se obtiene la lista de id de los actores del estudio
        for i in actores:
            lista_id.append(i.id)

        response = JsonResponse({'actores': lista_id,
                                 'lista': lista_registrados,
                                 'valores': lista_valores})
        return HttpResponse(response.content)


# Devuelve la lista de objetivos que no se han registrado en determinada matriz mao
def Consultar_objetivos_faltantes(request):

    if request.is_ajax():
        id = request.GET['id']
        idEstudio = int(request.GET['estudio'])
        tipo = request.GET['tipo']
        objetivos = Objetivo.objects.all().order_by('id')
        lista_registrados = []
        lista_valores = []
        lista_id = []

        # si se esta registrando una influencia 1mao
        if tipo == "form_1mao":
            # se obtiene la lista de relaciones  1mao registradas
            mao = Relacion_MAO.objects.filter(tipo=1,
                                              idEstudio=idEstudio,
                                              idExperto=request.user.id).order_by('idActorY', 'idObjetivoX')
            # se obtienen los id de los objetivos ya registrados en la matriz mao con ese actor Y
            for i in mao:
                if i.idActorY.id == int(id) and i.idExperto == request.user:
                    lista_registrados.append(i.idObjetivoX.id)
                    lista_valores.append(i.valor)

        # si se esta registrando una influencia 2mao
        elif tipo == "form_2mao":
            mao = Relacion_MAO.objects.all().filter(tipo=2,
                                                    idEstudio=idEstudio,
                                                    idExperto=request.user.id).order_by('idActorY', 'idObjetivoX')
            for i in mao:
                if i.idActorY.id == int(id):
                    lista_registrados.append(i.idObjetivoX.id)
                    lista_valores.append(i.valor)

        # se obtiene la lista de id de los objetivos del estudio
        for i in objetivos:
            lista_id.append(i.id)

        response = JsonResponse({'objetivos': lista_id,
                                 'lista': lista_registrados,
                                 'valores': lista_valores})
        return HttpResponse(response.content)

# --------------------------------------------------------------------------------------------------


# Determina si el usuario en sesion hace parte del proyecto y que rol ocupa
def obtener_tipo_usuario(request, idEstudio):

    estudio = Estudio_Mactor.objects.get(id=idEstudio)
    lista_expertos = estudio.idExpertos.all()
    tipo = ""

    # Si el usuario es coordinador y experto
    if request.user in lista_expertos and estudio.idCoordinador == request.user:
        tipo = "COORDINADOR_EXPERTO"
    # Si el usuario solo es coordinador or request.user.is_superuser
    elif estudio.idCoordinador == request.user:
        tipo = "COORDINADOR"
    # Si el usuario es solo experto
    elif request.user in lista_expertos:
        tipo = "EXPERTO"

    print(tipo, "-------")
    return tipo

# ---------------------------------------EXPORTACION A EXCEL------------------------------------------------------->


# Exporta a excel los datos basicos del estudio y sus respectivas entradas
def exportar_estudio_xls(request, idEstudio):

    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="estudio_mactor.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    hoja_estudio = wb.add_sheet('Estudio')
    hoja_actores = wb.add_sheet('Actores')
    hoja_fichas = wb.add_sheet('Estrategias')
    hoja_objetivos = wb.add_sheet('Objetivos')
    hoja_mid = wb.add_sheet('MID')
    hoja_1mao = wb.add_sheet('1MAO')
    hoja_2mao = wb.add_sheet('2MAO')

    # Sheet header, first row
    row_num = 0
    row_num2 = 0
    row_num3 = 0
    row_num4 = 0
    row_num5 = 0
    row_num6 = 0
    row_num7 = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Titulo', 'Descripción', 'Fecha Inicio', 'Fecha Fin']
    columns1 = ['Nombre Largo', 'Nombre Corto', 'Descripción']
    columns2 = ['Estrategias del actor', 'Sobre el actor', 'Estrategias']
    columns3 = ['Influencia del actor', 'Sobre el actor', 'Valor', 'Justificación']
    columns4 = ['Posicion del actor', 'Ante el objetivo', 'Valor', 'Justificación']

    for col_num in range(len(columns)):
        hoja_estudio.write(row_num7, col_num, columns[col_num], font_style)

    for col_num in range(len(columns1)):
        hoja_actores.write(row_num, col_num, columns1[col_num], font_style)

    for col_num in range(len(columns2)):
        hoja_fichas.write(row_num2, col_num, columns2[col_num], font_style)

    for col_num in range(len(columns1)):
        hoja_objetivos.write(row_num3, col_num, columns1[col_num], font_style)

    for col_num in range(len(columns3)):
        hoja_mid.write(row_num4, col_num, columns3[col_num], font_style)

    for col_num in range(len(columns4)):
        hoja_1mao.write(row_num5, col_num, columns4[col_num], font_style)

    for col_num in range(len(columns4)):
        hoja_2mao.write(row_num6, col_num, columns3[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    filas = obtener_datos_estudio(request, int(idEstudio))

    for row in filas['estudio']:
        row_num7 += 1
        for col_num in range(len(row)):
            hoja_estudio.write(row_num7, col_num, row[col_num], font_style)

    for row in filas['actores']:
        row_num += 1
        for col_num in range(len(row)):
            hoja_actores.write(row_num, col_num, row[col_num], font_style)

    for row in filas['fichas']:
        row_num2 += 1
        for col_num in range(len(row)):
            hoja_fichas.write(row_num2, col_num, row[col_num], font_style)

    for row in filas['objetivos']:
        row_num3 += 1
        for col_num in range(len(row)):
            hoja_objetivos.write(row_num3, col_num, row[col_num], font_style)

    for row in filas['mid']:
        row_num4 += 1
        for col_num in range(len(row)):
            hoja_mid.write(row_num4, col_num, row[col_num], font_style)

    for row in filas['1mao']:
        row_num5 += 1
        for col_num in range(len(row)):
            hoja_1mao.write(row_num5, col_num, row[col_num], font_style)

    for row in filas['2mao']:
        row_num6 += 1
        for col_num in range(len(row)):
            hoja_2mao.write(row_num6, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def obtener_datos_estudio(request, idEstudio):

    usuario = obtener_tipo_usuario(request, idEstudio)
    estudio = get_object_or_404(Estudio_Mactor, id=idEstudio)
    fila_estudio = Estudio_Mactor.objects.filter(id=estudio.id).values_list('titulo', 'descripcion', 'fecha_inicio', 'fecha_final')
    filas_actores = Actor.objects.filter(idEstudio=estudio.id).values_list('nombreLargo', 'nombreCorto', 'descripcion')
    filas_fichas = Ficha.objects.filter(idEstudio=estudio.id).values_list('idActorY__nombreLargo',
                                                                               'idActorX__nombreLargo',
                                                                               'estrategia')
    filas_objetivos = Objetivo.objects.filter(idEstudio=estudio.id).values_list('nombreLargo', 'nombreCorto',
                                                                               'descripcion')

    if usuario == "COORDINADOR":
        filas_mid = Relacion_MID.objects.filter(idActorY__idEstudio=estudio.id).values_list('idActorY__nombreLargo',
                                                                                 'idActorX__nombreLargo',
                                                                                 'valor', 'justificacion').order_by(
            'idActorY', 'idActorX')
        filas_1mao = Relacion_MAO.objects.filter(idEstudio=estudio.id, tipo=1).values_list('idActorY__nombreLargo',
                                                                                          'idObjetivoX__nombreLargo',
                                                                                          'valor',
                                                                                          'justificacion').order_by(
            'idActorY', 'idObjetivoX')
        filas_2mao = Relacion_MAO.objects.filter(idEstudio=estudio.id, tipo=2).values_list('idActorY__nombreLargo',
                                                                                          'idObjetivoX__nombreLargo',
                                                                                          'valor',
                                                                                          'justificacion').order_by(
            'idActorY', 'idObjetivoX')
    else:
        filas_mid = Relacion_MID.objects.filter(idActorY__idEstudio=estudio.id, idExperto=request.user.id).values_list(
            'idActorY__nombreLargo',
            'idActorX__nombreLargo',
            'valor', 'justificacion').order_by(
            'idActorY', 'idActorX')
        filas_1mao = Relacion_MAO.objects.filter(idEstudio=estudio.id, tipo=1, idExperto=request.user.id).values_list(
            'idActorY__nombreLargo',
            'idObjetivoX__nombreLargo',
            'valor',
            'justificacion').order_by(
            'idActorY', 'idObjetivoX')
        filas_2mao = Relacion_MAO.objects.filter(idEstudio=estudio.id, tipo=2, idExperto=request.user.id).values_list(
            'idActorY__nombreLargo',
            'idObjetivoX__nombreLargo',
            'valor',
            'justificacion').order_by(
            'idActorY', 'idObjetivoX')

    filas = {'estudio': fila_estudio, 'actores': filas_actores, 'fichas': filas_fichas, 'objetivos': filas_objetivos,
             'mid': filas_mid, '1mao': filas_1mao, '2mao': filas_2mao}

    return filas


def exportar_actores_xls(request, idEstudio):

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="tabla_actores.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Actores')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Nombre Largo', 'Nombre Corto', 'Descripción']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Actor.objects.filter(idEstudio=idEstudio).values_list('nombreLargo', 'nombreCorto', 'descripcion')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def exportar_fichas_xls(request, idEstudio):

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="fichas_estrategias.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Estrategias')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Estrategias del actor', 'Sobre el actor', 'Estrategias']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Ficha.objects.filter(idEstudio=idEstudio).values_list('idActorY__nombreLargo',
                                                                       'idActorX__nombreLargo',
                                                                       'estrategia')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def exportar_objetivos_xls(request, idEstudio):

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="tabla_objetivos.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Objetivos')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Nombre Largo', 'Nombre Corto', 'Descripción']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Objetivo.objects.filter(idEstudio=idEstudio).values_list('nombreLargo', 'nombreCorto', 'descripcion')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


# ----------------------------------------HISTOGRAMAS--------------------------------------------------------->

def histograma_mid(request, idEstudio):

    concenso = verificar_concenso(request, idEstudio)
    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    usuario = obtener_tipo_usuario(request, estudio.id)

    if concenso is True:
        influencias_mid = calcular_concenso_mid(estudio.id)
        cantidad_expertos = influencias_mid['num_expertos']
        contexto = {'estudio': estudio, 'usuario': usuario, 'expertos': cantidad_expertos}
    else:
        contexto = {'estudio': estudio, 'usuario': usuario}

    return render(request, 'influencia/graficos/histograma_mid.html', contexto)


def datos_histograma_mid(request):

    if request.is_ajax():
        estudio = get_object_or_404(Estudio_Mactor, id=int(request.GET['estudio']))
        usuario = obtener_tipo_usuario(request, estudio.id)
        actores = Actor.objects.filter(idEstudio=estudio.id).order_by('id')
        lista_nombres = []
        lista_influencias = []
        lista_dependencias = []

        concenso = verificar_concenso(request, request.GET['estudio'])
        valores_mid = []
        if concenso is True:
            valores_mid = calcular_concenso_mid(estudio.id)
            valores_mid = valores_mid['concenso']
        elif usuario != "COORDINADOR":
            valores_mid = Relacion_MID.objects.filter(idActorY__idEstudio=estudio.id,
                                                            idExperto=request.user.id).order_by('idActorY', 'idActorX')
        valores_mid = establecer_valores_mid(estudio.id, valores_mid)

        for i in valores_mid:
            # Valores de influencia
            if i.posicion == actores.count()+1:
                lista_influencias.append(i.valor)
            # Valores de dependencia
            if i.posicion == "" and len(lista_dependencias) < actores.count():
                lista_dependencias.append(i.valor)

        for i in actores:
            lista_nombres.append(i.nombreCorto)

        data = {'labels': lista_nombres,
                'influencias': lista_influencias,
                'dependencias': lista_dependencias}

        json_data = json.dumps(data)
        return HttpResponse(json_data)


def histograma_ri(request, idEstudio):
    concenso = verificar_concenso(request, idEstudio)
    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    usuario = obtener_tipo_usuario(request, estudio.id)

    if concenso is True:
        influencias_mid = calcular_concenso_mid(estudio.id)
        cantidad_expertos = influencias_mid['num_expertos']
        contexto = {'estudio': estudio, 'usuario': usuario, 'expertos': cantidad_expertos}
    else:
        contexto = {'estudio': estudio, 'usuario': usuario}

    return render(request, 'influencia/graficos/histograma_ri.html', contexto)


def datos_histograma_ri(request):
    if request.is_ajax():
        valores_ri = calcular_ri(request, request.GET['estudio'])  # str para que verifique si es concenso
        estudio = int(request.GET['estudio'])
        actores = Actor.objects.filter(idEstudio=estudio).order_by('id')
        lista_nombres = []

        for i in actores:
            lista_nombres.append(i.nombreCorto)

        for i in range(len(valores_ri)):
            valores_ri[i] = round(valores_ri[i], 2)

        data = {'labels': lista_nombres,
                'valores_ri': valores_ri}

        json_data = json.dumps(data)
        return HttpResponse(json_data)


def histograma_implicacion(request, idEstudio, numero_matriz):

    concenso = verificar_concenso(request, idEstudio)
    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    usuario = obtener_tipo_usuario(request, estudio.id)
    matriz = int(numero_matriz)

    if concenso is True:
        concenso_mao = calcular_concenso_mao(request, estudio.id, matriz)
        if matriz != 3:
            cantidad_expertos = concenso_mao['expertos']
        else:
            cantidad_expertos = calcular_concenso_mao(request, estudio.id, 2)
            cantidad_expertos = cantidad_expertos['expertos']

        contexto = {'estudio': estudio,  'numero_matriz': matriz,
                    'usuario': usuario, 'expertos': cantidad_expertos}
    else:
        contexto= {'estudio': estudio, 'numero_matriz': matriz, 'usuario': usuario}

    return render(request, 'mao/graficos/histograma_implicacion.html', contexto)


def histograma_movilizacion(request, idEstudio, numero_matriz):

    concenso = verificar_concenso(request, idEstudio)
    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    usuario = obtener_tipo_usuario(request, estudio.id)
    matriz = int(numero_matriz)

    if concenso is True:
        concenso_mao = calcular_concenso_mao(request, estudio.id, matriz)
        if matriz != 3:
            cantidad_expertos = concenso_mao['expertos']
        else:
            cantidad_expertos = calcular_concenso_mao(request, estudio.id, 2)
            cantidad_expertos = cantidad_expertos['expertos']

        contexto = {'estudio': estudio,  'numero_matriz': matriz,
                    'usuario': usuario, 'expertos': cantidad_expertos}
    else:
        contexto= {'estudio': estudio, 'numero_matriz': matriz, 'usuario': usuario}

    return render(request, 'mao/graficos/histograma_movilizacion.html', contexto)


def datos_histogramas_mao(request):

    if request.is_ajax():
        idEstudio = request.GET['estudio']
        numero_matriz = int(request.GET['numero_matriz'])
        tipo = request.GET['tipo']
        estudio = get_object_or_404(Estudio_Mactor, id=int(request.GET['estudio']))
        cant_objetivos = Objetivo.objects.filter(idEstudio=estudio.id).count()
        lista_nombres = []

        valores_mao = crear_contexto_mao(request, idEstudio, numero_matriz)
        valores_mao = valores_mao['valores_mao']
        valores_positivos = []
        valores_negativos = []

        if tipo == "IMPLICACION":
            labels = Actor.objects.filter(idEstudio=estudio.id).order_by('id')
            for i in valores_mao:
                if i.posicion == cant_objetivos+1:
                    valores_positivos.append(i.valor)
                elif i.posicion == cant_objetivos+2:
                    valores_negativos.append(i.valor)
        # si se trata de los valores de movilizacion
        else:
            labels = Objetivo.objects.filter(idEstudio=estudio.id).order_by('id')
            indice = 0
            for i in range(len(valores_mao)):
                if type(valores_mao[i].posicion) == int and valores_mao[i].posicion > cant_objetivos+4 and len(valores_positivos) < cant_objetivos:
                    valores_positivos.append(valores_mao[i].valor)
                if valores_mao[i].valor == "-":
                    indice += i

            contador = 0
            while contador < cant_objetivos:
                contador += 1
                valores_negativos.append(valores_mao[indice+contador].valor)

        for i in labels:
            lista_nombres.append(i.nombreCorto)

        data = {'labels': lista_nombres,
                'valores_positivos': valores_positivos,
                'valores_negativos': valores_negativos}

        json_data = json.dumps(data)
        return HttpResponse(json_data)


def histograma_caa_daa(request, idEstudio, numero_matriz):

    concenso = verificar_concenso(request, idEstudio)
    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    usuario = obtener_tipo_usuario(request, estudio.id)
    if concenso is True:
        num_expertos = valores_mao = crear_contexto_mao(request, idEstudio, int(numero_matriz))
        num_expertos = num_expertos['expertos']
        contexto = {'estudio': estudio, 'numero_matriz': int(numero_matriz),
                    'expertos': num_expertos, 'usuario': usuario}
    else:
        contexto = {'estudio': estudio, 'numero_matriz': int(numero_matriz), 'usuario': usuario}

    return render(request, 'mao/graficos/histograma_caa_daa.html', contexto)


def datos_histograma_caa_daa(request):

    if request.is_ajax():
        numero_matriz = int(request.GET['numero_matriz'])
        estudio = get_object_or_404(Estudio_Mactor, id=int(request.GET['estudio']))
        labels = Actor.objects.filter(idEstudio=estudio.id).order_by('id')
        lista_nombres = []

        valores_mao = crear_contexto_mao(request, request.GET['estudio'], numero_matriz)
        valores_caa = valores_mao['valores_caa']
        valores_daa = valores_mao['valores_daa']
        datos_caa = []
        datos_daa = []

        for i in range(len(valores_caa)):
            if valores_caa[i].posicion == "":
                datos_caa.append(valores_caa[i].valor)
                datos_daa.append(valores_daa[i].valor)

        for i in labels:
            lista_nombres.append(i.nombreCorto)

        data = {'labels': lista_nombres,
                'caa': datos_caa,
                'daa': datos_daa}

        json_data = json.dumps(data)
        return HttpResponse(json_data)


# ----------------------------------------PLANOS CARTESIANOS----------------------------------------------------->

def generar_mapa_midi(request, idEstudio):

    concenso = verificar_concenso(request, idEstudio)
    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    usuario = obtener_tipo_usuario(request, estudio.id)

    if concenso is True:
        influencias_mid = calcular_concenso_mid(estudio.id)
        cantidad_expertos = influencias_mid['num_expertos']
        contexto = {'estudio': estudio, 'usuario': usuario, 'expertos': cantidad_expertos}
    else:
        contexto = {'estudio': estudio, 'usuario': usuario}

    return render(request, 'influencia/graficos/mapa_actores.html', contexto)


def datos_mapa_midi(request):

    if request.is_ajax():
        valores_midi = calcular_midi(request, request.GET['estudio'])
        lista_nombres = []
        valores_ejeX = []
        valores_ejeY = []
        idEstudio = int(request.GET['estudio'])

        labels = Actor.objects.filter(idEstudio=idEstudio).order_by('id')

        for i in labels:
            lista_nombres.append(i.nombreCorto)

        for i in valores_midi:
            # Valores de influencia
            if i.posicion == labels.count()+1:
                valores_ejeX.append(i.valor)
            # Valores de dependencia
            if i.posicion == "" and len(valores_ejeY) < labels.count():
                valores_ejeY.append(i.valor)

        for i in range(len(valores_ejeX)):
            x = valores_ejeX[i]
            y = valores_ejeY[i]
            diferencia = x - y
            if abs(diferencia) > 2:
                if x > y:
                    valores_ejeY[i] = y * -1
                else:
                    valores_ejeX[i] = x * -1

        data = {'labels': lista_nombres,
                'valores_ejeX': valores_ejeX,
                'valores_ejeY': valores_ejeY}

        json_data = json.dumps(data)
        return HttpResponse(json_data)


def generar_mapa_caa_daa(request, idEstudio, numero_matriz):

    concenso = verificar_concenso(request, idEstudio)
    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    usuario = obtener_tipo_usuario(request, estudio.id)
    if concenso is True:
        influencias_mao = calcular_concenso_mao(request, estudio.id, int(numero_matriz))
        cantidad_expertos = influencias_mao['expertos']
        contexto = {'estudio': estudio, 'numero_matriz': int(numero_matriz),
                    'usuario': usuario, 'expertos': cantidad_expertos}
    else:
        contexto = {'estudio': estudio, 'numero_matriz': int(numero_matriz), 'usuario': usuario}

    return render(request, 'mao/graficos/mapa_caa_daa.html', contexto)


def datos_mapa_caa_daa(request):

    if request.is_ajax():
        numero_matriz = int(request.GET['numero_matriz'])
        lista_nombres = []

        valores_mao = crear_contexto_mao(request, request.GET['estudio'], numero_matriz)
        if valores_mao['estado_matriz'] == MATRIZ_COMPLETA:
            valores_caa = valores_mao['valores_caa']
            valores_daa = valores_mao['valores_daa']
        else:
            valores_caa = []
            valores_daa = []

        valores_ejeX = []
        valores_ejeY = []

        labels = Actor.objects.filter(idEstudio=int(request.GET['estudio'])).order_by('id')
        for i in valores_caa:
            if i.posicion == "":
                valores_ejeY.append(i.valor)

        for i in valores_daa:
            if i.posicion == "":
                valores_ejeX.append(i.valor)

        for i in labels:
            lista_nombres.append(i.nombreCorto)

        data = {'labels': lista_nombres,
                'valores_ejeX': valores_ejeX,
                'valores_ejeY': valores_ejeY}

        json_data = json.dumps(data)
        return HttpResponse(json_data)


# -------------------------------------------GRAFOS---------------------------------------------


def generar_grafo_caa(request, idEstudio, numero_matriz):

    concenso = verificar_concenso(request, idEstudio)
    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    usuario = obtener_tipo_usuario(request, estudio.id)
    if concenso is True:
        influencias_mao = calcular_concenso_mao(request, estudio.id, int(numero_matriz))
        cantidad_expertos = influencias_mao['expertos']
        contexto = {'estudio': estudio, 'numero_matriz': int(numero_matriz),
                    'usuario': usuario, 'expertos': cantidad_expertos}
    else:
        contexto = {'estudio': estudio, 'numero_matriz': int(numero_matriz), 'usuario': usuario}

    return render(request, 'mao/graficos/grafo_caa.html', contexto)


def datos_grafo_caa(request):

    if request.is_ajax():
        estudio = get_object_or_404(Estudio_Mactor, id=int(request.GET['estudio']))
        numero_matriz = int(request.GET['numero_matriz'])

        valores_mao = crear_contexto_mao(request, request.GET['estudio'], numero_matriz)
        valores_caa = valores_mao['valores_caa']
        actores = Actor.objects.filter(idEstudio=estudio.id).order_by('id')
        coordenadas = []
        nodos_id = []
        nodos_labels = []
        destinos_edge = []
        origenes_edge = []
        labels_edge = []

        # se eliminan de la matriz los nombres de fila y la fila se sumtoria de convergencias
        valores_caa = limpiar_matriz(valores_caa, actores)

        # se asigna a cada valor el eje x y y que le corresponde (actor x, actor y)
        contador = 0
        for i in actores:
            nodos_id.append(i.id)
            nodos_labels.append(i.nombreCorto)
            for j in actores:
                coordenadas.append(Valor_posicion(posicion=i,
                                                  valor=valores_caa[contador],
                                                  descripcion=j))
                contador += 1

        # eliminacion de los valores o en la diagonal
        contador = 0
        for i in range(len(coordenadas)):
            if i != contador:
                origenes_edge.append(coordenadas[i].posicion.id)
                destinos_edge.append(coordenadas[i].descripcion.id)
                labels_edge.append(str(coordenadas[i].valor))
            else:
                 contador += actores.count() + 1

        data = {'nodos_id': nodos_id,
                'nodos_labels': nodos_labels,
                'edge_origenes': origenes_edge,
                'edge_destinos': destinos_edge,
                'edge_labels': labels_edge}

        json_data = json.dumps(data)
        return HttpResponse(json_data)


def generar_grafo_daa(request, idEstudio, numero_matriz):

    concenso = verificar_concenso(request, idEstudio)
    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    usuario = obtener_tipo_usuario(request, estudio.id)
    if concenso is True:
        influencias_mao = calcular_concenso_mao(request, estudio.id, int(numero_matriz))
        cantidad_expertos = influencias_mao['expertos']
        contexto = {'estudio': estudio, 'numero_matriz': int(numero_matriz),
                    'usuario': usuario, 'expertos': cantidad_expertos}
    else:
        contexto = {'estudio': estudio, 'numero_matriz': int(numero_matriz), 'usuario': usuario}

    return render(request, 'mao/graficos/grafo_daa.html', contexto)


def datos_grafo_daa(request):

    if request.is_ajax():
        estudio = get_object_or_404(Estudio_Mactor, id=int(request.GET['estudio']))
        numero_matriz = int(request.GET['numero_matriz'])

        valores_mao = crear_contexto_mao(request, request.GET['estudio'], numero_matriz)
        valores_caa = valores_mao['valores_daa']
        actores = Actor.objects.filter(idEstudio=estudio.id).order_by('id')
        coordenadas = []
        nodos_id = []
        nodos_labels = []
        destinos_edge = []
        origenes_edge = []
        labels_edge = []

        # se eliminan de la matriz los nombres de fila y la fila se sumtoria de convergencias
        valores_caa = limpiar_matriz(valores_caa, actores)

        # se asigna a cada valor el eje x y y que le corresponde (actor x, actor y)
        contador = 0
        for i in actores:
            nodos_id.append(i.id)
            nodos_labels.append(i.nombreCorto)
            for j in actores:
                coordenadas.append(Valor_posicion(posicion=i,
                                                  valor=valores_caa[contador],
                                                  descripcion=j))
                contador += 1

        # eliminacion de los valores o en la diagonal
        contador = 0
        for i in range(len(coordenadas)):
            if i != contador:
                origenes_edge.append(coordenadas[i].posicion.id)
                destinos_edge.append(coordenadas[i].descripcion.id)
                labels_edge.append(str(coordenadas[i].valor))
            else:
                contador += actores.count() + 1

        data = {'nodos_id': nodos_id,
                'nodos_labels': nodos_labels,
                'edge_origenes': origenes_edge,
                'edge_destinos': destinos_edge,
                'edge_labels': labels_edge}

        json_data = json.dumps(data)
        return HttpResponse(json_data)


def limpiar_matriz(lista_valores, actores):

    lista_limpia = []
    contador = 0
    # eliminacion de los valores de la ultima fila
    while contador <= actores.count():
        lista_valores.pop()
        contador += 1

    # eliminacion  de las cabeceras de las filas (nombres en el eje y)
    for i in lista_valores:
        if type(i.valor) != str:
            lista_limpia.append(i.valor)

    return lista_limpia


# -------------------------------------------CONSENSO----------------------------------------------------------

# Verifica si el usuario desea visuaizar un concenso
def verificar_concenso(request, idEstudio):

    concenso = False
    tipo_usuario = obtener_tipo_usuario(request, int(idEstudio))
    if tipo_usuario == "COORDINADOR" or type(idEstudio) == str and idEstudio[0] == '0':
        concenso = True
    print(concenso)
    return concenso


def activar_concenso_influencias(request, idEstudio, tipo):

    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    idEstudio = "0"+str(estudio.id)
    tipo = int(tipo)

    if tipo == 1:
        return Generar_matriz_mid(request, idEstudio)
    elif tipo == 2:
        return Generar_matriz_midi(request, idEstudio)
    elif tipo == 3:
        return Generar_matriz_maxima(request, idEstudio)
    elif tipo == 4:
        return Generar_matriz_balance(request, idEstudio)
    elif tipo == 5:
        return Generar_matriz_ri(request, idEstudio)
    elif tipo == 6:
        return Generar_indicador_estabilidad(request, idEstudio)
    elif tipo == 7:
        return histograma_mid(request, idEstudio)
    elif tipo == 8:
        return generar_mapa_midi(request, idEstudio)
    elif tipo == 9:
        return histograma_ri(request, idEstudio)
    else:
        raise Http404("Error: Esta vista no existe")


# Calcula el concenso de la matriz mid
def calcular_concenso_mid(idEstudio):

    estudio = get_object_or_404(Estudio_Mactor, id=idEstudio)
    lista_expertos = estudio.idExpertos.all()
    actores = Actor.objects.filter(idEstudio=estudio.id).order_by('id')
    tamano_matriz_completa = len(actores)*len(actores)
    lista_concenso = []
    contador = 0

    for experto in lista_expertos:
        consulta = Relacion_MID.objects.filter(idActorY__idEstudio=estudio.id,
                                                        idExperto=experto.id).order_by('idActorY', 'idActorX')
        if len(consulta) == tamano_matriz_completa and len(lista_concenso) == 0:
            lista_concenso = consulta
            contador += 1
        elif len(consulta) == tamano_matriz_completa:
            contador += 1
            for i in range(len(lista_concenso)):
                lista_concenso[i].valor += consulta[i].valor

    if len(lista_concenso) > 0:
        for i in lista_concenso:
            i.valor = round(i.valor / contador)

    cantidad = str(contador) + "/" + str(len(lista_expertos))
    calculo = {'concenso': lista_concenso, 'num_expertos': cantidad}

    return calculo


# Agrega un cero al inicio del idEstudio para activar el concenso mao
def activar_concenso_mao(request, idEstudio, matriz, tipo):

    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    idEstudio = "0"+str(estudio.id)
    matriz = int(matriz)
    tipo = int(tipo)

    if matriz in [1, 2, 3] and tipo == 0:
        return Generar_matriz_mao(request, idEstudio, matriz)
    elif tipo == 4:
        return histograma_implicacion(request, idEstudio, str(matriz))
    elif tipo == 5:
        return histograma_movilizacion(request, idEstudio, str(matriz))
    else:
        raise Http404("Error: Esta vista no existe")


# Agrega un cero al inicio del idEstudio para activar el concenso de matrices de convergencia y divergencia
def activar_concenso_caa_daa(request, idEstudio, matriz, tipo):

    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    idEstudio = "0" + str(estudio.id)
    tipo = int(tipo)
    matriz = int(matriz)

    if tipo == 1:
        return Generar_matrices_caa_daa(request, idEstudio, matriz)
    elif tipo == 2:
        return generar_mapa_caa_daa(request, idEstudio, matriz)
    elif tipo == 3:
        return histograma_caa_daa(request, idEstudio, matriz)
    elif tipo == 4:
        return generar_grafo_caa(request, idEstudio, matriz)
    elif tipo == 5:
        return generar_grafo_daa(request, idEstudio, matriz)
    else:
        raise Http404("Error: Esta vista no existe")


# Calcula el concenso de las matrices 1mao y 2mao
def calcular_concenso_mao(request, idEstudio, num_matriz):

    estudio = get_object_or_404(Estudio_Mactor, id=idEstudio)
    lista_expertos = estudio.idExpertos.all()
    actores = Actor.objects.filter(idEstudio=estudio.id).order_by('id')
    objetivos = Objetivo.objects.filter(idEstudio=estudio.id).order_by('id')
    tamano_matriz_completa = len(actores)*len(objetivos)
    contador = 0
    lista_sublistas = []

    cont1 = 0
    while cont1 < tamano_matriz_completa:
        lista_sublistas.append([])
        cont1 += 1

    consulta_base = []
    if num_matriz < 3:
        for experto in lista_expertos:
            consulta = Relacion_MAO.objects.filter(idEstudio=estudio.id, idExperto=experto.id,
                                                                tipo=num_matriz).order_by('idActorY', 'idObjetivoX')

            if len(consulta) == tamano_matriz_completa and len(consulta) > 0:
                consulta_base = consulta
                contador += 1
                for i in range(len(consulta)):
                    sublista = lista_sublistas[i]
                    sublista.append(consulta[i].valor)
                    lista_sublistas[i] = sublista
    else:
        idEstudio = "0" + str(estudio.id)
        consulta_base = calcular_valores_3mao(request, idEstudio)

    if num_matriz == 1 and len(consulta_base) > 0:
        for i in range(len(lista_sublistas)):
            cont_uno_pos = lista_sublistas[i].count(1)
            cont_cero = lista_sublistas[i].count(0)
            cont_uno_neg = lista_sublistas[i].count(-1)

            if cont_uno_pos > max(cont_cero, cont_uno_neg):
                consulta_base[i].valor = 1
            elif cont_cero >= cont_uno_pos and cont_cero > cont_uno_neg:
                consulta_base[i].valor = 0
            elif cont_uno_neg >= max(cont_uno_pos, cont_cero):
                consulta_base[i].valor = -1

    elif num_matriz == 2 and len(consulta_base) > 0:
        for i in range(len(lista_sublistas)):
            cont_4 = lista_sublistas[i].count(-4)
            cont_3 = lista_sublistas[i].count(-3)
            cont_2 = lista_sublistas[i].count(-2)
            cont_1 = lista_sublistas[i].count(-1)
            cont0 = lista_sublistas[i].count(0)
            cont1 = lista_sublistas[i].count(1)
            cont2 = lista_sublistas[i].count(2)
            cont3 = lista_sublistas[i].count(3)
            cont4 = lista_sublistas[i].count(4)

            if cont_4 >= max(cont_3, cont_2, cont_1, cont0, cont1, cont2, cont3, cont4):
                consulta_base[i].valor = -4
            elif cont_3 >= max(cont_2, cont_1, cont0, cont1, cont2, cont3, cont4):
                consulta_base[i].valor = -3
            elif cont_2 >= max(cont_1, cont0, cont1, cont2, cont3, cont4):
                consulta_base[i].valor = -2
            elif cont_1 >= max(cont0, cont1, cont2, cont3, cont4):
                consulta_base[i].valor = -1
            elif cont0 >= max(cont1, cont2, cont3, cont4):
                consulta_base[i].valor = 0
            elif cont1 >= max(cont2, cont3, cont4):
                consulta_base[i].valor = 1
            elif cont2 >= max(cont3, cont4):
                consulta_base[i].valor = 2
            elif cont3 >= cont4:
                consulta_base[i].valor = 3
            else:
                consulta_base[i].valor = 4

    cantidad = str(contador) + "/" + str(len(lista_expertos))
    resultado = {'concenso': consulta_base, 'expertos': cantidad}

    return resultado


# VIEW MODELO INFORME FINAL

def Crear_informe(request, idEstudio):

    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    tipo_usuario = obtener_tipo_usuario(request, estudio.id)
    informes = Informe_Final.objects.filter(idCoordinador=request.user.id).order_by('id')

    flag = False
    for i in informes:
        if i.idEstudio.id == estudio.id and flag is False:
            flag = True

    print(flag)
    if flag is False:
        # si se va a guardar primera vez
        if request.method == 'POST':
            form = Form_Informe(request.POST)
            if form.is_valid():
                form.save()
            return redirect('mactor:lista_actores', estudio.id)
        else:
            form = Form_Informe()
        return render(request, 'informe/crear_informe.html', {'form': form, 'estudio': estudio, 'usuario': tipo_usuario,
                                                              })
    else:
        return Editar_informe(request, idEstudio)


def Editar_informe(request, idEstudio):

    estudio = get_object_or_404(Estudio_Mactor, id=int(idEstudio))
    tipo_usuario = obtener_tipo_usuario(request, estudio.id)
    informe_estudio = Informe_Final.objects.get(idEstudio=estudio.id)
    if request.method == 'GET':
        form = Form_Informe(instance=informe_estudio)
    else:
        form = Form_Informe(request.POST, instance=informe_estudio)
        if form.is_valid():
            form.save()
            return redirect('mactor:lista_actores', estudio.id)
    return render(request, 'informe/crear_informe.html', {'form': form,
                                                        'estudio': estudio,
                                                        'usuario': tipo_usuario,
                                                        'datos': informe_estudio,
                                                            })






































