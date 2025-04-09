from django.db import models


class Elevage(models.Model):
    name = models.CharField(max_length=200)
    nb_lapins_m = models.IntegerField()
    nb_lapins_f = models.IntegerField
    nb_cages = models.IntegerField()
    qt_nourriture = models.IntegerField()
    argent = models.IntegerField()
    
    def __str__(self):
        return self.name


class Individu(models.Model):
    sexe = models.CharField(max_length=1)        # "m" pour un lapin male et "f" pour un lapin femelle
    age = models.IntegerField()                  # âge en nombre de mois
    etat = models.CharField(max_length=10)       # "présent", "vendu", "mort" ou "gravide" 
    elevage = models.ForeignKey(Elevage, on_delete=models.CASCADE, related_name="individus")