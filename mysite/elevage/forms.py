from django import forms
from .models import Elevage, Individu


# Formulaire de création d'un élevage
class ElevageForm(forms.ModelForm):
    nb_males = forms.IntegerField(min_value=0, required=True, label="Nombre de lapins mâles")
    nb_femelles = forms.IntegerField(min_value=0, required=True, label="Nombre de lapins femelles")

    class Meta:
        model = Elevage  
        fields = ['name', 'qt_nourriture', 'nb_cages', 'argent']  # Champs à afficher dans le formulaire
        labels = {
            'qt_nourriture': 'Quantité de nourriture (kg)',
            'nb_cages': 'Nombre de cages',
            'argent': 'Argent (€)',
            'name': 'Nom de l’élevage',
        }




# Formulaire des actions que l’on peut faire à chaque tour de jeu
class ActionsForm(forms.Form):
    # Champ pour acheter de la nourriture (kg)
    nourriture_achetee = forms.FloatField(min_value=0, required=True, label="Nourriture achetée (kg)")

    # Champ pour acheter des cages
    cages_achetees = forms.IntegerField(min_value=0, required=True, label="Cages achetées")
    
    depenses_sante = forms.IntegerField(min_value=0, required=True, label="Dépenses santé (€)")

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
