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