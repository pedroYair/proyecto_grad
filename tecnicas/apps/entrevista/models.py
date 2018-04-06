from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


"""MODELO ESTUDIO ENTREVISTA---------------------------------------------------------------------------------"""


class EstudioEntrevista(models.Model):
    titulo = models.CharField(max_length=200)
    objetivo = models.TextField()
    entrevistador = models.TextField()
    entrevistado = models.TextField()
    idAdministrador = models.ForeignKey(User, verbose_name='Administrador', related_name='ent_administrador')
    idCoordinador = models.ForeignKey(User, verbose_name='Coordinador', related_name='ent_coordinador')
    idExpertos = models.ManyToManyField(User, verbose_name='Expertos', related_name='ent_expertos_set')
    fecha_inicio = models.DateField(default=now)
    fecha_final = models.DateField(default=now)
    estado = models.BooleanField(default=True)
    idProyecto = models.PositiveIntegerField(default=1)  # este campo junto con idAdministrador debe obtenerse mediante FK del modelo Proyecto.

    class Meta:
        verbose_name = 'Estudio_Entrevista'
        verbose_name_plural = 'Estudios_Entrevista'

    def __str__(self):
        return u'{0}'.format(self.titulo)


"""MODELO PREGUNTA-------------------------------------------------------------------------------------------"""


class Pregunta(models.Model):
    texto_pregunta = models.TextField()
    texto_respuesta = models.TextField(null=True, blank=True)
    observacion = models.TextField(null=True, blank=True)
    idEstudio = models.ForeignKey(EstudioEntrevista, null=True, blank=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'

    def __str__(self):
        return u'{0}'.format(self.texto_pregunta)


"""MODELO VALOR ESCALA LIKERT-------------------------------------------------------------------------------"""


class ValorEscalaLikert(models.Model):
    nombre = models.TextField()
    valor = models.IntegerField()
    descripcion = models.TextField()
    idEstudio = models.ForeignKey(EstudioEntrevista, null=True, blank=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Valor escala de Likert'
        verbose_name_plural = 'Valores escala de Likert'

    def __str__(self):
        return u'{0}'.format(self.nombre)


"""MODELO RONDA JUICIO---------------------------------------------------------------------------------------"""


class RondaJuicio(models.Model):
    numero_ronda = models.IntegerField()
    descripcion = models.TextField()
    estado = models.BooleanField(default=True)
    idEstudio = models.ForeignKey(EstudioEntrevista, null=True, blank=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Ronda de juicio'
        verbose_name_plural = 'Rondas de juicio'

    def __str__(self):
        return u'{0} - {1}'.format(self.numero_ronda, self.idEstudio)


"""MODELO JUICIO DE EXPERTOS----------------------------------------------------------------------------------------"""


class Juicio(models.Model):
    idPregunta = models.ForeignKey(Pregunta, null=True, blank=False, on_delete=models.CASCADE)
    idValorEscala = models.ForeignKey(ValorEscalaLikert, null=True, blank=False, on_delete=models.CASCADE)
    justificacion = models.TextField(null=True, blank=True)
    idExperto = models.ForeignKey(User, null=True)
    idRonda = models.ForeignKey(RondaJuicio, null=True, blank=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Juicio de expertos'
        verbose_name_plural = 'Juicios de los expertos'

    def __str__(self):
        return u'{0} - {1} - {2}'.format(self.idRonda, self.idPregunta, self.idValorEscala)







