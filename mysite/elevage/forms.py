from django import forms
from .models import Elevage, Individu
from django.forms import modelformset_factory

class ElevageForm(forms.ModelForm):
    class Meta:
        model = Elevage
        fields = ['name', 'qt_nourriture', 'nb_cages', 'argent']

class LapinForm(forms.ModelForm):
    class Meta:
        model = Individu
        fields = ['age', 'sexe', 'etat']

LapinFormSet = modelformset_factory(Individu, form=LapinForm, extra=3)  # On peut ajuster `extra`

class ChoixNombreLapinsForm(forms.Form):
    nombre_lapins = forms.IntegerField(label="Nombre de lapins", min_value=1, max_value=50)