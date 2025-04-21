from django.db import models
import random


class Elevage(models.Model):
    name = models.CharField(max_length=200)
    nb_cages = models.PositiveIntegerField()
    qt_nourriture = models.PositiveIntegerField()
    argent = models.PositiveIntegerField()
    
    def avancer_tour(self, nourriture_achetee, cages_achetees, lapins_vendus):
        # 1. Met à jour les ressources de l’élevage
        self.qt_nourriture += nourriture_achetee
        self.nb_cages += cages_achetees
        self.argent -= (
            nourriture_achetee * Regle.PRIX_NOURRITURE_PAR_KG +
            cages_achetees * Regle.PRIX_CAGE
        )
        self.argent += len(lapins_vendus) * Regle.PRIX_VENTE_LAPIN

        for lapin in lapins_vendus:
            lapin.etat = "vendu"
            lapin.save()

        # 2. Vieillissement des lapins
        lapins = self.individus.all()
        for lapin in lapins:
            lapin.age += 1
            lapin.save()

        # 3. Reproduction
        femelles = self.individus.filter(sexe='f', age__gte=Regle.AGE_MATURITE_GRAVIDITE, age__lte=Regle.AGE_MAX_GRAVIDITE, etat='présent')
        femelles_gravides = self.individus.filter(etat='gravide')
        males = self.individus.filter(sexe='m', age__gte=3)  # Mâles adultes
        
        # Accouchement des femelles gravides 
        for femelle in femelles_gravides:
            nb_bebes = random.randint(1, Regle.PORTEE_MAX)
            for _ in range(nb_bebes):
                sexe = random.choice(['f', 'm'])
                Individu.objects.create(
                    elevage=self,
                    age=0,
                    sexe=sexe,
                    etat='présent'
                )
            femelle.etat = 'présent'  # accouche, redevient normale
            femelle.save()
            
        for femelle in femelles:
            if random.random() < Regle.PROBA_REPRO: #and males.exists():  # On suppose 50% de chances qu'elle soit fécondée
                femelle.etat = "gravide"
                femelle.save()


        # 4. Nourriture
        morts_par_faim = []

        for lapin in self.individus.all():
            if lapin.age == 0:
                conso = 0
            elif lapin.age == 1:
                conso = Regle.CONSOMMATION_MOIS_2 * 30
            else:
                conso = Regle.CONSOMMATION_MOIS_3_ET_PLUS * 30

            if self.qt_nourriture >= conso:
                self.qt_nourriture -= conso
            else:
                morts_par_faim.append(lapin)

        for lapin in morts_par_faim:
            lapin.etat = "mort"
            lapin.save()

        # 5. Surpopulation
        lapins_restants = self.individus.filter(etat__in=['présent', 'gravide'])
        if lapins_restants.count() > self.nb_cages * Regle.INDIVIDUS_PAR_CAGE_SURPOP:
            morts = random.sample(list(lapins_restants), k=int(0.5 * lapins_restants.count()))
            for lapin in morts:
                lapin.etat = "mort"
                lapin.save()

        self.save()
    
    def __str__(self):
        return self.name


class Individu(models.Model):
    SEXE_CHOICES = [
        ('m', 'Mâle'),
        ('f', 'Femelle'),
    ]
    
    ETAT_CHOICES = [
    ('présent', 'Présent'),
    ('vendu', 'Vendu'),
    ('mort', 'Mort'),
    ('gravide', 'Gravide'),
    ]
    
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)        # "m" pour un lapin male et "f" pour un lapin femelle
    age = models.PositiveIntegerField()                                # âge en nombre de mois
    etat = models.CharField(max_length=10, choices=ETAT_CHOICES)       # "présent", "vendu", "mort" ou "gravide" 
    elevage = models.ForeignKey(Elevage, on_delete=models.CASCADE, related_name="individus")
    
    def __str__(self):
        return f"sexe : {self.sexe}, âge : {self.age}, état : {self.etat}"


class Regle:
    # Économie
    PRIX_NOURRITURE_PAR_KG = 1.0       # €
    PRIX_CAGE = 20.0                  # €
    PRIX_VENTE_LAPIN = 50.0            # €

    # Nourriture (par jour)
    CONSOMMATION_MOIS_1 = 0            # Lait maternel
    CONSOMMATION_MOIS_2 = 0.1          # kg / jour
    CONSOMMATION_MOIS_3_ET_PLUS = 0.25 # kg / jour

    # Reproduction
    PORTEE_MAX = 4                     # max lapereaux par mise bas
    PROBA_REPRO = 0.5
    INDIVIDUS_PAR_CAGE_MAX = 6
    INDIVIDUS_PAR_CAGE_SURPOP = 10

    AGE_MATURITE_GRAVIDITE = 6         # mois
    AGE_MAX_GRAVIDITE = 48             # mois
    DUREE_GESTATION = 1                # mois