from django.contrib import admin
from .models import EstudioMactor, Actor, Objetivo, RelacionMID, RelacionMAO


class EstudioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_inicio', 'fecha_final', 'estado')
    ordering = ('titulo',)

admin.site.register(EstudioMactor, EstudioAdmin)

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
    search_fields = ('idActorY',)                      # Campo de busqueda
    ordering = ('idActorY', 'idActorX',)               # Campo de ordenamiento

admin.site.register(RelacionMID, Relacion_MIDAdmin)

# ----------------------------------------------------------------------------


class Relacion_MAOAdmin(admin.ModelAdmin):
    list_display = ('idActorY', 'idObjetivoX', 'valor', 'tipo')   # Nombre de las columnas de la tabla de actores
    search_fields = ('idActorY',)                                 # Campo de busqueda
    ordering = ('idActorY', 'idObjetivoX',)                       # Campo de ordenamiento

admin.site.register(RelacionMAO, Relacion_MAOAdmin)
