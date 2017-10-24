from django.contrib.auth.models import User
from django.core import serializers
import json
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse, HttpResponse, request
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Estudio_Mactor, Actor, Ficha_actor, Objetivo, Relacion_MID, Relacion_MAO
from .forms import Form_Estudio, Form_Actor, Form_Ficha, Form_Objetivo, Form_MID, Form_1mao, Form_2mao


# ----------------------------------------VIEWS MODELO ESTUDIO MACTOR--------------------------------->

class Listar_estudio(ListView):
    model = Estudio_Mactor
    template_name = 'estudio/lista_estudios.html'


def Consultar_estudio(request):

    if request.is_ajax():
        id = request.GET['id']
        if id.count("est"):
            id = id.lstrip("est")
        elif id.count("id"):
            id = id.lstrip("id")
        estudio = Estudio_Mactor.objects.get(id=id)
        response = JsonResponse(
            {'titulo': estudio.titulo, 'descripcion': estudio.descripcion})
        return HttpResponse(response.content)
    else:
        return redirect('/')


class Editar_estudio(UpdateView):
    model = Estudio_Mactor
    form_class = Form_Estudio
    template_name = 'estudio/update_estudio.html'
    success_url = reverse_lazy('mactor:lista_estudios')


# -------------------------------------------VIEWS MODELO ACTOR--------------------------------------->

def Crear_actor(request):

   nombreLargo = request.GET['nombreLargo']
   nombreCorto = request.GET['nombreCorto']
   descripcion = request.GET['descripcion']
   #idEstudio = 1
   mensaje = "El actor " + nombreLargo + " se ha registrado con exito"
   lista_actor = Actor.objects.all()
   flag = False

   for i in lista_actor:
       if i.nombreCorto == nombreCorto:
           flag = True

   if flag is False:
        try:
            actor = Actor(nombreLargo=nombreLargo, nombreCorto=nombreCorto, descripcion=descripcion)
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


class Listar_actor(ListView):
    model = Actor
    template_name = 'actor/lista_actores.html'
    ordering = ('nombreLargo',)


def Editar_actor(request):

    if request.is_ajax():
        # se obtienen los datos modificados
        id = request.GET.get('id')
        nombreLargo = request.GET.get('nombreLargo')
        nombreCorto = request.GET.get('nombreCorto')
        descripcion = request.GET.get('descripcion')
        # idEstudio = 1

        # se elimina del id obtenido la subcadena "id"
        if id.count("act"):
            id = id.lstrip("act")

        # se obtiene el registro del actor a modificar
        lista_actor = Actor.objects.all().exclude(id=id)
        flag = False

        # se verifica que el nombre corto modificado no coincida con el de otros actores
        for i in lista_actor:
            if i.nombreCorto == nombreCorto:
                flag = True

        # se realiza la modificacion de los datos y se envia la respuesta
        if flag == False:
            try:
                actor = Actor.objects.get(id=id)
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

        if id.count("act"):         # verifica si la cadena contiene la subcadena especificada
            id = id.lstrip("act")   # elimina la subcadena especificada

        actor = Actor.objects.get(id=id)

        response = JsonResponse(
            {'nombreCorto': actor.nombreCorto,
             'nombreLargo': actor.nombreLargo,
             'descripcion': actor.descripcion})
        return HttpResponse(response.content)
    else:
        return redirect('/')        # redirecciona a la misma pagina


def Eliminar_actor_ajax(request):

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

class Crear_ficha(CreateView):
    model = Ficha_actor
    form_class = Form_Ficha
    template_name = 'ficha/crear_ficha.html'
    success_url = reverse_lazy('mactor:ficha')


class Listar_ficha(ListView):
    model = Ficha_actor
    template_name = 'ficha/lista_fichas.html'
    ordering = ('idActorY', 'idActorX',)


class Editar_ficha(UpdateView):
    model = Ficha_actor
    form_class = Form_Ficha
    template_name = 'ficha/crear_ficha.html'
    success_url = reverse_lazy('mactor:lista_fichas')


def Consultar_ficha(request):

    if request.is_ajax():
        # se verifica que ninguno de los parametros recibidos sea una cadena vacia
        if request.GET['id'] == "" or request.GET['id2'] == "":
            response = JsonResponse({'info': "Seleccione el par de actores a consultar"})
            return HttpResponse(response.content)
        else:
            # si los parametros son validos se busca la ficha de estrategias correspondiente
            ficha = Ficha_actor.objects.get(idActorX=request.GET['id'], idActorY=request.GET['id2'])
            response = JsonResponse({'info': ficha.estrategia})
            return HttpResponse(response.content)
    else:
        return redirect('/')


def Eliminar_ficha_ajax(request):

    if request.is_ajax():
        ficha = Ficha_actor.objects.get(id=request.GET['id'])
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

# ------------------------------------------VIEWS MODELO OBJETIVO------------------------------------>

def Crear_objetivo(request):

    nombreLargo = request.GET['nombreLargo']
    nombreCorto = request.GET['nombreCorto']
    descripcion = request.GET['descripcion']
    #idEstudio = request.GET['idEstudio']
    mensaje = "El objetivo " + nombreLargo + " se ha registrado con exito"
    lista_objetivo = Objetivo.objects.all()
    flag = False

    for i in lista_objetivo:
        if i.nombreCorto == nombreCorto:
            flag = True

    if flag is False:
        try:
            objetivo = Objetivo(nombreLargo=nombreLargo, nombreCorto=nombreCorto, descripcion=descripcion)
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


class Listar_objetivo(ListView):
    model = Objetivo
    template_name = 'objetivo/lista_objetivos.html'


def Editar_objetivo(request):

    if request.is_ajax():
        # se obtienen los datos modificados
        id = request.GET.get('id')
        nombreLargo = request.GET['nombreLargo']
        nombreCorto = request.GET['nombreCorto']
        descripcion = request.GET['descripcion']
        # idEstudio = 1

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
        if flag == False:
            try:
                objetivo = Objetivo.objects.get(id=id)
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
        id = request.GET['id']
        # se verifica si la cadena contiene la subcadena especificada
        if id.count("obj"):
            id = id.lstrip("obj")
        objetivo = Objetivo.objects.get(id=id)
        response = JsonResponse(
            {'nombreCorto': objetivo.nombreCorto,
             'nombreLargo': objetivo.nombreLargo,
             'descripcion': objetivo.descripcion})
        return HttpResponse(response.content)
    else:
        return redirect('/')


def Eliminar_objetivo_ajax(request):

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


class Crear_relacionInfluencia(CreateView):
    model = Relacion_MID
    form_class = Form_MID
    template_name = 'influencia/create_influencia.html'
    success_url = reverse_lazy('mactor:influencia')


# View generadora de la matriz MID
def Matriz_mid(request):

    actor = Actor.objects.all().order_by('id')
    inf = Relacion_MID.objects.all().order_by('idActorY', 'idActorX')
    valores = []    # contiene los valores que se muestran en la matriz
    cont = 0        # cuenta las influencias
    pos_list = 0    # determina el nombre corto que se ha de colocar en valores
    influencia = 0
    dependencia = 0

    for i in range(len(inf)):
        cont += 1
        # se ingresan los valores mid, asignando una posicion a cada valor para facilitar su impresion
        valores.append(Valor_posicion(posicion=cont, valor=inf[i].valor))
        # se suman los valores de influencia directa
        influencia += inf[i].valor
        # cuando la cantidad de valores ingresado alcanza la cantidad de actores se agrega el valor de influencia
        if cont == actor.count():
            valores.append(Valor_posicion(posicion=cont + 1, valor=influencia))
            # determina la posicion donde se va a colocar el nombre corto de la nueva fila
            cont2 = (actor.count() + 2) * pos_list
            # inserta el nombre corto de la nueva fila
            valores.insert(cont2, Valor_posicion(posicion=0, valor=actor[pos_list].nombreCorto))
            cont = 0
            pos_list += 1
            influencia = 0  # reinicio del valor de influencia

    # Agregado de la sumatoria de dependencias directas
    valores.append(Valor_posicion(posicion=0, valor="Dep. D"))
    cont = 1
    while cont <= actor.count():
        for i in valores:
            if i.posicion == cont:
                dependencia += i.valor
        valores.append(Valor_posicion(posicion=cont, valor=dependencia))
        cont += 1           # iteracion de las posiciones
        dependencia = 0     # reinicio a o del valor movilizacion

    midi = calcular_midi()  # obtencion de la matriz midi


    contexto = {'actores': actor, 'cantidad_mid': actor.count() + 1, 'cantidad_midi': actor.count() + 1,
                'valores': valores, 'valores_midi': midi}
    return render(request, 'influencia/matriz_mid.html', contexto)


# VIEWS MODELO RELACION_MAO---------------------------------------------------------------------------------->


class Crear_1mao(CreateView):
    model = Relacion_MAO
    form_class = Form_1mao
    template_name = 'mao/create_1mao.html'
    success_url = reverse_lazy('mactor:1mao')


def Generar_matriz_1mao(request):

    objetivos = Objetivo.objects.all().order_by('id')                               # objetivos registrados
    actores = Actor.objects.all().order_by('id')                                    # actores registrados
    mao = Relacion_MAO.objects.exclude(tipo=2).order_by('idActorY', 'idObjetivoX')  # relaciones mao registradas
    lista = generar_matriz_mao(objetivos=objetivos, actores=actores, mao=mao)       # lista con parametros del contexto

    contexto = {'objetivos': objetivos,
                'actores': actores,
                'valores': lista[0],                  # valores de la matriz
                'cantidad': objetivos.count() + 3,    # cantidad de columnas para saber cuando hacer el salto de fila
                                                      # +3 debido a la columna de nombrecorto y las 3 de implicacion
                'cantidad2': (objetivos.count()*2)+4, # cantidad de columnas para las sumatorias de movilizacion
                                                      # x2 y +4  ya que no tienen las mismas posiciones que anteriores
                'valores_caa': lista[1],              # valores de la  matriz de convergencia
                'cantidad3': actores.count(),         # cantidad de columnas para las matrices de conv y divergencia
                'valores_daa': lista[2]}              # valores de la matriz de divergencia

    return render(request, 'mao/matriz_1mao.html', contexto)


class Crear_2mao(CreateView):
    model = Relacion_MAO
    form_class = Form_2mao
    template_name = 'mao/create_2mao.html'
    success_url = reverse_lazy('mactor:2mao')


def Generar_matriz_2mao(request):

    objetivos = Objetivo.objects.all().order_by('id')                               # objetivos registrados
    actores = Actor.objects.all().order_by('id')                                    # actores registrados
    mao = Relacion_MAO.objects.exclude(tipo=1).order_by('idActorY', 'idObjetivoX')  # relaciones mao registradas
    lista = generar_matriz_mao(objetivos=objetivos, actores=actores, mao=mao)       # lista con parametros del contexto
    usuario = request.user.id
    id_user = User.objects.get(id=usuario)
    print(id_user.id)

    contexto = {'objetivos': objetivos,
                'actores': actores,
                'valores': lista[0],                  # valores de la matriz
                'cantidad': objetivos.count() + 3,    # cantidad de columnas para saber cuando hacer el salto de fila
                                                      # +3 debido a la columna de nombrecorto y las 3 de implicacion
                'cantidad2': (objetivos.count()*2)+4, # cantidad de columnas para las sumatorias de movilizacion
                                                      # x2 y +4  porque no tienen las mismas posiciones que los previos
                'valores_caa': lista[1],              # valores de la  matriz de convergencia
                'cantidad3': actores.count(),         # cantidad de columnas para las matrices de conv y divergencia
                'valores_daa': lista[2]}              # valores de la matriz de divergencia

    return render(request, 'mao/matriz_2mao.html', contexto)

# -------------------------------------CLASES AUXILIARES--------------------------------------------------------------->


# Clase auxiliar para la generacion de matrices, se asigna una posicion a un respectivo valor
class Valor_posicion:
    def __init__(self, posicion, valor):
        self.posicion = posicion
        self.valor = valor


# Ingresa las influencias con valor 0 de un actor sobre si mismo, necesario para que la matriz sea cuadrada
def auto_influencia():
    actor = Actor.objects.all().order_by('id')
    inf = Relacion_MID.objects.all().order_by('id')
    flag = False

    # se verifica si existen estas influencias ya existen
    for i in inf:
        if i.idActorX == i.idActorY:
            flag = True
    # sino existen estas influencias, se agregan a la bd, ya que se necesitan los atributos
    if flag == False:
        for j in range(len(actor)):
            a = Relacion_MID()
            a.idActorY = actor[j]
            a.idActorX = actor[j]
            a.valor = 0
            a.justificacion = "auto_inf"
            a.idExperto = inf[0].idExperto
            a.idEstudio = inf[0].idEstudio
            a.save()

    inf = Relacion_MID.objects.all().order_by('idActorY', 'idActorX')
    return inf

# -------------------------------------FUNCIONES AUXILIARES------------------------------------------------------------>

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Funciones influencias entre actores>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# Generacion de la matriz MIDIij = MID ij + Sum(Minimo [(MID ik, MID ik])
def calcular_midi():

    actor = Actor.objects.all().order_by('id')
    inf = auto_influencia()
    lista_minimo = []   # contiene las sublistas de valores minimos por cada actor Y
    lista_total = []    # contiene lista_minimo concatenado
    valores_midi = []   # contiene los valores correspondientes a MIDI

    # se agrega la sublista de valores minimos correspondiente al actorY a lista_minimo
    for i in range(len(inf)):
        if inf[i].idActorY == inf[i].idActorX:
            # cada valor de pos permite el calculo de una fila de la matriz
            lista_minimo.append(calcular_minimo(pos=i, mid=auto_influencia()))

    # concatenacion de lista_minimo para facilitar la suma con las influencias correspondientes (igual longitud)
    for i in lista_minimo:
        lista_total += i

    cont = 0
    pos_list = 0
    li = 0
    # se realiza la suma MID ij + Sum(Minimo [(MID ik, MID ik])
    for i in range(len(inf)):
        cont += 1
        valores_midi.append(Valor_posicion(posicion=cont, valor=inf[i].valor + lista_total[i]))
        # se calcula el valor li, donde no se incluye la influencia sobre si mismo
        if inf[i].idActorY != inf[i].idActorX and cont <= actor.count():
            li += inf[i].valor + lista_total[i]
        # se determina la posicion donde se va a colocar el nombre corto de la nueva fila
        if cont == actor.count():
            # se suma a la cantidad de actores 2 debido a la columna del nombreCorto y li
            cont2 = (actor.count() + 2) * pos_list
            # se inserta el nombre corto de la nueva fila
            valores_midi.insert(cont2, Valor_posicion(posicion=0, valor=actor[pos_list].nombreCorto))
            # se determina la posición de la columna li
            cont3 = cont2 + actor.count() + 1
            # inserta el valor li en la lista de valores midi de acuerdo a la posicion establecida
            valores_midi.insert(cont3, Valor_posicion(posicion=actor.count() + 1, valor=li))
            # se reinician los parametros paera recalcular
            cont = 0
            pos_list += 1
            li = 0

    # se calculan los valores di (ultima fila)
    valores_midi.append(Valor_posicion(posicion=0, valor="Di"))
    cont = 1
    di = 0
    suma_di = 0
    while cont <= actor.count():
        for i in valores_midi:
            if i.posicion == cont:
                di += i.valor
        # se obtiene el valor de influecia sobre si mismo para restarlo a di
        cont2 = valores_midi[((actor.count() + 2) * (cont - 1)) + cont].valor
        di = di - cont2
        # se inserta el valor di a la lista de valores midi
        valores_midi.append(Valor_posicion(posicion="", valor=di))
        suma_di += di     # sumatoria de los valores di
        cont += 1         # iteracion de las posiciones
        di = 0            # reinicio a 0 del valor di
    # se inserta la sumatoria total di donde di_total = li_total, ultima celda
    valores_midi.append(Valor_posicion(posicion="", valor=suma_di))

    return valores_midi


# Realiza la parte derecha de la formula: Sum(Minimo [(MID ik, MID ik])
def calcular_minimo(pos, mid):
    actor = Actor.objects.all().order_by('id')
    izquierdo = []       # contiene los valores izquierdos a comparar
    derecho = []         # contiene los valores derechos a comparar
    comparacion = []     # contiene los valores minimos establecidos al comparar izquierdo vs derecho
    lista_suma = []      # contiene la suma de los valores minimos establecidos al comparar

    # valores del lado derecho del minimo: influencias de los actores influenciados por Y sobre X excepto Y
    cont = 1
    aux = 0
    for i in range(len(mid)):
        lista_suma.append(0)
        # se verifica si en el registro actual (i), el campo idActorY no corresponde al recibido como parametro (pos)
        if mid[i].idActorY != mid[pos].idActorY:
            # de cumplirse la condicion se guarda el valor, asigandolo a una posición para facilitar la comparacion
            derecho.append(Valor_posicion(posicion=cont, valor=mid[i].valor))
            aux += 1
            if aux == actor.count():
                cont += 1
                aux = 0

    cont = 0
    # valores del lado izquierdo del minimo: influencias del actor Y sobre los demas
    for i in range(len(mid)):
        # se guardan las influencias del actorY recibido (pos) sobre los demas actores, excepto la de el mismo
        if mid[pos].idActorY != mid[i].idActorX and mid[i].idActorY == mid[pos].idActorY and len(izquierdo) < actor.count() - 1:
            izquierdo.append(Valor_posicion(posicion=cont + 1, valor=mid[i].valor))
            cont += 1

    cont = 0
    # se realiza la comparacion entre los elementos de derecho e izquierdo para determinar el valor minimo
    for i in range(len(derecho)):
        if izquierdo[cont].posicion == derecho[i].posicion and cont < actor.count():
            # si el valor izquierdo es menor al derecho
            if izquierdo[cont].valor <= derecho[i].valor:
                comparacion.append(izquierdo[cont].valor)
            else:
                comparacion.append(derecho[i].valor)
        else:
            cont += 1
            if izquierdo[cont].posicion == derecho[i].posicion:
                if izquierdo[cont].valor <= derecho[i].valor:
                    comparacion.append(izquierdo[cont].valor)
                else:
                    comparacion.append(derecho[i].valor)

    ini = 0              # indica el punto inicial de la sublista
    fin = actor.count()  # indica el punto final de la sublista

    # la lista comparacion es divida y sumada
    for i in range(fin):
        if i < actor.count() - 1:
            # se suman los valores minimos
            lista_suma = map(sum, zip(lista_suma, comparacion[ini:fin]))
            ini = fin                  # se actualiza el punto de inicio
            fin = fin + actor.count()  # se actualiza el punto final

    return lista_suma

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<Funciones matrices mao>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# Generacion de matriz de convergencias o divergencias
def generar_caa_daa(lista, actores, cant_objetivos, tipo):
    valores_mao = []
    cont = 1
    cont2 = 0

    # filtrado del contenido de la matriz 2mao (solo lo valores de relacion actor x objetivo)
    # al conjunto de valores de una fila se le asigna el una misma posicion para facilitar
    # los filtros y la posterior comparacion
    for i in lista:
        if i.posicion > 0 and i.posicion <= cant_objetivos:
            valores_mao.append(Valor_posicion(posicion=cont, valor=i.valor))
            cont2 += 1
            if cont2 == cant_objetivos:
                cont += 1
                cont2 = 0

    # Devuelve una lista con los valores que poseen la posicion pasada como parametro
    def filtrar_posicion(pos):
        sublista_aux = []
        for i in valores_mao:
            if i.posicion == pos:
                sublista_aux.append(i.valor)

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
        for i in valores_mao:
            if i.posicion != pos:
                sublista_aux.append(i.valor)
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
        valores_posicion.append(Valor_posicion(posicion=cont, valor=i))
        if cont == actores.count():
            cont = 0
        else:
            cont += 1

    if tipo == 1:
        valores_posicion.append(Valor_posicion(posicion=0, valor="Ci"))
    else:
        valores_posicion.append(Valor_posicion(posicion=0, valor="Di"))

    # Calculo del numero de convergencias o divergencias totales de cada actor
    cont = 1
    suma = 0
    while cont <= actores.count():
        for i in valores_posicion:
            if i.posicion == cont:
                suma += i.valor
        valores_posicion.append(
            Valor_posicion(posicion="", valor="{0:.1f}".format(suma)))  # posicion = "" para que no agregue el salto al final
        cont += 1
        suma = 0

    return valores_posicion


# Agrega a la lista de valores mao, los valores de movilizacion (ultimas 3 filas) correspondientes
def generar_lista_movilizacion(objetivos, valores):
    lista_positivos = []
    lista_negativos = []
    lista_movilizacion = []
    movilizacion = 0
    suma_positivos = 0
    suma_negativos = 0
    cont2 = objetivos.count() + 4  # +4 debido a las cuatro columnas extras en la matriz (nombres cortos y sumatorias)
    cont = 1

    # Determinacion de sumatorias de movilizacion (ultima fila) suma de columnas
    while cont <= objetivos.count():
        for i in valores:
            if i.posicion == cont:
                movilizacion += abs(i.valor)
                if i.valor == abs(i.valor):
                    # si el valor es positivo
                    suma_positivos += i.valor
                else:
                    # si el valor es negativo
                    suma_negativos += abs(i.valor)
        # se agregan a la lista los valores de movilizacion
        lista_negativos.append(Valor_posicion(posicion=0, valor=suma_negativos))
        lista_positivos.append(Valor_posicion(posicion=0, valor=suma_positivos))
        lista_movilizacion.append(Valor_posicion(posicion=0, valor=movilizacion))
        cont += 1           # iteracion de las posiciones
        movilizacion = 0    # reinicio del valor movilizacion
        suma_positivos = 0  # reinicio de la suma positiva
        suma_negativos = 0  # reinicio de la suma negativa

    # agregado de las sumatorias de movilizacion positiva a la lista de valores
    valores.append(Valor_posicion(posicion=0, valor="+"))
    for i in range(len(lista_positivos)):
        valores.append(Valor_posicion(posicion=cont2 + i + 1, valor=lista_positivos[i].valor))
    # agregado de las sumatorias de movilizacion negativa a la lista de valores
    valores.append(Valor_posicion(posicion=0, valor="-"))
    for i in range(len(lista_negativos)):
        valores.append(Valor_posicion(posicion=cont2 + i + 1, valor=lista_negativos[i].valor))
    # agregado de las sumatorias de movilizacion total a la lista de valores
    valores.append(Valor_posicion(posicion=0, valor="Mov."))
    for i in range(len(lista_movilizacion)):
        valores.append(Valor_posicion(posicion="", valor=lista_movilizacion[i].valor))

    return valores


# View generadora de las matrices mao
def generar_matriz_mao(objetivos, actores, mao):

    valores = []        # valores mostrados en la matriz
    cont = 0            # cuenta las influencias
    pos_list = 0        # auxiliar para el calculo de cont2
    implicacion = 0     # sumatoria absoluta del lado derecho de la matriz
    suma_positivos = 0  # sumatoria de los valores positivos de implicacion
    suma_negativos = 0  # sumatoria de los valores negativos de implicacion

    # se agregan las relaciones mao a la lista de valores que sera enviada como contexto
    for i in range(len(mao)):
        cont += 1
        # se agregan las relaciones mao registradas asignandoles una posicion para facilitar su impresion
        valores.append(Valor_posicion(posicion=cont, valor=mao[i].valor))
        # se calcula la sumatoria del valor de implicacion (ultima columna) sum de filas
        implicacion += abs(mao[i].valor)
        # se determinan las implicaciones positivas y negativas (columnas + y -)
        if mao[i].valor == abs(mao[i].valor):
            # si el valor es positivo
            suma_positivos += mao[i].valor
        else:
            # si el valor es negativo
            suma_negativos += abs(mao[i].valor)
            # cuando el numero de registros alcanza la cantidad de objetivos se tiene una fila de la matriz
            # se agregan entonces las sumatorias de implicacion (ultimas 3 columnas)
        if cont == objetivos.count():
            valores.append(Valor_posicion(posicion=cont + 1, valor=suma_positivos))
            valores.append(Valor_posicion(posicion=cont + 2, valor=suma_negativos))
            valores.append(Valor_posicion(posicion=cont + 3, valor=implicacion))
            # agregada la fila se determina la posicion donde se va a colocar el nombre corto de fila (primera columna)
            cont2 = (objetivos.count() + 4) * pos_list
            valores.insert(cont2, Valor_posicion(posicion=0, valor=actores[pos_list].nombreCorto))
            # se reinician los valores para crear la nueva fila
            cont = 0
            pos_list += 1
            implicacion = 0
            suma_positivos = 0
            suma_negativos = 0

    # ---------------------Determinacion de convergencias-------------------->
    valores_caa = generar_caa_daa(valores, actores, objetivos.count(), 1)
    # ---------------------Determinacion de divergencias--------------------->
    valores_daa = generar_caa_daa(valores, actores, objetivos.count(), 2)
    # ---------------------Valores de movilizacion  ------------------------->
    valores_mao = generar_lista_movilizacion(objetivos, valores)

    lista = []
    lista.append(valores_mao)             # valores:     valores de la matriz mao
    lista.append(valores_caa)             # valores_caa: valores de la matriz de convergencias
    lista.append(valores_daa)             # valores_daa: valores de la matriz de divergencias

    return lista


# Calculo del valor ri para la matriz 3mao
def calcular_ri(valores_midi, cant_actor):

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


# Calculo de los valores 3mao = 2mao * ri
def calcular_3mao(cant_objetivos, cant_actores):

    mao = Relacion_MAO.objects.exclude(tipo=1).order_by('idActorY', 'idObjetivoX')  # relaciones 2mao registradas
    valores_midi = calcular_midi()                                                  # relaciones midi calculadas
    valores_ri = calcular_ri(valores_midi, cant_actores)                            # valores ri a partir de los midi
    valores_3mao = []                                                               # lista que contiene a los 3mao

    # Multiplicacion de los valores 2mao por los valores ri para hallar los valores 3mao
    cont = 0
    cont2 = 0
    for i in mao:
        if cont2 < cant_objetivos:
            valor = i.valor * valores_ri[cont]
            # se agrega el valor calculado a la lista a mostrar
            valores_3mao.append(Valor_posicion(posicion=cont2+1, valor=round(valor, 1)))
            cont2 += 1
        # cuando se han calculado los valores (cantidad de objetivos) de una fila se reinician los parámetros
        else:
            cont2 = 0
            cont += 1
            valor = i.valor * valores_ri[cont]
            # se agrega el valor calculado a la lista a mostrar
            valores_3mao.append(Valor_posicion(posicion=cont2 + 1, valor=round(valor, 1)))
            cont2 += 1

    return valores_3mao


# View generadora de la matriz 3mao
def Generar_matriz_3mao(request):

        objetivo = Objetivo.objects.all().order_by('id')     # objetivos registrados
        actor = Actor.objects.all().order_by('id')           # actores registrados
        mao = calcular_3mao(cant_objetivos=objetivo.count(), cant_actores=actor.count())
        valores = []                                         # contiene los valores que se muestran en la matriz
        cont = 0                                             # cuenta las influencias
        pos_list = 0                                         # auxiliar para el calculo de cont2
        suma_positivos = 0                                   # sumatoria de los valores positivos de implicacion
        suma_negativos = 0                                   # sumatoria de los valores negativos de implicacion

        # agregado de las relaciones mao a la lista de valores que sera enviada como contexto
        for i in range(len(mao)):
            cont += 1
            valores.append(Valor_posicion(posicion=cont, valor=mao[i].valor))
            # se determinan las implicaciones positivas y negativas
            if mao[i].valor == abs(mao[i].valor):
                suma_positivos += mao[i].valor
            else:
                suma_negativos += abs(mao[i].valor)
                # al agregar los valores correspondientes a una fila se agrega el nombre corto de la siguiente
            if cont == objetivo.count():
                valores.append(Valor_posicion(posicion=cont + 1, valor=round(suma_positivos, 1)))
                valores.append(Valor_posicion(posicion=cont + 2, valor=round(suma_negativos, 1)))
                valores.append(Valor_posicion(posicion=cont + 3, valor=round(suma_positivos + suma_negativos, 1))) #implicacion
                # determina la posicion donde se va a colocar el nombre corto de la nueva fila
                cont2 = (objetivo.count() + 4) * pos_list
                # inserta el nombre corto de la nueva fila
                valores.insert(cont2, Valor_posicion(posicion=0, valor=actor[pos_list].nombreCorto))
                # reinicio de valores para iterar
                cont = 0
                pos_list += 1
                suma_positivos = 0
                suma_negativos = 0

        # ---------------------Determinacion de convergencias-------------------->
        valores_caa = generar_caa_daa(valores, actor, objetivo.count(), 1)
        # ---------------------Determinacion de divergencias--------------------->
        valores_daa = generar_caa_daa(valores, actor, objetivo.count(), 2)
        # ---------------------Calculo de los Valores de movilizacion  ---------->
        valores_mao = generar_lista_movilizacion(objetivo, valores)

        contexto = {'objetivos': objetivo,
                    'actores': actor,
                    'valores': valores_mao,            # valores de la matriz
                    'cantidad': objetivo.count() + 3,  # cantidad de columnas para saber cuando hacer el salto de fila
                                                       # +3 debido a la columna de nombrecorto y las 3 de implicacion
                    'cantidad2': (objetivo.count() * 2) + 4, # cantidad de columnas para las sumatorias de movilizacion
                    # x2 y +4  porque no tienen las mismas posiciones de columna que los anteriores valores.
                    'valores_caa': valores_caa,  # valores de la  matriz de convergencia
                    'cantidad3': actor.count(),  # cantidad de columnas para las matrices de conv y divergencia
                    'valores_daa': valores_daa}  # valores de la matriz de divergencia

        return render(request, 'mao/matriz_3mao.html', contexto)


# ------------------------------------VIEWS AJAX----------------------------------------------------

def Consultar_actores_faltantes(request):

    if request.is_ajax():
        id = request.GET['id']
        tipo = request.GET['tipo']
        print(tipo)
        actores = Actor.objects.all().order_by('id')
        lista_registrados = []
        lista_id = []

        # si se esta registrando una influencia mid
        if tipo == "form_mid":
            # para desactivar la opcion correspondiente a autoinfluencia se agrega el id como registrado
            lista_registrados.append(id)
            # se obtiene la lista de relaciones mid registradas
            mid = Relacion_MID.objects.all().order_by('idActorY', 'idActorX')
            # se obtienen los id de los actores ya registrados en la matriz mid
            for i in mid:
                if i.idActorY.id == int(id):
                    lista_registrados.append(i.idActorX.id)
        # si se esta registrando una ficha de estrategias
        if tipo == "form_ficha":
            fichas = Ficha_actor.objects.all().order_by('idActorY', 'idActorX')
            for i in fichas:
                if i.idActorY.id == int(id):
                    print(i.idActorX.nombreLargo)
                    lista_registrados.append(i.idActorX.id)

        # se obtiene la lista de id de los actores del estudio
        for i in actores:
            lista_id.append(i.id)

        response = JsonResponse({'actores': lista_id,
                                 'lista': lista_registrados})
        return HttpResponse(response.content)


def Consultar_objetivos_faltantes(request):

    if request.is_ajax():
        id = request.GET['id']
        tipo = request.GET['tipo']
        print(tipo)
        objetivos = Objetivo.objects.all().order_by('id')
        lista_registrados = []
        lista_id = []

        # si se esta registrando una influencia mid
        if tipo == "form_1mao":
            # se obtiene la lista de relaciones  1mao registradas
            mao = Relacion_MAO.objects.all().exclude(tipo=2).order_by('idActorY', 'idObjetivoX')
            # se obtienen los id de los objetivos ya registrados en la matriz mao con ese actor Y
            for i in mao:
                if i.idActorY.id == int(id):
                    lista_registrados.append(i.idObjetivoX.id)
        # si se esta registrando una ficha de estrategias
        if tipo == "form_2mao":
            mao = Relacion_MAO.objects.all().exclude(tipo=1).order_by('idActorY', 'idObjetivoX')
            for i in mao:
                if i.idActorY.id == int(id):
                    lista_registrados.append(i.idObjetivoX.id)

        # se obtiene la lista de id de los objetivos del estudio
        for i in objetivos:
            lista_id.append(i.id)

        response = JsonResponse({'objetivos': lista_id,
                                 'lista': lista_registrados})
        return HttpResponse(response.content)


def probar(request):
    print('hola')
