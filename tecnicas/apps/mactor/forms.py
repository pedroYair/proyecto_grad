from django import forms
from .models import Estudio_Mactor, Ficha, Relacion_MID, Relacion_MAO, Informe_Final
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
            'fecha_inicio': forms.DateInput(attrs={'class': 'datepicker'}),
            'fecha_final': forms.DateInput(attrs={'class': 'datepicker'}, ),
            'estado': forms.CheckboxInput(attrs={'class': 'form-control'}, ),
            'id_Proyecto': forms.TextInput(attrs={'class': 'form-control'}),
        }


# FORMULARIO FICHA DEL ACTOR------------------------------------------------------------------------------------>


class Form_Ficha(forms.ModelForm):

    class Meta:
        model = Ficha

        fields = [
            'idActorX',
            'idActorY',
            'estrategia',
        ]

        widgets = {
            'idActorX': forms.Select(attrs={'class': 'form-control'}),
            'idActorY': forms.Select(attrs={'class': 'form-control'}),
            'estrategia': forms.Textarea(attrs={'class': 'form-control', 'row': '3'}),
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
        ]

        widgets = {
            'idActorY': forms.Select(attrs={'class': 'form-control'}),
            'idActorX': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.Select(choices=VALORES, attrs={'class': 'regDropDown'}),
            'justificacion': forms.Textarea(attrs={'class': 'form-control', 'row': '3'}),
            'idExperto': forms.Select(attrs={'class': 'form-control'}),
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
            ]

        widgets = {
            'tipo': forms.TextInput(attrs={'class': 'form-control'}, ),
            'idActorY': forms.Select(attrs={'class': 'form-control'}),
            'idObjetivoX': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.Select(choices=VALORES_1MAO, attrs={'class': 'regDropDown'}),
            'justificacion': forms.Textarea(attrs={'class': 'form-control', 'row': '3'}),
            'idExperto': forms.Select(attrs={'class': 'form-control'}),
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
            ]

        widgets = {
            'tipo': forms.TextInput(attrs={'class': 'form-control'}, ),
            'idActorY': forms.Select(attrs={'class': 'form-control'}),
            'idObjetivoX': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.Select(choices=VALORES_2MAO, attrs={'class': 'regDropDown'}),
            'justificacion': forms.Textarea(attrs={'class': 'form-control', 'row': '3'}),
            'idExperto': forms.Select(attrs={'class': 'form-control'}),
            }


# FORMULARIO INFORME FINAL

class Form_Informe(forms.ModelForm):

    class Meta:
        model = Informe_Final

        fields = [
            'informe',
            'estado',
            'idCoordinador',
            'idEstudio',
        ]

        widgets = {
            'fecha': forms.TextInput(attrs={'class': 'form-control'}, ),
            'informe': forms.Textarea(attrs={'class': 'form-control', 'row': '3'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'idCoordinador': forms.Select(attrs={'class': 'form-control'}),
            'idEstudio': forms.Select(attrs={'class': 'form-control'}),
        }




