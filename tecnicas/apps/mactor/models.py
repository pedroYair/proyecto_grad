from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# MODELO ESTUDIO MACTOR---------------------------------------------------------------------------------------->

class Estudio_Mactor(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    idAdministrador = models.ForeignKey(User, verbose_name='administrador', related_name='mactor_administrador')
    idCoordinador = models.ForeignKey(User, verbose_name='coordinador', related_name='mactor_coordinador')
    idExpertos = models.ManyToManyField(User, verbose_name='Expertos', related_name='mactor_expertos_set')
    fecha_inicio = models.DateField(default=now)
    fecha_final = models.DateField(default=now)
    estado = models.BooleanField(default=True)
    idProyecto = models.PositiveIntegerField(default=1)  # modelo de integracion que permite listar los 
    # estudios donde el usuario es administrador, actualmente se listan solo aquellos donde el usuario es 
    # coordinador o experto del estudio.

# Definicion de nombre singular y plurar del modelo
    class Meta:
        verbose_name = 'Estudio_Mactor'
        verbose_name_plural = 'Estudios_Mactor'

# Campo a mostrar del modelo Estudio_Mactor (tabla en admin y listas desplegables)
    def __str__(self):
        return u'{0}'.format(self.titulo)


# MODELO ACTOR: FASE ----------------------------------------------------------------------------------------->


class Actor(models.Model):
    nombreLargo = models.CharField(max_length=50)
    nombreCorto = models.CharField(max_length=5)
    descripcion = models.TextField(max_length=500)
    idEstudio = models.ForeignKey(Estudio_Mactor, null=True, blank=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Actor'
        verbose_name_plural = 'Actores'

    def __str__(self):
        return u'{0} - {1}'.format(self.nombreCorto, self.nombreLargo)


# MODELO FICHA DE ESTRATEGIAS--------------------------------------------------------------------------------->


class Ficha(models.Model):
    idActorY = models.ForeignKey(Actor, null=True, blank=False, related_name='mactor_actorY_ficha', on_delete=models.CASCADE)
    idActorX = models.ForeignKey(Actor, null=True, blank=False, related_name='mactor_actorX_ficha', on_delete=models.CASCADE)
    estrategia = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Ficha'
        verbose_name_plural = 'Fichas'
        # para evitar que la pareja de registros se repita en ese mismo orden
        unique_together = ('idActorY', 'idActorX')

    def __str__(self):
        return u'{0} - {1} - {2}'.format(self.idActorX, self.idActorY, self.estrategia)


# MODELO OBJETIVO --------------------------------------------------------------------------------------------->

class Objetivo(models.Model):
    nombreLargo = models.CharField(max_length=50)
    nombreCorto = models.CharField(max_length=5)
    descripcion = models.TextField(max_length=500)
    idEstudio = models.ForeignKey(Estudio_Mactor, null=True, blank=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Objetivo'
        verbose_name_plural = 'Objetivos'

    def __str__(self):
        return u'{0} - {1}'.format(self.nombreCorto, self.nombreLargo)

# MODELO INFLUENCIAS MID---------------------------------------------------------------------->


class Relacion_MID(models.Model):
    idActorX = models.ForeignKey(Actor, null=True, blank=False, related_name='mactor_actorX_set', on_delete=models.CASCADE)
    idActorY = models.ForeignKey(Actor, null=True, blank=False, related_name='mactor_actorY_set', on_delete=models.CASCADE)
    valor = models.IntegerField()
    justificacion = models.TextField()
    idExperto = models.ForeignKey(User, null=True)

    class Meta:
        verbose_name = 'Relacion_de_Influencia'
        verbose_name_plural = 'Relaciones_de_influencia'
        # para evitar que la pareja de registros se repita en ese mismo orden
        unique_together = ('idActorX', 'idActorY', 'idExperto')

    def __str__(self):
        return u'{0} - {1} - {2}'.format(self.idActorY, self.idActorX, self.valor)


# MODELO RELACION MAO ------------------------------------------------------------------------------------------->

class Relacion_MAO(models.Model):
    tipo = models.IntegerField(null=True, blank=True)
    idActorY = models.ForeignKey(Actor, null=False, blank=False, on_delete=models.CASCADE)
    idObjetivoX = models.ForeignKey(Objetivo, null=False, blank=False, on_delete=models.CASCADE)
    valor = models.IntegerField()
    justificacion = models.TextField()
    idExperto = models.ForeignKey(User, null=True)

    class Meta:
        verbose_name = 'Relacion_MAO'
        verbose_name_plural = 'Relaciones_MAO'
        unique_together = ('tipo', 'idActorY', 'idObjetivoX', 'idExperto')

    def __str__(self):
        return u'{0} - {1} - {2} - {3} - {4} - {5}'.format(self.tipo, self.idActorY, self.idObjetivoX, self.valor, self.idExperto)


# MODELO INFORME FINAL ---------------------------------------------------------------------->


class Informe_Final(models.Model):
    fecha = models.DateField(auto_now=True)
    informe = models.TextField()
    estado = models.BooleanField(default=False)
    idEstudio = models.ForeignKey(Estudio_Mactor)

    class Meta:
        verbose_name = 'Informe_final'
        verbose_name_plural = 'Informes_finales'

    def __str__(self):
        return u'{0} - {1} - {2}'.format(self.idEstudio, self.fecha, self.informe, self.estado)

