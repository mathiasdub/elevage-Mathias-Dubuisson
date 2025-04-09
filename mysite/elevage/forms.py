from django import forms
from django.forms import inlineformset_factory
from .models import Elevage, Individu


class ElevageForm(forms.ModelForm):
    class Meta:
        model = Elevage
        fields = ['name', 'nb_cages', 'qt_nourriture', 'argent']


class IndividuForm(forms.ModelForm):
    class Meta:
        model = Individu
        fields = ['sexe', 'age', 'etat']


# Formset pour ajouter plusieurs individus à un élevage
IndividuFormSet = inlineformset_factory(
    Elevage,
    Individu,
    form=IndividuForm,
    extra=3,             # nombre de lignes de formulaire affichées
    can_delete=False     # on ne permet pas de supprimer dans la création
)