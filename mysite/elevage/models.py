from django.db import models


class Elevage(models.Model):
    name = models.CharField(max_length=200)
    nb_cages = models.PositiveIntegerField()
    qt_nourriture = models.PositiveIntegerField()
    argent = models.PositiveIntegerField()
    
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
    INDIVIDUS_PAR_CAGE_MAX = 6
    INDIVIDUS_PAR_CAGE_SURPOP = 10

    AGE_MATURITE_GRAVIDITE = 6         # mois
    AGE_MAX_GRAVIDITE = 48             # mois
    DUREE_GESTATION = 1                # mois