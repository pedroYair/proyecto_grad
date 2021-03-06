from django.contrib import admin
from .models import EstudioEntrevista, Pregunta, ValorEscalaLikert


class EstudioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_inicio', 'fecha_final', 'estado')
    ordering = ('titulo',)

admin.site.register(EstudioEntrevista, EstudioAdmin)


class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('texto_pregunta', 'idEstudio')
    ordering = ('idEstudio',)

admin.site.register(Pregunta, PreguntaAdmin)


class ValorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'valor')
    ordering = ('valor',)

admin.site.register(ValorEscalaLikert, ValorAdmin)


