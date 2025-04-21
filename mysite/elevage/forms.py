from django import forms
from .models import Elevage, Individu


# Formulaire de création d'un élevage
class ElevageForm(forms.ModelForm):
    class Meta:
        model = Elevage  
        fields = ['name', 'qt_nourriture', 'nb_cages', 'argent']  # Champs à afficher dans le formulaire


# Formulaire de création d'un lapin 
class LapinForm(forms.ModelForm):
    class Meta:
        model = Individu  
        fields = ['age', 'sexe', 'etat']  # Champs à afficher dans le formulaire


# Formulaire demandant à l'utilisateur combien de lapins il souhaite créer
class ChoixNombreLapinsForm(forms.Form):
    nombre_lapins = forms.IntegerField(label="Nombre de lapins", min_value=0, max_value=50)


# Formulaire des actions que l’on peut faire à chaque tour de jeu
class ActionsForm(forms.Form):
    # Champ pour acheter de la nourriture (kg)
    nourriture_achetee = forms.FloatField(min_value=0, required=True, label="Nourriture achetée (kg)")

    # Champ pour acheter des cages
    cages_achetees = forms.IntegerField(min_value=0, required=True, label="Cages achetées")

    # Champ pour sélectionner plusieurs lapins à vendre
    lapins_a_vendre = forms.ModelMultipleChoiceField(
        queryset=Individu.objects.none(),       # Initialement vide, rempli dynamiquement plus bas
        required=False,                         # L'utilisateur n'est pas obligé de vendre des lapins
        widget=forms.CheckboxSelectMultiple,    # Affiché sous forme de cases à cocher
        label="Lapins à vendre"
    )

    def __init__(self, *args, **kwargs):
        elevage = kwargs.pop('elevage', None) 
        super().__init__(*args, **kwargs)     

        # on limite les lapins à vendre à ceux de cet élevage parmi ceux qui sont présent ou gravide
        if elevage:
            self.fields['lapins_a_vendre'].queryset = elevage.individus.filter(etat__in=['présent', 'gravide'])
