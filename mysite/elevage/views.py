from django.shortcuts import render, get_object_or_404, redirect
from .models import Elevage, Individu, Regle, Sante
from .forms import ElevageForm, LapinForm, ChoixNombreLapinsForm, ActionsForm
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import Group
from .models import Elevage, Individu, Regle, ElevageDatas, IndividuSnapshot
from .forms import ElevageForm, LapinForm, ChoixNombreLapinsForm, ActionsForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse


    
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
    user = request.user
    # Vérifier l'appartenance à un groupe
    is_premium = user.groups.filter(name='premium').exists()

    # Si l'utilisateur est dans le groupe "basic", on limite le nombre d'élevages à 3
    if not is_premium:
        max_elevages = 3
    else:
        max_elevages = float('inf')  # Pas de limite pour les premium

    # Vérifier le nombre d'élevages existants
    elevages_existants = Elevage.objects.filter(user=user).count()

    if elevages_existants >= max_elevages :
        return render(request, 'elevage/liste.html', {
            'message': "Vous avez atteint le nombre d'élevages autorisés.",
            'elevages': Elevage.objects.filter(user=user),
        })


    if request.method == 'POST':
        form = ElevageForm(request.POST)
        if form.is_valid():
            elevage = form.save(commit=False)  # Créer l’objet sans le sauvegarder
            elevage.user = request.user  # Lier l’utilisateur après la création
            elevage.save()  # Sauvegarder l’élevage
            
            # Récupérer le nombre de mâles et femelles
            nb_males = form.cleaned_data['nb_males']
            nb_femelles = form.cleaned_data['nb_femelles']

            # Créer les lapins mâles
            for _ in range(nb_males):
                lapin = Individu.objects.create(
                    elevage=elevage,
                    age=6,  # Âge par défaut
                    sexe='m',
                    etat='présent',
                )
                sante = Sante.objects.create(
                    niveau_sante=100,
                    malade=False,
                )
                sante.individu = lapin
                sante.save()
                lapin.save()
                
                elevage_data = ElevageDatas.objects.create(
                elevage=elevage,
                tour=0,
                nb_males=nb_males,  # À ajuster en fonction des données des lapins créés
                nb_femelles=nb_femelles,  # À ajuster en fonction des données des lapins créés
                nb_lapereaux=0,  # À ajuster en fonction des données des lapins créés
                naissances=0,
                morts=0,
                ventes=0,
                argent=elevage.argent,  # À ajuster en fonction des ressources disponibles
                nourriture=elevage.qt_nourriture,  # À ajuster en fonction des ressources disponibles
                cages=elevage.nb_cages,  # À ajuster en fonction des ressources disponibles
                malades=0
            )
                
                # Création de snapshot pour chaque individu
                IndividuSnapshot.objects.create(
                    elevage_data=elevage_data,
                    sexe=lapin.sexe,
                    age=lapin.age,
                    etat=lapin.etat
                )

            # Créer les lapins femelles
            for _ in range(nb_femelles):
                lapin = Individu.objects.create(
                    elevage=elevage,
                    age=6,  # Âge par défaut
                    sexe='f',
                    etat='présent',
                )
                sante = Sante.objects.create(
                    niveau_sante=100,
                    malade=False,
                )
                sante.individu = lapin
                sante.save()
                lapin.save()
            
            

            return redirect('elevage:detail', elevage_id=elevage.id)
    else:
        form = ElevageForm()

    return render(request, 'elevage/nouveau.html', {'form': form})


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
            depenses_sante = form.cleaned_data['depenses_sante']




            try:
                elevage.avancer_tour(nourriture, cages, lapins_vendus, depenses_sante)
                messages.success(request, "Le tour a été avancé avec succès !")
            except ValueError as e:
                messages.error(request, str(e))  # On affiche l'erreur remontée par avancer_tour
                
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
        # Supprimer tous les objets ElevageDatas associés à cet élevage
        ElevageDatas.objects.filter(elevage=elevage).delete()
        
        # Supprimer les lapins de cet élevage
        Individu.objects.filter(elevage=elevage).delete()

        # Supprimer l’élevage lui-même
        elevage.delete()

        # Redirection après suppression
        return redirect('elevage:liste')

    return render(request, 'elevage/supprimer_elevage.html', {'elevage': elevage})


# Vue pour afficher l'historique des statistiques de l’élevage
def get_datas(request, elevage_id):
    data = list(ElevageDatas.objects.filter(elevage_id=elevage_id).order_by("tour").values())
    return JsonResponse(data, safe=False)

@login_required
def paiement(request):
    # Vérifier si l'utilisateur est déjà premium
    if request.user.groups.filter(name='premium').exists():
        messages.info(request, "Vous êtes déjà un membre Premium !")
        return redirect('elevage:menu')  # Redirige vers le menu du jeu

    if request.method == 'POST':
        # Simuler un paiement réussi (par exemple, une validation de paiement)
        groupe_premium = Group.objects.get(name='premium')
        
        # Ajouter l'utilisateur au groupe "premium"
        request.user.groups.add(groupe_premium)
        request.user.save()

        messages.success(request, "Vous êtes maintenant un membre Premium !")
        return redirect('elevage:menu')  # Redirige vers la page principale de l'application

    return render(request, 'elevage/paiement.html')

@login_required
def restaurer_tour(request, elevage_id, tour):
    elevage = get_object_or_404(Elevage, id=elevage_id, user=request.user)
    
    is_premium = request.user.groups.filter(name='premium').exists()
    if not is_premium:
        lien_paiement = reverse('elevage:paiement')  
        messages.error(
            request,
            f"La restauration de tours est réservée aux membres premium. "
            f"<a href='{lien_paiement}' style='color: #cc0000; text-decoration: underline;'>Devenir premium</a>"
        )
        return redirect('elevage:detail', elevage_id=elevage_id)

    try:
        elevage.restaurer_tour(tour)
        messages.success(request, f"Tour {tour} restauré avec succès.")
    except ValueError as e:
        messages.error(request, str(e))

    return redirect('elevage:detail', elevage_id=elevage.id)