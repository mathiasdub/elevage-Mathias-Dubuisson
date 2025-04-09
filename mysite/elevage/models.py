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