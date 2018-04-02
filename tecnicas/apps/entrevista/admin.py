from django.contrib import admin
from .models import EstudioEntrevista, Pregunta


class EstudioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_inicio', 'fecha_final', 'estado')
    ordering = ('titulo',)

admin.site.register(EstudioEntrevista, EstudioAdmin)


class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('texto_pregunta',)
    ordering = ('texto_pregunta',)

admin.site.register(Pregunta, PreguntaAdmin)

