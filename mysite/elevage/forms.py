from django import forms
from .models import Elevage, Individu


class ElevageForm(forms.ModelForm):
    class Meta:
        model = Elevage
        fields = ['name', 'qt_nourriture', 'nb_cages', 'argent']


class LapinForm(forms.ModelForm):
    class Meta:
        model = Individu
        fields = ['age', 'sexe', 'etat']


class ChoixNombreLapinsForm(forms.Form):
    nombre_lapins = forms.IntegerField(label="Nombre de lapins", min_value=0, max_value=50)
    

class ActionsForm(forms.Form):
    nourriture_achetee = forms.FloatField(min_value=0, required=True, label="Nourriture achetée (kg)")
    cages_achetees = forms.IntegerField(min_value=0, required=True, label="Cages achetées")
    lapins_a_vendre = forms.ModelMultipleChoiceField(
        queryset=Individu.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Lapins à vendre"
    )

    def __init__(self, *args, **kwargs):
        elevage = kwargs.pop('elevage', None)
        super().__init__(*args, **kwargs)
        # Charger les lapins de l’élevage
        if elevage:
           self.fields['lapins_a_vendre'].queryset = elevage.individus.all()