from django import forms
from .models import EstudioEntrevista, Pregunta, ValorEscalaLikert, RondaJuicio


"""FORMULARIO ESTUDIO ENTREVISTA------------------------------------------------------------------------------------"""


class FormEstudioE(forms.ModelForm):

    def clean_titulo(self):
        mensaje = self.cleaned_data["titulo"]
        palabras = len(mensaje.split())
        if palabras < 2:
            raise forms.ValidationError("Ingrese mínimo dos palabras para el título del estudio")
        return mensaje

    def clean_idExpertos(self):
        expertos = self.cleaned_data["idExpertos"]

        if self.cleaned_data["idCoordinador"] in expertos:
            raise forms.ValidationError("El coordinador no puede hacer parte del grupo de expertos")
        return expertos

    class Meta:
        model = EstudioEntrevista

        fields = [
            'titulo',
            'objetivo',
            'entrevistador',
            'entrevistado',
            'idAdministrador',
            'idCoordinador',
            'idExpertos',
            'fecha_inicio',
            'fecha_final',
            'estado',
            'idProyecto',
        ]

    widgets = {
            'titulo': forms.Textarea(),
            'objetivo': forms.Textarea(attrs={'class': 'form-control', 'row': '3'}),
            'entrevistador': forms.TextInput(attrs={'class': 'form-control'}),
            'entrevistado': forms.TextInput(attrs={'class': 'form-control'}),
            'idAdministrador': forms.Select(attrs={'class': 'form-control'}),
            'idCoordinador': forms.Select(attrs={'class': 'form-control'}),
            'idExpertos': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'datepicker'}),
            'fecha_final': forms.DateInput(attrs={'class': 'date'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'idProyecto': forms.TextInput(attrs={'class': 'form-control'}),
        }

"""FORMULARIO PREGUNTA------------------------------------------------------------------------------------"""


class FormPregunta(forms.ModelForm):

    class Meta:
        model = Pregunta

        fields = [
            'texto_pregunta',
            'texto_respuesta',
            'observacion',
            'idEstudio',
        ]

        widgets = {
            'texto_pregunta': forms.Textarea(attrs={'class': 'form-control', 'row': '2'}),
            'texto_respuesta': forms.Textarea(attrs={'class': 'form-control', 'row': '3'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'row': '3'}),
            'idEstudio': forms.Select(attrs={'class': 'form-control'}),
        }

"""FORMULARIO DE INFLUENCIAS-----------------------------------------------------------------------------------"""


class FormValorEscala(forms.ModelForm):

    class Meta:
        model = ValorEscalaLikert

        fields = [
            'nombre',
            'valor',
            'descripcion',
            'idEstudio',
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.TextInput(attrs={'class': 'form-control'}),
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'row': '3'}),
            'idEstudio': forms.Select(attrs={'class': 'form-control'}),
        }


"""FORMULARIO RONDAS----------------------------------------------------------------------------------------------"""


class FormRonda(forms.ModelForm):

    class Meta:
        model = RondaJuicio

        fields = [
            'numero_ronda',
            'descripcion',
            'estado',
            'idEstudio',
        ]

        widgets = {
            'numero_ronda': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'row': '3'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'idEstudio': forms.Select(attrs={'class': 'form-control'}),
        }

"""
FORMULARIO 2MAO---------------------------------------------------------------------------------------------


class Form2mao(forms.ModelForm):

    class Meta:
        model = RelacionMAO

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

FORMULARIO INFORME FINAL-------------------------------------------------------------------------------------


class FormInforme(forms.ModelForm):

    class Meta:
        model = InformeFinal

        fields = [
            'informe',
            'estado',
            'idEstudio',
        ]

        widgets = {
            'fecha': forms.TextInput(attrs={'class': 'form-control'}, ),
            'informe': forms.Textarea(attrs={'class': 'form-control', 'row': '3'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'idEstudio': forms.Select(attrs={'class': 'form-control'}),
        }

        """




