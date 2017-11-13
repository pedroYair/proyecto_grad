from django import forms
from .models import Estudio_Mactor, Actor, Ficha_actor, Objetivo, Relacion_MID, Relacion_MAO
from .choices import VALORES, VALORES_1MAO, VALORES_2MAO


# FORMULARIO DE ESTUDIO MACTOR---------------------------------------------------------------------------------->

class Form_Estudio(forms.ModelForm):
    def clean_titulo(self):
        mensaje = self.cleaned_data["titulo"]
        palabras = len(mensaje.split())
        if palabras < 2:
            raise forms.ValidationError("Ingrese mínimo dos palabras para el título")
        return mensaje

    class Meta:
        model = Estudio_Mactor

        fields = [
            'titulo',
            'descripcion',
            'idCoordinador',
            'idExpertos',
            'fecha_inicio',
            'fecha_final',
            'estado',
            'idProyecto',
        ]

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'row': '3'}),
            'idCoordinador': forms.Select(attrs={'class': 'form-control'}),
            'idExpertos': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.TextInput(attrs={'class': 'form-control'}, ),
            'fecha_final': forms.TextInput(attrs={'class': 'form-control'}, ),
            'estado': forms.TextInput(attrs={'class': 'form-control'}, ),
            'id_Proyecto': forms.TextInput(attrs={'class': 'form-control'}),
        }


# FORMULARIO DE ACTOR------------------------------------------------------------------------------------------>

class Form_Actor(forms.ModelForm):

    def clean_nombreCorto(self):
        act = Actor.objects.all()
        nombre = self.cleaned_data['nombreCorto']

        for i in act:
            if i.nombreCorto == nombre:
                raise forms.ValidationError('Ya existe un actor con este nombre corto')
            else:
                return nombre

    def clean_nombreLargo(self):
        act = Actor.objects.all()
        nombre = self.cleaned_data['nombreLargo']
        palabras = len(nombre.split())

        for i in act:
            if i.nombreLargo == nombre:
                raise forms.ValidationError('Ya existe un actor con este nombre largo')
            elif palabras < 2:
                raise forms.ValidationError(u"Se requieren mínimo dos palabras para el nombre largo")
            else:
                return nombre

    class Meta:
        model = Actor

        fields = [
            'nombreLargo',
            'nombreCorto',
            'descripcion',
            'idEstudio',
        ]

        widgets = {
            'nombreLargo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombreCorto': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'row': '3', 'placeholder': u'Ingrese información '
                         'relacionada a objetivos, preferencias, motivaciones, propuestas, comportamientos o recursos del actor.'}),
            'idEstudio': forms.Select(attrs={'class': 'form-control'}),
        }

# FORMULARIO FICHA DEL ACTOR------------------------------------------------------------------------------------>


class Form_Ficha(forms.ModelForm):

    class Meta:
        model = Ficha_actor

        fields = [
            'idActorX',
            'idActorY',
            'estrategia',
            'idEstudio',
        ]

        widgets = {
            'idActorX': forms.Select(attrs={'class': 'form-control'}),
            'idActorY': forms.Select(attrs={'class': 'form-control'}),
            'estrategia': forms.Textarea(attrs={'class': 'form-control', 'row': '3'}),
            'idEstudio': forms.TextInput(attrs={'class': 'form-control'}, ),
        }


# FORMULARIO DE OBJETIVO----------------------------------------------------------------------------------------------->

class Form_Objetivo(forms.ModelForm):

    def clean_nombreLargo(self):
        obj = Objetivo.objects.all()
        nombre = self.cleaned_data['nombreLargo']
        palabras = len(nombre.split())

        for i in obj:
            if i.nombreLargo == nombre:
                raise forms.ValidationError('Ya existe un objetivo con este nombre largo')
            elif palabras < 2:
                raise forms.ValidationError(u"Se requieren mínimo dos palabras para el nombre largo")
            else:
                return nombre

    def clean_nombreCorto(self):
        obj = Objetivo.objects.all()
        nombre = self.cleaned_data['nombreCorto']

        for i in obj:
            if i.nombreCorto == nombre:
                raise forms.ValidationError('Ya existe un objetivo con este nombre corto')
        else:
            return nombre

    class Meta:
        model = Objetivo

        fields = [
            'nombreLargo',
            'nombreCorto',
            'descripcion',
            'idEstudio',
        ]

        widgets = {
            'nombreLargo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombreCorto': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'row': '3'}),
            'idEstudio': forms.TextInput(attrs={'class': 'form-control'}, ),
        }


# FORMULARIO DE INFLUENCIAS-------------------------------------------------------------------------------------------->

class Form_MID(forms.ModelForm):

    class Meta:
        model = Relacion_MID

        fields = [
            'idActorY',
            'idActorX',
            'valor',
            'justificacion',
            'idExperto',
            'idEstudio',
        ]

        widgets = {
            'idActorY': forms.Select(attrs={'class': 'form-control'}),
            'idActorX': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.Select(choices=VALORES, attrs={'class': 'regDropDown'}),
            'justificacion': forms.Textarea(attrs={'class': 'form-control', 'row': '3'}),
            'idExperto': forms.Select(attrs={'class': 'form-control'}),
            'idEstudio': forms.TextInput(attrs={'class': 'form-control'}, ),
        }


# FORMULARIO 1MAO------------------------------------------------------------------------------------------------------>

class Form_1mao(forms.ModelForm):

    class Meta:
        model = Relacion_MAO

        fields = [
            'tipo',
            'idActorY',
            'idObjetivoX',
            'valor',
            'justificacion',
            'idExperto',
            'idEstudio',
            ]

        widgets = {
            'tipo': forms.TextInput(attrs={'class': 'form-control'}, ),
            'idActorY': forms.Select(attrs={'class': 'form-control'}),
            'idObjetivoX': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.Select(choices=VALORES_1MAO, attrs={'class': 'regDropDown'}),
            'justificacion': forms.Textarea(attrs={'class': 'form-control', 'row': '3'}),
            'idExperto': forms.Select(attrs={'class': 'form-control'}),
            'idEstudio': forms.Select(attrs={'class': 'form-control'}),
            }


# FORMULARIO 2MAO------------------------------------------------------------------------------------------------------>

class Form_2mao(forms.ModelForm):

    class Meta:
        model = Relacion_MAO

        fields = [
            'tipo',
            'idActorY',
            'idObjetivoX',
            'valor',
            'justificacion',
            'idExperto',
            'idEstudio',
            ]

        widgets = {
            'tipo': forms.TextInput(attrs={'class': 'form-control'}, ),
            'idActorY': forms.Select(attrs={'class': 'form-control'}),
            'idObjetivoX': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.Select(choices=VALORES_2MAO, attrs={'class': 'regDropDown'}),
            'justificacion': forms.Textarea(attrs={'class': 'form-control', 'row': '3'}),
            'idExperto': forms.Select(attrs={'class': 'form-control'}),
            'idEstudio': forms.Select(attrs={'class': 'form-control'}),
            }


