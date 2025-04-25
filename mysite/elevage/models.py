from django.db import models
import random


# Modèle représentant un élevage de lapins
class Elevage(models.Model):
    name = models.CharField(max_length=200)                 # Nom de l'élevage
    nb_cages = models.PositiveIntegerField()                # Nombre de cages disponibles
    qt_nourriture = models.PositiveIntegerField()           # Quantité de nourriture (en kg)
    argent = models.PositiveIntegerField()                  # Argent disponible (en €)

    # Fonction appelée à chaque tour pour mettre à jour l’état de l’élevage
    def avancer_tour(self, nourriture_achetee, cages_achetees, lapins_vendus):
        #----- Mise à jour des ressources de l’élevage -----#
        self.qt_nourriture += nourriture_achetee
        self.nb_cages += cages_achetees
        self.argent -= (
            nourriture_achetee * Regle.PRIX_NOURRITURE_PAR_KG +
            cages_achetees * Regle.PRIX_CAGE
        )
        self.argent += len(lapins_vendus) * Regle.PRIX_VENTE_LAPIN

        # Marque les lapins vendus comme vendus
        for lapin in lapins_vendus:
            lapin.etat = "vendu"
            lapin.save()

        #----- Vieillissement de tous les lapins -----#
        lapins = self.individus.all()
        for lapin in lapins:
            lapin.age += 1
            lapin.save()

        #----- Reproduction -----#
        # Récupération des femelles fécondables / femelles gravides / femelles adultes
        femelles = self.individus.filter(sexe='f', age__gte=Regle.AGE_MATURITE_GRAVIDITE, age__lte=Regle.AGE_MAX_GRAVIDITE, etat='présent')
        femelles_gravides = self.individus.filter(etat='gravide')
        femelles_adultes = self.individus.filter(sexe='f', age__gte=3)
        # Mâles adultes
        males = self.individus.filter(sexe='m', age__gte=3)  


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
            femelle.etat = 'présent'  # Elle redevient normale après l’accouchement
            femelle.save()

        # Fécondation aléatoire des femelles fécondables
        for femelle in femelles:
            if random.random() < Regle.PROBA_REPRO and males.exists():
                femelle.etat = "gravide"
                femelle.save()

        #----- Consommation de nourriture et gestion de la faim ------#
        morts_par_faim = []

        for lapin in self.individus.all():
            if lapin.age == 0 and not femelles_adultes.exists():
                morts_par_faim.append(lapin)    # aucune femelle pour nourrir le jeune lapin
            elif lapin.age == 0:
                conso = 0  # Lait maternel
            elif lapin.age == 1:
                conso = Regle.CONSOMMATION_MOIS_2 * 30
            else:
                conso = Regle.CONSOMMATION_MOIS_3_ET_PLUS * 30

            if self.qt_nourriture >= conso:
                self.qt_nourriture -= conso
            else:
                morts_par_faim.append(lapin)

        # Marque les lapins morts de faim comme morts
        for lapin in morts_par_faim:
            lapin.etat = "mort"
            lapin.save()

        #----- Gestion de la surpopulation -----#
        lapins_restants = self.individus.filter(etat__in=['présent', 'gravide'])
        if lapins_restants.count() > self.nb_cages * Regle.INDIVIDUS_PAR_CAGE_SURPOP:
            # 50% des lapins meurent si surpopulation
            morts = random.sample(list(lapins_restants), k=int(0.5 * lapins_restants.count()))
            for lapin in morts:
                lapin.etat = "mort"
                lapin.save()
        
        #----- Gestion des morts par vieillesse -----#
        lapins_restants = self.individus.filter(etat__in=['présent', 'gravide'], age__gte=Regle.DUREE_VIE_MAX)
        for lapin in lapins_restants:
            if random.random() < Regle.PROBA_MORT_VIEUX:
                lapin.etat = "mort"
                lapin.save()
            
                

        self.save()  # Sauvegarde finale des données

    def __str__(self):
        return self.name  # Représentation texte de l’élevage


# Modèle représentant un individu dans l’élevage
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

    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)                                 # Sexe : mâle ou femelle
    age = models.PositiveIntegerField()                                                         # Âge du lapin (en mois)
    etat = models.CharField(max_length=10, choices=ETAT_CHOICES)                                # État actuel du lapin
    elevage = models.ForeignKey(Elevage, on_delete=models.CASCADE, related_name="individus")    # Référence à l’élevage

    def __str__(self):
        return f"sexe : {self.sexe}, âge : {self.age} mois, état : {self.etat}"


# Classe contenant toutes les règles du jeu 
class Regle:
    # Économie
    PRIX_NOURRITURE_PAR_KG = 5.0        # €/kg
    PRIX_CAGE = 120.0                   # €
    PRIX_VENTE_LAPIN = 65.0             # €

    # Nourriture (en kg par jour selon l’âge)
    CONSOMMATION_MOIS_1 = 0            
    CONSOMMATION_MOIS_2 = 0.1          
    CONSOMMATION_MOIS_3_ET_PLUS = 0.25  

    # Reproduction
    PORTEE_MAX = 4                      # Taille maximale d’une portée
    PROBA_REPRO = 0.5                   # Probabilité de fécondation d’une femelle
    INDIVIDUS_PAR_CAGE_MAX = 6          # Capacité maximale normale d’une cage
    INDIVIDUS_PAR_CAGE_SURPOP = 10      # Seuil de surpopulation par cage

    AGE_MATURITE_GRAVIDITE = 6         # Âge minimum pour reproduction
    AGE_MAX_GRAVIDITE = 48             # Âge maximum pour reproduction
    DUREE_GESTATION = 1                # Durée de la gestation en mois
    
    # Mort par vieillesse
    DUREE_VIE_MAX = 96                 # Âge à partir duquel le lapin peut mourir de viellesse 
    PROBA_MORT_VIEUX = 0.1             # Proba du lapin de mourir de vieillesse une fois l'âge requis dépassé

class Sante(models.Model):
    individu = models.OneToOneField('Individu', on_delete=models.CASCADE, related_name='sante')
    niveau_sante = models.IntegerField(default=100)
    maladies = models.TextField(blank=True, null=True)
    dernier_checkup = models.DateField(auto_now=True)