from django.contrib import admin
from .models import EstudioEntrevista


class EstudioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_inicio', 'fecha_final', 'estado')
    ordering = ('titulo',)

admin.site.register(EstudioEntrevista, EstudioAdmin)
