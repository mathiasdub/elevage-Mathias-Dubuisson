from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from django.http import JsonResponse

from .models import Elevage, Individu, Regle, ElevageDatas
from .forms import ElevageForm, LapinForm, ChoixNombreLapinsForm, ActionsForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required



    
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('elevage:login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def menu(request):
    return render(request, "elevage/menu.html")  # Affiche la page d’accueil du jeu

# Vue pour créer un nouvel élevage
@login_required
def nouveau(request):
    if 'nombre_lapins' not in request.session:
        # demander combien de lapins on veut créer
        if request.method == 'POST':
            choix_form = ChoixNombreLapinsForm(request.POST)
            if choix_form.is_valid():
                request.session['nombre_lapins'] = choix_form.cleaned_data['nombre_lapins']
                return redirect('elevage:nouveau')
        else:
            choix_form = ChoixNombreLapinsForm()
        return render(request, 'elevage/choix_nombre_lapins.html', {'form': choix_form})

    # création du formulaire d’élevage + formulaire pour chaque lapin
    LapinFormSet = modelformset_factory(Individu, form=LapinForm, extra=request.session['nombre_lapins'])

    if request.method == 'POST':
        elevage_form = ElevageForm(request.POST)
        lapin_formset = LapinFormSet(request.POST, queryset=Individu.objects.none())
        if elevage_form.is_valid() and lapin_formset.is_valid():
            elevage = elevage_form.save(commit=False)  # Créer l’objet sans le sauvegarder
            elevage.user = request.user  # Lier l’utilisateur après la création
            elevage.save()  # Sauvegarder l’élevage
            
            for form in lapin_formset:     # Création et sauvegarde des lapins liés
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



# Vue qui affiche la liste des élevages
@login_required
def liste(request):
    elevages = Elevage.objects.filter(user=request.user)  
    return render(request, "elevage/liste.html", {"elevages" : elevages})


# Vue pour consulter un élevage en détail et effectuer les actions du tour
@login_required
def detail(request, elevage_id):
    elevage = get_object_or_404(Elevage, id=elevage_id)  
    lapins = elevage.individus.filter(etat__in=['présent', 'gravide'])  # Lapins actifs

    if request.method == 'POST':
        form = ActionsForm(request.POST, elevage=elevage)
        form.fields['lapins_a_vendre'].queryset = elevage.individus.filter(etat__in=['présent', 'gravide'])
        if form.is_valid():
            # Récupère les données du formulaire
            lapins_vendus = form.cleaned_data['lapins_a_vendre']
            nourriture = form.cleaned_data['nourriture_achetee']
            cages = form.cleaned_data['cages_achetees']

            # Fait avancer le jeu d’un tour
            elevage.avancer_tour(nourriture, cages, lapins_vendus)
    else:
        form = ActionsForm(elevage=elevage)
        form.fields['lapins_a_vendre'].queryset = elevage.individus.filter(etat__in=['présent', 'gravide'])

    return render(request, 'elevage/detail.html', {
        'elevage': elevage,
        'lapins': lapins,
        'form': form,
        'nombre_lapins': lapins.count(),  # Pour affichage dans le template
    })


# Vue qui affiche les règles du jeu (valeurs des constantes)
@login_required
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
        'DUREE_MAX_VIE' : Regle.DUREE_VIE_MAX,
        'PROBA_MORT_VIEUX' : Regle.PROBA_MORT_VIEUX,
    }
    return render(request, 'elevage/liste_regle.html', {'regles': regles})


# Vue pour supprimer un élevage et tous les lapins liés
@login_required
def supprimer_elevage(request, elevage_id):
    elevage = get_object_or_404(Elevage, id=elevage_id)  

    if request.method == 'POST':
        Individu.objects.filter(elevage=elevage).delete()  # Supprime les lapins de cet élevage
        elevage.delete()  # Supprime l’élevage lui-même
        return redirect('elevage:liste')  # Retour à la liste après suppression

    return render(request, 'elevage/supprimer_elevage.html', {'elevage': elevage})


# Vue pour afficher l'historique des statistiques de l’élevage
def get_datas(request, elevage_id):
    data = list(ElevageDatas.objects.filter(elevage_id=elevage_id).order_by("tour").values())
    return JsonResponse(data, safe=False)
