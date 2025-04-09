from django import forms
from .models import Elevage


class ElevageForm(forms.ModelForm):
    class Meta:
        model = Elevage
        fields = ['name', 'nb_cages', 'qt_nourriture', 'argent']