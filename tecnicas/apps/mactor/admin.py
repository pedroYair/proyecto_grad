from django.contrib import admin
from .models import Estudio_Mactor, Actor, Objetivo, Relacion_MID, Relacion_MAO


class EstudioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_inicio', 'fecha_final', 'estado')
    ordering = ('titulo',)

admin.site.register(Estudio_Mactor, EstudioAdmin)

# -------------------------------------------------------------------------


class ActorAdmin(admin.ModelAdmin):
    list_display = ('nombreCorto', 'nombreLargo', 'descripcion')   # Nombre de las columnas de la tabla de actores
    search_fields = ('nombreLargo',)                               # Campo de busqueda
    ordering = ('nombreLargo',)                                    # Campo de ordenamiento

admin.site.register(Actor, ActorAdmin)

# -------------------------------------------------------------------------


class ObjetivoAdmin(admin.ModelAdmin):
    list_display = ('nombreCorto', 'nombreLargo', 'descripcion')   # Nombre de las columnas de la tabla de actores
    search_fields = ('nombreLargo',)                               # Campo de busqueda
    ordering = ('nombreLargo',)                                    # Campo de ordenamiento

admin.site.register(Objetivo, ObjetivoAdmin)

# -------------------------------------------------------------------------


class Relacion_MIDAdmin(admin.ModelAdmin):
    list_display = ('idActorY', 'idActorX', 'valor')   # Nombre de las columnas de la tabla de actores
    search_fields = ('idActorY',)                               # Campo de busqueda
    ordering = ('idActorY', 'idActorX',)                                    # Campo de ordenamiento

admin.site.register(Relacion_MID, Relacion_MIDAdmin)

# ----------------------------------------------------------------------------


class Relacion_MAOAdmin(admin.ModelAdmin):
    list_display = ('idActorY', 'idObjetivoX', 'valor', 'tipo')   # Nombre de las columnas de la tabla de actores
    search_fields = ('idActorY',)                               # Campo de busqueda
    ordering = ('idActorY', 'idObjetivoX',)                                    # Campo de ordenamiento

admin.site.register(Relacion_MAO, Relacion_MAOAdmin)
