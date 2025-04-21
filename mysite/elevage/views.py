from django.shortcuts import render, get_object_or_404, redirect
from .models import Elevage, Individu, Regle
from .forms import ElevageForm, LapinForm, ChoixNombreLapinsForm, ActionsForm
from django.forms import modelformset_factory



def menu(request):
    return render(request, "elevage/menu.html")


def nouveau(request):
    if 'nombre_lapins' not in request.session:
        if request.method == 'POST':
            choix_form = ChoixNombreLapinsForm(request.POST)
            if choix_form.is_valid():
                request.session['nombre_lapins'] = choix_form.cleaned_data['nombre_lapins']
                return redirect('elevage:nouveau')
        else:
            choix_form = ChoixNombreLapinsForm()
        return render(request, 'elevage/choix_nombre_lapins.html', {'form': choix_form})

    # Étape 2 : formulaire complet avec x lapins
    LapinFormSet = modelformset_factory(Individu, form=LapinForm, extra=request.session['nombre_lapins'])

    if request.method == 'POST':
        elevage_form = ElevageForm(request.POST)
        lapin_formset = LapinFormSet(request.POST, queryset=Individu.objects.none())
        if elevage_form.is_valid() and lapin_formset.is_valid():
            elevage = elevage_form.save()
            for form in lapin_formset:
                lapin = form.save(commit=False)
                lapin.elevage = elevage
                lapin.save()
            del request.session['nombre_lapins']
            return redirect('elevage:detail', elevage_id=elevage.id)
    else:
        elevage_form = ElevageForm()
        lapin_formset = LapinFormSet(queryset=Individu.objects.none())

    return render(request, 'elevage/nouveau.html', {
        'elevage_form': elevage_form,
        'lapin_formset': lapin_formset,
    })


def liste(request):
    elevages = Elevage.objects.all()
    return render(request, "elevage/liste.html", {"elevages" : elevages})


def detail(request, elevage_id):
    elevage = get_object_or_404(Elevage, id=elevage_id)
    lapins = elevage.individus.filter(etat__in=['présent', 'gravide'])
    
    if request.method == 'POST':
        form = ActionsForm(request.POST, elevage=elevage)
        form.fields['lapins_a_vendre'].queryset = elevage.individus.filter(etat__in=['présent', 'gravide'])
        if form.is_valid():
            lapins_vendus = form.cleaned_data['lapins_a_vendre']
            nourriture = form.cleaned_data['nourriture_achetee']
            cages = form.cleaned_data['cages_achetees']
            
            elevage.avancer_tour(nourriture, cages, lapins_vendus)
    else:
        form = ActionsForm(elevage=elevage)
        form.fields['lapins_a_vendre'].queryset = elevage.individus.filter(etat__in=['présent', 'gravide'])


    return render(request, 'elevage/detail.html', {
        'elevage': elevage,
        'lapins': lapins,
        'form': form,
        'nombre_lapins': lapins.count(),
    })
    
    
def liste_regle(request):
    regles = {
        'PRIX_NOURRITURE_PAR_KG': Regle.PRIX_NOURRITURE_PAR_KG,
        'PRIX_CAGE': Regle.PRIX_CAGE,
        'PRIX_VENTE_LAPIN': Regle.PRIX_VENTE_LAPIN,
        'CONSOMMATION_MOIS_1': Regle.CONSOMMATION_MOIS_1,
        'CONSOMMATION_MOIS_2': Regle.CONSOMMATION_MOIS_2,
        'CONSOMMATION_MOIS_3_ET_PLUS': Regle.CONSOMMATION_MOIS_3_ET_PLUS,
        'PORTEE_MAX': Regle.PORTEE_MAX,
        'PROBA_REPRO': Regle.PROBA_REPRO,
        'INDIVIDUS_PAR_CAGE_MAX': Regle.INDIVIDUS_PAR_CAGE_MAX,
        'INDIVIDUS_PAR_CAGE_SURPOP': Regle.INDIVIDUS_PAR_CAGE_SURPOP,
        'AGE_MATURITE_GRAVIDITE': Regle.AGE_MATURITE_GRAVIDITE,
        'AGE_MAX_GRAVIDITE': Regle.AGE_MAX_GRAVIDITE,
        'DUREE_GESTATION': Regle.DUREE_GESTATION,
    }
    
    return render(request, 'elevage/liste_regle.html', {'regles': regles})